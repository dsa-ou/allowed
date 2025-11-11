"""Minimal client for interacting with type checker language servers via LSP."""

import json
import os
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any, Protocol

Location = tuple[int, int]  # (line_number, column_number)


class LspStdioConnection:
    """Handle LSP message exchange with a language server process using stdio."""

    def __init__(self, command: list[str]) -> None:
        """Start the process with connected stdio streams."""
        self._process = subprocess.Popen(  # nosec B603
            command,  # noqa: S603
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        if not self._process.stdin or not self._process.stdout:
            raise RuntimeError("Failed to open stdio for language server")  # noqa: EM101, TRY003
        self._stdin = self._process.stdin
        self._stdout = self._process.stdout
        self._request_id = 0

    def _read_message(self) -> dict[str, Any] | None:
        """Read a single LSP-framed JSON message from stdout.

        Assumes single 'content-length' header followed by blank line.
        """
        header = self._stdout.readline()
        if not header or not header.startswith(b"Content-Length: "):
            return None
        content_length = int(header.split(b":", 1)[1].strip())
        self._stdout.readline()  # Skip blank line, as per LSP specification.
        body = self._stdout.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def _write_message(self, payload: dict[str, Any]) -> None:
        """Write a single LSP-framed JSON message to stdin."""
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
        self._stdin.write(header + data)
        self._stdin.flush()

    def request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """Send a JSON-RPC request and return its result."""
        self._request_id += 1
        request_id = self._request_id
        msg = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            msg["params"] = params
        self._write_message(msg)

        while True:
            response = self._read_message()
            if response is None:
                raise RuntimeError("LSP stream ended before a response was received.")  # noqa: EM101, TRY003
            if response.get("id") == request_id:
                if "error" in response:
                    raise RuntimeError(f"{method} error: {response['error']}")  # noqa: EM102, TRY003
                return response.get("result")

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        """Send a JSON-RPC notification."""
        msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._write_message(msg)

    def close(self) -> None:
        """Shut down the language server cleanly."""
        try:
            self._process.terminate()
        finally:
            self._process.wait(0.25)


class LanguageServer(Protocol):
    """Define the Language server adaptor interface."""

    def command(self) -> list[str]:  # noqa: D102
        ...

    def initialise_params(self, root_uri: str) -> dict[str, Any]:  # noqa: D102
        ...

    def method(self) -> str:  # noqa: D102
        ...

    def choose_location(  # noqa: D102
        self, method_name: Location, receiver: Location
    ) -> Location:
        ...

    def parse_result(self, result: dict[str, Any] | None) -> str | None:  # noqa: D102
        ...


def _infer_literal(inner: str) -> str:
    """Infer base type from the inner value of a Literal[...] expression."""
    if re.match(r"^b(['\"].*['\"])$", inner):
        return "bytes"
    if re.match(r"^(['\"].*['\"])$", inner):
        return "str"
    if re.match(r"^[0-9]+$", inner):
        return "int"
    if re.match(r"^[0-9]*\.?[0-9]+$", inner):
        return "float"
    return "Literal"


class PyreflyServer:
    """Pyrefly language server adaptor."""

    def command(self) -> list[str]:
        """Return the command required to start the Pyrefly language server."""
        return ["pyrefly", "lsp"]

    def initialise_params(self, root_uri: str) -> dict[str, Any]:
        """Return the initialisation parameters for the LSP handshake."""
        return {
            "processId": os.getpid(),
            "rootUri": root_uri,
            "capabilities": {
                "textDocument": {"hover": {"contentFormat": ["markdown"]}}
            },
        }

    def method(self) -> str:
        """Return the LSP method used to query the document for type info."""
        return "textDocument/hover"

    def choose_location(self, method_loc: Location, receiver_loc: Location) -> Location:  # noqa: ARG002
        """Return a location on the method name."""
        return method_loc

    def parse_result(self, result: dict[str, Any] | None) -> str | None:
        """Return the receiver type name from a Pyrefly hover result, or None."""
        if not result:
            return None
        contents = result.get("contents")
        if not isinstance(contents, dict):
            return None
        type_name = None
        text = contents.get("value", "")
        # Capture type name after 'self:'
        if match := re.search(r"(?:^|[^\w])self\s*:\s*([^\s\[\],)]+)", text):
            type_name = match.group(1)
        if type_name == "LiteralString":
            type_name = "str"
        return type_name


class PyrightServer:
    """Pyright language server adaptor."""

    def command(self) -> list[str]:
        """Return the command required to start the Pyright language server."""
        return ["pyright-langserver", "--stdio"]

    def initialise_params(self, root_uri: str) -> dict[str, Any]:
        """Return the initialisation parameters for the LSP handshake."""
        return {
            "processId": os.getpid(),
            "rootUri": root_uri,
            "capabilities": {
                "textDocument": {"hover": {"contentFormat": ["markdown", "plaintext"]}}
            },
            "initializationOptions": {"typeCheckingMode": "basic"},
        }

    def method(self) -> str:
        """Return the name of the LSP method used to get type info."""
        return "textDocument/hover"

    def choose_location(self, method_loc: Location, receiver_loc: Location) -> Location:  # noqa: ARG002
        """Return a location on the receiver object."""
        return receiver_loc

    def parse_result(self, result: dict[str, Any] | None) -> str | None:
        """Return the receiver type name from a Pyright hover result, or None."""
        if not result:
            return None
        contents = result.get("contents", {})
        text = (
            contents.get("value", "") if isinstance(contents, dict) else str(contents)
        )
        lm = re.search(r"Literal\[(.*?)\]", text)
        if lm:
            return _infer_literal(lm.group(1).strip())
        m = re.search(r":\s*([^\s\)]+)", text) or re.search(
            r"\(class\)\s+([\w\.]+)", text
        )
        if not m:
            return None
        type_name = m.group(1)
        return type_name.split("[", 1)[0]


class TyServer:
    """Ty language server adaptor."""

    def command(self) -> list[str]:
        """Return the command required to start the Ty language server."""
        return ["ty", "server"]

    def initialise_params(self, root_uri: str) -> dict[str, Any]:
        """Return the initialisation parameters for the LSP handshake."""
        return {
            "processId": os.getpid(),
            "rootUri": root_uri,
            "capabilities": {
                "textDocument": {"hover": {"contentFormat": ["markdown", "plaintext"]}}
            },
        }

    def method(self) -> str:
        """Return the LSP method used to query the document for type info."""
        return "textDocument/hover"

    def choose_location(self, method_loc: Location, receiver_loc: Location) -> Location:  # noqa: ARG002
        """Return a location on the receiver object."""
        return receiver_loc

    def parse_result(self, result: dict[str, Any] | None) -> str | None:
        """Return the receiver type name from a Ty hover result, or None."""
        if not result:
            return None
        contents = result.get("contents", {})
        text = (
            contents.get("value", "") if isinstance(contents, dict) else str(contents)
        )
        text = text.strip().removeprefix("```python").removesuffix("```").strip()
        type_name = None
        if m := re.match(r"Literal\[(.*)\]", text):
            inner = m.group(1).strip()
            type_name = _infer_literal(inner)
        elif m := re.match(r"([A-Za-z_]\w*)", text):
            type_name = m.group(1)
        return type_name


class LSClient:
    """Generic language server client."""

    def __init__(self, source: str, server: LanguageServer) -> None:
        """Perform the handshake, open the document."""
        self._server = server
        self._uri = "file://" + str(Path.cwd() / "__inmemory__.py")
        self._connection = LspStdioConnection(self._server.command())
        # Handshake
        root_uri = Path.cwd().resolve().as_uri()
        self._connection.request("initialize", server.initialise_params(root_uri))
        self._connection.notify("initialized", {})
        # Open document
        self._connection.notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": self._uri,
                    "languageId": "python",
                    "version": 1,
                    "text": source,
                }
            },
        )

    def receiver_type(
        self, method_loc: Location | None, receiver_loc: Location | None
    ) -> str | None:
        """Return the receiver type given a method call expression, or None."""
        if method_loc is None or receiver_loc is None:
            return None
        line, column = self._server.choose_location(method_loc, receiver_loc)
        pos = {"line": line - 1, "character": column}  # 0-based location
        result = self._connection.request(
            self._server.method(),
            {"textDocument": {"uri": self._uri}, "position": pos},
        )
        return self._server.parse_result(result)

    def close(self) -> None:
        """Shut down the language server cleanly."""
        try:
            self._connection.request("shutdown")
            self._connection.notify("exit", {})
        finally:
            self._connection.close()

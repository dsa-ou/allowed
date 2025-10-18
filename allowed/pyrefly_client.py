"""Minimal client for interacting with pyrefly language server via LSP."""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

Location = tuple[int, int]  # (line_number, column_number), 0-based


class PyreflyClient:
    """Client for the pyrefly Language Server."""

    def __init__(self, source: str) -> None:
        """Start pyrefly lsp, perform handshake, open document."""
        self.source_code = source
        # LSP protocol requires a uri, even if we only pass source.
        self.uri = "file://" + str(Path.cwd() / "__inmemory__.py")
        self.next_request_id = 0
        self.process = subprocess.Popen(
            ["pyrefly", "lsp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout
        # LSP handshake
        self._send_request(
            "initialize",
            {
                "processId": os.getpid(),
                "rootUri": Path.cwd().resolve().as_uri(),
                "capabilities": {
                    "textDocument": {
                        "hover": {"contentFormat": ["markdown"]},
                    }
                },
            },
        )
        self._send_notification("initialized", {})
        # Open the document
        self._send_notification(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": self.uri,
                    "languageId": "python",
                    "version": 1,
                    "text": self.source_code,
                }
            },
        )

    def _read_message(self) -> dict[str, Any] | None:
        """Read a single LSP-framed JSON message from stdout.

        Assumes single 'content-length' header followed by blank line.
        """
        header = self.stdout.readline()
        if not header or not header.startswith(b"Content-Length: "):
            return None
        content_length = int(header.split(b":", 1)[1].strip())
        self.stdout.readline()  # Skip blank line, as per LSP specification.
        body = self.stdout.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def _write_message(self, payload: dict[str, Any]) -> None:
        """Write a single LSP-framed JSON message to stdin."""
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
        self.stdin.write(header + data)
        self.stdin.flush()

    def _send_notification(self, method: str, params: dict[str, Any]) -> None:
        """Send a JSON-RPC notification."""
        self._write_message({"jsonrpc": "2.0", "method": method, "params": params})

    def _send_request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """Send a JSON-RPC request and return its result."""
        self.next_request_id += 1
        request_id = self.next_request_id
        msg = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params:
            msg["params"] = params
        self._write_message(msg)

        while True:
            response = self._read_message()
            if response is None:
                raise RuntimeError("LSP stream ended before a response was received.")  # noqa: EM101
            if response.get("id") == request_id:
                if "error" in response:
                    raise RuntimeError(f"{method} error: {response['error']}")
                return response.get("result")

    def _hover(self, location: Location) -> dict[str, Any] | None:
        """Return the hover result from a given a location, or None."""
        line, column = location
        pos = {"line": line, "character": column}
        return self._send_request(
            "textDocument/hover", {"textDocument": {"uri": self.uri}, "position": pos}
        )

    def _parse_pyrefly_hover(self, hover_result: dict[str, Any] | None) -> str | None:
        """Parse the receiver type from a pyrefly hover on a method name, or None."""
        if not hover_result:
            return None
        contents = hover_result.get("contents")
        if not isinstance(contents, dict):
            return None
        typ = None
        text = contents.get("value", "")
        # Capture type name after 'self:' (start or non-word before, stops before space/bracket/comma/paren).
        if match := re.search(r"(?:^|[^\w])self\s*:\s*([^\s\[\],)]+)", text):
            typ = match.group(1)
        if typ == "LiteralString":
            typ = "str"
        return typ

    def receiver_type(self, location: Location) -> str | None:
        """Return the receiver type, given a location on the method name, or None."""
        return self._parse_pyrefly_hover(self._hover(location))

    def close(self) -> None:
        """Shut down the language server cleanly."""
        try:
            self._send_request("shutdown")
            self._send_notification("exit", {})
        finally:
            if self.process:
                self.process.terminate()

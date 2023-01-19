"""Check that Python files only use the allowed statements."""

import ast
import sys
import os
import re

# ----- configuration -----

# STATEMENTS contains the `ast` classes of the allowed statements.
# See https://docs.python.org/3/library/ast.html#statements for the available classes.
# For example, to allow `break` and `continue`, add `ast.Break` and `ast.Continue`.

STATEMENTS = (
    ast.Assign,
    ast.Expr,
    ast.If,
    ast.For,
    ast.While,
    ast.FunctionDef,
    ast.Return,
    ast.Pass,
    ast.Import,
    ast.ImportFrom,
    ast.ClassDef,
)

FOR_ELSE = False  # allow for-else statements?
WHILE_ELSE = False  # allow while-else statements?

STMT_MSG = "disallowed statement"
FOR_ELSE_MSG = "disallowed else in for-loop"
WHILE_ELSE_MSG = "disallowed else in while-loop"

# ----- end of configuration -----


class AllowedChecker:
    """Check if only the allowed statements are used."""

    def __init__(self, filename: str) -> None:
        """Open and parse the given file."""
        self._filename = filename
        with open(filename) as file:
            source = file.read()
        self._tree = ast.parse(source)
        self._source = source.splitlines()
        self._messages = []

    def _msg(self, node: ast.AST, message: str) -> None:
        line = node.lineno
        if message is STMT_MSG:
            extra = ": " + self._source[line - 1].strip()
        else:
            extra = ""
        self._messages.append((line, message, extra))

    def run(self) -> None:
        """Run the checker."""
        for node in ast.walk(self._tree):
            if isinstance(node, ast.stmt):
                if not isinstance(node, STATEMENTS):
                    self._msg(node, STMT_MSG)
                elif isinstance(node, ast.For) and not FOR_ELSE:
                    if node.orelse:
                        self._msg(node.orelse[0], FOR_ELSE_MSG)
                elif isinstance(node, ast.While) and not WHILE_ELSE:
                    if node.orelse:
                        self._msg(node.orelse[0], WHILE_ELSE_MSG)
        self._messages.sort()
        for (line, message, extra) in self._messages:
            print(f"{self._filename}:{line}: {message}{extra}")


def check_folder(folder: str) -> None:
    """Check all Python files in `folder` and its subfolders."""
    for current, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py"):
                path = os.path.join(current, filename)
                try:
                    AllowedChecker(path).run()
                except SyntaxError as error:
                    message = str(error)
                    match = re.search(r"\(.*, line (\d+)\)", message)
                    if match:
                        line = int(match.group(1))
                        message = message[: match.start()] + message[match.end() :]
                        print(f"{path}:{line}: can't parse: {message}")
                    else:
                        print(f"{path}: can't parse: {message}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python restrict.py <filename or folder>")
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        check_folder(sys.argv[1])
    else:
        AllowedChecker(sys.argv[1]).run()

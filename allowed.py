"""Check that Python files only use the allowed constructs."""

import ast
import sys
import os
import re

# ----- configuration -----

# FILE_UNIT is a regexp that extracts the unit from the file's name.
# If there's a match, the unit number is the first group.
# If your file names don't include the unit number, set `FILE_UNIT` to `None`.
# For example, if the unit number appears last, set it to `r"(\d+).py$"`.

FILE_UNIT = r"^(\d+)"  # file name starts with the unit number

# CONSTRUCTS maps unit numbers to the Python constructs they introduce.
# Constructs are represented by the corresponding `ast` classes, taken from
# https://docs.python.org/3/library/ast.html.
# For example, if `break` and `continue` are introduced in unit 5, add an entry
# `5: (ast.Break, ast.Continue),`.
# For some constructs, you must add auxiliary classes, e.g. `ast.FunctionDef`
# keeps the arguments in an `ast.arguments` object, which has a list of `ast.arg` objects.

CONSTRUCTS = {
    2: (
        ast.Assign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.FunctionDef,
        ast.Return,
        ast.Call,
        ast.arguments,
        ast.arg,
        ast.Module,
        ast.Import,
        ast.alias,
        ast.Expr,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
    ),
    3: (
        ast.If,
        ast.BoolOp,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Compare,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
    ),
    4: (
        ast.For,
        ast.While,
        ast.List,
        ast.Tuple,
        ast.In,
        ast.Subscript,
        ast.Slice,
        ast.Attribute,  # dot notation, e.g. math.sqrt
        ast.keyword,  # keyword arguments, e.g. print(..., end="")
    ),
    6: (ast.Pass, ast.ClassDef),
    7: (ast.ImportFrom,),
    8: (ast.Dict, ast.Set, ast.NotIn, ast.BitOr, ast.BitAnd),
}

FOR_ELSE = False  # allow for-else statements?
WHILE_ELSE = False  # allow while-else statements?

STMT_MSG = "disallowed statement"
FOR_ELSE_MSG = "disallowed else in for-loop"
WHILE_ELSE_MSG = "disallowed else in while-loop"

# ----- end of configuration -----

OPERATORS = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.USub: "-",
    ast.Pow: "**",
    ast.BitOr: "|",
    ast.BitAnd: "&",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitXor: "^",
    ast.Invert: "~",
    ast.Not: "not",
    ast.And: "and",
    ast.Or: "or",
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
}


class AllowedChecker:
    """Check if only the allowed constructs are used."""

    def __init__(self, filename: str, unit: int = -1) -> None:
        """Open and parse the given file."""
        # determine the unit number, if not given
        if unit == -1 and FILE_UNIT:
            match = re.match(FILE_UNIT, filename)
            if match:
                unit = int(match.group(1))
        # determine the allowed constructs
        self._constructs = ()
        for key, constructs in CONSTRUCTS.items():
            if unit == -1 or key <= unit:
                self._constructs += constructs

        self._filename = filename
        with open(filename) as file:
            source = file.read()
        self._tree = ast.parse(source)
        self._source = source.splitlines()
        self._messages = []

    def _msg(self, node: ast.AST, message: str) -> None:
        extra = ""
        line = 0
        try:
            line = node.lineno
            if message is STMT_MSG:
                extra = ": " + self._source[line - 1].strip()
        except AttributeError:
            # operators don't have a lineno
            extra = OPERATORS.get(type(node), "")
            if extra:
                extra = ": " + extra
        self._messages.append((line, message, extra))

    def run(self) -> None:
        """Run the checker."""
        for node in ast.walk(self._tree):
            if not isinstance(node, self._constructs):
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


def check_folder(folder: str, unit: int = -1) -> None:
    """Check all Python files in `folder` and its subfolders."""
    for current, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py"):
                path = os.path.join(current, filename)
                try:
                    AllowedChecker(path, unit).run()
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
    if len(sys.argv) < 2:
        print("Usage: python restrict.py <filename or folder> [<unit>]")
        print()
        print("unit: a non-negative number; if omitted, use all units")
        sys.exit(1)
    unit = -1 if len(sys.argv) < 3 else int(sys.argv[2])
    if os.path.isdir(sys.argv[1]):
        check_folder(sys.argv[1], unit)
    else:
        AllowedChecker(sys.argv[1], unit).run()

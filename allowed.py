"""Check that Python files only use the allowed constructs."""

import ast
import os
import re
import sys

# ----- configuration -----

# FILE_UNIT is a regexp that extracts the unit from the file's name.
# If there's a match, the unit number is the first group.
# If there's no match, the file is considered to be in all units.

FILE_UNIT = r"^(\d+)"  # file name starts with the unit number
# FILE_UNIT = r"(\d+).py$"  # file name ends with the unit number
# FILE_UNIT = ""  # file names don't include a unit number

# CONSTRUCTS maps unit numbers to the Python constructs they introduce.
# Constructs are represented by the corresponding `ast` classes, taken from
# https://docs.python.org/3/library/ast.html.
# For example, if `break` and `continue` are introduced in unit 5,
# add an entry `5: (ast.Break, ast.Continue),`.

CONSTRUCTS = {
    2: (
        ast.Assign,
        ast.Name,
        ast.Constant,
        ast.FunctionDef,
        ast.Return,
        ast.Call,
        ast.Import,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,  # integer division, e.g. 5 // 2
        ast.Mod,
        ast.Pow,
        ast.USub,  # unary minus, e.g. -x
    ),
    3: (
        ast.If,
        ast.And,
        ast.Or,
        ast.Not,
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
        ast.List,  # list literal, e.g. [1, 2, 3]
        ast.Tuple,  # tuple literal, e.g. (1, 2, 3)
        ast.In,
        ast.Subscript,  # indexing, e.g. x[0]
        ast.Slice,  # slicing, e.g. x[1:3], x[:3], x[1:]
        ast.Attribute,  # dot notation, e.g. math.sqrt
        ast.keyword,  # keyword argument, e.g. print(..., end="")
    ),
    6: (ast.Pass, ast.ClassDef),
    7: (ast.ImportFrom,),
    8: (
        ast.Dict,  # dictionary literal, e.g. {"a": 1, "b": 2}
        ast.Set,  # set literal, e.g. {1, 2, 3}
        ast.NotIn,
        ast.BitOr,  # set union, e.g. {1, 2, 3} | {2, 3, 4}
        ast.BitAnd,  # set intersection, e.g. {1, 2, 3} & {2, 3, 4}
    ),
}

FOR_ELSE = False  # allow for-else statements?
WHILE_ELSE = False  # allow while-else statements?

# ----- end of configuration -----

# ----- auxiliary functions -----


def get_unit(filename: str) -> int:
    """Return the file's unit or zero (consider all units)."""
    if FILE_UNIT and (match := re.match(FILE_UNIT, filename)):
        return int(match.group(1))
    else:
        return 0


def get_constructs(last_unit: int) -> tuple[ast.AST]:
    """Return the allowed constructs up to the given unit.

    If `last_unit` is zero, return the constructs in all units.
    """
    allowed = ()
    for unit, constructs in CONSTRUCTS.items():
        if not last_unit or unit <= last_unit:
            allowed += constructs
    return allowed


IGNORE = (  # wrapper nodes that can be skipped
    ast.Module,
    ast.alias,
    ast.arguments,
    ast.arg,
    ast.withitem,
    ast.Load,
    ast.Store,
    ast.Del,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
)

OPERATOR_CLASSES = (ast.operator, ast.boolop, ast.cmpop, ast.unaryop)

# ast doesn't unparse operators, so we need to do it ourselves
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


def check_tree(tree: ast.AST, allowed: tuple, source: list) -> list:
    """Return the constructs in the tree that are not allowed."""
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, IGNORE):
            pass
        elif not isinstance(node, allowed):
            if isinstance(node, OPERATOR_CLASSES):
                line = 0
                message = OPERATORS.get(type(node), "operator not allowed")
            else:
                line = node.lineno
                message = source[line - 1].strip()
            errors.append((line, message))
        elif isinstance(node, ast.For) and node.orelse and not FOR_ELSE:
            line = node.orelse[0].lineno
            message = "else in for-loop"
            errors.append((line, message))
        elif isinstance(node, ast.While) and node.orelse and not WHILE_ELSE:
            line = node.orelse[0].lineno
            message = "else in while-loop"
            errors.append((line, message))
    return errors


# ----- main functions -----


def check_folder(folder: str, last_unit: int) -> None:
    """Check all Python files in `folder` and its subfolders."""
    for current, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py"):
                fullname = os.path.join(current, filename)
                check_file(fullname, last_unit)


def check_file(filename: str, last_unit: int) -> None:
    """Check that the file only uses construct up to `last_unit`."""
    try:
        with open(filename) as file:
            source = file.read()
        tree = ast.parse(source)
        if last_unit:
            allowed = get_constructs(last_unit)
        else:
            allowed = get_constructs(get_unit(filename))
        source = source.splitlines()
        errors = check_tree(tree, allowed, source)
        errors.sort()
        for line, message in errors:
            print(f"{filename}:{line}: {message}")
    except OSError as error:
        print(error)
    except SyntaxError as error:
        message = str(error)
        if match := re.search(r"\(.*, line (\d+)\)", message):
            line = int(match.group(1))
            message = message[: match.start()] + message[match.end() :]
            print(f"{filename}:{line}: can't parse: {message}")
        else:
            print(f"{filename}: can't parse: {message}")


# ---- main program ----

HELP = """Usage: python allowed.py <file or folder> [<unit>]

Check the Python file (or all Python files in the folder and its subfolders)
for constructs that are NOT introduced up to the given unit (a positive number).
If unit is omitted, use all units or the unit given in the file's name.

See allowed.py for how to configure the allowed constructs.
"""

if __name__ == "__main__":
    try:
        argn = len(sys.argv)
        assert argn in (2, 3)
        name = sys.argv[1]
        unit = int(sys.argv[2]) if argn == 3 else 0
        assert unit >= 0
    except:
        print(HELP)
        sys.exit(1)

    if os.path.isdir(name):
        check_folder(name, unit)
    else:
        check_file(name, unit)

"""Check that Python files only use the allowed constructs."""

import argparse
import ast
import os
import re
import sys

PYTHON_VERSION = sys.version_info[:2]
if (3, 7) <= PYTHON_VERSION <= (3, 10):
    try:
        import pytype
        from pytype.tools.annotate_ast import annotate_ast

        PYTYPE_OPTIONS = pytype.config.Options.create(python_version=PYTHON_VERSION)
        METHOD_CHECK_ERROR = ""
    except ImportError:
        METHOD_CHECK_ERROR = "error: pytype not installed: method calls can not be checked"
else:
    METHOD_CHECK_ERROR = "error: Python version not supported: method calls can not be checked"

# ----- configuration -----

# FILE_UNIT is a regexp that extracts the unit from the file's name.
# If there's a match, the unit number must be the first group.
# If there's no match, the user-given unit will be used.

FILE_UNIT = r"^(\d+)"  # file name starts with the unit number
# FILE_UNIT = r"(\d+).py$"  # file name ends with the unit number
# FILE_UNIT = ""  # file names don't include a unit number

# LANGUAGE[n] are Python's syntax and built-in functions introduced in unit n.
# For the possible syntactical elements, see dictionary `SYNTAX` further below.
# Use strings "for else" and "while else" to allow the `else` clause in loops.
# For the possible built-in functions, see set `BUILTINS` further below.
LANGUAGE = {
    2: (
        "=",
        "name",
        "constant",
        "def",
        "return",
        "function call",
        "import",
        "+",
        "-",
        "*",
        "/",
        "//",
        "%",
        "**",
        "-x",  # unary minus
        "help",
        "min",
        "max",
        "round",
        "print",
        "int",
        "float",
    ),
    3: (
        "if",
        "and",
        "or",
        "not",
        "==",
        "!=",
        "<",
        "<=",
        ">",
        ">=",
    ),
    4: (
        "for",
        "while",
        "list literal",
        "tuple literal",
        "in",
        "index",
        "slice",
        "attribute",  # dot notation, e.g. math.sqrt
        "keyword argument",  # e.g. print(..., end="")
        "len",
        "sorted",
        "str",
        "range",
        "list",
        "tuple",
    ),
    6: ("pass", "class"),
    7: ("from import",),
    8: (
        "dict literal",
        "set literal",
        "not in",
        "|",
        "&",
        "dict",
        "set",
        "ord",
        "hash",
    ),
    17: ("super",),
    18: ("abs",),
}

# IMPORTS[n] is a dictionary of the modules and names introduced in unit n.
IMPORTS = {
    2: {"math": ["floor", "ceil", "trunc", "pi"]},
    6: {"math": ["inf"]},
    7: {"collections": ["deque"]},
    8: {"collections": ["Counter"]},
    11: {"math": ["sqrt", "factorial"], "itertools": ["permutations", "combinations"]},
    14: {"random": ["shuffle"], "typing": ["Callable"]},
    16: {"heapq": ["heappush", "heappop"]},
    17: {"typing": ["Hashable"], "random": ["random"]},
    27: {"inspect": ["getsource"]},
}

# METHODS[n] is a dictionary of the methods introduced in unit n: the keys are the types.
# Other builtin types are 'str' and 'Tuple'.

METHODS = {
    4: {"List": ["insert", "append", "pop", "sort"]},
    7: {"collections.deque": ["append", "appendleft", "pop", "popleft"]},
    8: {
        "Dict": ["items"],
        "Set": ["add", "discard", "union", "intersection", "difference"],
    },
    11: {"Set": ["pop"]},
}

# ----- end of configuration -----

# ----- Python's Abstract Syntax Tree (AST) -----

# ABSTRACT maps strings (syntax descriptions) to the `ast` node classes
# listed in https://docs.python.org/3.10/library/ast.html.
# The strings can appear in the values of dictionary `LANGUAGE` above.
# TODO: ABSTRACT doesn't cover all Python 3.10 syntax.
ABSTRACT = {
    # literals
    "constant": ast.Constant,  # e.g. 'Hi!', True, None, (1, 2), ...
    "f-string": ast.JoinedStr,
    "list literal": ast.List,
    "tuple literal": ast.Tuple,
    "set literal": ast.Set,
    "dict literal": ast.Dict,
    # variables
    "name": ast.Name,
    "*name": ast.Starred,
    # unary operators
    "+x": ast.UAdd,
    "-x": ast.USub,
    "not": ast.Not,
    "~": ast.Invert,
    # binary operators
    "+": ast.Add,
    "-": ast.Sub,
    "*": ast.Mult,
    "/": ast.Div,
    "//": ast.FloorDiv,
    "%": ast.Mod,
    "**": ast.Pow,
    "<<": ast.LShift,
    ">>": ast.RShift,
    "|": ast.BitOr,
    "^": ast.BitXor,
    "&": ast.BitAnd,
    "@": ast.MatMult,
    "and": ast.And,
    "or": ast.Or,
    # comparisons
    "==": ast.Eq,
    "!=": ast.NotEq,
    "<": ast.Lt,
    "<=": ast.LtE,
    ">": ast.Gt,
    ">=": ast.GtE,
    "is": ast.Is,
    "is not": ast.IsNot,
    "in": ast.In,
    "not in": ast.NotIn,
    # other expressions
    "function call": ast.Call,
    "keyword argument": ast.keyword,  # print(..., end=...), sorted(..., key=...)
    "if expression": ast.IfExp,  # x if x >= 0 else -x
    "index": ast.Subscript,  # x[0]
    "slice": ast.Slice,  # all forms: x[1:10:2], x[1:], x[::2], etc.
    "list comprehension": ast.ListComp,
    "set comprehension": ast.SetComp,
    "dict comprehension": ast.DictComp,
    "generator expression": ast.GeneratorExp,
    ":=": ast.NamedExpr,
    "attribute": ast.Attribute,  # dot notation, e.g. math.sqrt
    # control flow
    "if": ast.If,  # allows `elif` and `else`
    "for": ast.For,  # does NOT allow `else`
    "while": ast.While,  # does NOT allow `else`
    "break": ast.Break,
    "continue": ast.Continue,
    "raise": ast.Raise,
    "try": ast.Try,  # allows `else` and `finally`
    "except": ast.ExceptHandler,
    "with": ast.With,
    # other statements
    "=": ast.Assign,
    "assert": ast.Assert,
    "del": ast.Delete,
    "pass": ast.Pass,
    "import": ast.Import,  # allows `as`
    "from import": ast.ImportFrom,  # allows `as`
    "class": ast.ClassDef,
    # function constructs
    "def": ast.FunctionDef,
    "lambda": ast.Lambda,
    "global": ast.Global,
    "nonlocal": ast.Nonlocal,
    "return": ast.Return,
    "yield": ast.Yield,
    "yield from": ast.YieldFrom,
    # asynchronous constructs
    "async def": ast.AsyncFunctionDef,
    "async for": ast.AsyncFor,
    "async with": ast.AsyncWith,
    "await": ast.Await,
}

# CONCRETE is the inverse map. Needed for error messages.
CONCRETE = {ast_node: string for string, ast_node in ABSTRACT.items()}

# optional constructs that can be separately allowed
OPTIONS = {"for else", "while else"}

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

NO_LINE = (  # nodes without associated line numbers
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
    ast.comprehension,
)

# set of all built-in functions
BUILTINS = {
    "abs",
    "aiter",
    "all",
    "anext",
    "any",
    "ascii",
    "bin",
    "bool",
    "breakpoint",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "classmethod",
    "compile",
    "complex",
    "copyright",
    "credits",
    "delattr",
    "dict",
    "dir",
    "divmod",
    "enumerate",
    "eval",
    "exec",
    "exit",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "globals",
    "hasattr",
    "hash",
    "help",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "license",
    "list",
    "locals",
    "map",
    "max",
    "memoryview",
    "min",
    "next",
    "object",
    "oct",
    "open",
    "ord",
    "pow",
    "print",
    "property",
    "quit",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "setattr",
    "slice",
    "sorted",
    "staticmethod",
    "str",
    "sum",
    "super",
    "tuple",
    "type",
    "vars",
    "zip",
}

# ----- check configuration -----


def check_language() -> str:
    """Return non-empty message if some constructs in LANGUAGE are unknown."""
    allowed = set()
    for constructs in LANGUAGE.values():
        allowed.update(set(constructs))
    if unknown := allowed - ABSTRACT.keys() - BUILTINS - OPTIONS:
        return f"error: unknown constructs: {', '.join(unknown)}"
    return ""


def check_imports() -> str:
    """Return non-empty message if introduction of modules and import don't match."""
    statements = []
    for unit, elements in LANGUAGE.items():
        if "import" in elements or "from import" in elements:
            statements.append(unit)
    first_import = min(statements) if statements else 0
    first_module = min(IMPORTS.keys()) if IMPORTS else 0

    if first_module and not first_import:
        return (
            "error: modules are allowed but import statements aren't\n"
            "fix 1: make IMPORTS empty\n"
            "fix 2: add 'import' and/or 'from import' to LANGUAGE"
        )
    if first_import and not first_module:
        return (
            "error: import statement is allowed but no modules are introduced\n"
            "fix 1: add modules to IMPORTS\n"
            "fix 2: remove 'import' and 'from import' from LANGUAGE"
        )
    if first_module < first_import:
        return (
            "error: modules are introduced before import statement\n"
            "fix 1: in IMPORTS, move modules to unit {first_import} or later\n"
            "fix 2: in LANGUAGE, move import statements to unit {first_module} or earlier"
        )
    return ""


# ----- auxiliary functions -----


def get_unit(filename: str) -> int:
    """Return the file's unit or zero (consider all units)."""
    if FILE_UNIT and (match := re.match(FILE_UNIT, filename)):
        return int(match.group(1))
    else:
        return 0


def get_language(last_unit: int) -> tuple[ast.AST]:
    """Return the allowed language elements up to the given unit.

    If `last_unit` is zero, return the elements in all units.
    """
    allowed = []
    for unit, constructs in LANGUAGE.items():
        if not last_unit or unit <= last_unit:
            for construct in constructs:
                if ast_class := ABSTRACT.get(construct, None):
                    allowed.append(ast_class)
    return tuple(allowed)


def get_options(last_unit: int) -> list[str]:
    """Return the allowed language options up to the given unit.

    If `last_unit` is zero, return the options in all units.
    """
    allowed = []
    for unit, constructs in LANGUAGE.items():
        if not last_unit or unit <= last_unit:
            for construct in constructs:
                if construct in OPTIONS:
                    allowed.append(construct)
    return allowed


def get_imports(last_unit: int) -> dict[str, list[str]]:
    """Return the allowed imports up to the given unit.

    If `last_unit` is zero, return the imports in all units.
    """
    allowed = {}
    for unit, imports in IMPORTS.items():
        if not last_unit or unit <= last_unit:
            for module, names in imports.items():
                if module in allowed:
                    allowed[module].extend(names)
                else:
                    allowed[module] = names
    return allowed


def get_functions(last_unit: int) -> set[str]:
    """Return the allowed functions up to the given unit.

    If `last_unit` is zero, return the functions in all units.
    """
    allowed = set()
    for unit, constructs in LANGUAGE.items():
        if not last_unit or unit <= last_unit:
            for construct in constructs:
                if construct in BUILTINS:
                    allowed.add(construct)
    return allowed


def get_methods(last_unit: int) -> dict[str, list[str]]:
    """Return the allowed methods up to the given unit.

    If `last_unit` is zero, return the methods in all units.
    """
    allowed = {}
    for unit, methods in METHODS.items():
        if not last_unit or unit <= last_unit:
            for type, names in methods.items():
                if type in allowed:
                    allowed[type].extend(names)
                else:
                    allowed[type] = names
    return allowed


def get_constructs(last_unit: int) -> tuple:
    """Return the allowed constructs up to the given unit."""
    return (
        IGNORE + get_language(last_unit),
        get_options(last_unit),
        get_imports(last_unit),
        get_functions(last_unit),
        get_methods(last_unit),
    )


def check_tree(tree: ast.AST, constructs: tuple, source: list) -> list:
    """Check if tree only uses allowed constructs."""
    language, options, imports, functions, methods = constructs
    errors = []
    for node in ast.walk(tree):
        # if a node has no line number, handle it via its parent
        if isinstance(node, NO_LINE):
            pass
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp)):
            if not isinstance(node.op, language):
                line = node.lineno
                message = CONCRETE.get(type(node.op), "unknown operator")
                errors.append((line, message))
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if not isinstance(op, language):
                    line = node.lineno
                    message = CONCRETE.get(type(op), "unknown operator")
                    errors.append((line, message))
        elif not isinstance(node, language):
            if hasattr(node, "lineno"):
                line = node.lineno
                message = source[line - 1].strip()
            else:
                # if a node has no line number, report it for inclusion in NO_LINE
                line = 0
                message = f"unknown construct {str(node)} at unknown line"
            errors.append((line, message))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in imports:
                    line = alias.lineno
                    message = f"import {alias.name}"
                    errors.append((line, message))
        elif isinstance(node, ast.ImportFrom):
            if node.module not in imports:
                line = node.lineno
                message = f"from {node.module} import ..."
                errors.append((line, message))
            else:
                for alias in node.names:
                    if alias.name not in imports[node.module]:
                        line = alias.lineno
                        message = f"from {node.module} import {alias.name}"
                        errors.append((line, message))
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            name = node.value
            attribute = node.attr
            if name.id in imports and attribute not in imports[name.id]:
                line = node.lineno
                message = f"{name.id}.{attribute}"
                errors.append((line, message))
            elif hasattr(name, "resolved_annotation"):
                type_name = re.match(r"[a-zA-Z.]*", name.resolved_annotation).group()
                if type_name in methods and attribute not in methods[type_name]:
                    line = name.lineno
                    message = (
                        f"method {attribute} called on {type_name.lower()} {name.id}"
                    )
                    errors.append((line, message))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = node.func.id
            if function in BUILTINS and function not in functions:
                line = node.lineno
                message = f"built-in function {function}()"
                errors.append((line, message))
        elif isinstance(node, ast.For) and node.orelse and "for else" not in options:
            line = node.orelse[0].lineno
            message = "else in for-loop"
            errors.append((line, message))
        elif (
            isinstance(node, ast.While) and node.orelse and "while else" not in options
        ):
            line = node.orelse[0].lineno
            message = "else in while-loop"
            errors.append((line, message))
    errors.sort()
    for index in range(len(errors) - 1, 0, -1):
        if errors[index] == errors[index - 1]:
            del errors[index]
    return errors


# ----- main functions -----


def check_folder(folder: str, last_unit: int, check_method_calls: bool) -> None:
    """Check all Python files in `folder` and its subfolders."""
    global_constructs = get_constructs(last_unit)
    for current_folder, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py"):
                if not last_unit and (file_unit := get_unit(filename)):
                    constructs = get_constructs(file_unit)
                else:
                    constructs = global_constructs
                fullname = os.path.join(current_folder, filename)
                check_file(fullname, constructs, check_method_calls)


def check_file(filename: str, constructs: tuple, check_method_calls: bool) -> None:
    """Check that the file only uses the allowed constructs."""
    try:
        with open(filename) as file:
            source = file.read()
        if check_method_calls and METHODS:
            tree = annotate_ast.annotate_source(source, ast, PYTYPE_OPTIONS)
        else:
            tree = ast.parse(source)
        errors = check_tree(tree, constructs, source.splitlines())
        for line, message in errors:
            print(f"{filename}:{line}: {message}")
    except OSError as error:
        print(error)
    except SyntaxError as error:
        #  write 'file:n: error' instead of 'file: error (..., line n)'
        message = str(error)
        if match := re.search(r"\(.*, line (\d+)\)", message):
            line = int(match.group(1))
            message = message[: match.start()] + message[match.end() :]
            print(f"{filename}:{line}: can't parse: {message}")
        else:
            print(f"{filename}: can't parse: {message}")
    except annotate_ast.PytypeError as error:
        #  write 'file:n: error' instead of 'Error reading file ... at line n: error'
        message = str(error)
        if match := re.match(r"Error .* at line (\d+): (.*)", message):
            line = int(match.group(1))
            message = match.group(2)
            print(f"{filename}:{line}: can't parse: {message}")
        else:
            print(f"{filename}: can't parse: {message}")


# ---- main program ----

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Check that the code only uses certain constructs. "
        "See allowed.py for how to specify the allowed constructs."
    )
    argparser.add_argument(
        "-m",
        "--methods",
        action="store_true",
        help="Enable method call checking",
    )
    argparser.add_argument(
        "-u",
        "--unit",
        type=int,
        default=0,
        help="only use constructs from units 1 to UNIT (default: all units)",
    )
    argparser.add_argument(
        "file_or_folder", nargs="+", help="Python file or folder to check"
    )
    args = argparser.parse_args()

    if args.unit < 0:
        sys.exit("error: unit must be positive")

    if error := check_language() or (error := check_imports()):
        sys.exit(error)

    if args.methods:
        if METHOD_CHECK_ERROR:
            sys.exit(METHOD_CHECK_ERROR)
        else:
            check_method_calls = True
        reminder = ""
    else:
        check_method_calls = False
        reminder = "Method calls have NOT been checked. Use option -m or --methods to enable (pytype and Python version 3.7 to 3.10 required)"

    args.file_or_folder.sort()
    for name in args.file_or_folder:
        if os.path.isdir(name):
            check_folder(name, args.unit, check_method_calls)
        elif name.endswith(".py"):
            unit = args.unit if args.unit else get_unit(name)
            check_file(name, get_constructs(unit), check_method_calls)
        else:
            print(f"{name}: not a folder nor a Python file")

    if reminder:
        print(reminder)
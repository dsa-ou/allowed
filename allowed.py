"""Check that Python and notebook files only use the allowed constructs."""

import argparse
import ast
import json
import os
import re
import sys

PYTHON_VERSION = sys.version_info[:2]
if (3, 7) <= PYTHON_VERSION <= (3, 10):
    try:
        import pytype
        from pytype.tools.annotate_ast import annotate_ast

        PYTYPE_OPTIONS = pytype.config.Options.create(python_version=PYTHON_VERSION)
        PYTYPE_INSTALLED = True
    except ImportError:
        PYTYPE_INSTALLED = False
else:
    PYTYPE_INSTALLED = False
try:
    from IPython.core.inputtransformer2 import TransformerManager as Transformer

    IPYTHON_INSTALLED = True
except ImportError:
    IPYTHON_INSTALLED = False


# ----- Python's Abstract Syntax Tree (AST) -----

# ABSTRACT maps strings (syntax descriptions) to the `ast` node classes
# listed in https://docs.python.org/3.10/library/ast.html.
# The strings can appear as values of dictionary "LANGUAGE" in the JSON file.
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

# optional constructs that can appear in dictionary "LANGUAGE"
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

# set of all built-in functions that can appear in dictionary "LANGUAGE"
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


def check_language() -> set:
    """Return the unknown constructs in LANGUAGE."""
    allowed = set()
    for constructs in LANGUAGE.values():
        allowed.update(set(constructs))
    return allowed - ABSTRACT.keys() - BUILTINS - OPTIONS


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


def location(line: int, line_cell_map: list) -> tuple[int, int]:
    """Return (0, line) if not a notebook, otherwise (cell, relative line)."""
    return line_cell_map[line] if line_cell_map else (0, line)


# ----- main functions -----


def check_tree(
    tree: ast.AST,
    constructs: tuple,
    source: list,
    line_cell_map: list,
    errors: list,
) -> None:
    """Check if tree only uses allowed constructs. Add violations to errors."""
    language, options, imports, functions, methods = constructs
    for node in ast.walk(tree):
        # if a node has no line number, handle it via its parent
        if isinstance(node, NO_LINE):
            pass
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp)):
            if not isinstance(node.op, language):
                cell, line = location(node.lineno, line_cell_map)
                message = CONCRETE.get(type(node.op), "unknown operator")
                errors.append((cell, line, message))
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if not isinstance(op, language):
                    cell, line = location(node.lineno, line_cell_map)
                    message = CONCRETE.get(type(op), "unknown operator")
                    errors.append((cell, line, message))
        elif not isinstance(node, language):
            if hasattr(node, "lineno"):
                cell, line = location(node.lineno, line_cell_map)
                message = source[node.lineno - 1].strip()
            else:
                # if a node has no line number, report it for inclusion in NO_LINE
                cell, line = 0, 0
                message = f"unknown construct {str(node)} at unknown line"
            errors.append((cell, line, message))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in imports:
                    cell, line = location(alias.lineno, line_cell_map)
                    message = f"import {alias.name}"
                    errors.append((cell, line, message))
        elif isinstance(node, ast.ImportFrom):
            if node.module not in imports:
                cell, line = location(node.lineno, line_cell_map)
                message = f"from {node.module} import ..."
                errors.append((cell, line, message))
            else:
                for alias in node.names:
                    if alias.name not in imports[node.module]:
                        cell, line = location(alias.lineno, line_cell_map)
                        message = f"from {node.module} import {alias.name}"
                        errors.append((cell, line, message))
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            name = node.value
            attribute = node.attr
            if name.id in imports and attribute not in imports[name.id]:
                cell, line = location(node.lineno, line_cell_map)
                message = f"{name.id}.{attribute}"
                errors.append((cell, line, message))
            elif hasattr(name, "resolved_annotation"):
                type_name = re.match(r"[a-zA-Z.]*", name.resolved_annotation).group()
                if type_name in methods and attribute not in methods[type_name]:
                    cell, line = location(name.lineno, line_cell_map)
                    message = (
                        f"method {attribute} called on {type_name.lower()} {name.id}"
                    )
                    errors.append((cell, line, message))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = node.func.id
            if function in BUILTINS and function not in functions:
                cell, line = location(node.lineno, line_cell_map)
                message = f"built-in function {function}()"
                errors.append((cell, line, message))
        elif isinstance(node, ast.For) and node.orelse and "for else" not in options:
            cell, line = location(node.orelse[0].lineno, line_cell_map)
            message = "else in for-loop"
            errors.append((cell, line, message))
        elif (
            isinstance(node, ast.While) and node.orelse and "while else" not in options
        ):
            cell, line = location(node.orelse[0].lineno, line_cell_map)
            message = "else in while-loop"
            errors.append((cell, line, message))


def check_folder(folder: str, last_unit: int, check_method_calls: bool) -> None:
    """Check all Python files in `folder` and its subfolders."""
    global_constructs = get_constructs(last_unit)
    for current_folder, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py") or filename.endswith(".ipynb"):
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
            if filename.endswith(".ipynb"):
                source, line_cell_map, errors = read_notebook(file.read())
            else:
                source = file.read()
                line_cell_map = []
                errors = []
        if check_method_calls and METHODS:
            tree = annotate_ast.annotate_source(source, ast, PYTYPE_OPTIONS)
        else:
            tree = ast.parse(source)
        check_tree(tree, constructs, source.splitlines(), line_cell_map, errors)
        errors.sort()
        last_error = None
        for error in errors:
            if error != last_error:
                cell, line, message = error
                if cell:
                    print(f"{filename}:cell_{cell}:{line}: {message}")
                else:
                    print(f"{filename}:{line}: {message}")
            last_error = error
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


SYNTAX_MSG = "SYNTAX ERROR: this cell has not been checked"


def read_notebook(file_contents: str) -> tuple[str, list, list]:
    """Return a triple (source, map, errors).

    source: the concatenated lines of the code cells without syntax errors
    map: an array mapping absolute lines 1, 2, ... to (cell, relative line) pairs
    errors: (cell, line, message) triples indicating where syntax errors occurred

    If IPython isn't installed, cells with magics trigger syntax errors.
    """
    cell_num = 0
    line_cell_map = [(0, 0)]  # line_cell_map[0] is never used
    source_list, errors = [], []
    notebook = json.loads(file_contents)
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell_num += 1
            cell_source = "".join(cell["source"])
            try:
                if IPYTHON_INSTALLED:
                    cell_source = Transformer().transform_cell(cell_source)
                ast.parse(cell_source)
                source_list.append(cell_source)
                for cell_line_num in range(1, cell_source.count("\n") + 2):
                    line_cell_map.append((cell_num, cell_line_num))
            except SyntaxError as error:
                errors.append((cell_num, error.lineno, SYNTAX_MSG))
    source_str = "\n".join(source_list)
    return source_str, line_cell_map, errors


# ---- main program ----

if __name__ == "__main__":
    if PYTHON_VERSION < (3, 10):
        sys.exit("error: can't check files (need Python 3.10 or higher)")

    argparser = argparse.ArgumentParser(
        description="Check that the code only uses certain constructs. "
        "See http://github.com/dsa-ou/allowed for how to specify the constructs."
    )
    argparser.add_argument(
        "-m",
        "--methods",
        action="store_true",
        help="enable method call checking",
    )
    argparser.add_argument(
        "-u",
        "--unit",
        type=int,
        default=0,
        help="only use constructs from units 1 to UNIT (default: all units)",
    )
    argparser.add_argument(
        "-c",
        "--config",
        default="m269.json",
        help="configuration file (default: m269.json)",
    )
    argparser.add_argument("file_or_folder", nargs="+", help="file or folder to check")
    args = argparser.parse_args()

    if args.methods and not PYTYPE_INSTALLED:
        sys.exit("error: can't check method calls (need pytype)")
    if args.unit < 0:
        sys.exit("error: unit must be positive")

    configuration = json.load(open(args.config))
    FILE_UNIT = configuration.get("FILE_UNIT", "")
    LANGUAGE = {}
    for key, value in configuration["LANGUAGE"].items():
        LANGUAGE[int(key)] = value
    IMPORTS = {}
    for key, value in configuration["IMPORTS"].items():
        IMPORTS[int(key)] = value
    METHODS = {}
    for key, value in configuration["METHODS"].items():
        METHODS[int(key)] = value
    if unknown := check_language():
        sys.exit(f"error: unknown constructs: {', '.join(unknown)}")
    if error := check_imports():
        sys.exit(error)

    for name in args.file_or_folder:
        if os.path.isdir(name):
            check_folder(name, args.unit, args.methods)
        elif name.endswith(".py") or name.endswith(".ipynb"):
            unit = args.unit if args.unit else get_unit(os.path.basename(name))
            check_file(name, get_constructs(unit), args.methods)
        else:
            print(f"{name}: not a folder, Python file or notebook")

    if not args.methods:
        print("warning: didn't check method calls (use option -m)")
    if not IPYTHON_INSTALLED:
        print("warning: didn't check notebook cells with magics (need IPython)")

"""Check that Python and notebook files only use the allowed constructs."""

__version__ = "1.5.2"  # same as in pyproject.toml

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

issues = 0  # number of issues (unknown constructs) found
py_checked = 0  # number of Python files checked
nb_checked = 0  # number of notebooks checked
unchecked = 0  # number of .py and .ipynb files skipped due to syntax or other errors

PYTHON_VERSION = sys.version_info[:2]

# pytype works for <= 3.12 and allowed for >= 3.10, when `ast` module changed
if PYTHON_VERSION in [(3, 10), (3, 11), (3, 12)]:
    try:
        import pytype
        from pytype.tools.annotate_ast import annotate_ast

        # configuration for 3.12 crashes when annotating AST with comprehensions
        PYTYPE_OPTIONS = pytype.config.Options.create(
            python_version=min((3, 11), PYTHON_VERSION)
        )
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
    "try": ast.Try,  # allows `except`, `else` and `finally`
    "with": ast.With,
    # other statements
    "=": ast.Assign,
    "+=": ast.AugAssign,  # allows `-=`, `*=`, etc.
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

# these 'wrapper' nodes must not be flagged as unknown constructs
IGNORE = (
    ast.Module,
    ast.alias,  # part of an `import` statement
    ast.AnnAssign,  # wraps an assignment with a type hint
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
    ast.ExceptHandler,  # part of a `try` statement
    ast.FormattedValue,  # part of an f-string
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

# types that pytype reports in lowercase since 2024.10.11
BUILTIN_TYPES = ("Dict", "List", "Set", "Tuple")

# ----- check configuration -----

# the configuration will be read in main()
FILE_UNIT: str  # regex of unit within file name
LANGUAGE: dict[int, list[str]]  # unit -> list of constructs
IMPORTS: dict[int, dict[str, list[str]]]  # unit -> module -> list of names
METHODS: dict[int, dict[str, list[str]]]  # unit -> datatype -> list of methods


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
            "CONFIGURATION ERROR: modules are allowed but import statements aren't\n"
            "fix 1: make IMPORTS empty\n"
            "fix 2: add 'import' and/or 'from import' to LANGUAGE"
        )
    if first_import and not first_module:
        return (
            "CONFIGURATION ERROR: no modules to import\n"
            "fix 1: add modules to IMPORTS\n"
            "fix 2: remove 'import' and 'from import' from LANGUAGE"
        )
    if first_module < first_import:
        return (
            "CONFIGURATION ERROR: modules are introduced before import statement\n"
            f"fix 1: in IMPORTS, move modules to unit {first_import} or later\n"
            f"fix 2: in LANGUAGE, move import statements to unit {first_module} or earlier"  # noqa: E501
        )
    return ""


# ----- auxiliary functions -----


def plural(number: int) -> str:
    """Return 's' or '' depending on number."""
    return "" if number == 1 else "s"


def show_units(filename: str, last_unit: int) -> None:
    """Print a message about the units being checked."""
    if last_unit == 1:
        units = "unit 1"
    elif last_unit > 0:
        units = f"units 1–{last_unit}"  # noqa: RUF001 (it's an en-dash)
    else:
        units = "all units"
    print(f"INFO: checking {filename} against {units}")


def get_unit(filename: str) -> int:
    """Return the file's unit or zero (consider all units)."""
    if FILE_UNIT and (match := re.search(FILE_UNIT, filename)):
        return int(match.group(1))
    return 0


def get_language(last_unit: int) -> tuple[type[ast.AST], ...]:
    """Return the allowed language elements up to the given unit.

    If `last_unit` is zero, return the elements in all units.
    """
    allowed = []
    for unit, constructs in LANGUAGE.items():
        if not last_unit or unit <= last_unit:
            for construct in constructs:
                if ast_class := ABSTRACT.get(construct, None):
                    allowed.append(ast_class)  # noqa: PERF401
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
                    allowed.append(construct)  # noqa: PERF401
    return allowed


def get_imports(last_unit: int) -> dict[str, list[str]]:
    """Return the allowed imports up to the given unit.

    If `last_unit` is zero, return the imports in all units.
    """
    allowed: dict[str, list[str]] = {}
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
    allowed: dict[str, list[str]] = {}
    for unit, methods in METHODS.items():
        if not last_unit or unit <= last_unit:
            for datatype, names in methods.items():
                if datatype in BUILTIN_TYPES:
                    datatype = datatype.lower()
                if datatype in allowed:
                    allowed[datatype].extend(names)
                else:
                    allowed[datatype] = names
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


def ignore(node: ast.AST, source: list[str]) -> bool:
    """Return True if node is on a line to be ignored."""
    return hasattr(node, "lineno") and source[node.lineno - 1].rstrip().endswith(
        "# allowed"
    )


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
        # If a node has no line number, handle it via its parent.
        if isinstance(node, NO_LINE) or ignore(node, source):
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
                message = CONCRETE.get(type(node), "unknown construct")
            else:
                # If a node has no line number, report it for inclusion in NO_LINE.
                cell, line = 0, 0
                message = f"unknown construct {node} at unknown line"
            errors.append((cell, line, message))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in imports:
                    cell, line = location(alias.lineno, line_cell_map)
                    message = f"{alias.name}"
                    errors.append((cell, line, message))
        elif isinstance(node, ast.ImportFrom):
            if node.module not in imports:
                cell, line = location(node.lineno, line_cell_map)
                message = f"{node.module}"
                errors.append((cell, line, message))
            else:
                for alias in node.names:
                    if alias.name not in imports[node.module]:
                        cell, line = location(alias.lineno, line_cell_map)
                        message = f"{alias.name}"
                        errors.append((cell, line, message))
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            name = node.value
            attribute = node.attr
            if name.id in imports:
                if attribute not in imports[name.id]:
                    cell, line = location(node.lineno, line_cell_map)
                    message = f"{name.id}.{attribute}"
                    errors.append((cell, line, message))
            elif hasattr(name, "resolved_annotation"):  # noqa: SIM102
                if matched := re.match(r"[a-zA-Z.]*", name.resolved_annotation):
                    type_name = matched.group()
                    if type_name in BUILTIN_TYPES:
                        type_name = type_name.lower()
                    if type_name in methods and attribute not in methods[type_name]:
                        cell, line = location(name.lineno, line_cell_map)
                        message = f"{type_name}.{attribute}()"
                        errors.append((cell, line, message))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = node.func.id
            if function in BUILTINS and function not in functions:
                cell, line = location(node.lineno, line_cell_map)
                message = f"{function}()"
                errors.append((cell, line, message))
        elif isinstance(node, ast.For) and node.orelse and "for else" not in options:
            # we assume `else:` is in the line before the first statement in that block
            cell, line = location(node.orelse[0].lineno - 1, line_cell_map)
            message = "for-else"
            errors.append((cell, line, message))
        elif (
            isinstance(node, ast.While) and node.orelse and "while else" not in options
        ):
            cell, line = location(node.orelse[0].lineno - 1, line_cell_map)
            message = "while-else"
            errors.append((cell, line, message))


def check_folder(
    folder: str,
    last_unit: int,
    check_method_calls: bool,  # noqa: FBT001
    report_first: bool,  # noqa: FBT001
    verbose: bool,  # noqa: FBT001
) -> None:
    """Check all Python files in `folder` and its subfolders."""
    global_constructs = get_constructs(last_unit)
    for current_folder, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith((".py", ".ipynb")):
                fullname = str(Path(current_folder) / filename)
                if not last_unit and (file_unit := get_unit(filename)):
                    constructs = get_constructs(file_unit)
                    if verbose:
                        show_units(fullname, file_unit)
                else:
                    constructs = global_constructs
                    if verbose:
                        show_units(fullname, last_unit)
                check_file(fullname, constructs, check_method_calls, report_first)


def check_file(
    filename: str,
    constructs: tuple,
    check_method_calls: bool,  # noqa: FBT001
    report_first: bool,  # noqa: FBT001
) -> None:
    """Check that the file only uses the allowed constructs."""
    global py_checked, nb_checked, unchecked, issues

    try:
        with Path(filename).open(encoding="utf-8", errors="surrogateescape") as file:
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
        messages = set()  # for --first option: the unique messages (except errors)
        last_error = None
        for cell, line, message in errors:
            if (cell, line, message) != last_error and message not in messages:
                if cell:
                    print(f"{filename}:cell_{cell}:{line}: {message}")
                else:
                    print(f"{filename}:{line}: {message}")
                # don't count syntax errors as unknown constructs
                if "ERROR" not in message:
                    issues += 1
                if report_first and "ERROR" not in message:
                    messages.add(message)
                last_error = (cell, line, message)
        if filename.endswith(".py"):
            py_checked += 1
        else:
            nb_checked += 1
    except OSError as error:
        print(f"{filename}: OS ERROR: {error.strerror}")
        unchecked += 1
    except SyntaxError as error:
        print(f"{filename}:{error.lineno}: SYNTAX ERROR: {error.msg}")
        unchecked += 1
    except UnicodeError as error:
        print(f"{filename}: UNICODE ERROR: {error}")
        unchecked += 1
    except json.decoder.JSONDecodeError as error:
        print(f"{filename}:{error.lineno}: FORMAT ERROR: invalid notebook format")
        unchecked += 1
    except ValueError as error:
        print(f"{filename}: VALUE ERROR: {error}")
        unchecked += 1
    except annotate_ast.PytypeError as error:
        #  write 'file:n: error' instead of 'Error reading file ... at line n: error'
        message = str(error)
        if match := re.match(r"Error .* at line (\d+): (.*)", message):
            line = int(match.group(1))
            message = match.group(2)
            print(f"{filename}:{line}: PYTYPE ERROR: {message}")
        else:
            print(f"{filename}: PYTYPE ERROR: {message}")
        unchecked += 1


def read_notebook(file_contents: str) -> tuple[str, list, list]:
    """Return a triple (source, map, errors).

    source: the concatenated lines of the code cells without syntax errors
    map: an array mapping absolute lines 1, 2, ... to (cell, relative line) pairs
    errors: (cell, line, message) triples indicating where syntax errors occurred

    If IPython isn't installed, cells with magics trigger syntax errors.
    """
    cell_num = 0
    line_cell_map: list[tuple[int, int]] = [(0, 0)]  # line_cell_map[0] is never used
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
                    line_cell_map.append((cell_num, cell_line_num))  # noqa: PERF401
            except SyntaxError as error:
                errors.append((cell_num, error.lineno, f"SYNTAX ERROR: {error.msg}"))
    source_str = "\n".join(source_list)
    return source_str, line_cell_map, errors


# ---- main program ----


def main() -> None:
    """Implement the CLI."""
    global FILE_UNIT, LANGUAGE, IMPORTS, METHODS

    argparser = argparse.ArgumentParser(
        prog="allowed",
        description="Check that the code only uses certain constructs. "
        "See http://dsa-ou.github.io/allowed for how to specify the constructs.",
    )
    argparser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    argparser.add_argument(
        "-f",
        "--first",
        action="store_true",
        help="report only the first of each disallowed construct (per file)",
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
        help="only allow constructs from units 1 to UNIT (default: all units)",
    )
    argparser.add_argument(
        "--file-unit",
        default="",
        help="regular expression of unit number in file name (default: '')",
    )
    argparser.add_argument(
        "-c",
        "--config",
        default="m269.json",
        help="allow the constructs given in CONFIG (default: m269.json)",
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show additional info as files are processed",
    )
    argparser.add_argument("file_or_folder", nargs="+", help="file or folder to check")
    args = argparser.parse_args()

    if PYTHON_VERSION < (3, 10):
        print("ERROR: can't check code (Python 3.10 or later needed)")
        sys.exit(1)
    if args.methods and not PYTYPE_INSTALLED:
        if PYTHON_VERSION > (3, 12):
            print("ERROR: can't check method calls (Python < 3.13 needed)")
        else:
            print("ERROR: can't check method calls (pytype not installed)")
        sys.exit(1)
    if args.unit < 0:
        print("ERROR: unit must be positive")
        sys.exit(1)

    try:
        filename = args.config
        if not filename.endswith(".json"):
            filename += ".json"
        # Look for configuration locally, then in this script's folder.
        for file in (Path(filename), Path(__file__).parent / filename):
            if file.exists():
                with file.open() as config_file:
                    configuration = json.load(config_file)
                    if args.verbose:
                        print(f"INFO: using configuration {file.resolve()}")
                    break
        else:
            print(f"CONFIGURATION ERROR: {filename} not found")
            sys.exit(1)
        FILE_UNIT = args.file_unit
        LANGUAGE = {}
        for key, value in configuration["LANGUAGE"].items():
            if not isinstance(value, list):
                raise TypeError
            LANGUAGE[int(key)] = value
        IMPORTS = {}
        for key, value in configuration["IMPORTS"].items():
            if not isinstance(value, dict):
                raise TypeError
            IMPORTS[int(key)] = value
        METHODS = {}
        for key, value in configuration["METHODS"].items():
            if not isinstance(value, dict):
                raise TypeError
            METHODS[int(key)] = value
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("CONFIGURATION ERROR: invalid JSON format")
        sys.exit(1)
    if unknown := check_language():
        print(f"CONFIGURATION ERROR: unknown constructs:\n{', '.join(unknown)}")
        sys.exit(1)
    if error := check_imports():
        print(error)
        sys.exit(1)

    for name in args.file_or_folder:
        if Path(name).is_dir():
            check_folder(name, args.unit, args.methods, args.first, args.verbose)
        elif name.endswith((".py", ".ipynb")):
            unit = args.unit if args.unit else get_unit(Path(name).name)
            if args.verbose:
                show_units(name, unit)
            check_file(name, get_constructs(unit), args.methods, args.first)
        else:
            print(f"WARNING: {name} skipped: not a folder, Python file or notebook")

    if args.verbose:
        print(
            "INFO: checked",
            f"{py_checked} Python file{plural(py_checked)} and",
            f"{nb_checked} notebook{plural(nb_checked)}",
        )
        if issues:
            print(
                f"INFO: the {issues} Python construct{plural(issues)}",
                f"listed above {'are' if issues > 1 else 'is'} not allowed",
            )
        elif nb_checked or py_checked:
            print("INFO: found no disallowed Python constructs")
        if unchecked:
            print(
                f"INFO: didn't check {unchecked} Python",
                f"file{plural(unchecked)} or notebook{plural(unchecked)}",
                "due to syntax or other errors",
            )
    if args.first and issues:
        print(
            "WARNING:",
            "other occurrences of the listed constructs may exist (don't use option -f)",  # noqa: E501
        )
    if (py_checked or nb_checked) and not args.methods:
        print("WARNING: didn't check method calls (use option -m if possible)")
    if nb_checked and not IPYTHON_INSTALLED:
        print(
            "WARNING: didn't check notebook cells with %-commands (IPython not installed)"  # noqa: E501
        )


if __name__ == "__main__":
    main()

"""Check that Python files only use the allowed constructs."""

import ast
import os
import re
import sys

PYTHON_VERSION = sys.version_info[:2]
if (3, 7) <= PYTHON_VERSION <= (3, 10):
    try:
        import pytype
        from pytype.tools.annotate_ast import annotate_ast
        PYTYPE_OPTIONS = pytype.config.Options.create(python_version = PYTHON_VERSION)
        CHECK_METHOD_CALLS = True
    except ImportError:
        print("warning: pytype not installed: won't check method calls")
        CHECK_METHOD_CALLS = False
else:
    print("warning: Python version not supported: won't check method calls")
    CHECK_METHOD_CALLS = False

# ----- configuration -----

# FILE_UNIT is a regexp that extracts the unit from the file's name.
# If there's a match, the unit number must be the first group.
# If there's no match, the user-given unit will be used.

FILE_UNIT = r"^(\d+)"  # file name starts with the unit number
# FILE_UNIT = r"(\d+).py$"  # file name ends with the unit number
# FILE_UNIT = ""  # file names don't include a unit number

# LANGUAGE[n] are the language elements introduced in unit n.
# Language elements are represented by the corresponding `ast` classes,
# taken from https://docs.python.org/3/library/ast.html.
# For example, if `break` and `continue` are introduced in unit 5,
# add an entry `5: (ast.Break, ast.Continue),`.
# Each entry must be a tuple (not a list or set).

LANGUAGE = {
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

# FUNCTIONS[n] are the functions introduced in unit n.
FUNCTIONS = {
    2: ["help", "min", "max", "round", "print", "int", "float"],
    4: ["len", "sorted", "str", "range", "list", "tuple"],
    8: ["dict", "set", "ord", "hash"],
    17: ["super"],
    18: ["abs"],
}

# METHODS[n] is a dictionary of the methods introduced in unit n: the keys are the types.
# Other builtin types are 'str' and 'Tuple'.

METHODS = {
    4: {"List": ["insert", "append", "pop", "sort"]},
    7: {"collections.deque": ["append", "appendleft", "pop", "popleft"]},
    8: {"Dict": ["items"], "Set": ["add", "discard", "union", "intersection", "difference"]},
    11: {"Set": ["pop"]},
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


def get_language(last_unit: int) -> tuple[ast.AST]:
    """Return the allowed language elements up to the given unit.

    If `last_unit` is zero, return the elements in all units.
    """
    allowed = ()
    for unit, elements in LANGUAGE.items():
        if not last_unit or unit <= last_unit:
            allowed += elements
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
    for unit, functions in FUNCTIONS.items():
        if not last_unit or unit <= last_unit:
            allowed.update(functions)
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
        get_imports(last_unit),
        get_functions(last_unit),
        get_methods(last_unit),
    )


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

# ast doesn't unparse operators, so we need to do it ourselves
OPERATORS = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.MatMult: "@",  # matrix multiplication
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    ast.LShift: "<<",
    ast.RShift: ">>",
    # unary operators
    ast.USub: "-",
    ast.UAdd: "+",
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
    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
}


def check_tree(tree: ast.AST, constructs: tuple, source: list) -> list:
    """Check if tree only uses allowed constructs."""
    language, imports, functions, methods = constructs
    errors = []
    for node in ast.walk(tree):
        # an operator node has no line number, so handle it via its parent
        if isinstance(node, (ast.operator, ast.unaryop, ast.boolop, ast.cmpop)):
            pass
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp)):
            if not isinstance(node.op, language):
                line = node.lineno
                message = OPERATORS.get(type(node.op), "unknown operator")
                errors.append((line, message))
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if not isinstance(op, language):
                    line = node.lineno
                    message = OPERATORS.get(type(op), "unknown operator")
                    errors.append((line, message))
        elif not isinstance(node, language):
            line = node.lineno
            message = source[line - 1].strip()
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
            elif hasattr(name, 'resolved_annotation'):
                type_name = re.match(r'[a-zA-Z.]*', name.resolved_annotation).group()
                if type_name in methods and attribute not in methods[type_name]:
                    line = name.lineno
                    message = f"method {attribute} called on {type_name.lower()} {name.id}"
                    errors.append((line, message))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function = node.func.id
            if function in BUILTINS and function not in functions:
                line = node.lineno
                message = f"built-in function {function}()"
                errors.append((line, message))
        elif isinstance(node, ast.For) and node.orelse and not FOR_ELSE:
            line = node.orelse[0].lineno
            message = "else in for-loop"
            errors.append((line, message))
        elif isinstance(node, ast.While) and node.orelse and not WHILE_ELSE:
            line = node.orelse[0].lineno
            message = "else in while-loop"
            errors.append((line, message))
    errors.sort()
    for index in range(len(errors) - 1, 0, -1):
        if errors[index] == errors[index - 1]:
            del errors[index]
    return errors


# ----- main functions -----


def check_folder(folder: str, last_unit: int) -> None:
    """Check all Python files in `folder` and its subfolders."""
    global_constructs = get_constructs(last_unit)
    for current, subfolders, files in os.walk(folder):
        subfolders.sort()
        for filename in sorted(files):
            if filename.endswith(".py"):
                if not last_unit and (file_unit := get_unit(filename)):
                    constructs = get_constructs(file_unit)
                else:
                    constructs = global_constructs
                fullname = os.path.join(current, filename)
                check_file(fullname, constructs)


def check_file(filename: str, constructs: tuple) -> None:
    """Check that the file only uses the allowed constructs."""
    try:
        with open(filename) as file:
            source = file.read()
        if CHECK_METHOD_CALLS and METHODS:
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



def first_import_and_module() -> tuple[int, int]:
    """Return when an import statement and a module are first introduced."""
    statements = []
    for unit, elements in LANGUAGE.items():
        if ast.Import in elements or ast.ImportFrom in elements:
            statements.append(unit)
    first_import = min(statements) if statements else 0
    first_module = min(IMPORTS.keys()) if IMPORTS else 0
    return first_import, first_module


# ---- main program ----

HELP = """Usage: python allowed.py <file or folder> [<unit>]

Check the Python file (or all Python files in the folder and its subfolders)
for constructs that are NOT introduced up to the given unit (a positive number).
If unit is omitted, use all units or the unit given in the file's name.

See allowed.py for how to configure the allowed constructs.
"""

if __name__ == "__main__":
    try:
        ARGN = len(sys.argv)
        assert ARGN in (2, 3)
        NAME = sys.argv[1]
        unit = int(sys.argv[2]) if ARGN == 3 else 0
        assert unit >= 0
    except:
        print(HELP)
        sys.exit(1)

    first_import, first_module = first_import_and_module()
    if first_module and not first_import:
        print(
            "error: modules are allowed but import statements aren't\n"
            "fix 1: make IMPORTS empty\n"
            "fix 2: add ast.Import and/or ast.ImportFrom to LANGUAGE"
        )
        sys.exit(1)
    elif first_import and not first_module:
        print(
            "error: import statement is allowed but no modules are introduced\n"
            "fix 1: add modules to IMPORTS\n"
            "fix 2: remove ast.Import and ast.ImportFrom from LANGUAGE"
        )
        sys.exit(1)
    elif first_module < first_import:
        print(
            "error: modules are introduced before import statement\n"
            "fix 1: in IMPORTS, move modules to unit {first_import} or later\n"
            "fix 2: in LANGUAGE, move import statements to unit {first_module} or sooner"
        )
        sys.exit(1)

    if os.path.isdir(NAME):
        check_folder(NAME, unit)
    else:
        if not NAME.endswith(".py"):
            print(f"{NAME}: not a Python file")
            sys.exit(1)
        if not unit:
            unit = get_unit(NAME)
        check_file(NAME, get_constructs(unit))

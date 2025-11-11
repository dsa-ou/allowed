"""Meaningless code just to test the checker.

The code in this file MUST be executable, without syntax errors.
This file is NOT meant to cover all Python constructs.
"""

import math
import types
from random import choice, shuffle
from typing import Any, Iterable

# Atomic types: literals, operators, functions

# Numbers
f = 9e5 + 8.3e-2 - 7_000 * 6 / -5 // 4 % 3**2
1 << 3
abs(min(1, max(2, 3)))
f.is_integer()  # allowed

# Booleans
True and False or not True
5 < 3 > 2 == 1 != 0 <= 5 >= -4
True if 1 > 0 else False

# Built-in collections: literals, operators, functions, methods

# Strings
s = "hello" + str(123)
f: float
f"{f}3" in s
s.upper()
"abc".upper()
s[2].join(["A", "B", "C"])
("" + " ").count(1)

# Lists
l = [] + list("abc") + [letter for letter in "abc"]
l.sort(reverse=True)
l.append(1)
l.pop()
l.insert(0, 2)

# Tuples
t = () + (1,) + tuple("abc")

# Operations common to all sequences
t[2] not in l[:3:-1] * 2
# The following allows all constructs on the same line.
l.count(t.index(1))  # allowed

# Sets
items = set() | {1, 2, 3} & {2, 3} ^ {3, 4} - {i for i in range(1, 10, 2)}
items.add(items.pop())
items.discard(9)
items.union(l)

# Dictionaries
d: dict[str, int] = {"a": 1, "b": 2}
d["c"]: int = int(f) + int("3")  # duplicate constructs are reported once per line
d.pop("a")
for key, value in d.items():
    print(key, value)

# Control flow statements
try:  # allowed
    for i in range(1, 5):
        while i < 6:
            if i == 0:
                i = 6
            elif i > 3:
                break
            else:
                i *= 2
        else:
            continue
    else:
        assert False, "unreachable"
except AssertionError as error:
    pass


# Functions
def whatever(values: list[int]) -> bool:
    """Pointless function."""
    return True


def some_function(strings: Iterable[str]) -> list[str]:
    list_of_str: list[str] = []
    for string in strings:
        list_of_str.append(string.strip().lower())  # chained methods
    return list_of_str


def another_test(txt: str):
    print(txt[0].upper())

def text_found(text, substring: str) -> bool:  # Ruff flags missing type hint
    return text.find(substring) != -1  # find() isn't reported

def text_found_2(text: str, substring: str) -> bool:
    text_copy: Any = text # Any is reported in line 10
    text_copy.find(substring) != -1  # find() isn't reported
    return [text][0].find(substring) != -1  # find() is reported


# Imported methods
math.sqrt(math.e)

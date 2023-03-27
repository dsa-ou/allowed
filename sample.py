# This is a test file for the allowed checker.

# Unit 2
# =, name, constant, def, return, function call, import, attribute,
# +, -, *, /, //, %, **, -x, help, min, max, round, print,
# math: floor, ceil, trunc, pi

# Constant
CONSTANT = 42

# Name
name = "example"

# Function definition, return, and function call
def square(x):
    return x ** 2

result = square(CONSTANT)

# Import and attribute
import math
pi = math.pi

# Arithmetic operations
addition = 1 + 2
subtraction = 5 - 3
multiplication = 2 * 3
division = 10 / 2
floor_division = 9 // 2
modulo = 10 % 3
exponentiation = 2 ** 3
negation = -CONSTANT

# Help, min, max, round, print
help(math.sqrt)
minimum = min(1, 2, 3)
maximum = max(1, 2, 3)
rounded = round(3.14)
print("Hello, world!")

# floor, ceil, trunc, and pi from math
floor_result = math.floor(3.14)
ceil_result = math.ceil(3.14)
trunc_result = math.trunc(3.14)
pi_value = math.pi

# Unit 3
# if, and, or, not, ==, !=, <, <=, >, >=

x = 5
y = 10

# If, and, or, not
if x < y and not x == y or x != y:
    print("x is less than y")

# Comparison operators
equal = x == y
not_equal = x != y
less_than = x < y
less_than_or_equal = x <= y
greater_than = x > y
greater_than_or_equal = x >= y

# Unit 4
# for, while, list literal, tuple literal, in, index, slice,
# keyword argument, bool, float, int, len, sorted, str, range, list, tuple,
# List: insert, append, pop, sort

# For loop
for i in range(5):
    print(i)

# While loop
count = 0
while count < 5:
    print(count)
    count = count + 1

# List and tuple literals
list_literal = [1, 2, 3]
tuple_literal = (1, 2, 3)

# In, index, slice
element_in_list = 1 in list_literal
index_value = list_literal[0]
sliced_list = list_literal[1:3]

# Keyword argument
def greet(person, greeting="Hello"):
    print(greeting, person)

greet("John", greeting="Hi")

# Bool, float, int
boolean_value = True
float_value = 3.14
integer_value = 42
boolean_value = bool(integer_value)
float_value = float(boolean_value)
integer_value = int(float_value)

# Len, sorted, str, range, list, tuple
list_length = len(list_literal)
sorted_list = sorted(list_literal, reverse=True)
string_value = str(integer_value)
range_value = range(5)
list_value = list(tuple_literal)
tuple_value = tuple(list_literal)

# List methods - insert, append, pop, sort
my_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
my_list.insert(2, 7)
my_list.append(3)
my_list.pop(4)
my_list.sort()

# Unit 6
# pass, class
# math: inf

# Pass
def do_nothing():
    pass

# Class
class MyClass:
    pass

# math.inf
inf = math.inf

# Unit 7
# from import
# deque

from collections import deque

# deque methods - append, appendleft, pop, popleft
dq = deque()
for n in range(5):
    dq.append(n)
dq.appendleft(dq.pop())
dq.popleft()

# Unit 8
# dict literal, set literal, not in, |, &, dict, set, ord, hash
# collections.Counter

# Dict and set literals
dict_literal = {"a": 1, "b": 2, "c": 3}
set_literal = {1, 2, 3}

# Not in, ord, hash
element_not_in_set = 4 not in set_literal
ascii_value = ord("a")
dash = hash("dash")

# dict, 
my_dict = dict()

# dict methods - items
for item in dict_literal.items():
    print(item)

# Set methods - add, discard, |, &, -, union, intersection, difference
my_set = set([1, 2, 3])
my_set.add(4)
my_set.discard(2)

union_set = {1, 2, 3} | {3, 4, 5}
intersection_set = {1, 2, 3} & {3, 4, 5}
difference_set = {1, 2, 3} - {3, 4, 5}

union_set = union_set.union(intersection_set)
intersection_set = intersection_set.intersection(union_set)
difference_set = difference_set.difference(intersection_set)

# collections.Counter (Unit 8)
from collections import Counter
word_count = Counter("dlrow olleh")

# Unit 11
# permutations, combinations, sqrt, factorial

import itertools

# Permutations and combinations from itertools
permutations = list(itertools.permutations([1, 2, 3]))
combinations = list(itertools.combinations([1, 2, 3], 2))

# Sqrt and factorial from math
square_root = math.sqrt(16)
factorial = math.factorial(5)

# Set methods - pop
my_set.pop()

# Unit 14
# shuffle, Callable

import random
import typing
from typing import Callable

# Shuffle from random
my_list = [1, 2, 3, 4, 5]
random.shuffle(my_list)

# Callable from typing
def call_me(callable_obj: Callable):
    callable_obj()

def my_func():
    print("Hello, world!")

call_me(my_func)

# Unit 16
# heapq: heappush, heappop

import heapq
from heapq import heappush, heappop

# Unit 17
# Hashable, random, super

import random
from typing import Hashable

# Random
random_value = random.random()

# Super
class Parent:
    def __init__(self, x):
        self.x = x

class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

# Unit 18
# abs

# Absolute value
abs_value = abs(-42)

# Unit 27
# getsource

import inspect

# Get source
source = inspect.getsource(greet)

# Random python with some dissallowed constructs

import types
from random import choice, shuffle

def is_prime(n: int) -> bool:
    """Check if a positive integer is prime."""
    assert n > 0
    if n == 1:
        return False
    for factor in range(2, n):
        if n % factor == 0:
            decision = False
            break
        elif factor > math.sqrt(n):
            decision = True
            break
    else:  # no break
        decision = True
    return decision


for n in range(10):
    try:
        print(n, "prime" if is_prime(n) else "not prime")
    except AssertionError:
        print(n, "not positive")


def odd_numbers(n: int) -> list[int]:
    """Return a list of the first n odd numbers."""
    result = []
    value = 0
    while True:
        if len(result) == n:
            break
        value += 1
        if value % 2 == 1:
            result.append(value)
        else:
            continue
    else:  # no break
        pass  # infinite loop finished
    return result


FIRST = 5
odd = odd_numbers(FIRST)
print(f"first {FIRST} odd numbers: {odd}")
if odd.count(2) == 1:
    print("2 is considered odd: that's odd!")
print("last odd generated:", odd.pop())

print("2^6 =", 1 << 6)
print("Euler number e =", math.e)
if type(odd_numbers) == types.FunctionType:
    print("odd_numbers is a function")


x = 5
x = "five"

"""Sample code to test the checker."""

import math
from random import shuffle, choice
import types


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
print(f"first {FIRST} odd numbers: {odd_numbers(FIRST)}")

print("2^6 =", 1 << 6)
print("Euler number e =", math.e)
if type(odd_numbers) == types.FunctionType:
    print("odd_numbers is a function")

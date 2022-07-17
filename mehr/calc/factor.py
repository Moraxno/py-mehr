import math
from typing import List, Tuple


def closest_factorization(x: int) -> Tuple[int, int]:
    """
    Returns the closest factorization (a, b) of x, where a is the larger factor and b is the smaller factor."""
    return next(factorization_generator(x))


def factors_of(x: int) -> List[int]:
    """
    Returns a list of the factors of x.
    """
    factors = [factor for factorization in factorization_generator(x) for factor in factorization]

    if factors[0] == factors[1]:
        return factors[1:]
    else:
        return factors


def factorization_generator(x: int) -> Tuple[int, int]:
    """
    Generates the factorization (a, b) of x from closest to farthest,
    where a is the larger factor and b is the smaller factor.
    """
    if int(x) != x:
        raise TypeError('x must be an integer.')

    x = int(x)

    if x < 1:
        raise ValueError('x must be greater than 0.')

    for i in range(int(math.sqrt(x)), 0, -1):
        if x % i == 0:
            yield x // i, i

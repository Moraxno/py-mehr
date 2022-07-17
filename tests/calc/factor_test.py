import pytest

from mehr.calc.factor import closest_factorization, factors_of

INT_TEST_SET = [
    (1, (1, 1)),
    (2, (2, 1)),
    (3, (3, 1)),
    (4, (2, 2)),
    (5, (5, 1)),
    (6, (3, 2)),
    (7, (7, 1)),
    (8, (4, 2)),
    (9, (3, 3)),
    (10, (5, 2)),
    (45, (9, 5)),
    (100, (10, 10)),
    (1_000, (40, 25)),
    (1_000_000, (1_000, 1_000))
]

FLOAT_TEST_SET = [
    (1.0, (1, 1)),
    (2.0, (2, 1)),
    (3.0, (3, 1)),
    (4.0, (2, 2)),
    (5.0, (5, 1)),
    (6.0, (3, 2)),
    (7.0, (7, 1)),
    (8.0, (4, 2)),
    (9.0, (3, 3)),
    (10.0, (5, 2)),
    (45.0, (9, 5)),
    (100.0, (10, 10)),
    (1_000.0, (40, 25)),
    (1_000_000.0, (1_000, 1_000))
]

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 9267975659
]

BIG_NUM = 5040

SQUARE_NUM = 64

FACTORS_OF_BIG_NUM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 35, 36, 40, 42, 45, 48, 56, 60, 63, 70, 72, 80, 84, 90, 105, 112, 120, 126, 140, 144, 168, 180, 210, 240, 252, 280, 315, 336, 360, 420, 504, 560, 630, 720, 840, 1008, 1260, 1680, 2520, 5040]

TOO_SMALL_VALUES = [0, -1, -42, -1_000_000_000]

FRACTION_VALUES = [1.00001, 1.5, 1.999, 0.333, 0.2, 1.0 / 7.0, 1.0 / 163.0]


def test_int_factorizations():
    for x, expected in INT_TEST_SET:
        assert closest_factorization(x) == expected


def test_floats_of_whole_numbers_factorization():
    for x, expected in FLOAT_TEST_SET:
        assert closest_factorization(x) == expected


def test_reject_lower_than_one():
    for x in TOO_SMALL_VALUES:
        with pytest.raises(ValueError):
            closest_factorization(x)


def test_reject_fractions():
    for x in FRACTION_VALUES:
        with pytest.raises(TypeError):
            closest_factorization(x)


def test_int_has_higher_priority_than_bigger_one():
    with pytest.raises(TypeError):
        closest_factorization(-1.0 / 163.0)


def test_factors_of_primes():
    for x in PRIMES:
        assert factors_of(x) == [x, 1]


def test_factors_of_big_num():
    maybe_factors = factors_of(BIG_NUM)

    for mf in maybe_factors:
        assert mf in FACTORS_OF_BIG_NUM

    for sf in FACTORS_OF_BIG_NUM:
        assert sf in maybe_factors


def test_factors_of_square():
    factors = factors_of(SQUARE_NUM)
    unique_factors = set(factors)

    assert len(factors) == len(unique_factors)

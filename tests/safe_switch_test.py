import pytest

from mehr import safe_switch
from mehr.exceptions import \
    CaseAfterDefaultException, \
    SameCaseException, \
    DoubleDefaultException, \
    NoDefaultException


def test_normaluse():
    i = 4
    j = 0

    with safe_switch(i) as (case, default, break_):
        if case(2):
            j = 1
        if case(4):
            j = 2
        if case(10):
            j = 5
            break_()
        if case(25):
            j = 12.5
        if default():
            j = -1

    assert(j == 5)


def test_caseafterdefault_does_raise():
    with pytest.raises(CaseAfterDefaultException):
        with safe_switch(42) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if default():
                pass
            if case(3):
                pass


def test_doubledefault_does_raise():
    with pytest.raises(DoubleDefaultException):
        with safe_switch(42) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if default():
                pass
            if default():
                pass


def test_samecase_does_raise():
    with pytest.raises(SameCaseException):
        with safe_switch(2) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if case(2):
                pass
            if default():
                pass


def test_nodefault_does_raise():
    with pytest.raises(NoDefaultException):
        with safe_switch(52) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if case(52):
                pass


def test_samecase_dominates_nodefault():
    with pytest.raises(SameCaseException):
        with safe_switch(52) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if case(2):
                pass


def test_samecase_raises_even_after_break():
    with pytest.raises(SameCaseException):
        with safe_switch(52) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if case(3):
                break_()
            if case(2):
                pass

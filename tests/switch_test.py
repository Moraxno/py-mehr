import pytest

from mehr import switch
from mehr.exceptions import \
    CaseAfterDefaultException, \
    SameCaseException, \
    DoubleDefaultException, \
    NoDefaultException


def test_normaluse():
    i = 4
    j = 0

    with switch(i) as (case, default, break_):
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
        with switch(42) as (case, default, break_):
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
        with switch(42) as (case, default, break_):
            if case(1):
                pass
            if case(2):
                pass
            if default():
                pass
            if default():
                pass

def test_samecase_doesnt_raise():
    j = 0
    with switch(2) as (case, default, break_):
        if case(1):
            pass
        if case(2):
            j = 2
        if case(2):
            j = 3
        if default():
            pass

    assert(j == 3)

def test_samecase_doesnt_raise_after_break():
    j = 0
    with switch(2) as (case, default, break_):
        if case(1):
            pass
        if case(2):
            j = 2
        if case(3):
            j = 42
            break_()
        if case(2):
            j = 3
        if default():
            pass

    assert(j == 42)

def test_unexpected_nameerror():
    with switch(52) as (case, default, break_):
        if case(1):
            pass
        if case(2):
            j = 2
        if case(2):
            j = 3
    
    with pytest.raises(NameError):
        x = (j == 0)
from enum import Enum

from mehr.exceptions import \
    CaseAfterDefaultException, \
    SameCaseException, \
    DoubleDefaultException, \
    NoDefaultException, \
    BreakNotification


class SwitchMode(Enum):
    STEPPING = 0
    ACTIVE = 1
    STOPPED = 2
    DEFAULTED = 3


class SwitchStatement:
    def __init__(self, target):
        self._target = target
        self._mode = SwitchMode.STEPPING

    def __enter__(self):
        return lambda x: self._case(x), \
               lambda: self._default(), \
               lambda: self._break()

    def __exit__(self, type_, value, traceback):
        if value is None or isinstance(value, BreakNotification):
            return True
        else:
            return False

    def _case(self, x):
        if self._mode == SwitchMode.DEFAULTED:
            raise CaseAfterDefaultException()
        elif self._mode == SwitchMode.ACTIVE:
            return True
        elif self._target == x:
            self._mode = SwitchMode.ACTIVE
            return True
        else:
            return False

    def _default(self):
        if self._mode == SwitchMode.DEFAULTED:
            raise DoubleDefaultException()

        result = self._mode == SwitchMode.ACTIVE
        self._mode = SwitchMode.DEFAULTED
        return result

    def _break(self):
        raise BreakNotification


class SafeSwitchStatement(SwitchStatement):
    def __init__(self, value):
        super().__init__(value)
        self._tracker = []

    def _case(self, x):
        result = super()._case(x)

        if x in self._tracker:
            raise SameCaseException(x)

        self._tracker.append(x)
        return result

    def _break(self):
        self._mode = SwitchMode.STOPPED

    def __exit__(self, type_, value, traceback):
        if type_ is None and self._mode != SwitchMode.DEFAULTED:
            raise NoDefaultException()
        elif self._mode == SwitchMode.DEFAULTED:
            return True
        else:
            return False


def switch(x):
    """ Enters a context and returns three callables: `case`, `default` and `break`.
    """
    return SwitchStatement(x)


def safe_switch(x):
    return SafeSwitchStatement(x)

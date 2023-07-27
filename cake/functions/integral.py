from __future__ import annotations
from typing import Any
from cake import Function, to_radians, Real

from math import trunc, ceil, floor


class Truncate(Function):
    ''' Truncate function, see :py:obj:`math.trunc`

    .. code-block:: py

        >>> t = Truncate(Variable('x'))
        >>> t.evaluate(x=1.55)
        Real(1.0)
        >>> t.evaluate(x=3)
        Real(3.0)
        >>> t.evaluate(x=Variable('y'))
        Truncate(y)
    '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        try:
            return Real(trunc(v))
        except Exception:
            return Truncate(v)


class Ceil(Function):
    ''' Ceil function, see :py:obj:`math.ceil`

    .. code-block:: py

        >>> c = Ceil(Variable('x'))
        >>> c.evaluate(x=1.2)
        Real(2.0)
        >>> c.evaluate(x=1.532)
        Real(2.0)
        >>> c.evaluate(x=Variable('y'))
        Ceil(y)
    '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        try:
            return Real(ceil(v))
        except Exception:
            return Ceil(v)


class Floor(Function):
    ''' Floor function, see :py:obj:`math.floor`
    '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        try:
            return Real(floor(v))
        except Exception:
            return Floor(v)


class Round(Function):
    ''' Round function, see :py:obj:`math.round`
    '''
    def __init__(self, parameter: Any, coefficient: Any = 1, power: Any = 1, n_places: int = 2) -> None:
        super().__init__(parameter, coefficient, power)
        self.n_places = n_places

    def __repr__(self) -> str:
        return f'Round(parameter={repr(self.parameter)}, coefficient={repr(self.coefficient)}, power={repr(self.power)}, n_places={repr(self.n_places)})'

    def __str__(self) -> str:
        s = super().__str__()[:-1]
        return s + f', {self.n_places})'

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        
        try:
            return Real(round(v, self.n_places))
        except Exception:
            return Round(v)

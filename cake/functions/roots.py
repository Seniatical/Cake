from __future__ import annotations
from typing import Any
from cake import Real, Function, to_radians, Expression, Divide

from functools import reduce
from operator import mul


def _prime_factors(factorable: Any) -> list:
    val = getattr(factorable, 'value', factorable)
    if not isinstance(val, (int, float)):
        raise TypeError('Cannot generate prime factors for type %s' % factorable.__class__.__name__)

    i = 2
    factors = []

    while i ** 2 <= val:
        if val % i:
            i += 1
        else:
            val //= i
            factors.append(i)

    if val > 1:
        factors.append(val)
    return factors


class Root(Function):
    base: Real

    def __init__(self, base: Any, parameter: Any, coefficient: Any = 1, power: Any = 1) -> None:
        self.base = base
        super().__init__(parameter, coefficient, power)

    def copy(self) -> Function:
        f = self.__class__(self.base, self.parameter, self.coefficient, self.power)
        
        f.auto_to_radians = self.auto_to_radians
        f.auto_preprocess = self.auto_preprocess
        f.preprocessor = self.preprocessor
        f.auto_postprocess = self.auto_postprocess
        f.postprocessor = self.postprocessor
        f.auto_prehandle = self.auto_prehandle
        f.prehandler = self.prehandler

        return f 
    
    def __str__(self) -> str:
        x = super().__str__()[:-1]
        x += f', base={self.base})'
        return x
        
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        return v ** self.base


class Sqrt(Root):
    def __init__(self, parameter: Any, coefficient: Any = 1, power: Any = 1) -> None:
        super().__init__(Real(0.5), parameter, coefficient, power)

    def __str__(self) -> str:
        return Function.__str__(self)

    copy = Function.copy

    def _reduce_if_possible(self, v):
        bases = _prime_factors(v)

        # a perfect square
        if len(bases) == 2:
            # sqrt ^ 2 (4) -> 2 ** 2 -> 4
            return ((v ** self.base) ** self.power) * self.coefficient
        # Unfactorable crap, return whole value just to be safe.
        if len(bases) == 1:
            return Sqrt(v, coefficient=self.coefficient, power=self.power)

        min_val = min(bases)
        bases.remove(min_val)

        if len(bases) == 2 and bases[0] == bases[1]:
            co = bases[0]
        else:
            co = int(reduce(mul, bases) ** 0.5)

        return Sqrt(min_val, coefficient=co * self.coefficient, power=self.power)

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        if isinstance(v, (Real, float)):
            top, bottom = map(self._reduce_if_possible, v.as_integer_ratio())
            return Expression(Divide(top, bottom))
        
        return self._reduce_if_possible(v)

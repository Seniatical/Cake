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
        try:
            bases = _prime_factors(v)
        except TypeError:
            return Sqrt(v)

        if not bases or len(bases) == 1:
            return Sqrt(v)

        groups = []
        ungrouped = []

        for base in bases:
            if base in ungrouped:
                groups.append(base)
                ungrouped.remove(base)
            else:
                ungrouped.append(base)

        if not ungrouped:
            ## Perfect square
            x = reduce(mul, groups)
            return x
        coefficient = reduce(mul, groups)
        param = reduce(mul, ungrouped)

        return Sqrt(param, coefficient)

    def true_value(self, /, to_radians: bool = False, use_prehandler: bool = False, use_postprocess: bool = False) -> Any:
        v = self._evaluate(to_rad=to_radians, prehandler=use_prehandler, o_v=True)
        v **= Real(0.5)
        value = self._try_solve_co({}) * (v ** self._try_solve_pow({}))

        if (use_postprocess or self.auto_postprocess) and self.postprocessor:
            return self.postprocessor(value)
        return value

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        if isinstance(v, (Real, float)):
            top, bottom = map(self._reduce_if_possible, v.as_integer_ratio())
            return Expression(Divide(top, bottom))
        
        return self._reduce_if_possible(v)

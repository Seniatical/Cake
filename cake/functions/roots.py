from __future__ import annotations
from typing import Any
from cake import Real, Function, to_radians, Expression, Divide, utils

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
    ''' Generic function for representing `n ** 1/x`,
    unlike :class:`Sqrt` the :class:`Root` function doesn't reduce values to its simplest form.

    .. code-block:: py

        >>> r = Root(3, Variable('x'))
        ## Same as (x ** (1/3))
        >>> r.evaluate(x=27)
        3.0
        >>> r = Root(Variable('y'), Variable('x'))
        ## Same as x ** y
        >>> r.evaluate(y=1/3, x=27)
        3.0

    Parameters
    ----------
    base: Any[Like[cake.BasicNode]]
        The base to raise the parameter to, 
        if base < 0 then the value raised is equal to ``(1/base)``
    parameter: Any[Like[cake.BasicNode]]
        Function parameter
    coefficient: Any[Like[cake.BasicNode]]
        Function coefficient
    power: Any[Like[cake.BasicNode]]
        Value the function is raised to
    '''
    base: Real

    def __init__(self, base: Any, parameter: Any, coefficient: Any = 1, power: Any = 1) -> None:
        self.base = base if base < 0 else 1/base
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
    ''' Built in sqrt function, which implements reducing into simplest form if possible.

    .. code-block:: py

        >>> f = Sqrt(Variable('x'))
        >>> f.evaluate(x=18)
        3*Sqrt(2)
        >>> f.evaluate(x=4)
        Real(2.0)
    '''
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
            return Real(x)
        coefficient = reduce(mul, groups)
        param = reduce(mul, ungrouped)

        return Sqrt(param, coefficient)

    def true_value(self, /, to_radians: bool = False, use_prehandler: bool = False, use_postprocess: bool = False, **kwds) -> Any:
        ''' Reduces the value of the function to its true value if possible

        .. code-block:: py

            >>> Sqrt(2).true_value()
            Real(1.4142135623730951)
            >>> Sqrt(2, coefficient=Variable('x')).true_value(x=2)
            Real(2.8284271247461903)

        Inherits all parameters from :meth:`Function.evaluate`
        '''
        v = self._evaluate(to_rad=to_radians, prehandler=use_prehandler, o_v=True, **kwds)
        v **= Real(0.5)
        value = self._try_solve_co(kwds) * (v ** self._try_solve_pow(kwds))

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

'''
Functions in the cake library are used to imitate the default Sin, Cos and Tan mathmatical functions,
except they are able to operate using core components in the cake library such as ``Variables``.

>>> from cake import Sin, Variable, Expression, Add
>>> Sin(Variable('x'))
Sin(x)
>>> Sin(Expression(Add('x', 3)))
Sin(x + 3)
>>> S = Sin(Variable('x'))
>>> Expr = Expression(Add('x', 3))
>>> Expr += S
>>> Expr
x + 3 + Sin(x)
>>> Expr.solve(x=90)
94
'''
from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod

import cake
from math import *


class Function(cake.IFunction, ABC):
    _err: Any = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(parameter={repr(self.parameter)}, coefficient={repr(self.coefficient)}, power={repr(self.power)})'

    def __str__(self) -> str:
        if self.coefficient != 1:
            coefficient = str(self.coefficient)
        else:
            coefficient = ''

        if self.power != 1:
            power = f'**{self.power}'
        else:
            power = ''

        return f'{coefficient}{self.__class__.__name__}{power}({self.parameter})'

    @abstractmethod
    def _handler(self, v, **opts) -> Any:
        raise NotImplemented

    def _try_solve_co(self, kwds) -> Any:
        try:
            if hasattr(self.coefficient, 'solve'):
                return self.coefficient.solve(**kwds)
            elif hasattr(self.coefficient, 'evaluate'):
                return self.coefficient.evaluate(**kwds)
        except Exception:
            return self.coefficient
        return self.coefficient

    def _try_solve_pow(self, kwds) -> Any:
        try:
            if hasattr(self.power, 'solve'):
                return self.power.solve(**kwds)
            elif hasattr(self.power, 'evaluate'):
                return self.power.evaluate(**kwds)
        except Exception:
            return self.power
        return self.power

    def _evaluate(self,
                  to_rad: bool = False,
                  prehandler: bool = False,
                  **kwds) -> Any:
        if isinstance(self.parameter, cake.Expression):
            e = self.parameter.solve(**kwds)
            if not hasattr(e, 'value'):
                return self.__class__(e)
            return self._handler(e, rad=to_rad)
        elif isinstance(self.parameter, cake.BasicVariable):
            return self._handler(self.parameter.solve(**kwds), rad=to_rad)

        value = getattr(self.parameter, 'value', self.parameter)
        return self._handler(value, rad=to_rad, prehandle=prehandler)

    def evaluate(self, /, to_radians: bool = False, 
                          use_preprocess: bool = False, 
                          use_postprocess: bool = False, 
                          use_prehandler: bool = False, 
                          **kwds) -> Any:
        try:
            if (use_preprocess or self.auto_preprocess) and self.preprocessor:
                kwds = self.preprocessor(kwds)

            r = self._evaluate(to_radians, use_prehandler, **kwds)
            value = self._try_solve_co(kwds) * (r ** self._try_solve_pow(kwds))

            if (use_postprocess or self.auto_postprocess) and self.postprocessor:
                return self.postprocessor(value)
            return value
        except Exception as e:
            self._err = e
            return self


class Truncate(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(trunc(v))


class Ceil(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(ceil(v))


class Floor(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(floor(v))


class Sqrt(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(sqrt(v))


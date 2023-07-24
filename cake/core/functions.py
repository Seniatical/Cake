'''
Functions in the cake library are used to imitate mathmatical functions such as Sin, Cos and Tan,
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
from cake.basic import OtherType
from cake.core.numbers import NumInstance
from math import *


''' Meths Implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__, __neg__
__pow__, __rpow__, __ipow__

__eq__, __ne__
__lt__, __le__, __gt__, __ge__
'''
class Function(cake.IFunction, ABC):
    ''' Represents a basic function in the cake library,
    this base function can be used to define your own functions in an elegant manner.

    .. code-block:: py

        from cake import *

        class MyFunc(Function):
            def _handler(self, value, **options) -> Any:
                return value * 3

        f = MyFunc(Variable('x'))
        print(f.evaluate(x=3))
        # 9

    Parameters
    ----------
    parameter: Any[Like[cake.BasicNode]]:
        Parameter of the function, can be any value which is like a ``BasicNode``.
    coefficient: Any[Like[cake.BasicNode]]
        Coefficient of the function, can be any value which is like a ``BasicNode``.
    power: Any[Like[cake.BasicNode]]
        The value the function may be raised to, can be any value which is like a ``BasicNode``.

        .. code-block:: py

            >>> s = Sin(Variable('x'), power=2)
            # s == sin^2(x)
    '''
    _err: Any = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(parameter={repr(self.parameter)}, coefficient={repr(self.coefficient)}, power={repr(self.power)})'

    def __str__(self) -> str:
        if self.coefficient != 1:
            coefficient = f'{str(self.coefficient)}*'
        else:
            coefficient = ''

        if self.power != 1:
            power = f'**{self.power}'
        else:
            power = ''

        return f'{coefficient}{self.__class__.__name__}{power}({self.parameter})'

    @abstractmethod
    def _handler(self, value, **options) -> Any:
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
                  o_v: bool = False,
                  **kwds) -> Any:
        if hasattr(self.parameter, 'solve'):
            value = self.parameter.solve(**kwds)
        elif hasattr(self.parameter, 'evaluate'):
            value = self.parameter.evaluate(**kwds)
        else:
            value = self.parameter
        value = getattr(value, 'value', value)

        ## Only the solved value wanted.
        if o_v:
            return value

        return self._handler(value, rad=to_rad, prehandle=prehandler)

    def evaluate(self, /, to_radians: bool = False, 
                          use_preprocess: bool = False, 
                          use_postprocess: bool = False, 
                          use_prehandler: bool = False, 
                          **kwds) -> Any:
        ''' Evaluates the function, returning a result.

        Parameters
        ----------
        to_radians: :class:`bool`
            Whether to convert value given to radians,
            useful for trig applications.
        use_preprocess: :class:`bool`
            Whether to use given pre processor, if any.
        use_postprocess: :class:`bool`
            Whether to use given post processor, if any.
        use_prehandler: :class:`bool`
            Whether to use given pre handler, if any.
        **kwds: Any[Like[cake.BasicNode]]
            Any values for variables to use.
        '''
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

    ''' Comparitive Methods '''
    def __eq__(self, other: OtherType) -> Any:
        if not isinstance(other, Function):
            return False
        if other.name != self.name:
            return False
        elif other.parameter != self.parameter:
            return False
        return True

    def __ne__(self, other: OtherType) -> Any:
        ## Genius
        return not (self == other)

    def __lt__(self, other: OtherType) -> Any:
        return cake.Comparity(self.copy(), other, cake.ComparitySymbol.LESS_THAN)

    def __le__(self, other: OtherType) -> Any:
        return cake.Comparity(self.copy(), other, cake.ComparitySymbol.LESS_OR_EQUAL_TO)

    def __gt__(self, other: OtherType) -> Any:
        return cake.Comparity(self.copy(), other, cake.ComparitySymbol.GREATER_THAN)

    def __ge__(self, other: OtherType) -> Any:
        return cake.Comparity(self.copy(), other, cake.ComparitySymbol.GREATER_OR_EQUAL_TO)

    ''' Numerical Methods '''

    def __add__(self, other: OtherType) -> Any:
        if other == self:
            c = self.copy()
            c.coefficient += 1
            return c
        return cake.Expression(cake.Add(self.copy(), other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> Any:
        return self.__add__(-other)

    def __rsub__(self, other: OtherType) -> Any:
        f = self.copy()
        f.coefficient *= -1

        return f.__add__(other)

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> Any:
        if other == 1:
            return self.copy()

        if self == other:
            s = self.copy()
            s.coefficient *= other.coefficient
            s.power += other.power
            return s
        elif isinstance(other, (cake.BasicVariable, NumInstance)):
            s = self.copy()
            s.coefficient *= other
            return s
        return cake.Expression(cake.Multiply(self.copy(), other))

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__
    
    def __neg__(self) -> Function:
        s = self.copy()
        s.coefficient = s.coefficient * -1
        return s

    def __pow__(self, other: OtherType) -> Any:
        s = self.copy()
        s.power *= other
        return s

    def __ipow__(self, other: OtherType) -> Any:
        return cake.Expression(cake.Power(other, self.copy()))

    __ipow__ = __pow__

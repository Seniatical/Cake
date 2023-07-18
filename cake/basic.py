## Basic representations for datatypes,
## These are mainly used for typehinting within in the module to prevent circular import messes
## Actual methods for these classes are found in core/numbers.py

from __future__ import annotations
from ._abc import BasicNode, BasicExpression
from abc import abstractmethod
import numbers

from typing import Any, List, TypeVar, Generic, Union


U = TypeVar('U')
F = TypeVar('F')
N = TypeVar('N', complex, float, int, str)


class Number(BasicNode, numbers.Number):
    ''' Represents a basic number '''
    value: Any

    def __init__(self, __value: N, /) -> None:
        self.__value = __value
        
        super().__init__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def check_before_set(self, new: Any) -> None:
        if hasattr(self, '_type'):
            assert isinstance(new, self._type), 'Invalid value set'
        self.__value = new


class Unknown(Generic[U], BasicNode):
    ''' Represents an unknown value, 
        this can be used inplace of any integer throughout the cake library.
        
        ..note::
            Where a specific type is required,
            having a default value is preferable

        ..rubric:: Solving for when 'a' is known

        ..code-block:: py

            >>> a = Unknown('a')
            >>> expr = (a + 5) / 2
            >>> expr.solve() == expr
            True
            >>> expr.solve(a=9)
            Real(7.0)

        ..rubric:: Solving for 'a' when result is known

        ..code-block:: py
        
            >>> expr
            Expression((a + 5) / 2)
            >>> equation = expr.to_equation(right=10)
            # So we now have an equation where (a + 5) / 2 = 10
            >>> equation *= 2
            # Equivalent to multiplying both sides by 2
            # a + 5 = 20
            >>> equation -= 5
            # a = 15
            >>> equation.result(as_unknown=True)
            Unknown('a', default_value=15)
    '''
    representation: str
    coefficient: Any
    power: Any

    def __init__(self, repr: str, coefficient: Any = 1, power: Any = 1) -> None:
        self.__repr = repr

        self.coefficient = coefficient
        self.power = power

    def __str__(self) -> str:
        return f'{self.coefficient if self.coefficient != 1 else ""}{self.representation}{f"**{self.power}" if self.power != 1 else ""}'

    def __repr__(self) -> str:
        return f'Unknown(\'{self.representation}\', coefficient={self.coefficient}, power={self.power})'

    @property
    def representation(self) -> str:
        return self.__repr

    @representation.setter
    def set_repr(self, new: str) -> None:
        self.__repr = str(new)

    @classmethod
    def many(cls, *symbols) -> List[Unknown]:
        ''' Returns a list of unknowns from the input given

        .. code-block:: py

            >>> Unknown.many('x', 'y')
            [Unknown('x'), Unknown('y')]
            >>> Unknown.many(('x', 5), ('y', 1, 2), 'z')
            [Unknown('x', coefficient=5), Unknown('y', coefficient=1, power=2), Unknown('z')]
        '''
        return [cls(i) if isinstance(i, str) else cls(*i) for i in symbols]


class Function(Generic[F], BasicNode):
    ''' Base class for creating functions,
    behaves similarly to an unknown in the sense the value of the function is not calcuated until called.
    This feature allows it to intake unknowns as values.
    '''
    cofficient: Any
    power: Any
    parameter: Any

    def __init__(self, parameter: Any, coefficient: Any = 1, power: Any = 1) -> None:
        self.parameter = parameter
        self.cofficient = coefficient
        self.power = power

    @abstractmethod
    def evaluate(self, **kwds) -> Any:
        ''' Evaluates the function returning either an updated version of the parameter or a value.

        >>> F = Function(Expression(Add(3, 'x')))
        >>> F
        Function(3 + x)
        >>> F.evaluate(x=3)
        Function(3 + 3)         ## Result is returned here
        >>> F.evaluate()
        Function(3 + x)         ## Function is returned as x is still unknown
        '''

OtherType = Union[Number, Unknown, BasicExpression, numbers.Number]


class Complex(Number):
    ''' Represents a complex number '''
    value: complex

    def __init__(self, real: N, imag: N = 0, /) -> None:
        self._Number__value = complex(real, imag)


class Real(Complex):
    ''' Represents a real/float '''
    value: float

    def __init__(self, value: N, /) -> None:
        self._Number__value = float(value)

    def to_rational(self) -> Rational:
        return Rational(self.value)


class Rational(Real):
    ''' Represents a rational number '''
    value: float
    numerator: Number
    denominator: Number

    def __init__(self, value_or_numerator, /, denominator = None) -> None:
        if not denominator:
            value_or_numerator = float(value_or_numerator)

            self._Number__value = value_or_numerator
            self.numerator, self.denominator = value_or_numerator
        else:
            self._Number__value = value_or_numerator / denominator
            self.numerator = value_or_numerator
            self.denominator = denominator


class Integral(Rational):
    ''' Represents a integral number '''
    value: int

    def __init__(self, value: int) -> None:
        self._Number__value = int(value)

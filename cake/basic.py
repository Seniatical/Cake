## Basic representations for datatypes,
## These are mainly used for typehinting within in the module to prevent circular import messes
## Actual methods for these classes are found in core/numbers.py

from __future__ import annotations
from ._abc import BasicNode, BasicExpression
from abc import abstractmethod
import numbers

from typing import Any, Callable, List, TypeVar, Generic, Union
import cake


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


class Variable(Generic[U], BasicNode):
    ''' Represents an Variable value, 
        this can be used inplace of any integer throughout the cake library.
        
        ..note::
            Where a specific type is required,
            having a default value is preferable

        ..rubric:: Solving for when 'a' is known

        ..code-block:: py

            >>> a = Variable('a')
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
            Variable('a', default_value=15)
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
        return f'Variable(\'{self.representation}\', coefficient={self.coefficient}, power={self.power})'

    @property
    def representation(self) -> str:
        return self.__repr

    @representation.setter
    def set_repr(self, new: str) -> None:
        self.__repr = str(new)

    @classmethod
    def many(cls, *symbols) -> List[Variable]:
        ''' Returns a list of Variables from the input given

        .. code-block:: py

            >>> Variable.many('x', 'y')
            [Variable('x'), Variable('y')]
            >>> Variable.many(('x', 5), ('y', 1, 2), 'z')
            [Variable('x', coefficient=5), Variable('y', coefficient=1, power=2), Variable('z')]
        '''
        return [cls(i) if isinstance(i, str) else cls(*i) for i in symbols]


class Function(Generic[F], BasicNode):
    ''' Base class for creating functions,
    behaves similarly to an Variable in the sense the value of the function is not calcuated until called.
    This feature allows it to intake Variables as values.
    '''

    coefficient: Any
    ''' Functions coefficient '''
    power: Any
    ''' Power function is raised to '''
    parameter: Any
    ''' Internal parameter of function '''

    auto_to_radians: bool
    ''' Convert value to radians before passing through function '''

    auto_preprocess: bool
    ''' Whether to automatically preprocess value '''
    preprocessor: Callable[[dict], dict]
    ''' preprocessor function, the value passed is the dictionary of given values,
    must return a new mapping of values to use instead.
    '''

    auto_postprocess: bool
    ''' Whether to automatically post process value '''
    postprocessor: Callable[[Any], Any]
    ''' postprocessor function '''

    auto_prehandle: bool
    ''' Whether to automatically pre-handle a value, 
        this is right before the value is passed through the handler
        
        .. warning:: 
            this is after the value is converted to radians! '''

    prehandler: Callable[[Any], Any]
    ''' prehandler function '''

    def __init__(self, parameter: Any, coefficient: Any = 1, power: Any = 1) -> None:
        self.parameter = parameter if not isinstance(parameter, cake.Operation) else cake.Expression(parameter)
        self.coefficient = coefficient if not isinstance(coefficient, cake.Operation) else cake.Expression(coefficient)
        self.power = power if not isinstance(power, cake.Operation) else cake.Expression(power)

        self.auto_to_radians = False

        self.auto_preprocess = False
        self.preprocessor = None

        self.auto_postprocess = False
        self.postprocessor = None

        self.auto_prehandle = False
        self.prehandler = None

    def copy(self) -> Function:
        ''' Returns a shallow copy of the function '''

        f = self.__class__(self.parameter, self.coefficient, self.power)
        f.auto_to_radians = self.auto_to_radians
        f.auto_preprocess = self.auto_preprocess
        f.preprocessor = self.preprocessor
        f.auto_postprocess = self.auto_postprocess
        f.postprocessor = self.postprocessor
        f.auto_prehandle = self.auto_prehandle
        f.prehandler = self.prehandler

        return f 

    @abstractmethod
    def evaluate(self, /, to_radians: bool = False, 
                          use_preprocess: bool = False,
                          use_postprocess: bool = False,
                          use_prehandler: bool = False,
                          **kwds) -> Any:
        ''' Evaluates the function returning either an updated version of the parameter or a value.

        >>> F = Function(Expression(Add(3, 'x')))
        >>> F
        Function(3 + x)
        >>> F.evaluate(x=3)
        Function(3 + 3)         ## Result is returned here
        >>> F.evaluate()
        Function(3 + x)         ## Function is returned as x is still Variable
        '''

    @property
    def name(self) -> str:
        return self.__class__.__name__

OtherType = Union[Number, Variable, BasicExpression, numbers.Number, Function]


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

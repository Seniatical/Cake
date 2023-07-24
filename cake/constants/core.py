from __future__ import annotations
from typing import Any, Union

from cake import Expression, Variable, VariableGroup, Number
from abc import ABC, abstractproperty, abstractmethod, abstractclassmethod

from cake.core.variables import OtherType, ResultType


class Constant(Variable, ABC):
    def __new__(cls, coefficient: Any = 1, power: Any = 1) -> Union[Number, Constant]:
        self = super().__new__(cls, cls.__class__.__name__)

        return self

    @abstractmethod
    def solve(self, *_, **kwds) -> Any:
        ''' Solves the current value of the constant, 
            args parameter is provided to mimick :meth:`Variable.solve` '''
        raise NotImplemented

    @abstractclassmethod
    def _to_type(cls, coefficient: Any = 1, power: Any = 1) -> Constant:
        raise NotImplemented

    @abstractproperty
    def c_value(self) -> Any:
        ''' Returns default value of the constant '''
        raise NotImplemented

    def copy(self) -> Constant:
        return self.__class__(coefficient=self.coefficient, power=self.power)

    def __add__(self, other: OtherType) -> ResultType:
        v = super().__add__(other)
        if isinstance(v, Expression):
            return v
        return self.__class__(v.coefficient, v.power)

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> ResultType:
        return self.__add__(-other)

    def __rsub__(self, other: OtherType) -> ResultType:
        s = -(self.copy())
        return s.__add__(other)
    
    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> ResultType:
        v = super().__mul__(other)
        if isinstance(v, (Expression, VariableGroup)):
            return v
        return self.__class__(v.coefficient, v.power)

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

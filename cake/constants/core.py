from __future__ import annotations
from typing import Any, Union

from cake import Expression, Variable, VariableGroup, Number, utils
from abc import ABC, abstractproperty, abstractclassmethod

from cake.core.variables import OtherType, ResultType


class Constant(Variable, ABC):
    ''' Generic base class for defining constants,
    behaves similar to :class:`Variable`.

    .. code-block:: py

        class MyConstant(Constant):
            @classmethod
            def _to_type(cls, coefficient: Any = 1, power: Any = 1) -> MyConstant:
                return cls(coefficient, power)
            
            @property
            def c_value(self) -> Any:
                return 5.5  ## Value of the constant

        ## Lets use our constant
        mc = MyConstant()
        x = Variable(x)
        expr = x + mc(2)
        print(expr)
        ### x + 2MyConstant
        print(expr.solve(x=3))
        ### 14

    Parameters
    ----------
    coefficient: Any[Like[cake.BasicNode]]
        Coefficient of constant
    power: Any[Like[cake.BasicNode]]
        Power the constant is raised to
    '''

    def __new__(cls, coefficient: Any = 1, power: Any = 1) -> Union[Number, Constant]:
        self = super().__new__(cls, cls.__class__.__name__)

        return self

    def solve(self, *_, **kwds) -> Any:
        v = self.c_value ** utils.solve_if_possible(self.power, **kwds)
        return utils.solve_if_possible(self.coefficient, **kwds) * v

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

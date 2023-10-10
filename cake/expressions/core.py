from __future__ import annotations
from typing import Any, Tuple
from abc import *
from cake._abc import Like, BasicExpression
from cake import Expression


class ExpressionBase(BasicExpression, Like[Expression], ABC):

    @abstractmethod
    def solve(self, **kwds) -> Any:
        ''' Solves the expression using given values, parameters may vary '''

    @abstractmethod
    def r_solve(self, **kwds) -> Any:
        ''' Solves expression when the result is known, parameters may vary '''

    @abstractclassmethod
    def generic(cls) -> ExpressionBase:
        ''' Returns generic version of expression '''

    @abstractclassmethod
    def from_expression(cls, expr: Expression) -> ExpressionBase:
        ''' Creates expression from :class:`Expression` '''


class PolynomialExpression(ExpressionBase):
    max_power: int
    ''' Highest power in the expression '''

    @abstractmethod
    def differentiate(self) -> Any:
        ''' Differentiates a polynomial expression '''

    @abstractmethod
    def integrate(self) -> Any:
        ''' Integrates a polynomial expression '''

    @abstractmethod
    def roots(self) -> Tuple[Any, ...]:
        ''' Returns roots of polynomial '''

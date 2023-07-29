## Linear expressions
from __future__ import annotations
from typing import Any, Tuple, TypeVar, Generic

from cake import Add, Expression, Variable, utils
import cake

from .core import PolynomialExpression

M = TypeVar('M')
C = TypeVar('C')


class LinearExpression(PolynomialExpression, Generic[M, C]):
    ''' Represents a basic linear expression, 
    this expression can also be expressed as ``y = mx + c``.

    Parameters
    ----------
    m: Any[Like[cake.BasicNode]]
        Gradient of expression
    c: Any[Like[cake.BasicNode]]
        Intercept of expression
    '''
    def __init__(self, m: M, c: C) -> None:
        self.m = m
        self.c = c

    def as_expression(self) -> Expression:
        ''' Returns a :class:`Expression` in the form of a :class:`LinearExpression` ''' 
        return Expression(Add(Variable('x', coefficient=self.m), self.c))

    def solve(self, x: Any, **kwds) -> Any:
        ''' Returns a value for when ``x`` is given,
        kwargs for other values may be passed as well but ``x`` is always overwritten.

        .. code-block:: py

            >>> y = LinearExpression(Real(0.5), 10)
            >>> y
            0.5*x + 10
            >>> y.solve(x=5)
            12.5
        '''
        kwds.update(x=x)
        return self.as_expression().solve(**kwds)

    def r_solve(self, y: Any, **kwds) -> Any:
        ''' Returns a value for when ``y`` is given,
        kwargs for other values may be passed as well but ``y`` is always overwritten

        .. code-block:: py

            >>> y = LinearExpression(2, 10)
            >>> y
            2*x + 10
            >>> y.r_solve(y=10)
            0
            >>> y.r_solve(y=3)
            -3.5
        '''
        kwds.update(y=y)
        r = getattr(y, 'copy', lambda: y)()
        r -= utils.solve_if_possible(self.c, **kwds)
        r /= utils.solve_if_possible(self.m, **kwds)

        return r

    def differentiate(self) -> M:
        return getattr(self.m, 'copy', lambda: self.m)()

    def integrate(self) -> 'cake.expressions.QuadraticExpression':
        return cake.expressions.QuadraticExpression(a=self.m / 2, b=self.c, c=0)

    def roots(self) -> Tuple[Any, ...]:
        return (self.r_solve(y=0),)

    ''' Properties and setters ''' 

    @property
    def gradient(self) -> M:
        ''' Returns the gradient of the expression '''
        return self.m
    
    @property
    def intercept(self) -> C:
        ''' Returns the intercept of the expression '''
        return self.m

    ''' Classmethods '''

    @classmethod
    def from_points(cls, point1: 'cake.geometry.Point2D', point2: 'cake.geometry.Point2D', /) -> LinearExpression:
        ''' Returns a linear expression from 2 given 2D points

        Parameters
        ----------
        point1, point2: :class:`geometry.Point2D`
            A 2D point to use
        '''
        gradient = (point1.y - point2.y) / (point1.x - point2.x)
        intercept = point2.y - (gradient * point1.x)

        return LinearExpression(gradient, intercept)

    @classmethod
    def generic(cls) -> LinearExpression:
        ''' Returns a generic linear expression '''
        return LinearExpression(Variable('m'), Variable('c'))

    @classmethod
    def through_origin(cls, m: Any) -> LinearExpression:
        ''' Returns a linear expression which passes through the origin

        Parameters
        ----------
        m: Any[Like[cake.BasicNode]]
            Gradient of the expression
        '''
        return LinearExpression(m, 0)

    @classmethod
    def from_expression(cls, expr: Expression) -> LinearExpression:
        ''' Creates a :class:`LinearExpression` from a :class:`Expression`.

        Parameters
        ----------
        expr: :class:`Expression`
            Expression to use, must be in the form ``Add(variable, Any, ...)``
            Any values after ``Any`` will expressed as ``Add(Any, ...)``

        Raises
        ------
        :py:obj:`TypeError`: 
            Invalid expression was given, either operation was not Add or it didn't match the valid pattern.
        '''
        if not isinstance(expr.exp, Add):
            raise TypeError('Invalid expression passed')
        
        try:
            gradient, *intercept = expr.exp.nodes
            gradient = gradient.coefficient

            if len(intercept) > 1:
                intercept = Expression(Add(*intercept))
            else:
                intercept = intercept[0]

        except (AttributeError, ValueError):
            raise TypeError('Invalid expression passed')
        return LinearExpression(gradient, intercept)

    ''' Internal '''

    def __str__(self) -> str:
        return f'{self.m}*x + {self.c}'

    def __repr__(self) -> str:
        return f'LinearExpression(m={repr(self.m)}, c={repr(self.m)})'

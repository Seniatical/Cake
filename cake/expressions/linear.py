## Linear expressions
from __future__ import annotations
from typing import Any

from cake._abc import BasicExpression, Like
from cake import Add, Expression, geometry, Variable, utils


class LinearExpression(BasicExpression, Like[Expression]):
    ''' Represents a basic linear expression, 
    this expression can also be expressed as **``y = mx + c``**.

    Parameters
    ----------
    m: Any[Like[cake.BasicNode]]
        Gradient of expression
    c: Any[Like[cake.BasicNode]]
        Intercept of expression
    '''
    def __init__(self, m: Any, c: Any) -> None:
        self.__m = m
        self.__c = c
        self.__exp = Expression(Add(Variable('x', coefficient=self.__m), self.__c))

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
        return self.__exp.solve(**kwds)

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
        r -= utils.solve_if_possible(self.__c, **kwds)
        r /= utils.solve_if_possible(self.__m, **kwds)

        return r

    @property
    def gradient(self) -> Any:
        ''' Returns the gradient of the expression '''
        return self.__m
    
    @property
    def intercept(self) -> Any:
        ''' Returns the intercept of the expression '''
        return self.__m

    @classmethod
    def from_points(cls, point1: geometry.Point2D, point2: geometry.Point2D, /) -> LinearExpression:
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

    def __str__(self) -> str:
        return f'{self.__m}*x + {self.__c}'

    def __repr__(self) -> str:
        return f'LinearExpression(m={repr(self.__m)}, c={repr(self.__m)})'

from __future__ import annotations
from typing import Any, Tuple

from .core import PolynomialExpression
from cake import Add, Sqrt, Expression, Variable
import cake


class QuadraticExpression(PolynomialExpression):
    ''' Represents a quadratic expression,
    can be expressed in the form ``ax**2 + bx + c``

    Parameters
    ----------
    a, b, c: Any[Like[cake.BasicNode]]
        Values for expression
    '''
    max_power: int = 2

    def __init__(self, a: Any, b: Any, c: Any) -> None:
        self.a = a
        self.b = b
        self.c = c

    def as_expression(self) -> Expression:
        return Expression(Add(
            (self.a * Variable('x', power=2)),
            (self.b * Variable('x')),
            self.c
        ))

    def solve(self, x: Any, **kwds) -> Any:
        ''' Solves expression for a given value of **x** '''
        kwds.update(x=x)
        return self.as_expression().solve(**kwds)

    def r_solve(self, y: Any, **kwds) -> Any:
        ''' Solves expression for a given value of **y** '''
        kwds.update(y=y)

        y = getattr(y, 'copy', lambda: y)()
        expr = QuadraticExpression(a=self.a, b=self.b, c=self.c - y)
        roots = expr.roots(**kwds)

        return roots

    def differentiate(self) -> 'cake.expressions.LinearExpression':
        ''' Differentiates a quadratic expression, returing a linear expression '''
        return cake.expressions.LinearExpression(
            m=self.a * 2,
            c=self.b
        )

    def integrate(self) -> Expression:
        ## TODO: cubic expressions
        ''' Integrates a quadratic expression, returning and expression '''
        return Expression(Add(
            (self.a / 3) * Variable('x', power=3),
            (self.b / 2) * Variable('x', power=2),
            self.c
        ))

    def discriminant(self) -> Any:
        return Sqrt((self.b ** 2) - (4 * self.a * self.c))

    def roots(self, *, evaluate: bool = True, **ev_kwds) -> Tuple[Any, Any]:
        ''' Returns roots of quadratic '''
        left: Expression = (-self.b + self.discriminant()) / (self.a * 2)
        right: Expression = (-self.b - self.discriminant()) / (self.a * 2)

        if evaluate:
            return left.solve(**ev_kwds), right.solve(**ev_kwds)
        return left, right

    def turning_point(self) -> 'cake.geometry.Point2D':
        ''' Works out the min/max point on the curve
        '''
        d = self.differentiate()
        h = d.r_solve(y=0)

        return cake.geometry.Point2D(h, self.solve(x=h))
        
    ''' Class methods '''

    @classmethod
    def generic(cls) -> QuadraticExpression:
        return QuadraticExpression(a=Variable('a'), b=Variable('b'), c=Variable('c'))

    @classmethod
    def from_expression(cls, expr: Expression) -> QuadraticExpression:
        ''' Converts a :class:`Expression` to a :class:`cake.expressions.QuadraticExpression`.

        .. note::
            Expression must be in the form ``Add(ax**2, bx, c, [...])``

        Parameters
        ----------
        expr: :class:`Expression`
            Expression to convert

        Raises
        ------
        :py:obj:`TypeError`: 
            Expression of incorrect form was passed
        '''
        try:
            assert isinstance(expr.exp, Add)
            a, b, *c = expr.exp.nodes

            if len(c) > 1:
                c = Expression(Add(*c))
            else:
                c = c[0]
            return QuadraticExpression(a.coefficient, b.coefficient, c)

        except (AssertionError, AttributeError, ValueError):
            raise TypeError('Invalid expression passed')

    ''' Properties '''

    @property
    def intercept(self) -> Any:
        ''' Returns when the graph intersects the y axis '''
        return self.c

    @property
    def has_max(self) -> bool:
        ''' Returns whether a graph has a maximum point '''
        return (x := self.a < 0) and not isinstance(x, cake.Comparity)

    @property
    def has_min(self) -> bool:
        ''' Returns whether a graph has a minimum point '''
        return (x := self.a > 0) and not isinstance(x, cake.Comparity)

    ''' Internals '''

    def __str__(self) -> str:
        return f'{self.a}*x**2 + {self.b}*x + {self.c}'
    
    def __repr__(self) -> str:
        return f'QuadraticExpression(a={repr(self.a)}, b={repr(self.b)}, c={repr(self.c)})'
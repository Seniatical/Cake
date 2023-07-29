from __future__ import annotations
from typing import Any, Tuple

from .core import PolynomialExpression
from cake import Add, Sqrt, Expression, Variable, utils
import cake


class QuadraticExpression(PolynomialExpression):
    ''' Represents a quadratic expression,
    can be expressed in the form ``ax**2 + bx + c``

    Parameters
    ----------
    a, b, c: Any[Like[cake.BasicNode]]
        Values for expression
    '''

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

    def roots(self, **kwds) -> Tuple[Any, Any]:
        ''' Returns roots of quadratic '''
        left: Expression = (-self.b + self.discriminant()) / (self.a * 2)
        right: Expression = (-self.b - self.discriminant()) / (self.a * 2)

        return left.solve(**kwds), right.solve(**kwds)
        
    ''' Class methods '''

    @classmethod
    def generic(cls) -> QuadraticExpression:
        return QuadraticExpression(a=Variable('a'), b=Variable('b'), c=Variable('c'))

    @classmethod
    def from_expression(cls, expr: Expression) -> QuadraticExpression:
        raise NotImplemented

    ''' Properties '''

    @property
    def intercept(self) -> Any:
        return self.c

    ''' Internals '''

    def __str__(self) -> str:
        return f'{self.a}*x**2 + {self.b}*x + {self.c}'
    
    def __repr__(self) -> str:
        return f'QuadraticExpression(a={repr(self.a)}, b={repr(self.b)}, c={repr(self.c)})'
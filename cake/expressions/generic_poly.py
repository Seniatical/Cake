'''
Generic polynomial class,
matches input args and may return an existing defined polynomial expression
'''
from __future__ import annotations
from typing import Any, Tuple, Union
import numbers

from cake import Variable, Expression, Add, Rational

from .core import PolynomialExpression


class Polynomial(PolynomialExpression):
    '''
    A generic polynomial expression which can be used to express custom expressions which may use higher powers,
    we recomend using :class:`cake.expressions.BinomialBase` which simulates very high power polynomial expressions,
    such as **(x + 5) ^ 25** or **(x / 2 + 3.5) ^ 15**.
    '''
    
    def __init__(self, *args)-> None:
        if not args:
            raise AttributeError('Cannot define an empty polynomial class')

        self._cleaned_args = {}
        self._chosen_factor = None

        for index, arg in enumerate(args):
            if not isinstance(arg, (Variable, numbers.Number)):
                raise TypeError('Argument {}, expected type either unknown or number, instead got {}'.format(index, arg.__class__.__name__))
            if isinstance(arg, Variable):
                if self._chosen_factor and self._chosen_factor != arg.representation:
                    raise TypeError('Invalid representation received, expected {} got {}'.format(self._chosen_factor, arg.representation))
                elif not self._chosen_factor:
                    self._chosen_factor = arg.representation
            
            # Verfied they are of correct type

            # Now get values from unhashable cake objects
            # check powers only
            power = getattr(arg, 'power', -1)
            power = getattr(power, 'value', power)

            if power in self._cleaned_args:
                self._cleaned_args[power] += arg
            else:
                self._cleaned_args[power] = arg

        self._expr = sum(self._cleaned_args.values())

    @property
    def max_power(self) -> int:
        return max(self._cleaned_args.keys())

    def solve(self, **kwds) -> Any:
        return self._expr.solve(**kwds)
    
    def r_solve(self, **kwds) -> Any:
        return super().r_solve(**kwds)
    
    @classmethod
    def from_expression(cls, expression: Expression) -> Polynomial:
        assert isinstance(expression.exp, Add), 'Invalid expression provided'
        return cls(*expression.exp.nodes)

    @classmethod
    def from_coefficients(cls, *coefficients, representation: str = 'x') -> Polynomial:
        ''''''
        powers = range(len(coefficients))
        coefficients = coefficients[::-1]

        args = []

        for index, power in enumerate(powers):
            if not power:
                args.append(coefficients[index])
            else:
                args.append(Variable(representation, coefficients[index], power))
        
        return cls(*args)
    

    def roots(self) -> Tuple[Any, ...]:
        return super().roots()
    

    def differentiate(self) -> Union[Polynomial, Any]:
        new_args = []
        for arg in self._cleaned_args.values():
            if not isinstance(arg, Variable):
                continue
            
            power = arg.power - 1
            coeff = arg.coefficient * arg.power
            new_args.append(Variable(self._chosen_factor, coeff, power))
        return Polynomial(*new_args)
    
    def integrate(self) -> Polynomial:
        new_args = []
        for arg in self._cleaned_args.values():
            if not isinstance(arg, Variable):
                new_args.append(Variable(self._chosen_factor, arg))
                continue

            power = arg.power + 1
            coeff = arg.coefficient / power
            new_args.append(Variable(self._chosen_factor, coeff, power))
        return Polynomial(*new_args)
    
    def generic(self, length: int) -> Polynomial:
        return super().generic()
    
    ''' Magic methods '''
    
    def __str__(self) -> str:
        return str(self._expr)

from __future__ import annotations
from copy import deepcopy

from cake._abc import BasicExpression, BasicNode
from cake.basic import OtherType
import cake
from typing import Any, List, Union


from .add import (
    Operation,
    Add,
)
from .divide import Divide

OtherType = Union[OtherType, Operation]


'''Meths implemented
__iter__, __next__,
__repr__, __str__,
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__
__neg__, __pos__
'''
class Expression(BasicExpression):
    ''' Represents an expression within the cake library,
    and expression is not equal to a value, 
    inorder to compute equations use an :class:`Equations` object.

    Which are simply 2 expressions with a comparity operator between them.

    .. tip::
        Expressions can be directly executed using :meth:`Expression.solve`.
        However, for specific methods for different mathmatical expressions such as Quadratics,
        use the dedicated methods.

        .. rubric:: Example

        .. code-block:: py

            from cake.expressions import QuadraticExpr

            expr = QuadraticExpr.random()
            print('Expression: ', expr)
            print('Solutions: ', expr.solve())

    .. hint::
        Iterating through expressions simply returns the node,
        not the operand between them.

    .. code-block:: py

        # Making your own expressions
        >>> expr = Expression(Add('x', 5))
        >>> expr
        x + 5
    '''
    def __init__(self, starting_op: Operation) -> None:
        self.exp = starting_op

    
    def __repr__(self) -> str:
        return f'Expression({str(self.exp)})'

    def __str__(self) -> str:
        return str(self.exp)
    
    ''' Numerical Methods '''
    def __add__(self, other: OtherType) -> Expression:
        return Expression(Add(self.exp, other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> Expression:
        return Expression(Add(self.exp, -other))

    def __rsub__(self, other: OtherType) -> Expression:
        return Expression(Add(other, -self.exp))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> Expression:
        if isinstance(self.exp, Divide):
            return Expression(Divide(self.exp.nodes[0] * other, self.exp.nodes[1]))
        
        nodes = []
        for node in self.exp.nodes:
            nodes.append(node * other)
        return Expression(Add(*nodes))

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

    ''' END NUMERIC METHODS '''

    ''' UNARY OPS '''

    ''' END UNARY OPS '''

    ''' OTHER METHODS '''

    def __next__(self) -> BasicNode:
        raise NotImplemented

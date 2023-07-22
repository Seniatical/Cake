from __future__ import annotations

from cake._abc import BasicExpression, BasicNode
from cake.basic import OtherType
import cake
from typing import Any, List, Union


from .add import (
    Operation,
    Add,
)
from .divide import Divide
from .multiply import Multiply, Power

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


    def _add(self, node: Add, **vals) -> Any:
        r = 0
        for child in node.nodes:
            try:
                if hasattr(child, 'solve'):
                    r += child.solve(**vals)
                elif hasattr(child, 'evaluate'):
                    r += child.evaluate(**vals)
                elif isinstance(child, Operation):
                    r += self._identify_helper(child, raise_not_impl=True)(child, **vals)
                else:
                    r += child
            except Exception as e:
                r += child

        return r


    def _identify_helper(self, node: Any = None, *, raise_not_impl: bool = False) -> Any:
        node = node or self.exp
        if isinstance(node, Add):
            return self._add

        if raise_not_impl:
            raise NotImplemented


    def solve(self, **values) -> Any:
        ''' Produces a solution to the expression using provided values.

        .. code-block:: py

            >>> expr = Expression(Add('x', 5))
            >>> expr
            x + 5
            >>> expr.solve(x=3)
            Integral(8)
        '''
        # Since expression is a tree, we use a recursive type approach.
        # Gather nodes for base expression, whilst traversing through these nodes solve and repeat
        ## So with Add(..., Power(3, x), ...)
        ## We add onto 0, if x is provided, compute and add if possible else expression
        ## if x is not provided we create an add expression for Add(..., Power(3, x))

        return self._identify_helper(raise_not_impl=True)(self.exp, **values)

    
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

            if isinstance(other, Divide):
                return Expression(Divide(self.exp.nodes[0] * other.nodes[0], self.exp.nodes[1] * other.nodes[0]))
            elif isinstance(other, Expression) and isinstance(other.exp, Divide):
                return Expression(Divide(self.exp.nodes[0] * other.exp.nodes[0], self.exp.nodes[1] * other.exp.nodes[0]))

            return Expression(Divide(self.exp.nodes[0] * other, self.exp.nodes[1]))
        
        if isinstance(self.exp, Add):
            nodes = []
            for node in self.exp.nodes:
                nodes.append(node * other)
            return Expression(Add(*nodes))

        return Expression(Multiply(self.exp, other))

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

    ''' END NUMERIC METHODS '''

    ''' UNARY OPS '''

    def __neg__(self) -> Expression:
        return self * -1

    ''' END UNARY OPS '''

    ''' OTHER METHODS '''

    def __next__(self) -> BasicNode:
        raise NotImplemented

from __future__ import annotations

from cake._abc import BasicExpression, BasicNode
from cake.basic import OtherType
from cake import (
    Comparity,
    ComparitySymbol
)
from typing import Any, Union


from .add import (
    Operation,
    Add,
)
from .divide import Divide, FloorDiv, Modulo
from .multiply import Multiply, Power
from .binaries import LeftShift, RightShift, And, Xor, Or

OtherType = Union[OtherType, Operation]


'''Meths implemented
__iter__, __next__,
__repr__, __str__,
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__,
__truediv__, __rtruediv__, __itruediv__
__floordiv__, __rfloordiv__, __ifloordiv__
__mod__, __rmod__, __imod__
__pow__, __rpow__, __ipow__,
__lshift__, __rlshift__, __ilshift__
__rshift__, __rrshift__, __irshift__
__and__, __rand__, __iand__
__xor__, __rxor__, __ixor__
__or__, __ror__, __ior__
__neg__, __pos__

__eq__, __ne__
__gt__, __ge__, __lt__, __le__
'''
class Expression(BasicExpression):
    ''' Represents an expression within the cake library,
    and expression is not equal to a value, 
    inorder to compute equations use an :class:`Equations` object.

    Which are simply 2 expressions with a comparity operator between them.

    .. hint::
        Iterating through expressions simply returns the node,
        not the operand between them.

    .. warning::
        Expressions when being compared using symbols such as ``>`` will not return a boolean value,
        instead :class:`Comparity` is returned.

    .. code-block:: py

        # Making your own expressions
        >>> expr = Expression(Add('x', 5))
        >>> expr
        x + 5

    Parameters
    ----------
    starting_op: :class:`cake.Operation`
        Operation the expression begins with.

        .. code-block:: py

            >>> op = Add('x', 5)
            >>> Expression(op)
            x + 5
    '''
    def __init__(self, starting_op: Operation) -> None:
        self.exp = starting_op

    def _try_get_child_value(self, child: Any, **kwds) -> Any:
        if hasattr(child, 'solve'):
            return child.solve(**kwds)
        elif hasattr(child, 'evaluate'):
            return child.evaluate(**kwds)
        elif isinstance(child, Operation):
            return self._identify_helper(child, raise_not_impl=True)(child, **kwds)
        return child

    ''' Operations '''
    
    def _add(self, node: Add, **kwds) -> Any:
        r = 0
        for child in node.nodes:
            try:
                r += self._try_get_child_value(child, **kwds)
            except Exception:
                r += child
        return r

    def _multiply(self, node: Multiply, **kwds) -> Any:
        r = self._try_get_child_value(node.nodes[0], **kwds)
        for child in node.nodes[1:]:
            try:
                r *= self._try_get_child_value(child, **kwds)
            except Exception:
                r *= child
        return r

    def _power(self, node: Power, **kwds) -> Any:
        base, power = node.nodes        ## Validates is true power op
        base = self._try_get_child_value(base, **kwds)
        power = self._try_get_child_value(power, **kwds)

        return base ** power

    def _truediv(self, node: Divide, **kwds) -> Any:
        numerator, denominator = node.nodes      ## Validates node is a division
        numerator = self._try_get_child_value(numerator, **kwds)
        denominator = self._try_get_child_value(denominator, **kwds)

        return numerator / denominator

    def _floordiv(self, node: Divide, **kwds) -> Any:
        numerator, denominator = node.nodes
        numerator = self._try_get_child_value(numerator, **kwds)
        denominator = self._try_get_child_value(denominator, **kwds)

        return numerator // denominator

    def _modulo(self, node: Divide, **kwds) -> Any:
        numerator, denominator = node.nodes
        numerator = self._try_get_child_value(numerator, **kwds)
        denominator = self._try_get_child_value(denominator, **kwds)

        return numerator % denominator

    def _leftshift(self, node: LeftShift, **kwds) -> Any:
        left, right = node.nodes
        left = self._try_get_child_value(left, **kwds)
        right = self._try_get_child_value(right, **kwds)

        return left << right

    def _rightshift(self, node: LeftShift, **kwds) -> Any:
        left, right = node.nodes
        left = self._try_get_child_value(left, **kwds)
        right = self._try_get_child_value(right, **kwds)

        return left >> right

    def _and(self, node: LeftShift, **kwds) -> Any:
        left, right = node.nodes
        left = self._try_get_child_value(left, **kwds)
        right = self._try_get_child_value(right, **kwds)

        return left & right

    def _xor(self, node: LeftShift, **kwds) -> Any:
        left, right = node.nodes
        left = self._try_get_child_value(left, **kwds)
        right = self._try_get_child_value(right, **kwds)

        return left ^ right

    def _or(self, node: LeftShift, **kwds) -> Any:
        left, right = node.nodes
        left = self._try_get_child_value(left, **kwds)
        right = self._try_get_child_value(right, **kwds)

        return left | right

    ''' End operations '''

    def _identify_helper(self, node: Any = None, *, raise_not_impl: bool = False) -> Any:
        node = node or self.exp
        if isinstance(node, Add):
            return self._add
        elif isinstance(node, Multiply):
            return self._multiply
        elif isinstance(node, Power):
            return self._power
        elif isinstance(node, Divide):
            return self._truediv
        elif isinstance(node, FloorDiv):
            return self._floordiv
        elif isinstance(node, Modulo):
            return self._modulo
        elif isinstance(node, LeftShift):
            return self._leftshift
        elif isinstance(node, RightShift):
            return self._rightshift
        elif isinstance(node, And):
            return self._and
        elif isinstance(node, Xor):
            return self._xor
        elif isinstance(node, Or):
            return self._or
        elif isinstance(node, Operation):
            if hasattr(node, 'run'):
                return node.run

        if raise_not_impl:
            raise NotImplemented
        return None

    def solve(self, **values) -> Any:
        ''' Produces a solution to the expression using provided values.
        Any variables in the expression must be passed as a **kwarg**!

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

        r = self._identify_helper(raise_not_impl=True)(self.exp, **values)
        if isinstance(r, Operation):
            return Expression(r)
        return r
    
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
        if (x := other == 1) and not isinstance(x, Comparity):
            return Expression(self.exp) # Reduces messy expressions

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

    def __truediv__(self, other: OtherType) -> Expression:
        return Expression(Divide(self.exp, other))

    def __rtruediv__(self, other: OtherType) -> Expression:
        return Expression(Divide(other, self.exp))

    __itruediv__ = __truediv__

    def __floordiv__(self, other: OtherType) -> Expression:
        return Expression(FloorDiv(self.exp, other))

    def __rfloordiv__(self, other: OtherType) -> Expression:
        return Expression(FloorDiv(other, self.exp))

    __ifloordiv__ = __floordiv__

    def __mod__(self, other: OtherType) -> Expression:
        return Expression(Modulo(self.exp, other))

    def __rmod__(self, other: OtherType) -> Expression:
        return Expression(Modulo(other, self.exp))

    __imod__ = __mod__

    def __pow__(self, other: OtherType) -> Expression:
        if other == 1:
            return Expression(self.exp)     ## Reduces messy expressions
        return Expression(Power(self.exp, other))

    def __rpow__(self, other: OtherType) -> Expression:
        return Expression(Power(other, self.exp))

    __ipow__ = __pow__

    def __lshift__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(self.exp, other))

    def __rlshift__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(other, self.exp))

    __ilshift__ = __lshift__

    def __rshift__(self, other: OtherType) -> Expression:
        return Expression(RightShift(self.exp, other))

    def __rrshift__(self, other: OtherType) -> Expression:
        return Expression(RightShift(other, self.exp))

    __irshift__ = __rshift__

    def __and__(self, other: OtherType) -> Expression:
        return Expression(And(self.exp, other))

    def __rand__(self, other: OtherType) -> Expression:
        return Expression(And(other, self.exp))

    __iand__ = __and__

    def __xor__(self, other: OtherType) -> Expression:
        return Expression(Xor(self.exp, other))

    def __rxor__(self, other: OtherType) -> Expression:
        return Expression(Xor(other, self.exp))

    __ixor__ = __xor__

    def __or__(self, other: OtherType) -> Expression:
        return Expression(Or(self.exp, other))

    def __ror__(self, other: OtherType) -> Expression:
        return Expression(Or(other, self.exp))
    
    __ior__ = __or__

    ''' END NUMERIC METHODS '''

    ''' UNARY OPS '''

    def __neg__(self) -> Expression:
        return self * -1

    def __pos__(self) -> Expression:
        return Expression(self.exp)

    ''' END UNARY OPS '''

    ''' OTHER METHODS '''

    def __eq__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.EQUAL_TO)

    def __ne__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.NOT_EQUAL_TO)

    def __lt__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.LESS_THAN)

    def __le__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.LESS_OR_EQUAL_TO)

    def __gt__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.GREATER_THAN)

    def __ge__(self, other: OtherType) -> Comparity:
        return Comparity(self, other, ComparitySymbol.GREATER_OR_EQUAL_TO)

    def __next__(self) -> BasicNode:
        raise NotImplemented

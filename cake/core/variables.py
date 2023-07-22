from __future__ import annotations
from abc import ABC, abstractmethod

from cake import (
    IVariable,
    Expression,
    BasicExpression,
    BasicNode,
    Comparity, ComparitySymbol,
    Add, Divide, Multiply, Power, FloorDiv,
    Modulo
)
from cake.basic import OtherType
from .numbers import Number, Integral
from typing import Any, Dict, Generic, TypeVar, Union

from .expressions.binaries import *

U = TypeVar('U', bound=IVariable)
ResultType = Union[IVariable, BasicExpression, U]


''' Meths implemented
__pos__
__floordiv__, __rfloordiv__, __ifloordiv__
__mod__, __rmod__, __imod__,
__lshift__, __rlshift__, __ilshift__
__rshift__, __rrshift__, __irshift__
__and__, __rand__, __iand__
__xor__, __rxor__, __ixor__
__or__, __ror__, __ior__
__eq__, __ne__, __lt__, __le__, __gt__, __ge__

Unimplementable Methods
- __divmod__ : 
    needs to return a tuple, cannot really do
- __int__, __complex__, __float__, __bool__ : 
    can't convert with no existing value
- __round__, __trunc__, __floor__, __ceil__ :
    same reason as above
- __invert__ : 
    Dont see the point in it
'''
class BasicVariable(ABC):
    ''' Holds methods which will be the same for every type of Variable'''

    @abstractmethod
    def copy(self) -> U:
        raise NotImplemented

    def __pos__(self) -> U:
        return self.copy()

    def __abs__(self) -> U:
        if hasattr(self, 'coefficient'):
            if self.coefficient > 0:
                return self.copy()
            copy = self.copy()
            copy.coefficient = -copy.coefficient
            return copy
        return self

    def __floordiv__(self, other) -> Expression:
        return Expression(FloorDiv(self.copy(), other))

    def __rfloordiv__(self, other) -> Expression:
        return Expression(FloorDiv(other, self.copy()))

    __ifloordiv__ = __floordiv__

    def __mod__(self, other) -> Expression:
        return Expression(Modulo(self.copy(), other))

    def __rmod__(self, other) -> Expression:
        return Expression(Modulo(other, self.copy()))

    __imod__ = __mod__

    ''' Misc '''

    def __lshift__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(self.copy(), other))

    def __rlshift__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(other, self.copy()))

    __ilshift__ = __lshift__

    def __rshift__(self, other: OtherType) -> Expression:
        return Expression(RightShift(self.copy(), other))

    def __rrshift__(self, other: OtherType) -> Expression:
        return Expression(RightShift(other, self.copy()))

    __irshift__ = __rshift__

    def __and__(self, other: OtherType) -> Expression:
        return Expression(And(self.copy(), other))

    def __rand__(self, other: OtherType) -> Expression:
        return Expression(And(other, self.copy()))

    __iand__ = __and__

    def __xor__(self, other: OtherType) -> Expression:
        return Expression(Xor(self.copy(), other))

    def __rxor__(self, other: OtherType) -> Expression:
        return Expression(Xor(other, self.copy()))

    __ixor__ = __xor__

    def __or__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(self.copy(), other))

    def __ror__(self, other: OtherType) -> Expression:
        return Expression(LeftShift(other, self.copy()))

    __ior__ = __or__

    ''' Comparitive methods '''

    def __eq__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.EQUAL_TO)

    def __ne__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.NOT_EQUAL_TO)

    def __lt__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.LESS_THAN)

    def __le__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.LESS_OR_EQUAL_TO)

    def __gt__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.GREATER_THAN)

    def __ge__(self, other: OtherType) -> Comparity:
        return Comparity(self.copy(), other, ComparitySymbol.GREATER_OR_EQUAL_TO)


''' Meths implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__, __call__
__truediv__, __rtruediv__, __itruediv__
__pow__, __rpow__, __ipow__
__neg__
'''
class Variable(IVariable, BasicVariable):
    ''' An object which represents an Variable number/value,
    this class be integrated with other components within the cake library.

    .. note::
        Using comparity operators such as `==` will not return a boolean value.

        .. code-block:: py

            >>> x = Variable('x')
            >>> x > 9
            Comparity(left=x, right=9, symbol='>')
            >>> (x > 9).fits(x=10)
            True
            >>> (x > 9).fits(x=5)
            False
            >>> (5 < x < 10).fits(x=10)
            False
            >>> (5 < x < 10).fits(x=7)
            True

    .. tip::
        Using Variables in trig

        .. code-block:: py

            from cake import Sin, Variable
            from cake.shapes import Triangle

            t = Triangle.rand_right_angle()
            t['A'] = 30
            
            # Assume t is modelled at AB=12, BC=5 and AC=13
            # Angle BAC = 30 and the opposite side is BC
            # Lets work out ACB
            left = Sin(30) / 5
            right = Sin(Variable('x')) / 12
            eq = left.to_equation(right=right)

            eq.multiply(12)
            # (12 * Sin(30)) / 5 = Sin(x)
            x = ArcSin(eq.left)
            print(x.compute())
    '''
    def __new__(cls, repr: str, coefficient: Any = 1, power: Any = 1) -> Union[Number, Variable]:
        if power == 0:
            return Integral(1) * coefficient
        elif coefficient == 0:
            return Integral(0)

        return super(Variable, cls).__new__(cls)

    def copy(self) -> Variable:
        return Variable(self.representation, self.coefficient, self.power)

    @staticmethod
    def is_similar(x: Variable, y: Variable) -> bool:
        ''' Returns whether 2 Variables can be merged into a single one,

        so ``Variable.is_similar(3x, 4x)`` is True but ``Variable.is_similar(4y, 3x)`` is False.
        '''
        if not (x.representation == y.representation):
            return False
        elif not (x.power == y.power):
            return False
        return True

    def solve(self, value: OtherType = None, **_v) -> ResultType:
        v = value
        if v is None:
            v = _v.pop(self.representation, None)

        if v is None:
            raise ValueError('No value provided')

        return (self.coefficient * v) ** self.power

    def __add__(self, other: OtherType) -> ResultType:
        if isinstance(other, Variable) and self.is_similar(self, other):
            co = self.coefficient + other.coefficient
            return Variable(self.representation, co, self.power)

        elif isinstance(other, BasicExpression):
            return Expression(Add(self.copy(), other.exp))

        return Expression(Add(self.copy(), other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> ResultType:
        if isinstance(other, Variable) and self.is_similar(self, other):
            co = self.coefficient - other.coefficient
            return Variable(self.representation, co, self.power)

        return Expression(Add(self.copy(), -other))

    def __rsub__(self, other: OtherType) -> ResultType:
        if isinstance(other, Variable) and self.is_similar(self, other):
            co = other.coefficient - self.coefficient
            return Variable(self.representation, co, self.power)

        return Expression(Add(-self, other))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return other * self
        elif isinstance(other, Variable):
            if self.representation == other.representation:
                co = self.coefficient * other.coefficient
                po = self.power + other.power
                return Variable(self.representation, co, po)
            
            co_ef = self.coefficient * other.coefficient
            return VariableGroup(co_ef, self, other)
        else:
            return Variable(self.representation, self.coefficient * other, self.power)

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__
    __neg__ = lambda self: self * -1

    def __truediv__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return Expression(Divide(self.copy(), other))
        
        elif isinstance(other, Variable) and other.representation == self.representation:
            coefficient = self.coefficient / other.coefficient
            power = self.power - other.power

            return Variable(self.representation, coefficient, power)
        elif isinstance(other, VariableGroup):
            return other.__rtruediv__(self)
        
        return Expression(Divide(self.copy(), other))

    def __rtruediv__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return Expression(Divide(other, self.copy()))

        elif isinstance(other, Variable) and other.representation == self.representation:
            coefficient = other.coefficient - self.coefficient
            power = other.power - self.power

            return Variable(self.representation, coefficient, power)
        elif isinstance(other, VariableGroup):
            return other.__truediv__(self)
        
        return Expression(Divide(other, self.copy()))

    __itruediv__ = __truediv__

    def __pow__(self, other: OtherType, *modulo) -> ResultType:
        power = self.power * other
        coefficient = self.coefficient ** other
        r = Variable(self.representation, coefficient, power)

        if modulo:
            return Expression(Modulo(r, modulo[0]))
        return r

    def __rpow__(self, other: OtherType, *modulo) -> ResultType:
        if modulo:
            return RaisedVariable(base=other, power=self.copy()).__mod__(modulo[0])
        return RaisedVariable(base=other, power=self.copy())

    __ipow__ = __pow__

# Variables as a power

''' Meths implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__, __call__
__truediv__, __rtruediv__, __itruediv__
__pow__, __rpow__, __ipow__
__neg__
'''
class RaisedVariable(Generic[U], BasicNode, BasicVariable):
    ''' A raised Variable is where a literal or Variable value is raised to another Variable value,
    we use this class as it maintains logic within the library.
    
    .. note::
        Most operations which are ran on this object will more then likely return expressions!

    .. code-block:: py

        >>> I = Integral(3)
        >>> X = Variable('x')
        >>> R = I ** X
        RaisedVariable(3 ** x)
        >>> R * 2
        Expression(Multiply(3 ** x, 2))
    '''
    def __init__(self, base: Any, power: Any = 1) -> None:
        self.base = base
        self.power = power

    def copy(self) -> RaisedVariable:
        return RaisedVariable(self.base, self.power)


    def solve(self, **kwds) -> ResultType:
        if hasattr(self.base, 'solve'):
            base = self.base.solve(**kwds)
        else:
            base = self.base

        if hasattr(self.power, 'solve'):
            power = self.power.solve(**kwds)
        else:
            power = self.power

        return base ** power


    def __repr__(self) -> str:
        return f'RaisedVariable(base={self.base}, power={self.power})'

    def __str__(self) -> str:
        return f'{self.base} ** {self.power}'

    def __add__(self, other: OtherType) -> Expression:
        return Expression(Add(self, other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> Expression:
        return Expression(Add(self.copy(), -other))

    def __rsub__(self, other: OtherType) -> Expression:
        return Expression(Add(-self, other))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> Expression:
        return Expression(Multiply(self.copy(), other))
    
    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

    def __neg__(self) -> RaisedVariable:
        return RaisedVariable(-self.base, self.power)

    def __truediv__(self, other: OtherType) -> Expression:
        return Expression(Divide(self.copy(), other))

    def __rtruediv__(self, other: OtherType) -> Expression:
        return Expression(Divide(other, self.copy()))

    __itruediv__ = __truediv__

    def __pow__(self, other: OtherType, *modulo) -> RaisedVariable:
        if modulo:
            return Expression(Modulo(RaisedVariable(self.base, self.power * other), modulo[0]))
        return RaisedVariable(self.base, self.power * other)

    def __rpow__(self, other: OtherType, *modulo) -> ResultType:
        if hasattr(other, 'power'):
            other = getattr(other, 'copy', lambda: other)()
            other.power = other.power * self
            return other
        
        if modulo:
            return Expression(Modulo(Power(other, self), modulo[0]))
        return Expression(Power(other, self))

    __ipow__ = __pow__

# Variable groups

''' Meths Implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__, __neg__
__truediv__, __rtruediv__, __itruediv__
__pow__, __rpow__, __ipow__
'''
class VariableGroup(Generic[U], BasicNode, BasicVariable):
    ''' An Variable group is used where multiple Variables make up a single Variable value,
    So, ``5x`` is an Variable whereas ``5x * y`` would be an VariableGroup as theres 2 values.

    .. warning::
        Reading coffecients from :attr:`VariableGroup.groups` will always be one,
        instead use :attr:`VariableGroup.coefficient`.

    .. note::
        Groups generally shouldn't need to be made manually,
        they can easily be made by manipulating standard Variables.

    .. code-block:: py

        >>> x, y = Variable.gen_many('x', 'y')
        >>> g = x * y
        >>> g
        VariableGroup(xy)
        >>> g.groups
        [Variable('x'), Variable('y')]
        >>> g * y
        VariableGroup(xy**2)
        # Groups == [Variable('x'), Variable('y', power=2, ...)]
        >>> g + y
        Expression(xy + y)
    '''
    def __new__(cls, coefficient: Any, *Variables) -> None:
        if coefficient == 0 or len(Variables) == 0:
            return Integral(0)
        elif len(Variables) == 1:
            return Variables[0]
        return super(VariableGroup, cls).__new__(cls)

    def __init__(self, coefficient: Any, *Variables) -> None:
        self.coefficient = coefficient
        self.power = None
        self.groups = []

        for group in Variables:
            if isinstance(group, Variable):
                group = Variable(group.representation, 1, group.power)
                self.groups.append(group)
            else:
                self.coefficient *= group

    def __repr__(self) -> str:
        return f'VariableGroup({self.__str__()})'

    def __str__(self) -> str:
        return (str(self.coefficient) if self.coefficient != 1 else '') + ''.join(map(lambda x: f'{x.representation}{f"**{x.power}" if x.power != 1 else ""}', self.groups))


    @staticmethod
    def is_similar(x: VariableGroup, y: VariableGroup):
        if len(x.groups) != len(y.groups):
            return False
        
        x = {f'{i.representation}**{i.power}' for i in x.groups}
        y = {f'{i.representation}**{i.power}' for i in x.groups}

        if (x != y):
            return False
        return True

    @property
    def representation(self) -> str:
        return ''.join(i.representation for i in self.groups)

    def as_mapping(self) -> dict:
        d = dict()
        for u in self.groups:
            if u.representation not in d:
                d[u.representation] = u
            else:
                d[u.representation] *= u
        return d

    def copy(self) -> VariableGroup:
        return VariableGroup(self.coefficient, *self.groups)

    def solve(self, **values) -> ResultType:
        result = 0
        for node in self.groups:
            if node.representation in values:
                result += values[node.representation] ** node.power
        return Number.convert(result * self.coefficient)

    ''' Wrapped methods for handling these groups '''

    def __add__(self, other: OtherType) -> ResultType:
        if isinstance(other, VariableGroup):
            if not self.is_similar(self, other):
                return Expression(Add(self.copy(), other.copy()))
            return VariableGroup(self.coefficient + other.coefficient, *self.groups)
        return Expression(Add(self.copy(), other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> ResultType:
        if isinstance(other, VariableGroup):
            if not self.is_similar(self, other):
                return Expression(Add(self.copy(), -other))
            return VariableGroup(self.coefficient - other.coefficient, *self.groups)
        return Expression(Add(self.copy(), -other))

    def __rsub__(self, other: OtherType) -> ResultType:
        if isinstance(other, VariableGroup):
            if not self.is_similar(self, other):
                return Expression(Add(-self, other.copy()))
            return VariableGroup(-self.coefficient + other.coefficient, *self.groups)
        return Expression(Add(-self, other))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> None:
        if isinstance(other, VariableGroup):
            coefficient = self.coefficient * other.coefficient
            mapping = self.as_mapping()
            for co in other.groups:
                co.coefficient = 1

                if rep := co.representation in mapping:
                    mapping[rep] = mapping[rep] * co
                else:
                    mapping[rep] = co
            nodes = mapping.values()

            return VariableGroup(coefficient, *nodes)

        elif isinstance(other, Variable):
            coefficient = self.coefficient * other.coefficient
            mapping = self.as_mapping()

            for node in mapping:
                if other.representation == node:
                    mapping[node] = mapping[node] * other
                    break
            else:
                mapping[other.representation] = other
            return VariableGroup(coefficient, *mapping.values())

        coefficient = self.coefficient * other
        return VariableGroup(coefficient, *self.groups)

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

    def __neg__(self) -> VariableGroup:
        return VariableGroup(self.coefficient * -1, *self.groups)

    def __truediv__(self, other: OtherType) -> ResultType:
        if isinstance(other, VariableGroup):
            coefficient = self.coefficient / other.coefficient
            mapping = self.as_mapping()

            remaining = []
            for group in other.groups:
                if group.representation in mapping:
                    g1 = mapping[group.representation]
                    g2 = g1 / group
                    mapping[group.representation] = g2
                else:
                    remaining.append(group)
            
            top = VariableGroup(coefficient, *mapping.values())
            if not remaining:
                return top

            r = remaining.pop(0)
            while remaining:
                r *= remaining.pop(0)

            return Expression(Divide(top, r))
        
        elif isinstance(other, Variable):
            mapping = self.as_mapping()

            if other.representation in mapping:
                g = mapping[other.representation] / other
                mapping[other.representation] = g

                coefficient = self.coefficient / other.coefficient
                return VariableGroup(coefficient, *mapping.values())
            
            return Expression(Divide(self.copy(), other))

        elif isinstance(other, BasicExpression):
            return Expression(Divide(self.copy(), other))

        return VariableGroup(self.coefficient / other, *self.groups)

    def __rtruediv__(self, other: OtherType) -> ResultType:
        if isinstance(other, VariableGroup):
            coefficient = other.coefficient / self.coefficient
            mapping = other.as_mapping()

            remaining = []
            for group in self.groups:
                if group.representation in mapping:
                    g1 = mapping[group.representation]
                    g2 = g1 / group
                    mapping[group.representation] = g2
                else:
                    remaining.append(group)
            
            top = VariableGroup(coefficient, *mapping.values())
            if not remaining:
                return top

            r = remaining.pop(0)
            while remaining:
                r *= remaining.pop(0)

            return Expression(Divide(top, r))
        
        elif isinstance(other, Variable):
            mapping = self.as_mapping()

            if other.representation in mapping:
                g = other / mapping[other.representation]
                
                if isinstance(g, Number):
                    mapping.pop(other.representation)
                bottom = VariableGroup(self.coefficient, *mapping.values())

                return Expression(Divide(g, bottom))
            
            return Expression(Divide(other, self.copy()))

        elif isinstance(other, BasicExpression):
            return Expression(Divide(other, self.copy()))

        return VariableGroup(other / self.coefficient, *self.groups)

    __itruediv__ = __truediv__

    def __pow__(self, other: OtherType, *modulo) -> VariableGroup:
        mapping = self.as_mapping()
        coefficient = self.coefficient ** other

        result = VariableGroup(coefficient, *map(lambda x: x ** other, mapping.values()))
        if modulo:
            return result % modulo[0]
        return result

    def __rpow__(self, other: OtherType, *modulo) -> Expression:
        if modulo:
            return Expression(Modulo(Power(other, self.copy()), modulo[0]))
        return Expression(Power(other, self.copy()))

    __ipow__ = __pow__
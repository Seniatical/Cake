from __future__ import annotations
from copy import deepcopy

from cake import (
    IUnknown,
    Expression,
    BasicExpression,
    BasicNode,
    Add, Divide
)
from cake.basic import OtherType
from .numbers import NumInstance
from typing import Any, Generic, TypeVar, Union

U = TypeVar('U', bound=IUnknown)
ResultType = Union[IUnknown, BasicExpression, U]


''' Meths implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__
__div__, __rdiv__, __idiv__
__neg__
'''
class Unknown(IUnknown):
    ''' An object which represents an unknown number/value,
    this class be integrated with other components within the cake library.

    .. tip::
        Using unknowns in trig

        .. code-block:: py

            from cake import Sin, Unknown
            from cake.shapes import Triangle

            t = Triangle.rand_right_angle()
            t['A'] = 30
            
            # Assume t is modelled at AB=12, BC=5 and AC=13
            # Angle BAC = 30 and the opposite side is BC
            # Lets work out ACB
            left = Sin(30) / 5
            right = Sin(Unknown('x')) / 12
            eq = left.to_equation(right=right)

            eq.multiply(12)
            # (12 * Sin(30)) / 5 = Sin(x)
            x = ArcSin(eq.left)
            print(x.compute())
    '''

    @staticmethod
    def is_similar(x: Unknown, y: Unknown) -> bool:
        ''' Returns whether 2 unknowns can be merged into a single one,

        so ``Unknown.is_similar(3x, 4x)`` is True but ``Unknown.is_similar(4y, 3x)`` is False.
        '''
        if not (x.representation == y.representation):
            return False
        elif not (x.power == y.power):
            return False
        return True

    def __add__(self, other: OtherType) -> ResultType:
        if isinstance(other, Unknown) and self.is_similar(self, other):
            co = self.coefficient + other.coefficient
            return Unknown(self.representation, co, self.power)
        elif isinstance(other, BasicExpression):
            return Expression(Add(self, other.exp))

        return Expression(Add(self, other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> ResultType:
        if isinstance(other, Unknown) and self.is_similar(self, other):
            co = self.coefficient - other.coefficient
            return Unknown(self.representation, co, self.power)

        return Expression(Add(self, -other))

    def __rsub__(self, other: OtherType) -> ResultType:
        if isinstance(other, Unknown) and self.is_similar(self, other):
            co = other.coefficient - self.coefficient
            return Unknown(self.representation, co, self.power)

        return Expression(Add(-self, other))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return other * self
        elif isinstance(other, Unknown):
            if self.representation == other.representation:
                co = self.coefficient * other.coefficient
                po = self.power + other.power
                return Unknown(self.representation, co, po)
            
            co_ef = self.coefficient * other.coefficient
            return UnknownGroup(co_ef, self, other)
        else:
            return Unknown(self.representation, self.coefficient * other, self.power)

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__
    __neg__ = lambda self: self * -1

    def __div__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return Expression(Divide(deepcopy(self), other))
        elif isinstance(other, Unknown) and other.representation == self.representation:
            coefficient = self.coefficient / other.coefficient
            power = self.power - other.power

            return Unknown(self.representation, coefficient, power)
        elif isinstance(other, UnknownGroup):
            return Expression(Divide(deepcopy(self), other))
        
        return Unknown(self.representation, self.coefficient / other, self.power)

    def __rdiv__(self, other: OtherType) -> ResultType:
        if isinstance(other, BasicExpression):
            return Expression(Divide(other, deepcopy(self)))
        elif isinstance(other, Unknown) and other.representation == self.representation:
            coefficient = other.coefficient - self.coefficient
            power = other.power - self.power

            return Unknown(self.representation, coefficient, power)
        elif isinstance(other, UnknownGroup):
            return Expression(Divide(other, deepcopy(self)))
        
        return Unknown(self.representation, other / self.coefficient, self.power)

    __idiv__ = __div__

# Unknown groups

''' Meths Implemented
__add__, __radd__, __iadd__
__sub__, __rsub__, __isub__
__mul__, __rmul__, __imul__, __neg__

'''
class UnknownGroup(Generic[U], BasicNode):
    ''' An unknown group is used where multiple unknowns make up a single unknown value,
    So, ``5x`` is an Unknown whereas ``5x * y`` would be an UnknownGroup as theres 2 values.

    .. warning::
        Reading coffecients from :attr:`UnknownGroup.groups` will always be one,
        instead use :attr:`UnknownGroup.coefficient`.

    .. note::
        Groups generally shouldn't need to be made manually,
        they can easily be made by manipulating standard unknowns.

    .. code-block:: py

        >>> x, y = Unknown.gen_many('x', 'y')
        >>> g = x * y
        >>> g
        UnknownGroup(xy)
        >>> g.groups
        [Unknown('x'), Unknown('y')]
        >>> g * y
        UnknownGroup(xy**2)
        # Groups == [Unknown('x'), Unknown('y', power=2, ...)]
        >>> g + y
        Expression(xy + y)
    '''
    def __init__(self, coefficient: Any, *unknowns) -> None:
        self.coefficient = coefficient
        self.power = None
        self.groups = [deepcopy(u) for u in unknowns]

        for g in self.groups:
            g.coefficient = 1

    def __repr__(self) -> str:
        return f'UnknownGroup({self.__str__()})'

    def __str__(self) -> str:
        return str(self.coefficient) + ''.join(map(lambda x: f'{x.representation}{f"**{x.power}" if x.power != 1 else ""}', self.groups))


    @staticmethod
    def is_similar(x: UnknownGroup, y: UnknownGroup):
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

    ''' Wrapped methods for handling these groups '''

    def __add__(self, other: OtherType) -> ResultType:
        if isinstance(other, UnknownGroup):
            if not self.is_similar(self, other):
                return Expression(Add(self, other))
            return UnknownGroup(self.coefficient + other.coefficient, *self.groups)
        return Expression(Add(self, other))

    __radd__ = __add__
    __iadd__ = __add__

    def __sub__(self, other: OtherType) -> ResultType:
        if isinstance(other, UnknownGroup):
            if not self.is_similar(self, other):
                return Expression(Add(self, -other))
            return UnknownGroup(self.coefficient - other.coefficient, *self.groups)
        return Expression(Add(self, -other))

    def __rsub__(self, other: OtherType) -> ResultType:
        if isinstance(other, UnknownGroup):
            if not self.is_similar(self, other):
                return Expression(Add(-self, other))
            return UnknownGroup(-self.coefficient + other.coefficient, *self.groups)
        return Expression(Add(-self, other))

    __isub__ = __sub__

    def __mul__(self, other: OtherType) -> None:
        if isinstance(other, UnknownGroup):
            coefficient = self.coefficient * other.coefficient
            mapping = self.as_mapping()
            for co in other.groups:
                co.coefficient = 1

                if rep := co.representation in mapping:
                    mapping[rep] = mapping[rep] * co
                else:
                    mapping[rep] = co
            nodes = mapping.values()

            return UnknownGroup(coefficient, *nodes)

        elif isinstance(other, Unknown):
            coefficient = self.coefficient * other.coefficient

            res = None
            e = None
            for i, g in enumerate(self.groups):
                if g.representation == other.representation:
                    res = g * other
                    break
            else:
                e = other
    
            if res:
                nodes = [i for i in self.groups]
                for i, v in enumerate(nodes):
                    if i.representation == res.represenation:
                        nodes[i] = v
                    
                return UnknownGroup(coefficient, *nodes)
            groups = self.groups + [e]
            return UnknownGroup(coefficient, *groups)

        coefficient = self.coefficient * other
        return UnknownGroup(coefficient, *self.groups)

    __rmul__ = __mul__
    __imul__ = __mul__
    __call__ = __mul__

    def __neg__(self) -> UnknownGroup:
        return UnknownGroup(self.coefficient * -1, *self.groups)

    def __div__(self, other: OtherType) -> ResultType:
        if isinstance(other, UnknownGroup):
            coefficient = self.coefficient / other.coefficient
            mapping = self.as_mapping()

            for group in other.groups:
                if group.representation in mapping:
                    g1 = mapping[group.representation]
                    g2 = g1 / group
                    mapping[group.representation] = g2
                else:
                    mapping[group.representation] = group
            
            return UnknownGroup(coefficient, *mapping.values())
        
        elif isinstance(other, Unknown):
            ...

        elif isinstance(other, BasicExpression):
            return Expression(Divide(deepcopy(self), other))

        return UnknownGroup(self.coefficient / other, *self.groups)

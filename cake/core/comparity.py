from __future__ import annotations
from enum import Enum
from typing import TypeVar, Generic
import cake

L = TypeVar('L')
R = TypeVar('R')


def pairwise(supports_len) -> list:
    while len(supports_len) > 2:
        yield (supports_len[0], supports_len[1], supports_len[2])
        supports_len = supports_len[2:]


## Got to explain each symbol in docstring
class ComparitySymbol(str, Enum):
    ''' Represents the comparison being made between 2 objects.

    .. rubric:: EQUAL_TO

    * Represents the ``==`` operator

    .. rubric:: NOT_EQUAL_TO

    * Represents the ``!=`` operator

    .. rubric:: GREATER_THAN

    * Represents the ``>`` operator

    .. rubric:: GREATER_OR_EQUAL_TO

    * Represents the ``>=`` operator

    .. rubric:: LESS_THAN
    
    * Represents the ``<`` operator

    .. rubric:: LESS_OR_EQUAL_TO

    * Represents the ``<=`` operator
    '''

    EQUAL_TO: str               = '=='
    NOT_EQUAL_TO: str           = '!='
    GREATER_THAN: str           = '>'
    GREATER_OR_EQUAL_TO: str    = '>='
    LESS_THAN: str              = '<'
    LESS_OR_EQUAL_TO: str       = '<='

    def __repr__(self) -> str:
        return f'ComparitySymbol.{self._name_}'

    @staticmethod
    def _eq(l, r):
        return l == r
    
    @staticmethod
    def _neq(l, r):
        return l != r

    @staticmethod
    def _gt(l, r):
        return l > r

    @staticmethod
    def _ge(l, r):
        return l >= r

    @staticmethod
    def _lt(l, r):
        return l < r

    @staticmethod
    def _le(l, r):
        return l <= r


_mthds = {
    '==': ComparitySymbol._eq, '!=': ComparitySymbol._neq,
    '>': ComparitySymbol._gt, '>=': ComparitySymbol._ge, 
    '<': ComparitySymbol._lt, '<=': ComparitySymbol._le,
}


class Comparity(Generic[L, R]):
    ''' Generic class for representing a comparison between 2 values,
        Values can be chained.

        .. code-block:: py

            >>> (5 < x)
            Comparity(x > 5)
            >>> (5 < x) < y
            Comparity(y > x > 5)
            >>> ((x < 5) > y) < z
            Comparity(z > y < x < 5)
    '''
    def __init__(self, left: L, right: R, symbol: ComparitySymbol) -> None:
        self.left = left
        self.right = right
        self.symbol = ComparitySymbol(symbol)

    def __str__(self, *, repr_: bool = False) -> str:
        f = str if not repr_ else repr

        return f'{f(self.left)} {self.symbol.value} {f(self.right)}'

    def __repr__(self) -> str:
        return f'Comparity(left={repr(self.left)}, right={repr(self.right)}, symbol={repr(self.symbol)})'

    def _gather(self) -> list:
        r = []
        if isinstance(self.left, Comparity):
            r.extend(self.left._gather())
        else:
            r.extend((self.left, self.symbol))

        if isinstance(self.right, Comparity):
            r.extend(self.right._gather())
        else:
            r.append(self.right)

        return r

    def fits(self, **kwds) -> bool:
        ''' Checks whether given values fit inside of the comparitive expression,
        for chained expressions each pair is worked out, 
        any pairs returning Comparity are assumed False.

        .. note::
            Any variables must be passed as a **kwarg**!

        .. code-block:: py

            >>> c = x > 5
            >>> c
            Comparity(x > 5)
            >>> c.fits(x=6)
            True
            >>> c.fits(x=1)
            False
        '''
        nodes = self._gather()
        pairs = tuple(pairwise(nodes))
        results = []

        for pair in pairs:
            l, s, r = pair

            l = cake.utils.solve_if_possible(l, **kwds)
            r = cake.utils.solve_if_possible(r, **kwds)

            if isinstance(r := _mthds[s.value](l, r), bool):
                results.append(r)
            else:
                results.append(False)

        return all(results)

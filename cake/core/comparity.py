from __future__ import annotations
from enum import Enum
from typing import Any, TypeVar, Iterable, Generic


L = TypeVar('L')
R = TypeVar('R')


class ComparitySymbol(str, Enum):
    EQUAL_TO: str               = '=='
    NOT_EQUAL_TO: str           = '!='
    GREATER_THAN: str           = '>'
    GREATER_OR_EQUAL_TO: str    = '>='
    LESS_THAN: str              = '<'
    LESS_OR_EQUAL_TO: str       = '<='

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

    def _methds(self) -> dict:
        return {'==': self._eq, '!=': self._neq,
                '>': self._gt, '>=': self._ge, 
                '<': self._lt, '<=': self._le,
               }


class Comparity(Generic[L, R]):
    def __init__(self, left: L, right: R, symbol: ComparitySymbol) -> None:
        self.left = left
        self.right = right
        self.symbol = ComparitySymbol(symbol)

    def __str__(self) -> str:
        return f'{self.left} {self.symbol.value} {self.right}'

    def __repr__(self) -> str:
        return f'Comparity(left={self.left}, right={self.right}, symbol={self.symbol})'

    @staticmethod
    def _fill(l, v):
        if isinstance(v, dict):
            return l.solve(**v)
        elif isinstance(v, Iterable):
            return l.solve(*v)
        return l.solve(*(v,))

    def fits(self, left: Any = None, right: Any = None) -> bool:
        r1 = self.left
        if hasattr(self.left, 'solve') and left:
            r1 = self._fill(self.left, left)
            changed = True
        elif left:
            r1 = left
            changed = True

        r2 = self.right
        if hasattr(self.right, 'solve') and right:
            r2 = self._fill(self.right, right)
        elif right:
            r2 = right

        return self.symbol._methds()[self.symbol.value](r1, r2)

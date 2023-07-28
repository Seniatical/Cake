## Represents a coordinate in a nutshell
from __future__ import annotations
from typing import Any, Tuple, Union

from .core import GeometryO
import cake
from random import randint


class Point2D(GeometryO):
    ''' Represents a co-ordinate on a 2D plane, meaning it only has 2 values **x** and **y**.

    Parameters
    ----------
    x, y: Any[Like[:class:`cake.BasicNode`]]
        Value for co-ordinate
    '''
    def __init__(self, x: Any, y: Any) -> None:
        self.x = x
        self.y = y

    def length_to(self, other: Union[Point2D, Tuple[Any, Any]], *, evaluate: bool = True, **ev_kwds) -> Any:
        ''' Calculates the length between 2 points

        Parameters
        ----------
        other: Union[:class:`Point2D`, Tuple[Any[Like[:class:`cake.BasicNode`], ...]]]
            Point to calcuate distance to
        '''
        x1, y1 = self.as_tuple()
        x2, y2 = getattr(other, 'as_tuple', lambda: (other[0], other[1]))()

        r = cake.Sqrt(((x2 - x1) ** 2) + ((y1 - y2) ** 2))
        if evaluate:
            return r.evaluate(**ev_kwds)
        return r

    @classmethod
    def random(cls, *, start: int = -1000, end: int = 1000) -> Point2D:
        return Point2D(randint(start, end), randint(start, end))

    @classmethod
    def from_tuple(cls, tup: Tuple[Any, Any]) -> Point2D:
        ''' Generates a 2D point from a tuple

        Parameters
        ----------
        tup: Tuple[Any[Like[:class:`cake.BasicNode`]], Any[Like[:class:`cake.BasicNode`]]]
            Tuple to create point from
        '''
        return Point2D(*tup)

    def as_tuple(self) -> Tuple[Any, Any]:
        ''' Returns point as tuple '''
        return (self.x, self.y)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'Point2D(x={repr(self.x)}, y={repr(self.y)})'

## Represents a coordinate in a nutshell
from __future__ import annotations
from typing import Any, Tuple

from .core import GeometryO


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

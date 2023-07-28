## Represents a coordinate in a nutshell
from __future__ import annotations
from typing import Any, Tuple

from .core import GeometryO


class Point2D(GeometryO):
    def __init__(self, x: Any, y: Any) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, tup: Tuple[Any, Any]) -> Point2D:
        return Point2D(*tup)

    def as_tuple(self) -> Tuple[Any, Any]:
        ''' Returns point as tuple '''
        return (self.x, self.y)

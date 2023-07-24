from __future__ import annotations
from typing import Any
import math


def to_radians(x: Any) -> Any:
    return x * (math.pi / 180)


def to_degrees(x: Any) -> Any:
    return x / (math.pi / 180)


def solve_if_possible(x: Any, **kwds) -> Any:
    if hasattr(x, 'solve'):
        return x.solve(**kwds)
    elif hasattr(x, 'evaluate'):
        return x.evaluate(**kwds)
    return x

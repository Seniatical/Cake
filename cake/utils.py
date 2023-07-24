from __future__ import annotations
from typing import Any
import math


def to_radians(x: Any) -> Any:
    return x * (math.pi / 180)


def to_degrees(x: Any) -> Any:
    return x / (math.pi / 180)


def solve_if_possible(__x_v: Any, **kwds) -> Any:
    if hasattr(__x_v, 'solve'):
        return __x_v.solve(**kwds)
    elif hasattr(__x_v, 'evaluate'):
        return __x_v.evaluate(**kwds)
    return __x_v

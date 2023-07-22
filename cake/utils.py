from __future__ import annotations
from typing import Any
import math


def to_radians(x: Any) -> Any:
    return x * (math.pi / 180)


def to_degrees(x: Any) -> Any:
    return x / (math.pi / 180)

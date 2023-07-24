from __future__ import annotations
from typing import Any

from cake import utils, Real
from .core import Constant

from math import pi 


class Pi(Constant):
    def __init__(self, coefficient: Any = 1, power: Any = 1) -> None:
        super().__init__('Pi', coefficient, power)

    @classmethod
    def _to_type(cls, coefficient: Any = 1, power: Any = 1) -> Pi:
        return cls(coefficient, power)

    def solve(self, *_, **kwds) -> Any:
        v = self.c_value ** utils.solve_if_possible(self.power, **kwds)
        return utils.solve_if_possible(self.coefficient, **kwds) * v

    @property
    def c_value(self) -> Real:
        return Real(pi)

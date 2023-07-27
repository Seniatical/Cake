from __future__ import annotations
from typing import Any

from cake import Real
from .core import Constant

from math import pi 


class Pi(Constant):
    '''
    Represents the PI constant, value is equal to :py:obj:`math.pi`.
    '''

    def __init__(self, coefficient: Any = 1, power: Any = 1) -> None:
        super().__init__('Pi', coefficient, power)

    @classmethod
    def _to_type(cls, coefficient: Any = 1, power: Any = 1) -> Pi:
        return cls(coefficient, power)

    @property
    def c_value(self) -> Real:
        return Real(pi)

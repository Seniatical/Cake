from __future__ import annotations
from typing import Any
from cake import Real, Function, to_radians
from math import sqrt


class Sqrt(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return Real(sqrt(v))

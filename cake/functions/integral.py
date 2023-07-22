from __future__ import annotations
from typing import Any
from cake import Function, to_radians, Real

from math import trunc, ceil, floor


class Truncate(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return Real(trunc(v))


class Ceil(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return Real(ceil(v))


class Floor(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return Real(floor(v))

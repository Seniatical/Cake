from __future__ import annotations
from typing import Any

from cake.core.functions import Function
import cake
from math import *

class Sin(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(sin(v))


class Cos(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(cos(v))


class Tan(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(tan(v))


class ASin(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(asin(v))


class ACos(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(acos(v))


class ATan(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(atan(v))


class ATan2(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(atan2(v))


class SinH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(sinh(v))


class CosH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(cosh(v))


class TanH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(tanh(v))


class ASinH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(asinh(v))


class ACosH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(acosh(v))


class ATanH(Function):
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        return cake.Real(atanh(v))

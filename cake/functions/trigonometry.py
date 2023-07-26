from __future__ import annotations
from typing import Any

from cake.core.functions import Function
import cake
from math import *

class Sin(Function):
    ''' Sin function ''' 

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        
        try:
            return cake.Real(sin(v))
        except Exception:
            return Sin(v)

class Cos(Function):
    ''' Cos function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(cos(v))
        except Exception:
            return Cos(v)


class Tan(Function):
    ''' tan function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(tan(v))
        except Exception:
            return Tan(v)


class ASin(Function):
    ''' arc sin or inverse sin function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(asin(v))
        except Exception:
            return ASin(v)


class ACos(Function):
    ''' arc cos or inverse cos function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        try:
            return cake.Real(acos(v))
        except Exception:
            return ACos(v)


class ATan(Function):
    ''' arc tan or inverse tan function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(atan(v))
        except Exception:
            return ATan(v)


class ATan2(Function):
    ''' arc tan2 or inverse tan2 function '''

    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(atan2(v))
        except Exception:
            return ATan2(v)


class SinH(Function):
    ''' Hyperbolic sin function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)
        try:
            return cake.Real(sinh(v))
        except Exception:
            return SinH(v)


class CosH(Function):
    ''' Hyperbolic cos function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(cosh(v))
        except Exception:
            return CosH(v)


class TanH(Function):
    ''' Hyperbolic tan function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(tanh(v))
        except Exception:
            return TanH(v)


class ASinH(Function):
    ''' Arc hyperbolic sin or inverse hyperbolic sin function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(asinh(v))
        except Exception:
            return ASinH(v)


class ACosH(Function):
    ''' Arc hyperbolic cos or inverse hyperbolic cos function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(acosh(v))
        except Exception:
            return ACosH(v)


class ATanH(Function):
    ''' Arc hyperbolic tan or inverse hyperbolic tan function '''
    def _handler(self, v, **opts) -> Any:
        if opts.get('rad'):
            v = cake.to_radians(v)
        if opts.get('prehandle'):
            v = self.prehandler(v)

        try:
            return cake.Real(atanh(v))
        except Exception:
            return ATanH(v)

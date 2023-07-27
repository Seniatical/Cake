from __future__ import annotations
from typing import Any
import math
import cake


def to_radians(x: Any, *, use_constant: bool = False) -> Any:
    ''' Converts the desired input from degrees into radians

    Parameters
    ----------
    x: Any
        Value to convert to radians
    use_constant: :class:`bool`
        Whether to use :class:`Pi` instead of :py:obj:`math.pi`
    '''
    p = cake.Pi() if use_constant else cake.Real(math.pi)
    return x * (p / 180)


def to_degrees(x: Any, *, use_constant: bool = False) -> Any:
    ''' Converts the desired input from radians to degrees

    Parameters
    ----------
    x: Any
        Value to convert to radians
    use_constant: :class:`bool`
        Whether to use :class:`Pi` instead of :py:obj:`math.pi`
    '''
    p = cake.Pi() if use_constant else cake.Real(math.pi)
    return x / (p / 180)


def solve_if_possible(__x_v: Any, /, **kwds) -> Any:
    ''' Attempts to solve a given value if possible else returns original value.

    .. code-block:: py

        >>> f = Sqrt(Variable('x') + 3)
        >>> f
        Sqrt(x + 3)
        >>> utils.solve_if_possible(f, x=6)
        Real(3.0)
        >>> utils.solve_if_possible(Real(5), x=3)
        Real(5.0)
    '''
    if hasattr(__x_v, 'solve'):
        return __x_v.solve(**kwds)
    elif hasattr(__x_v, 'evaluate'):
        return __x_v.evaluate(**kwds)
    return __x_v

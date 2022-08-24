from typing import Dict
from .base import Polygon


class Triangle(Polygon):
    """Base object for defining triangles

    ..code-block::py
        >>> from cake.geometry import Triangle
        >>> t = Triangle(3, 3, 3)
        >>> t.is_equilateral()
        True

    Parameters
    ----------
    Shares same parameters as :class:`Polygon`
    """
    def __post_init__(self):
        if len(self.lengths) != 3:
            raise ValueError("Triangles must have 3 sides")
        if sum(self.angles.values()) > 180:
            raise TypeError("Angles in triangle must sum to 180")
        

    def is_right_angled(self) -> bool:
        """Check if triangle is a right angle triangle"""
        a, b, c = self.lengths.values()
        if (a ** 2 + b ** 2) ** 0.5 == c and \
            any(i for i in self.angles.values() if i == 90):
            return True
        return False

    def is_equilateral(self) -> bool:
        """Check if triangle is equilateral"""
        a, b, c = self.lengths.values()
        if a == b == c and \
            all(i == 60 for i in self.angles.values()):
            return True
        return False

    def is_isosceles(self) -> bool:
        """Check if triangle is isosceles"""
        if self.is_equilateral():
            return False

        a, b, c = self.lengths.values()
        A, B, C = self.angles.values()

        if (a == b) or (b == c) or (a == c):
            return True
        if (A == B) or (B == C) or (A == C):
            return True
        return False

    def is_scalene(self) -> bool:
        """ Checks if trangle is scalene """
        if not (self.is_equilateral() and self.is_isosceles()):
            return True
        return False


class RATriangle(Triangle):
    """Object for working with right angled triangles

    * **a** - Adjacent (Adj)
    * **b** - Opposite (Opp)
    * **c** - Hypotenuse (Hyp)

    ..code-block:: py
        >>> from cake.geometry import RATriangle
        >>> t = RATriangle(5, 12, 0)
        >>> t.calc_hypotenuse(update=True)
        13
        >>> t
        Polygon(a=5, b=12, c=13)
        >>> t = RATriangle(5, 0, 0, angles={"bca": 30})
    """
    def __init__(self, 
                 a: float, 
                 b: float, 
                 c: float,
                 *,
                 angles: Dict[str, float] = {}
                ) -> None:
        super().__init__(a, b, c, angles=angles)

        self.a = a
        self.b = b
        self.c = c

    def __post_init__(self):
        super().__post_init__()
        assert self.is_right_angled()

    def calc_hypotenuse(self, update: bool = False) -> float:
        if self.a and self.b:
            c = ((self.a ** 2) + (self.b ** 2)) ** 0.5
            if update:
                self.c = c
                self.lengths["c"] = c
            return c

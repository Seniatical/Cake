from math import cos, sin, tan, degrees
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
        13.0
        >>> t
        Polygon(a=5, b=12, c=13.0)
    """
    def __init__(self, 
                 a: float, 
                 b: float, 
                 c: float,
                 *,
                 angles: Dict[str, float] = {}
                ) -> None:

        angles.update(ABC=90)
        super().__init__(a, b, c, angles=angles)

        if len(self.angles) == 2:
            # Fill last angle in

            if angle := self.get_angle("BCA"):
                self.set_angle("CAB", (180 - 90 - degrees(angle)))
            else:
                self.set_angle("BCA", (180 - 90 - degrees(self.get_angle("CAB"))))

        self.a, self.b, self.c = a, b, c

    def __post_init__(self):
        super().__post_init__()
        assert self.is_right_angled()

    def calc_hypotenuse(self, *, update: bool = False) -> float:
        if self.a and self.b:
            # A ** 2 + B ** 2 = C ** 2
            c = ((self.a ** 2) + (self.b ** 2)) ** 0.5
        elif self.b and (angle := self.get_angle("BCA")):
            # sin C * B = C
            c = sin(angle) * self.b
        elif self.a and (angle := self.get_angle("CAB")):
            # A / cos A = C
            c = self.a / cos(angle)
        else:
            raise ValueError("Not enough values")
        if update:
            self.update_length("CA", c)
            self.c = c
        return c

    def calc_adjacent(self, *, update: bool = False) -> float:
        if self.c and self.b:
            a = ((self.c ** 2) - (self.b ** 2)) ** 0.5
        elif self.c and (angle := self.get_angle("ABC")):
            a = cos(angle) * self.c
        else:
            raise ValueError("Not enough values")
        if update:
            self.update_length("AB", a)
            self.a = a
        return a

    def calc_opposite(self, *, update: bool = False) -> float:
        if self.c and self.a:
            # sqrt(C ** 2 - A ** 2) = B
            b = ((self.c ** 2) - (self.a ** 2)) ** 0.5
        elif self.a and (angle := self.get_angle("CAB")):
            b = tan(angle) * self.a
        else:
            raise ValueError("Not enough values")
        if update:
            self.update_length("BC", b)
            self.b =b
        return b

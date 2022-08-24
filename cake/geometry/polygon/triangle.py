from math import cos, sin, tan, degrees
from typing import Dict, Tuple
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
    angle_maps = {
        "ABC": "CA",
        "BCA": "AB",
        "CAB": "BC"
    }
    length_maps = {v: k for k, v in angle_maps.items()}

    def __init__(self, 
                 a: float, 
                 b: float, 
                 c: float,
                 *,
                 angles: Dict[str, float] = {}
                ) -> None:
        self.a, self.b, self.c = a, b, c

        super().__init__(a, b, c, angles=angles)

    def __post_init__(self):
        if len(self.lengths) != 3:
            raise ValueError("Triangles must have 3 sides")
        if sum(self.angles.values()) > 180:
            raise TypeError("Angles in triangle must sum to 180")
        
    def calc_side_usine(self, pair: Tuple[str, str], angle: str, *, set: bool = False) -> Tuple[str, int]:
        """Calculate the length of a side using sine rule

        Parameters
        ----------
        pair: Tuple[:class:`str`, :class:`str`]
            A paired tuple with (SIDE, ANGLE),
            were side is one of the triangles length name and angle is its opposite angle.
        angle: :class:`str`
            Name of the angle which is opposite to the desired length
        set: :class:`bool`
            Whether to set value
        """
        length, _angle = pair
        length_value = self.get_length(length)
        _angle_value = self.get_angle(_angle)

        angle_value = self.get_angle(angle)
        side_name = self.get_length(self.angle_maps.get(self.get_angle(angle, name=True)), name=True)
        side_value = (length_value / sin(_angle_value)) * sin(angle_value)

        if set:
            self.update_length(side_name, side_value)
        return side_name, side_value

    def calc_side_ucosine(self, *, set: bool = False) -> Tuple[str, int]:
        """Calculates remaining length using cosine rule

        Parameters
        ----------
        set: :class:`bool`
            Whether to set value
        """
        sides = [self.a, self.b, self.c]
        if all(sides) or len([i for i in sides if i != 0]) < 2:
            raise ValueError("Cannot use cosine rule on current state")

        index = sides.index(0)
        name = tuple(self.lengths.keys())[index]
        op_angle = self.get_angle(self.length_maps[name])

        sides.pop(index)
        a, b = sides

        if not op_angle:
            raise ValueError(f"Cannot use cosine rule, angle opposite {name} is missing")
        
        c = ((a ** 2) + (b ** 2) - (2 * a * b) * cos(op_angle)) ** 0.5

        if set:
            self.update_length(name, c)
        return name, c

    def median(self) -> float:
        """Returns median of triangle"""
        sides = [self.a, self.b, self.c]

        if not all(sides):
            raise ValueError("Inorder to workout median of triangle, all sides must be provided")
        
        a, b, c = sides
        a = (a ** 2) / 2
        b = (b ** 2) / 4
        c = (c ** 2) / 2

        return ((a + c) - b) ** 0.5

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
        A, B, C = [self.get_angle(i) for i in self.angle_maps.keys()]
        
        if ((a == b) or (b == c) or (c == a)) and \
            ((A == B) or (B == C) or (C == A)):
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
            # Fill last angle in, if exists

            if angle := self.get_angle("BCA"):
                self.set_angle("CAB", (180 - 90 - degrees(angle)))
            else:
                self.set_angle("BCA", (180 - 90 - degrees(self.get_angle("CAB"))))

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

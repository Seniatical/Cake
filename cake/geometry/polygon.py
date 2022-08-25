from math import radians, sin, cos, tan, pi
from .basic import Shape
from typing import Tuple


class Polygon(Shape):
    """Base object for creating irregular/regular polygons.

    Parameters
    ----------
    Shares same parameters as :class:`Shape`
    """

    def __init__(self, *lengths, **kwds) -> None:
        super().__init__(*lengths, **kwds)

        if self.sides < 2:
            raise ValueError("Polygons must have more then 2 sides!")
        if sum(self.angles.values()) > self.sum_angles():
            raise ValueError(f"Sum of angles for this polygon must be less then {self.sum_angles()}")

    def set_angle(self, angle: str, size: float, *, convert: bool = True) -> None:
        if not 0 < size < 360:
            raise ValueError("Angle must be greater then 0 and less then 360")

        suma = self.sum_angles()
        current = sum(self.get_angle(i) for i in self.angle_maps)

        if current > radians(suma):
            raise ValueError("Invalid angles")
        c = self.get_angle(angle)
        nsum = current - c + size

        if nsum > radians(suma):
            raise ValueError("Invalid angle")

        self.angles[self.get_angle(angle, name=True)] = radians(size) if convert else size

    def area(self) -> float:
        side = self.lengths[list(self.lengths)[0]]
        return (self.sides * side * self.apothem_from_crad()) / 2

    def perimeter(self) -> float:
        return sum(self.lengths.values())

    def sum_angles(self) -> float:
        return (self.sides - 2) * 180

    def triangles(self) -> int:
        """ Returns the number of triangle that can be fitted in the regular polygon """
        return self.sides - 2

    def exterior_angle(self) -> float:
        """ Return size of exterior angle for regular polygons """
        return 360 / self.sides

    def interior_angle(self) -> float:
        """ Returns size of interior polygon for regular polygons """
        return 180 - (360 / self.sides)

    def circumradius(self, *, length: str = None) -> float:
        """ Returns the circumradius for polygone

        Parameters
        ----------
        length: :class:`str`
            Length to use
        """
        side = self.get_length(length or list(self.lengths.keys())[0])

        return side / (2 * sin(pi / self.sides))

    def apothem_from_length(self, *, length: str = None) -> float:
        """ Return apothem using a side of polygon

        Parameters
        ----------
        length: :class:`str`
            Length to use
        """
        side = self.get_length(length or list(self.lengths.keys())[0])

        return (side / (2 * tan(pi / self.sides)))

    def apothem_from_crad(self, *, length: str = None):
        """ Return apothem using the circumradius of polygon

        Parameters
        ----------
        length: :class:`str`
            Length to use when calculating circumradius
        """
        c_rad = self.circumradius(length=length)
        return c_rad * cos(pi / self.sides)

    def centroid(self, **vec_y) -> Tuple[int, int]:
        """ Calculates the centroid of the polygon.

        Parameters
        ----------
        **vec_y: :class:`float`
            Kwarg mapping for :meth:`Shape.vectorize`
        """
        area = 1 / (6 * self.area())
        try:
            vec = self._vector
        except AttributeError:
            vec = self.vectorize(**vec_y)

        cx, cy = 0, 0
        
        for i in range(len(vec)):
            x0, y0 = vec[i - 1]
            x1, y1 = vec[i]

            v = (x0 * y1) - (x1 * y0)
            cx += v * (x0 + x1)
            cy += v * (y0 + y1)
        
        return ((area * cx), (area * cy))

    def is_regular(self) -> bool:
        """Checks whether the polygon is regular.

        * **All** sides are the same
        * **All** angles are the same.

        .. note::
            If there are no angles provided, it will skip the check for angles,
            assuming there all the same.
        """
        r = sum(self.lengths.values()) % (self.lengths[list(self.lengths)[0]])
        interior = self.interior_angle()
        a = all(i == interior for i in self.angles.values())

        if not r and a:
            return True
        return False

    def __repr__(self) -> str:
        sides = [f"{k}={v}" for k, v in self.lengths.items()]
        return f"Polygon({' '.join(sides)})"

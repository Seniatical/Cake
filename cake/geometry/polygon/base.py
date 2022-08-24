from math import sin, cos, pi, tan
from cake.geometry.basic import Shape


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

    def area(self) -> float:
        side = self.lengths[list(self.lengths)[0]]
        return (self.sides * side * self.apothem_from_crad()) / 2

    def set_angle(self, angle: str, size: float) -> None:
        if not 0 < size < 360:
            raise ValueError("Angle must be greater then 0, and less then 360")

        if any(i for i in angle if i not in self.lengths):
            raise ValueError("Unknown points in angle")
        self.angles[angle] = size

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

    def circumradius(self, *, side_index: int = 0) -> float:
        """ Returns the circumradius for polygone

        Parameters
        ----------
        size_index: :class:`int`
            Index of side to use

            .. rubric:: Example
                .. code-block::py
                    >>> p = Polygon(3, 3, 3, 3)
                        #           ^  ^  ^  ^
                        #           a  b  c  d
                    >>> p.circumradius(side_index=2)
                    # Uses side c
        """
        side = self.lengths[list(self.lengths)[side_index]]

        return side / (2 * sin(pi / self.sides))

    def apothem_from_length(self, *, side_index: int = 0) -> float:
        """ Return apothem using a side of polygon

        Parameters
        ----------
        side_index: :class:`int`
            Index of side to use, refer to :meth:`cake.geometry.Polygon.circumradius` for usage.
        """
        side = self.lengths[list(self.lengths)[side_index]]

        return (side / (2 * tan(pi / self.sides)))

    def apothem_from_crad(self, *, side_index: int = 0):
        """ Return apothem using the circumradius of polygon

        Parameters
        ----------
        side_index: :class:`int`
            Index of side to use, refer to :meth:`cake.geometry.Polygon.circumradius` for usage.
        """
        c_rad = self.circumradius(side_index=side_index)
        return c_rad * cos(pi / self.sides)

    def is_regular(self) -> bool:
        """Checks whether the polygon is regular.

        * **All** sides are the same
        * **All** angles are the same.

        .. note::
            If there are no angles provided, it will skip the check for angles,
            assuming there all the same.
        """
        r = sum(self.lengths.values()) % (self.lengths[list(self.lengths)[0]])

        if self.angles:
            a = sum(self.angles) % self.lengths[list(self.angles.keys())[0]]
        else:
            a = 0

        if r == 0 and a == 0:
            return True
        return False

    def __repr__(self) -> str:
        sides = [f"{k}={v}" for k, v in self.lengths.items()]
        return f"Polygon({' '.join(sides)})"

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

    def perimeter(self) -> float:
        return sum(self.lengths.values())

    def sum_angles(self) -> float:
        return (self.sides - 2) * 180

    def triangles(self) -> int:
        return self.sides - 2

    def exterior_angle(self) -> float:
        assert self.is_regular(), "Exterior angle can only be worked out for regular polygons"
        return 360 / self.sides

    def interior_angle(self) -> float:
        assert self.is_regular(), "Interior angle can only be worked out for regular polygons"
        return 180 - (360 / self.sides)

    def circumradius(self, *, side_index: int = 0) -> float:
        side = self.lengths[list(self.lengths)[side_index]]

        return side / (2 * sin(pi / self.sides))

    def apothem_from_length(self, *, side_index: int = 0) -> float:
        side = self.lengths[list(self.lengths)[side_index]]

        return (side / (2 * tan(pi / self.sides)))

    def apothem_from_crad(self):
        c_rad = self.circumradius()
        return c_rad * cos(pi / self.sides)


    def is_regular(self) -> bool:
        r = sum(self.lengths.values()) % (self.lengths[list(self.lengths)[0]])

        if self.angles:
            a = sum(self.angles) % self.lengths[list(self.angles.keys())[0]]
        else:
            a = 0

        if r == 0 and a == 0:
            return True
        return False

    def set_angle(self, angle: str, size: float) -> None:
        ...

    def __repr__(self) -> str:
        sides = [f"{k}={v}" for k, v in self.lengths.items()]
        return f"Polygon({' '.join(sides)})"

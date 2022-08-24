# A base ABC class for defining geometrical objects
from abc import ABC, abstractproperty, abstractmethod
from typing import Dict
from string import ascii_lowercase


def _get_numerical_key(_data: dict) -> int:
    # Fetch the greatest letter in the alphabet
    if not _data:
        return -1

    keys = _data.keys()
    sorted_keys = sorted(keys, key=lambda key: ascii_lowercase.index(key))
    return ascii_lowercase.index(sorted_keys[-1])


class Shape(ABC):
    r"""
    Base object for generating shapes, or shape types

    Parameters
    ----------
    *r_lengths: :class:`float`
        Lengths of shape
    lengths: Dict[:class:`str`, :class:`float`]
        Provide lengths and length names using a premade mapping.

        .. rubric:: Example
            .. code-block::py
                >>> from cake.geometry import Shape
                >>> Shape(lengths={"a": 2, "b": 2, "c": 2})
                Shape(a=2, b=2, c=2)
                >>> Shape(2, 2, lengths={"a": 2})
                Shape(a=2, b=2, c=2)
    angles: Dict[:class:`str`, :class:`float`]
        Angle mapping for the shape, must be in the format ``XXX``.

        .. rubric:: Example
            .. code-block::py
                >>> from cake.geometry import Shape
                >>> Shape(5, 12, 13, angles={"BAC": 30, "ABC": 60, "BCA": 90})
                >>> ... # Valid shape
    """
    def __init__(
        self, *r_lengths,
        lengths: Dict[str, float] = {},
        angles: Dict[str, float] = {},
    ) -> None:
        self.lengths = lengths
        self.angles = angles

        if any(i for i in self.angles.values() if not (0 < i < 360)):
            raise ValueError("Angles in shape must be greater then 0, and less then 360")

        if r_lengths:
            curr = _get_numerical_key(self.lengths)
            for v in r_lengths:
                curr += 1
                self.lengths[ascii_lowercase[curr]] = v

        self.sides = len(self.lengths)

    @abstractmethod
    def set_angle(self, angle: str, size: float) -> float:
        """Update or set the size of an angle

        Parameters
        ----------
        angle: :class:`str`
            Angle to target
        size: :class:`float`
            Angle size
        """

    @abstractmethod
    def area(self):
        """ Returns area of shape """

    @abstractmethod
    def perimeter(self):
        """ Returns perimeter of shape """

    @abstractmethod
    def sum_angles(self):
        """ Returns the sum of the angles in the shape """

    def __repr__(self, *, prefix: str = "Shape") -> str:
        sides = [f"{k}={v}" for k, v in self.lengths.items()]
        return f"{prefix}({' '.join(sides)})"

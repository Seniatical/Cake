# A base ABC class for defining geometrical objects
from abc import ABC, abstractmethod
from typing import Dict, List
from string import ascii_lowercase
from itertools import permutations


def _get_numerical_key(_data: dict) -> int:
    # Fetch the greatest letter in the alphabet
    if not _data:
        return -1

    keys = _data.keys()
    return ascii_lowercase.index(list(keys)[-1])


def _chain_items(data: list) -> list:
    # [A, B, C, D]
    d = [i.upper() for i in data]
    result = []
    previous = d[0]

    for i in d[1:]:
        result.append(previous + i)
        previous = i
    result.append(previous + d[0])

    return result


class Shape(ABC):
    r"""
    Base object for generating shapes, or shape types

    .. note::
        If any lengths/angles are set to 0,
        Cake will assume that the value is unknown.

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
    def _clean_angles(self) -> None:
        if any(i for i in self.angles.values() if not 0 < i < 360):
            raise ValueError("Angles must be greater then 0 and less then 360")

        angles = self.angles.copy()
        combinations = self.possible_angles()
        markers = []

        for angle, value in angles.items():
            self.angles.pop(angle)

            if len(angle) != 3:
                raise ValueError(f"Invalid angle {angle}")
            if angle.upper() not in combinations:
                raise ValueError(f"Unknown points in angle {angle}")
            if angle[1] not in markers:
                markers.append(angle[1])
                self.angles[angle.upper()] = value

    def __init__(
        self, *r_lengths,
        lengths: Dict[str, float] = None,
        angles: Dict[str, float] = None,
    ) -> None:
        self.lengths = lengths or dict()
        self.angles = angles or dict()

        if r_lengths:
            curr = _get_numerical_key(self.lengths)
            for v in r_lengths:
                curr += 1
                self.lengths[ascii_lowercase[curr]] = v

        _lengths = _chain_items(self.lengths.keys())
        self.lengths = {_lengths[i]: self.lengths[v] for i, v in enumerate(self.lengths.keys())}

        self.sides = len(self.lengths)
        self._clean_angles()

    def possible_angles(self) -> List[str]:
        """Returns all possible angle combinations in the shape"""
        angles = permutations([i[1] for i in self.lengths], 3)

        return [''.join(angle).upper() for angle in angles]

    def get_angle(self, angle: str) -> List[str]:
        """Get an angle assigned from :attr:`Shape.angles`

        Parameters
        ----------
        angle: :class:`str`
            Angle to search for
        """
        angle = angle.upper()
        if angle not in self.possible_angles():
            raise ValueError("Unknown angle")

        marker = angle[1]
        similar_permutation = None
        for angle in self.angles:
            if angle[1] == marker:
                similar_permutation = angle
                break
        
        if not similar_permutation:
            return 0
        return self.angles[similar_permutation]

    def get_length(self, length: str) -> None:
        """Get a length from the polygon

        Parameters
        ----------
        length: :class:`str`
            Length to get
        """
        _length = self.lengths.get(length.upper())
        if not _length:
            _length = self.lengths.get(length[::-1].upper())
            if not _length:
                raise ValueError(f"Cannot find length {length}")
            return _length

        return _length

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

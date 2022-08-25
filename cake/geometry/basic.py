# A base ABC class for defining geometrical objects
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Dict, Generator, List, Tuple, Union
from string import ascii_lowercase
from itertools import permutations
from math import radians        # Convert deg to rad


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

    .. note::
        Defining shapes using points,
        Cake supports the use of vectors and can export shapes as vectors

        .. rubric:: Defining

        .. code-block::py
            >>> from cake.geometry import Shape
            >>> s = Shape((5, 0), (2, 2), (5, 2), (2, 0))
            
            # AB -> 5   Y=0
            # BC -> 2   Y=2
            # CD -> 5   Y=2
            # DA -> 2   Y=0

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
    def _clean_angles(self, convert: bool) -> None:
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
                if convert:
                    value = radians(value)

                markers.append(angle[1])
                self.angles[angle.upper()] = value

    def _seperate_lengths(self) -> None:
        for key, value in self.lengths.items():
            if isinstance(value, Iterable):
                x, y = value
                self.lengths[key] = x
                self.y_centroids[key] = y

    def __init__(
        self, *r_lengths,
        lengths: Dict[str, float] = None,
        angles: Dict[str, float] = None,
        convert_to_rad: bool = True
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
        self.y_centroids = {}

        self.sides = len(self.lengths)
        self._clean_angles(convert_to_rad)
        self._seperate_lengths()

    def possible_angles(self) -> List[str]:
        """Returns all possible angle combinations in the shape"""
        angles = permutations([i[1] for i in self.lengths], 3)

        return [''.join(angle).upper() for angle in angles]

    def get_angle(self, angle: str, *, name: bool = False) -> Union[float, str]:
        """Get an angle assigned from :attr:`Shape.angles`

        Parameters
        ----------
        angle: :class:`str`
            Angle to search for
        name: :class:`bool`
            Whether to return classified name instead of value
        """
        angle = angle.upper()
        if angle not in self.possible_angles():
            raise ValueError("Unknown angle")

        marker = angle[1]
        similar_permutation = None
        for _angle in self.angles:
            if _angle[1] == marker:
                similar_permutation = _angle
                break
        
        if name:
            return similar_permutation or angle

        if not similar_permutation:
            return 0
        return self.angles[similar_permutation]

    def get_length(self, length: str, *, name: bool = False) -> float:
        """Get a length from the polygon

        Parameters
        ----------
        length: :class:`str`
            Length to get
        name: :class:`str`
            Whether to return the true length name instead of value
        """
        length = length.upper()

        _length = self.lengths.get(length)
        if _length is None:
            length = length[::-1]
            _length = self.lengths.get(length)

            if _length is None:
                raise ValueError(f"Cannot find length {length}")

        if name:
            return length

        return _length

    def update_length(self, length: str, value: float) -> None:
        """Update a length

        Parameters
        ----------
        length: :class:`str`
            Length to update
        value: :class:`float`
            New length value
        """
        self.lengths[self.get_length(length, name=True)] = float(value)

    def vectorize(self, **y_kwds) -> Generator[Tuple[int, int], None, None]:
        """ Returns shape as a 2D vector

        Parameters
        ----------
        **y_kwds: :class:`float`
            kwargs for mapping of Y values

            .. code-block::py
                >>> from cake.geometry import Shape
                >>> s = Shape(2, 3, 4)
                >>> s.vectorize(AB=0, BC=5, CA=0)
                ... [(2, 0), (3, 5), (4, 0)]
        """
        y_kwds = {**self.y_centroids, **y_kwds}

        for length in self.lengths:
            x = self.get_length(length)
            y = y_kwds.get(length, 0)
            yield (x, y)  

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

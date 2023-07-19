## All the odd few binary operators
from .add import Operation


class LeftShift(Operation):
    def __flatten__(self) -> None:
        assert len(self.nodes) == 2, 'Invalid shift op given, must only contain 2 nodes'


class RightShift(Operation):
    def __flatten__(self) -> None:
        assert len(self.nodes) == 2, 'Invalid shift op given, must only contain 2 nodes'


class And(Operation):
    def __flatten__(self) -> None:
        assert len(self.nodes) == 2, 'Invalid and op given, must only contain 2 nodes'


class Xor(Operation):
    def __flatten__(self) -> None:
        assert len(self.nodes) == 2, 'Invalid xor op given, must only contain 2 nodes'


class Or(Operation):
    def __flatten__(self) -> None:
        assert len(self.nodes) == 2, 'Invalid Or op given, must only contain 2 nodes'

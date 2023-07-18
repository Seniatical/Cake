## Holds values to be multiplied, these are not simplified like the addition and divide operations,
## As a result it is not recomended to directly use this operator
from .add import Operation
from typing import Any


class Multiply(Operation):

    def flatten(self) -> None:
        return

class Power(Operation):

    @property
    def base(self) -> Any:
        return self.nodes[0]

    @property
    def power(self) -> Any:
        return self.nodes[1]

    def flatten(self) -> None:
        assert len(self.nodes) == 2, 'Power operation only take 2 nodes, base and power'

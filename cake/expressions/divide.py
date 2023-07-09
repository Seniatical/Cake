## Mimics a fraction expr
##
## Divide(1, 3) -> 1/3
##
## Divide(Add('x', 1), 2) -> (x + 1) / 2
##
## Expression(Divide(1, 3)) * 3 -> 1/3 * 3 -> 1
##
from .add import Operation


class Divide(Operation):
    ''' The divide operation mimicks a fractional element.
    Unlike the rational class which only accepts numerical values for top and bottom values,
    the ``Divide`` op can function using unknowns.
    '''

    def __str__(self) -> str:
        return ' / '.join(map(str, self.nodes))

    def flatten(self) -> None:
        assert len(self.nodes) == 2, 'Invalid divide op given, must only contain 2 nodes'

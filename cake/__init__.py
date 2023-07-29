__version__ = '0.2.0a5'
__author__ = 'Seniatical'

from ._abc import (
    Basic,
    BasicNode,
    BasicExpression
)

from .basic import (
    Number as INumber,
    Complex as IComplex,
    Real as IReal,
    Rational as IRational,
    Integral as IIntegeral,
    Variable as IVariable,
    Function as IFunction
)
IFloat = IReal

from .utils import (
    to_radians,
    to_degrees,
    math
)

from .core.comparity import ComparitySymbol, Comparity
from .core.expressions.core import (
    Expression
)

from .core.expressions.add import ExpressionNode, Operation, Add
from .core.expressions.divide import Divide, FloorDiv, Modulo
from .core.expressions.multiply import Multiply, Power
from .core.expressions.binaries import (
    LeftShift,
    RightShift,
    And,
    Xor,
    Or
)

from .core.numbers import (
    Number,
    Complex,
    Real,
    Rational,
    Integral
)
Float = Real
from .core.variables import BasicVariable, Variable, VariableGroup, RaisedVariable
from .core.functions import (
    Function,
)

from .constants.core import (
    Constant,
)
from .constants.pi import Pi

from .functions.trigonometry import (
    Sin,
    Cos,
    Tan,
    ASin,
    ACos,
    ATan,
    ATan2,
    SinH,
    CosH,
    TanH,
    ASinH,
    ACosH,
    ATanH,
)
from .functions.integral import (
    Truncate,
    Ceil,
    Floor,
    Round,
)
from .functions.roots import Root, Sqrt

from . import (
    geometry,
    expressions
)

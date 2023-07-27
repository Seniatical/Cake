from __future__ import annotations
from abc import ABC

from typing import Generic, TypeVar, Iterator


Self = TypeVar('Self')


class Like(Generic[Self]):
    ''' Typehint used throughout the cake library,
    used to symbolise that a class behaves or can be shown as another implementation.
    '''


class Basic(ABC, object):
    '''
    Represents a basic object which all objects in the cake library derive from,
    Using this class we can check if any object belongs to the cake library
    '''


class BasicNode(Basic):
    ''' Represents an object which can be represented as a node in an expression,
    Objects such as shapes and matrices which cannot form an :class:`Expression` object
    don't inherit this object.

    .. code-block:: py

        >>> issubclass(Variable, BasicNode)
        True
        >>> issubclass(Number, BasicNode)
        True
        >>> issubclass(Function, BasicNode)
        True
    '''


class BasicExpression(Like[Iterator[BasicNode]]):
    '''
    An object which represents an expression,
    any object which can be solved to return a desired result.

    .. note::
        Expressions generally should not be created directly,
        this is to keep code bases simple and easy to understand.

        .. tip::
            :meth:`Expression.from_string` A helper method for parsing stringed expressions such as,
            ``a + b + c`` can be used to generate the example below.

    .. code-block:: py
        
        from cake import Variable

        a, b, c = Variable.gen_many('a', 'b', 'c')
        expr = a + b + c

        print(expr.solve(a=10, b=10, c=10))
        ## >> 30
    '''

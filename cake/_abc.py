from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Type, TypeVar, Iterator, Union


Self = TypeVar('Self')


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

        >>> issubclass(Unknown, BasicNode)
        True
        >>> issubclass(Number, BasicNode)
        True
        >>> issubclass(Function, BasicNode)
        True
    '''


class BasicExpression(Iterator[BasicNode]):
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
        
        from cake import Unknown

        a, b, c = Unknown.gen_many('a', 'b', 'c')
        expr = a + b + c

        print(expr.solve(a=10, b=10, c=10))
        ## >> 30
    '''

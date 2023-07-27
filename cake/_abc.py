from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Any, Generic, TypeVar, Iterator


Self = TypeVar('Self')


class Like(Generic[Self]):
    ''' Typehint used throughout the cake library,
    used to symbolise that a class behaves or can be shown as another implementation.
    '''


class Maybe(Generic[Self]):
    ''' Typehint used throughout the cake library,
    used to hint that an object may derive or be included in another category of objects.
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


class BasicSolvable(Basic, Maybe[BasicNode]):
    ''' An object which can be solved via the function ``solve`` '''

    @abstractmethod
    def solve(self, **kwds) -> Any:
        ''' Values for solving the object for a desired value.

        .. note::
            The parameter format may change for certain objects.
        '''


class BasicEvaluator(Basic, Maybe[BasicNode]):
    ''' An object which can be evaluated,
    like a :class:`BasicSolvable` object except it is abit more then just an expression. 
    '''

    @abstractmethod
    def evaluate(self, **kwds) -> Any:
        ''' Values for evaluating the object for a desired value.

        .. note::
            The parameter format may change for certain objects.
        '''


class BasicExpression(Like[Iterator[BasicNode]], BasicSolvable):
    ''' An object which represents a generic expression. '''


class BasicVariable(BasicSolvable, Like[BasicExpression]):
    ''' Represents a variable '''


class BasicFunction(BasicEvaluator):
    ''' Represents a mathmatical function '''

## Nodes are used for generating syntax trees for simplifying expressions
## For example:
##
## Unknown + Unknown -> Add(Unknown, Unknown)
##
## Expression('x + y') / 5 -> Divide(Add(Unknown, Unknown), 5)
##
## Unknown + Unknown - Unknown -> Add(Add(Unknown, Unknown), -Unknown)
##
## (U1 + U2)(U3 - U4) -> Add(U1 * U3, U1 * U4, U2 * U3, U2 * U4)
##                    -> Add(U1 * U3, Add(U1 * U4 + U2 * U3), U2 * U4)
##                    -> ...
##
from __future__ import annotations
from abc import ABC, abstractmethod
from cake.basic import BasicNode
import cake


class ExpressionNode(ABC, object):
    ''' Base class for identifying nodes in an expression '''

    def __init__(self, x: BasicNode, y: BasicNode, /, *nodes: BasicNode) -> None:
        self.nodes = (x, y) + nodes

        self.__post_init__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(str, self.nodes))})'

    @abstractmethod
    def __post_init__(self) -> None:
        ...


class Operation(ExpressionNode):
    ''' Base class for defining operations within the cake library,
    operations cannot be individually manipulated. 
    Use :class:`Expression` to assist in this.
    '''

    def __post_init__(self) -> None:
        self.flatten()
    
    @abstractmethod
    def flatten(self) -> None:
        ''' Simplifies the expression into its simplest form if possible,
        can also be used as a check method when new operations are executed.
        '''
        raise NotImplemented


class Add(Operation):
    def __str__(self) -> str:
        return ' + '.join(map(str, self.nodes))

    def flatten(self) -> None:
        cleaned_nodes = []
        nodes = []

        for node in self.nodes:

            ## Expression has been passed
            if hasattr(node, 'exp'):
                node = node.exp

            if isinstance(node, Add):
                nodes.extend(node.nodes)
            else:
                nodes.append(node)

        for node in nodes:
            if not node:
                continue

            if not isinstance(node, BasicNode):
                if isinstance(node, str):
                    node = cake.Unknown(node)
                else:
                    node = cake.Number.convert(node)

            for index, cleaned_node in enumerate(cleaned_nodes):
                if isinstance(node, cake.Number) and isinstance(cleaned_node, cake.Number):
                    cleaned_nodes[index] = node + cleaned_nodes[index]
                    break

                if isinstance(node, cake.Unknown) and isinstance(cleaned_node, cake.Unknown):
                    similar = cake.Unknown.is_similar(node, cleaned_node)
                    if similar:
                        cleaned_nodes[index] = cleaned_nodes[index] + node
                        break

                if isinstance(node, cake.UnknownGroup) and isinstance(cleaned_node, cake.UnknownGroup):
                    similar = cake.UnknownGroup.is_similar(node, cleaned_node)
                    if similar:
                        cleaned_nodes[index] = cleaned_nodes[index] + node

            else:
                cleaned_nodes.append(node)

        self.nodes = cleaned_nodes
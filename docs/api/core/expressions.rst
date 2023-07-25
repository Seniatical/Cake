.. meta::
    :title: Cake - API Reference [Expressions]
    :type: website
    :url: https://cakepy.rtfd.io
    :description: API Reference for interacting with expressions in cake.
    :theme-color: #f54646

.. currentmodule:: cake


***********
Expressions
***********
Expressions can be viewed as a collection of nodes, 
these nodes are binded to each other using operators.

Expression
==========
.. autoclass:: cake.Expression
    :members:
    :show-inheritance:

Operations
==========
Operations are a fundemental part of expressions, 
you can use our built in operations which cover most of the python arithmetic range.

Creating your own
-----------------
If your in need of your own operation, look no further.
But first lets define our own operation:

.. code-block:: py

    class MyOperation(cake.Operation):

        ## My cool operation will return the sum of the nodes * 3
        def run(self, node: MyOperation, **kwds) -> Any:
            solved = map(lambda x: cake.utils.solve_if_possible(x, **kwds), self.nodes)
            return sum(solved) * 3

        ## Don't forget the flatten method, this serves as a cleanup function
        ## Called straight after you initialise your operation
        ## We dont need it for anything in our case.
        def flatten(self) -> None:
            return

Now that our operation is defined lets use it!

.. code-block:: py 

    >>> op = MyOperation('x', 'y', 5)
    # Same as doing (x + y + 5) * 3 in our case
    >>> expr = Expression(op)
    >>> expr
    MyOperation(x, y, 5)
    >>> expr.solve(x=5, y=5)
    45

Prettifying Outputs
-------------------
You may have noticed that the string version of our operation isn't very nice,
you can define your own `__str__` method which can better represent how your operation works,
in our case its easy!

.. code-block:: py
    :emphasize-lines: 14,15,16,17

    class MyOperation(cake.Operation):

        ## My cool operation will return the sum of the nodes * 3
        def run(self, node: MyOperation, **kwds) -> Any:
            solved = map(lambda x: cake.utils.solve_if_possible(x, **kwds), self.nodes)
            return sum(solved) * 3

        ## Don't forget the flatten method, this serves as a cleanup function
        ## Called straight after you initialise your operation
        ## We dont need it for anything in our case.
        def flatten(self) -> None:
            return

        ## Lets define a new str function
        def __str__(self) -> str:
            nodes = ' + '.join(map(str, self.nodes))
            return f'({nodes}) * 3'

Now whenever we want to print out our expression, we have a consistent approach

.. code-block:: py

    >>> op = MyOperation('x', 'y', 5)
    >>> op
    ## Before: MyOperation(x, y, 5)
    (x + y + 5) * 3

Predefined Operations
---------------------

* Add: :class:`Add` ~ Many nodes are able to be passed, represents the addition of all nodes.
    - For subtraction simply use the Add operation but negate the subtraction node
* Divide: :class:`Divide` ~ 2 nodes (x, y) are able to be passed, represents the division of 2 nodes.
    - Properties ``numerator`` and ``denominator`` are used to represent the 2 nodes
* FloorDiv: :class:`FloorDiv` ~ Inherits all properties of :class:`Divide`, except represents the floor division of the nodes.
* Modulo: :class:`Modulo` ~ Inherits all properties of :class:`Divide`, except represents mod of the 2 nodes.
* Multiply: :class:`Multiply` ~ Many nodes are able to be passed, represents the multiplication of all nodes
* Power: :class:`Power` ~ 2 nodes (x, y) are able to be passed, represents one node is raised to the other node
    - Properties ``base`` and ``power`` are used to represent the 2 nodes.

Binary operators: :class:`LeftShift` (<<), :class:`RightShift` (>>), :class:`And` (&), :class:`Xor` (^) and :class:`Or` (|)
- These are also supported and can only take 2 nodes (x, y) with no other special properties.
- Each operation represents ``x ? y`` where *?* is the operator at hand.

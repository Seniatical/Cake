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
    >>> expr.solve(x=5, y=5)
    45

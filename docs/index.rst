.. cake documentation master file, created by
   sphinx-quickstart on Mon Jul 24 15:20:02 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

********************************
Welcome to Cake's documentation!
********************************
Welcome to the cake library, a powerful OOP based mathmatical library for python.

.. code-block:: py

   from cake import *

   x = Variable('x')
   expr = Sqrt(x + 5)

   print(expr.solve(x=20))
   # 5


Getting Started 
===============
To get started with cake, we need you to install it first.

.. code-block:: sh

   ## Windows
   pip install git+https://github.com/Seniatical/Cake

   ## Linux/Mac
   pip3 install git+https://github.com/Seniatical/Cake


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

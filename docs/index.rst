.. meta::
   :title: Cake - Documentation
   :type: website
   :url: https://cakepy.rtfd.io
   :description: Welcome to Cake's documentation.
   :theme-color: #f54646


********************************
Welcome to Cake's documentation!
********************************
Welcome to the cake library, a powerful OOP based mathmatical library for python.

.. code-block:: py

   from cake import *

   x = Variable('x')
   expr = x + 5

   print(expr.solve(x=5))
   # 10


Getting Started 
===============
To get started with cake, we need you to install it first.

.. code-block:: sh

   ## Windows
   pip install git+https://github.com/Seniatical/Cake

   ## Linux/Mac
   pip3 install git+https://github.com/Seniatical/Cake

Once installed, have fun!


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

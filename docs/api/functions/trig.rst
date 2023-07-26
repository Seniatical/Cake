.. meta::
    :title: Cake - API Reference [Trigonometric Functions]
    :type: website
    :url: https://cakepy.rtfd.io
    :description: API Reference for interacting with trigonometric functions in cake.
    :theme-color: #f54646

.. currentmodule:: cake

***********************
Trigonometric Functions
***********************
Cake offers built in support for the standard trigonometric functions which can be found in the :py:mod:`math` library.

Modifying Handlers
==================
You may have noticed that functions have attributes such as :attr:`Function.preprocessor`, but don't know how they can be used?
Simply set the attribute to the desired value.

.. code-block:: py

    from cake import *

    my_awesome_pre_processor = lambda **kwds: kwds
    f = Sin(Variable('x'))
    f.preprocessor = my_awesome_pre_processor

    ## Now we can carry on doing what we want with f

Sin
===
.. autoclass:: cake.Sin
    :members:
    :show-inheritance:


ASin
====
.. autoclass:: cake.ASin
    :members:
    :show-inheritance:


SinH
====
.. autoclass:: cake.SinH
    :members:
    :show-inheritance:


ASinH
=====
.. autoclass:: cake.ASinH
    :members:
    :show-inheritance:


Cos
===
.. autoclass:: cake.Cos
    :members:
    :show-inheritance:


ACos
====
.. autoclass:: cake.ACos
    :members:
    :show-inheritance:


CosH
====
.. autoclass:: cake.CosH
    :members:
    :show-inheritance:


ACosH
=====
.. autoclass:: cake.ACosH
    :members:
    :show-inheritance:


Tan
===
.. autoclass:: cake.Tan
    :members:
    :show-inheritance:


ATan
====
.. autoclass:: cake.ATan
    :members:
    :show-inheritance:


ATan2
=====
.. autoclass:: cake.ATan2
    :members:
    :show-inheritance:


TanH
====
.. autoclass:: cake.TanH
    :members:
    :show-inheritance:


ATanH
=====
.. autoclass:: cake.ATanH
    :members:
    :show-inheritance:

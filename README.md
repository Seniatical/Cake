<p align="center">
    <img width="468" height="132" src="https://raw.githubusercontent.com/Seniatical/Cake/main/logos/logo.png" alt="Cake logo">
</p>

<p align="center">
    <a href='https://cakepy.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/cakepy/badge/?version=latest' alt='Documentation Status' />
    </a>
</p>

<p align="center">
    Cake is a <b>WIP</b> computer algebraic system, which utilises pythons OOP to create powerful objects which can be used to simulate mathmatical expressions.
</p>

# Documentation
You can view our documentation for cake [here](https://cakepy.rtfd.io).

# Installation
```sh
## Windows
pip install -U git+https://github.com/Seniatical/Cake

## Linux/Mac
pip3 install -U git+https://github.com/Seniatical/Cake
```

# Basic Usage
```py
from cake import *

x, y = Variable.many('x', 'y')
expr = x + y
print(expr.solve(x=5, y=3))
# 8
```

## Integrating with functions
```py
from cake import *

x = Variable('x')
expr = Sqrt(x ** 2 + 3 * x)
print(expr)
# Sqrt(x**2 + 3x)
print(expr.evaluate(x=3))
# 3*Sqrt(2)
print(expr.evaluate(x=3).true_value())
# 4.242640687119286
```

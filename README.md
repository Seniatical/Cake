<p align="center">
    <img width="468" height="132" src="https://raw.githubusercontent.com/Seniatical/Cake/main/logos/logo.png" alt="Cake logo">
</p>

# Cake

## Overview
(WIP) Cake, an algebraic math library for python.

## Basic Usage
```py
from cake import *

x, y = Variable.many('x', 'y')
expr = x + y
print(expr.solve(x=5, y=3))
# 8

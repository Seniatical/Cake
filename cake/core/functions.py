'''
Functions in the cake library are used to imitate the default Sin, Cos and Tan mathmatical functions,
except they are able to operate using core components in the cake library such as ``Unknowns``.

>>> from cake import Sin, Unknown, Expression, Add
>>> Sin(Unknown('x'))
Sin(x)
>>> Sin(Expression(Add('x', 3)))
Sin(x + 3)
>>> S = Sin(Unknown('x'))
>>> Expr = Expression(Add('x', 3))
>>> Expr += S
>>> Expr
x + 3 + Sin(x)
>>> Expr.solve(x=90)
94
'''


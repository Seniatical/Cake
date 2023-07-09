from cake import Unknown, Expression
from cake.expressions.add import Add

x = Unknown('x')
xx = x * 2

print(x, '/', xx, '=', x / xx)

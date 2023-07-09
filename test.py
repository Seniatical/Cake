from cake import Unknown, Expression
from cake.expressions.add import Add

x = Unknown('x')
a = Add(x, 'x', 5)
b = Add('x', 4)


print(Add(a, b))
print(Expression(a) + b)

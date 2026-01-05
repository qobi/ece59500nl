# x+y
# sin(x)
# f(x)
# x f x
# f(x,y)

def plus(x, y):
    return x+y

def plus(u):
    x, y = u
    return x+y

def plus(u):
    x = u[0]
    y = u[1]
    return x+y

# Tupling ML, SML, SML/NJ, OCaml

def plus(x):
    def internal(y):
        return x+y
    return internal

def f(x):
    return 2*x+1

one = 1
two = 2

def f(x):
    return two*x+one

# Alonzo Church

f = lambda x: 2*x+1

def plus(x):
    return lambda y: x+y

plus = lambda x: lambda y: x+y

# Currying (Haskell Curry) Haskell

def pm(x, y):
    return x+y, x-y

def pm(x, y):
    return (x+y, x-y)

def pm(u):
    x, y = u
    return (x+y, x-y)

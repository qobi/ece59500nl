def plus(x, y):
    return x+y

plus(3, 4)

def plus(x):
    def internal(y):
        return x+y
    return internal

plus(3)(4)

# Currying (Haskell Curry)

def f(x):
    return 2*x+1

two = 2
one = 1

def f(x):
    return two*x+one

# Lambda expressions
# Lambda calculus (Alonzo Church)

lambda x: 2x+1

f = lambda x: 2x+1

def plus(x):
    internal = lambda y: x+y
    return internal

def plus(x):
    return lambda y: x+y

plus = lambda x: lambda y: x+y

def plus(u):
    x, y = u
    return x+y

plus((3, 4))

# ML style

#def plus((x, y)):
     return x+y

#plus((3, 4))

# Haskell style

# def plus x y:
     return x+y

# plus(3)(4)

# plus 3 4

def f(x, y):
    return x+y, x-y

u, v = f(x, y)

# S -> NP VP

# typedef S = boolean

# NP(VP):S

# sin:(real->real)(x:real):real

# typedef VP = alpha

# NP(VP:alpha):boolean
# NP:(alpha->boolean)

# typedef N = object->boolean

# table:N
# chair:N

# table:object->boolean
# chair:object->boolean

# typedef A = N->N
# typedef A = (object->boolean)->(object->boolean)
# big:A

# big(table:N):N
# big(chair:N):N

# some table
#some chair
# some big table
# some big chair

# chair on the table
# chair on the chair
# table on the table
# table on the chair

# on the table:PP

# NB -> A N
# A(N)

# typedef PP = N<-N

# NB -> N PP
# PP(N)

# sin x
# n!

# on the table:PP
# on(the table):PP

# P:NP->PP(NP:alpha):PP

# P:NP->(N<-N)(NP:alpha):(N<-N)

# typedef P = NP->(N<-N)

# primitive type: object boolean
# typedef S = boolean
# typedef VP = alpha
# typedef N = object->S
# typedef P = NP->(N<-N)
# typedef PP = N<-N
# typedef NP = beta
# typedef V = gammar

foo = lambda x, y: x+y
bar = lambda x, y: x+y
baz = lambda x, y: x+y
quux = lambda x, y: x+y

x+y==y+x
3+4==4+3

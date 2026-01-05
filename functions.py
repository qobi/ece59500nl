def plus(x, y):
    return x+y

plus(3, 4)

def plus(u):
    x, y = u
    return x+y

plus((3, 4))

# Tupling

def plus((x, y)):
    return x+y

def pm(x, y):
    return x+y, x-y

u, v = pm(3, 4)

def pm(x, y):
    return (x+y, x-y)

(u, v) = pm(3, 4)

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

lambda x: 2*x+1

(lambda x: 2*x+1)(3)

f = lambda x: 2*x+1

f(3)

lambda x, y: x+y

(lambda x, y: x+y)(3, 4)

plus = lambda x, y: x+y

plus(3, 4)

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

def plus((x, y)):
     return x+y

plus((3, 4))

# Haskell style

def plus x y:
     return x+y

plus(3)(4)

plus 3 4

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

# primitive types: object boolean
# typedef S = boolean
# typedef VP = alpha
# typedef N = object->S
# typedef A = N->N
# typedef PP = N<-N
# typedef P = NP->(N<-N)
# typedef NP = beta

# primitive types: object boolean
# typedef S = boolean
# typedef VP = S<-NP
# typedef N = object->S
# typedef A = N->N
# typedef PP = N<-N
# typedef P = NP->(N<-N)
# typedef NP = N->S
# typedef Vintrans = S<-NP
# typedef D = N->NP
# typedef Vtrans = NP->VP

foo = lambda x, y: x+y
bar = lambda x, y: x+y
baz = lambda x, y: x+y
quux = lambda x, y: x+y

x+y==y+x
3+4==4+3

# some pawn:NP
# the pawn:NP
# some:N->NP(pawn:N):NP
# some:D

# some pawn moves:S
# some(pawn) moves:S
# moves:S<-NP(some:D(pawn:N):NP):S
# captures:Vtrans(some:D(bishop:N):NP):VP(some:D(pawn:N):NP):S

all(lambda x: P(x), objects)
some(lambda x: P(x), objects)

all(lambda x: P(x))
some(lambda x: P(x))

all([P(x) for x in objects])
any([P(x) for x in objects])

# every pawn moves

all(lambda x: pawn(x) implies moves(x))
all(lambda x: (not pawn(x)) or moves(x))

all(lambda x: pawn(x)->moves(x))

moves:Vintrans
moves: S<-NP
moves: boolean<-NP

moves = lambda subject_NP: subject_NP((lambda x: moves(x)):NP->VP)

every = (
    lambda noun: (
        lambda noun1: (
            all(lambda x: noun(x)->noun1(x)))))

pawn = (lambda x: pawn(x))

every(pawn) = (
    (lambda noun: (
        lambda noun1: (
            all(lambda x: noun(x)->noun1(x)))))
    (lambda x: pawn(x)))

every(pawn) = (
    (lambda noun: (
        lambda noun1: (
            all(lambda y: noun(x)->noun1(y)))))
    (lambda x: pawn(x)))

every(pawn) = (
    lambda noun1: (
        all(lambda y: pawn(x)->noun1(y))))

move(pawn) = all(lambda y: pawn(x)->moves(y))

moves(noun1) = all(lambda y: noun1(x)->moves(y))

moves = lambda noun1: all(lambda x: noun1(x)->moves(x))

moves = lambda subject_np: subject_np(lambda x: moves(x))

moves(every(pawn)) = (
    (lambda subject_np: subject_np(lambda x: moves(x)))
    (lambda noun1: (
        all(lambda x: pawn(x)->noun1(x)))))

moves(every(pawn)) = (
    (lambda noun1: (
        all(lambda x: pawn(x)->noun1(x))))
    (lambda x: moves(x)))

moves(every(pawn)) = (
    all(lambda x: pawn(x)->(lambda y: moves(y))(x)))

moves(every(pawn)) = (
    all(lambda x: pawn(x)->moves(x)))

every = (
    lambda noun: (
        lambda noun1: (
            all(lambda x: noun(x)->noun1(x)))))

pawn = (lambda x: pawn(x))

moves = lambda subject_np: subject_np(lambda x: moves(x))

moves(every(pawn)) = (
    all(lambda x: pawn(x)->moves(x)))

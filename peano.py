# n==0
# n+1
# n-1

# n++
# n--

def plus(x, y):
    if y==0:
        return x
    else:
        return plus(x+1, y-1)

def minus(x, y):
    if y==0:
        return x
    else:
        return minus(x-1, y-1)

def times(x, y):
    if y==0:
        return 0
    else:
        return plus(x, times(x, y-1))

def divide(x, y):
    if x==0:
        return 0
    else:
        return divide(minus(x, y), y)+1

#

def plus(x, y):
    return x if y==0 else plus(x+1, y-1)

def minus(x, y):
    return x if y==0 else minus(x-1, y-1)

def times(x, y):
    return 0 if y==0 else plus(x, times(x, y-1))

def divide(x, y):
    return 0 if x==0 else divide(minus(x, y), y)+1

#

plus = lambda x, y: x if y==0 else plus(x+1, y-1)
minus = lambda x, y: x if y==0 else minus(x-1, y-1)
times = lambda x, y: 0 if y==0 else plus(x, times(x, y-1))
divide = lambda x, y: 0 if x==0 else divide(minus(x, y), y)+1

# E ::= V
#   |   E(E)
#   |   lambda V: E

plus = lambda x: lambda y: x if y==0 else plus(x+1)(y-1)
minus = lambda x: lambda y: x if y==0 else minus(x-1)(y-1)
times = lambda x: lambda y: 0 if y==0 else plus(x)(times(x)(y-1))
divide = lambda x: lambda y : 0 if x==0 else divide(minus(x)(y))(y)+1

def cons(a, d):
    def internal(c):
        return c(a, d)
    return internal

def car(c):
    def internal(a, d):
        return a
    return c(internal)

def cdr(c):
    def internal(a, d):
        return d
    return c(internal)

def cons(a, d):
    return lambda c: c(a, d)

def car(c):
    return c(lambda a, d: a)

def cdr(c):
    return c(lambda a, d: d)

cons = lambda a, d: lambda c: c(a, d)

car = lambda c: c(lambda a, d: a)

cdr = lambda c: c(lambda a, d: d)

cons = lambda a: lambda d: lambda c: c(a)(d)

car = lambda c: c(lambda a: lambda d: a)

cdr = lambda c: c(lambda a: lambda d: d)

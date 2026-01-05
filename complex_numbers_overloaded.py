import math

class complex_number:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
    def __pos__(self): return self
    def __neg__(self): return 0-self
    def __add__(self, y): return plus(self, y)
    def __radd__(self, x): return plus(x, self)
    def __sub__(self, y): return minus(self, y)
    def __rsub__(self, x): return minus(x, self)
    def __mul__(self, y): return times(self, y)
    def __rmul__(self, x): return times(x, self)
    def __div__(self, y): return divide(self, y)
    def __rdiv__(self, x): return divide(x, self)
    def __truediv__(self, y): return divide(self, y)
    def __rtruediv__(self, x): return divide(x, self)
    def __lt__(self, x): return lt(self, x)
    def __le__(self, x): return le(self, x)
    def __gt__(self, x): return gt(self, x)
    def __ge__(self, x): return ge(self, x)
    def __eq__(self, x): return eq(self, x)
    def __ne__(self, x): return ne(self, x)

def complex(real, imaginary):
    return complex_number(real, imaginary)

def real(x):
    if isinstance(x, complex_number): return x.real
    else: return x

def imaginary(x):
    if isinstance(x, complex_number): return x.imaginary
    else: return 0

def is_complex_number(thing):
    return type(thing)==complex_number

def lift_real_to_complex(real):
    return complex(real, 0)

def plus(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return complex(real(x)+real(y),
                           imaginary(x)+imaginary(y))
        else:
            return plus(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return plus(lift_real_to_complex(x), y)
        else:
            return x+y

def minus(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return complex(real(x)-real(y),
                           imaginary(x)-imaginary(y))
        else:
            return minus(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return minus(lift_real_to_complex(x), y)
        else:
            return x-y

def times(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return complex(real(x)*real(y)-imaginary(x)*imaginary(y),
                           real(x)*imaginary(y)+imaginary(x)*real(y))
        else:
            return times(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return times(lift_real_to_complex(x), y)
        else:
            return x*y

def divide(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return complex((real(x)*real(y)+imaginary(x)*imaginary(y))/
                           (real(y)*real(y)+imaginary(y)*imaginary(y)),
                           (imaginary(x)*real(y)-real(x)*imaginary(y))/
                           (real(y)*real(y)+imaginary(y)*imaginary(y)))
        else:
            return divide(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return divide(lift_real_to_complex(x), y)
        else:
            return x/y

def sqrt(x):
    if is_complex_number(x):
        r = math.sqrt(real(x)*real(x)+
                      imaginary(x)*imaginary(x))
        if imaginary(x)<0:
            return complex(math.sqrt((real(x)+r)/2),
                           -math.sqrt((r-real(x))/2))
        else:
            return complex(math.sqrt((real(x)+r)/2),
                           mathsqrt((r-real(x))/2))
    elif x>=0:
        return math.sqrt(x)
    else:
        return complex(0, math.sqrt(-x))

def lt(x, y):
    raise RuntimeError("Can't compare complex numbers")

def le(x, y):
    raise RuntimeError("Can't compare complex numbers")

def gt(x, y):
    raise RuntimeError("Can't compare complex numbers")

def ge(x, y):
    raise RuntimeError("Can't compare complex numbers")

def eq(x, y):
    return real(x)==real(y) and imaginary(x)==imaginary(y)

def ne(x, y):
    return not (x==y)

def quadratic(a, b, c, x):
    return a*x*x+b*x+c

def quadratic_roots(a, b, c):
    return (((-b+sqrt(b*b-4*a*c))/(2*a)),
            ((-b-sqrt(b*b-4*a*c))/(2*a)))

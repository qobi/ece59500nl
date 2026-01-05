def if_function(p, q, r):
    if p:
        return q
    else:
        return r

if_function(p, lambda _: q, lambda _: r)(garbage)

def if_function(p, q, r):
    return q if p else r

if_function = lambda p, q, r: q if p else r

true = car
false = cdr
if_function = lambda p, q, r: p(cons(q, r))

if_function = lambda p: lambda q: lambda r: p(cons(q)(r))

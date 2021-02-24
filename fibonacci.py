import numpy as np

def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def fib1(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        chart = np.zeros((n+1,), dtype=np.int)
        chart[0] = 0
        chart[1] = 1
        for i in range(2, n+1):
            chart[i] = chart[i-1]+chart[i-2]
        return chart[n]

def memoize(f):
    chart = {}
    def internal(x):
        if x in chart:
            return chart[x]
        else:
            result = f(x)
            chart[x] = result
            return result
    return internal

def fib2(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib2(n-1)+fib2(n-2)

fib2 = memoize(fib2)

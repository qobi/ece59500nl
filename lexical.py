def plus(x):
    def internal(y):
        return x+y
    return internal

Y = lambda f:(lambda g: lambda x: f(g(g))(x))(lambda g: lambda x: f(g(g))(x))
factorial = Y(lambda f: lambda n: 1 if n==0 else n*f(n-1))
fibonacci = Y(lambda f: lambda n: 0 if n==0 else 1 if n==1 else f(n-1)+f(n-2))

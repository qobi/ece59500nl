import argparse
parser = argparse.ArgumentParser(description = "Template")
parser.add_argument("-d",
                    default=False,
                    action="store_true")
parser.add_argument("-m",
                    default=False,
                    action="store_true")
options = parser.parse_args()

debug = options.d
memoized = options.m

def top_down_s(words):
    if debug:
        print((words, "s"))
    n = len(words)
    possibilities = []
    if n!=1:
        for k in range(1, n):
            for possibility1 in top_down_np(words[0:k]):
                for possibility2 in top_down_vp(words[k:n]):
                    possibilities.append(("s", possibility1, possibility2))
    return possibilities

def top_down_np(words):
    if debug:
        print((words, "np"))
    n = len(words)
    possibilities = []
    if n!=1:
        for k in range(1, n):
            for possibility1 in top_down_d(words[0:k]):
                for possibility2 in top_down_nb(words[k:n]):
                    possibilities.append(("np", possibility1, possibility2))
            for possibility1 in top_down_d(words[0:k]):
                for possibility2 in top_down_n(words[k:n]):
                    possibilities.append(("sp", possibility1, possibility2))
    return possibilities

def top_down_nb(words):
    if debug:
        print((words, "nb"))
    n = len(words)
    possibilities = []
    if n!=1:
        for k in range(1, n):
            for possibility1 in top_down_a(words[0:k]):
                for possibility2 in top_down_nb(words[k:n]):
                    possibilities.append(("nb", possibility1, possibility2))
            for possibility1 in top_down_a(words[0:k]):
                for possibility2 in top_down_n(words[k:n]):
                    possibilities.append(("nb", possibility1, possibility2))
            for possibility1 in top_down_nb(words[0:k]):
                for possibility2 in top_down_pp(words[k:n]):
                    possibilities.append(("nb", possibility1, possibility2))
            for possibility1 in top_down_n(words[0:k]):
                for possibility2 in top_down_pp(words[k:n]):
                    possibilities.append(("nb", possibility1, possibility2))
    return possibilities

def top_down_pp(words):
    if debug:
        print((words, "pp"))
    n = len(words)
    possibilities = []
    if n!=1:
        for k in range(1, n):
            for possibility1 in top_down_p(words[0:k]):
                for possibility2 in top_down_np(words[k:n]):
                    possibilities.append(("pp", possibility1, possibility2))
    return possibilities

def top_down_vp(words):
    if debug:
        print((words, "vp"))
    n = len(words)
    possibilities = []
    if n!=1:
        for k in range(1, n):
            for possibility1 in top_down_v(words[0:k]):
                for possibility2 in top_down_np(words[k:n]):
                    possibilities.append(("vp", possibility1, possibility2))
            for possibility1 in top_down_v(words[0:k]):
                for possibility2 in top_down_pp(words[k:n]):
                    possibilities.append(("vp", possibility1, possibility2))
    return possibilities

def top_down_n(words):
    if debug:
        print((words, "n"))
    n = len(words)
    if n==1:
        if (words[0]=="square" or
            words[0]=="piece" or
            words[0]=="pawn" or
            words[0]=="bishop" or
            words[0]=="knight" or
            words[0]=="rook" or
            words[0]=="queen" or
            words[0]=="king" or
            words[0]=="rank" or
            words[0]=="file" or
            words[0]=="edge" or
            words[0]=="corner"):
            return [("n", words[0])]
    return []

def top_down_a(words):
    if debug:
        print((words, "a"))
    n = len(words)
    if n==1:
        if (words[0]=="black" or words[0]=="white"):
            return [("a", words[0])]
    return []

def top_down_d(words):
    if debug:
        print((words, "d"))
    n = len(words)
    if n==1:
        if (words[0]=="every" or words[0]=="some" or words[0]=="the"):
            return [("d", words[0])]
    return []

def top_down_v(words):
    if debug:
        print((words, "v"))
    n = len(words)
    if n==1:
        if (words[0]=="is"):
            return [("v", words[0])]
    return []

def top_down_p(words):
    if debug:
        print((words, "p"))
    n = len(words)
    if n==1:
        if (words[0]=="of" or words[0]=="on"):
            return [("p", words[0])]
    return []

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

if memoized:
    top_down_s = memoize(top_down_s)
    top_down_np = memoize(top_down_np)
    top_down_nb = memoize(top_down_nb)
    top_down_pp = memoize(top_down_pp)
    top_down_vp = memoize(top_down_vp)
    top_down_n = memoize(top_down_n)
    top_down_a = memoize(top_down_a)
    top_down_d = memoize(top_down_d)
    top_down_v = memoize(top_down_v)
    top_down_p = memoize(top_down_p)

print(top_down_s(("some", "pawn", "is", "on", "some", "square")))

print(top_down_s(("some", "pawn", "is", "on", "some")))

print(top_down_s(("some", "pawn", "is", "on", "some", "square", "square")))

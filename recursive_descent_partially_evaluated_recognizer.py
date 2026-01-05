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

def strip_s(words):
    if debug:
        print((words, "s"))
    if len(words)==0:
        return []
    possibilities = []
    for words_prime in strip_np(words):
        possibilities += strip_vp(words_prime)
    return possibilities

def strip_np(words):
    if debug:
        print((words, "np"))
    if len(words)==0:
        return []
    possibilities = []
    for words_prime in strip_d(words):
        possibilities += strip_nb(words_prime)
    for words_prime in strip_d(words):
        possibilities += strip_n(words_prime)
    return possibilities

def strip_nb(words):
    if debug:
        print((words, "nb"))
    if len(words)==0:
        return []
    possibilities = []
    for words_prime in strip_a(words):
        possibilities += strip_nb(words_prime)
    for words_prime in strip_a(words):
        possibilities += strip_n(words_prime)
    # for words_prime in strip_nb(words):
    #     possibilities += strip_np(words_prime)
    for words_prime in strip_n(words):
        possibilities += strip_np(words_prime)
    return possibilities

def strip_pp(words):
    if debug:
        print((words, "pp"))
    if len(words)==0:
        return []
    possibilities = []
    for words_prime in strip_p(words):
        possibilities += strip_np(words_prime)
    return possibilities

def strip_vp(words):
    if debug:
        print((words, "vp"))
    if len(words)==0:
        return []
    possibilities = []
    for words_prime in strip_v(words):
        possibilities += strip_np(words_prime)
    for words_prime in strip_v(words):
        possibilities += strip_pp(words_prime)
    return possibilities

def strip_n(words):
    if debug:
        print((words, "n"))
    if len(words)==0:
        return []
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
        return [words[1:]]
    return []

def strip_a(words):
    if debug:
        print((words, "a"))
    if len(words)==0:
        return []
    if (words[0]=="black" or words[0]=="white"):
        return [words[1:]]
    return []

def strip_d(words):
    if debug:
        print((words, "d"))
    if len(words)==0:
        return []
    if (words[0]=="every" or words[0]=="some" or words[0]=="the"):
        return [words[1:]]
    return []

def strip_v(words):
    if debug:
        print((words, "v"))
    if len(words)==0:
        return []
    if (words[0]=="is"):
        return [words[1:]]
    return []

def strip_p(words):
    if debug:
        print((words, "p"))
    if len(words)==0:
        return []
    if (words[0]=="of" or words[0]=="on"):
        return [words[1:]]
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
    strip = memoize(strip)

def recursive_descent_s(words):
    return () in strip_s((words))

print(recursive_descent_s(("some", "pawn", "is", "on", "some", "square")))

print(recursive_descent_s(("some", "pawn", "is", "on", "some")))

print(recursive_descent_s(
    ("some", "pawn", "is", "on", "some", "square", "square")))

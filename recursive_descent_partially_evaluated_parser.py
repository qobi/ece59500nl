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
    for possibility1, words_prime1 in strip_np(words):
        for possibility2, words_prime2 in strip_vp(words_prime1):
            possibilities.append((("s", possibility1, possibility2),
                                  words_prime2))
    return possibilities

def strip_np(words):
    if debug:
        print((words, "np"))
    if len(words)==0:
        return []
    possibilities = []
    for possibility1, words_prime1 in strip_d(words):
        for possibility2, words_prime2 in strip_nb(words_prime1):
            possibilities.append((("np", possibility1, possibility2),
                                  words_prime2))
    for possibility1, words_prime1 in strip_d(words):
        for possibility2, words_prime2 in strip_n(words_prime1):
            possibilities.append((("np", possibility1, possibility2),
                                  words_prime2))
    return possibilities

def strip_nb(words):
    if debug:
        print((words, "nb"))
    if len(words)==0:
        return []
    possibilities = []
    for possibility1, words_prime1 in strip_a(words):
        for possibility2, words_prime2 in strip_nb(words_prime1):
            possibilities.append((("nb", possibility1, possibility2),
                                  words_prime2))
    for possibility1, words_prime1 in strip_a(words):
        for possibility2, words_prime2 in strip_n(words_prime1):
            possibilities.append((("nb", possibility1, possibility2),
                                  words_prime2))
    # for possibility1, words_prime1 in strip_nb(words):
    #     for possibility2, words_prime2 in strip_pp(words_prime1):
    #         possibilities.append((("nb", possibility1, possibility2),
    #                               words_prime2))
    for possibility1, words_prime1 in strip_n(words):
        for possibility2, words_prime2 in strip_pp(words_prime1):
            possibilities.append((("nb", possibility1, possibility2),
                                  words_prime2))
    return possibilities

def strip_pp(words):
    if debug:
        print((words, "pp"))
    if len(words)==0:
        return []
    possibilities = []
    for possibility1, words_prime1 in strip_p(words):
        for possibility2, words_prime2 in strip_np(words_prime1):
            possibilities.append((("pp", possibility1, possibility2),
                                  words_prime2))
    return possibilities

def strip_vp(words):
    if debug:
        print((words, "vp"))
    if len(words)==0:
        return []
    possibilities = []
    for possibility1, words_prime1 in strip_v(words):
        for possibility2, words_prime2 in strip_np(words_prime1):
            possibilities.append((("vp", possibility1, possibility2),
                                  words_prime2))
    for possibility1, words_prime1 in strip_v(words):
        for possibility2, words_prime2 in strip_pp(words_prime1):
            possibilities.append((("vp", possibility1, possibility2),
                                  words_prime2))
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
        return [(("n", words[0]), words[1:])]
    return []

def strip_a(words):
    if debug:
        print((words, "a"))
    if len(words)==0:
        return []
    if (words[0]=="black" or words[0]=="white"):
        return [(("a", words[0]), words[1:])]
    return []

def strip_d(words):
    if debug:
        print((words, "d"))
    if len(words)==0:
        return []
    if (words[0]=="every" or words[0]=="some" or words[0]=="the"):
        return [(("d", words[0]), words[1:])]
    return []

def strip_v(words):
    if debug:
        print((words, "v"))
    if len(words)==0:
        return []
    if (words[0]=="is"):
        return [(("v", words[0]), words[1:])]
    return []

def strip_p(words):
    if debug:
        print((words, "p"))
    if len(words)==0:
        return []
    if (words[0]=="of" or words[0]=="on"):
        return [(("p", words[0]), words[1:])]
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
    possibilities = []
    for possibility, words in strip_s(words):
        if len(words)==0:
            possibilities.append(possibility)
    return possibilities

print(recursive_descent_s(("some", "pawn", "is", "on", "some", "square")))

print(recursive_descent_s(("some", "pawn", "is", "on", "some")))

print(recursive_descent_s(
    ("some", "pawn", "is", "on", "some", "square", "square")))

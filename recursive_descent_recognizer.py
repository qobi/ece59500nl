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

lexicon = {"square": set(["n"]),
           "piece": set(["n"]),
           "pawn": set(["n"]),
           "bishop": set(["n"]),
           "knight": set(["n"]),
           "rook": set(["n"]),
           "queen": set(["n"]),
           "king": set(["n"]),
           "rank": set(["n"]),
           "file": set(["n"]),
           "edge": set(["n"]),
           "corner": set(["n"]),
           "black": set(["a"]),
           "white": set(["a"]),
           "every": set(["d"]),
           "some": set(["d"]),
           "the": set(["d"]),
           "is": set(["v"]),
           "of": set(["p"]),
           "on": set(["p"])}

grammar = [("s", "np", "vp"),   # S -> NP VP
           ("np", "d", "nb"),   # NP -> D Nbar
           ("np", "d", "n"),    # NP -> D N
           ("nb", "a", "nb"),   # Nbar -> A Nbar
           ("nb", "a", "n"),    # Nbar -> A N
           #("nb", "nb", "pp"),  # Nbar -> Nbar PP
           ("nb", "n", "pp"),   # Nbar -> N PP
           ("pp", "p", "np"),   # PP -> P NP
           ("vp", "v", "np"),   # VP -> V NP
           ("vp", "v", "pp")]   # VP -> V PP

def strip(args):
    words, category = args
    if debug:
        print((words, category))
    if len(words)==0:
        return []
    possibilities = []
    if category in lexicon[words[0]]:
        possibilities.append(words[1:])
    for A, B, C in grammar:
        if A==category:
            for words_prime in strip((words, B)):
                possibilities += strip((words_prime, C))
    return possibilities

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

def recursive_descent(words, category):
    return () in strip((words, category))

print(recursive_descent(("some", "pawn", "is", "on", "some", "square"), "s"))

print(recursive_descent(("some", "pawn", "is", "on", "some"), "s"))

print(recursive_descent(
    ("some", "pawn", "is", "on", "some", "square", "square"), "s"))

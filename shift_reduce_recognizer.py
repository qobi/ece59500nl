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
           ("nb", "nb", "pp"),  # Nbar -> Nbar PP
           ("nb", "n", "pp"),   # Nbar -> N PP
           ("pp", "p", "np"),   # PP -> P NP
           ("vp", "v", "np"),   # VP -> V NP
           ("vp", "v", "pp")]   # VP -> V PP

def shift(stack, words):
    if len(words)==0:
        return []
    else:
        possibilities = []
        for category in lexicon[words[0]]:
            possibilities += repeat(((category,)+stack, words[1:]))
        return possibilities

def reduce(stack, words):
    possibilities = []
    for A, B, C in grammar:
        if len(stack)>=2 and stack[0]==C and stack[1]==B:
            possibilities += repeat(((A,)+stack[2:], words))
    return possibilities

def repeat(args):
    stack, words = args
    if debug:
        print((stack, words))
    new = shift(stack, words)+reduce(stack, words)
    if len(new)==0:
        return [(stack, words)]
    else:
        return new

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
    repeat = memoize(repeat)

def accept(stack, words, category):
    return len(words)==0 and len(stack)==1 and stack[0]==category

def shift_reduce(words, category):
    for stack, words in repeat(((), words)):
        if accept(stack, words, category):
            return True
    return False

print(shift_reduce(("some", "pawn", "is", "on", "some", "square"), "s"))

print(shift_reduce(("some", "pawn", "is", "on", "some"), "s"))

print(shift_reduce(
    ("some", "pawn", "is", "on", "some", "square", "square"), "s"))

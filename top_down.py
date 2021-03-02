debug = True

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

grammar = [("s", "np", "vp"),
           ("np", "d", "nb"),
           ("np","d", "n"),
           ("nb", "a", "nb"),
           ("nb", "a", "n"),
           ("nb", "n", "pp"),
           ("pp", "p", "np"),
           ("vp", "v", "np"),
           ("vp", "v", "pp")]

def top_down(args):
    words, category = args
    if debug:
        print words, category
    n = len(words)
    if n==1:
        if category in lexicon[words[0]]:
            return True
    else:
        for k in range(1, n):
            for A, B, C in grammar:
                if (A==category and
                    top_down((words[0:k], B)) and
                    top_down((words[k:n], C))):
                    return True
    return False

print top_down((("some", "pawn", "is", "on", "some", "square"), "s"))

print top_down((("some", "pawn", "is", "on", "some"), "s"))

print top_down((("some", "pawn", "is", "on", "some", "square", "square"), "s"))

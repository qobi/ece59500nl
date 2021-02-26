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

# O(n^3)
def cky(words, category):
    n = len(words)              # O(n)
    chart = [[set() for i in range(n+1)] for j in range(n+1)] # O(n^2)
    # O(n)
    for i in range(n):
        word = words[i]
        categories = lexicon[word]
        chart[i][i+1] |= categories
    # O(n^3)
    for l in range(2, n+1):     # O(n)
        for i in range(n-l+1):  # O(n)
            j = i+l
            for k in range(i+1, j): # O(n)
                for A, B, C in grammar:
                    if B in chart[i][k] and C in chart[k][j]:
                        chart[i][j] |= set([A])
    #print chart
    # O(1)
    if category in chart[0][n]:
        return True
    else:
        return False

print cky(("some", "pawn", "is", "on", "some", "square"), "s")

print cky(("some", "pawn", "is", "on", "some"), "s")

print cky(("some", "pawn", "is", "on", "some", "square", "square"), "s")

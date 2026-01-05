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

def cky(words, category):
    n = len(words)                                            # O(1)
    chart = [[set() for i in range(n+1)] for j in range(n+1)] # O(n^2)
    # O(n)
    for i in range(n):                                        # O(n)
        word = words[i]             # O(1)
        categories = lexicon[word]  # O(1)
        chart[i][i+1] |= categories # O(1)
    # O(n^3)
    for l in range(2, n+1):         # O(n)
        for i in range(n-l+1):      # O(n)
            j = i+l
            for k in range(i+1, j): # O(n)
                for A, B, C in grammar: # O(1)
                    if B in chart[i][k] and C in chart[k][j]:
                        chart[i][j] |= set([A])
    #print(chart)
    return category in chart[0][n] # O(1)

print(cky(("some", "pawn", "is", "on", "some", "square"), "s"))

print(cky(("some", "pawn", "is", "on", "some"), "s"))

print(cky(("some", "pawn", "is", "on", "some", "square", "square"), "s"))

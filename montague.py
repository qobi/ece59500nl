objects = ([("square", i, j) for i in range(8) for j in range(8)]+
           [("rank", i) for i in range(8)]+
           [("file", j) for j in range(8)]+
           [("white", "pawn", 0, 3),
            ("black", "bishop", 0, 7),
            ("white", "king", 4, 2),
            ("white", "pawn", 4, 3),
            ("black", "king", 4, 7),
            ("black", "rook", 7, 0),
            ("white", "pawn", 7, 2),
            ("black", "bishop", 7, 7)])

def on(x, y):
    if x[0]=="square" and y[0]=="rank":
        return x[1]==y[1]
    elif x[0]=="square" and y[0]=="file":
        return x[2]==y[1]
    elif (x[0]=="white" or x[0]=="black") and y[0]=="square":
        return x[2]==y[1] and x[3]==y[2]
    elif (x[0]=="white" or x[0]=="black") and y[0]=="rank":
        return x[2]==y[1]
    elif (x[0]=="white" or x[0]=="black") and y[0]=="file":
        return x[3]==y[1]
    # this implements a semantic constraint
    else:
        return None

def of(x, y):
    if x[0]=="square" and y[0]=="rank":
        return x[1]==y[1]
    elif x[0]=="square" and y[0]=="file":
        return x[2]==y[1]
    elif x[0]=="square" and (y[0]=="white" or y[0]=="black"):
        return x[1]==y[2] and x[2]==y[3]
    elif x[0]=="rank" and y[0]=="square":
        return x[1]==y[1]
    elif x[0]=="rank" and (y[0]=="white" or y[0]=="black"):
        return x[1]==y[2]
    elif x[0]=="file" and y[0]=="square":
        return x[1]==y[2]
    elif x[0]=="file" and (y[0]=="white" or y[0]=="black"):
        return x[1]==y[3]
    # this implements a semantic constraint
    else:
        return None

noun = ("object", "->", "boolean")
adjective = (noun, "->", noun)
np = (noun, "->", "boolean")
vp = ("boolean", "<-", np)
determiner = (noun, "->", np)
pp = (noun, "<-", noun)
preposition = (np, "->", pp)
verb_np = (np, "->", vp)
verb_pp = (pp, "->", vp)

lexicon = {
    "square": [(noun, lambda x: x[0]=="square")],
    "piece": [(noun,
              lambda x: (
                  x[1] in
                  ("pawn", "bishop", "knight", "rook", "queen", "king")))],
    "pawn": [(noun, lambda x: x[1]=="pawn")],
    "bishop": [(noun, lambda x: x[1]=="bishop")],
    "knight": [(noun, lambda x: x[1]=="knight")],
    "rook": [(noun, lambda x: x[1]=="rook")],
    "queen": [(noun, lambda x: x[1]=="queen")],
    "king": [(noun, lambda x: x[1]=="king")],
    "rank": [(noun, lambda x: x[0]=="rank")],
    "file": [(noun, lambda x: x[0]=="file")],
    "edge": [(noun, lambda x: ((x[0]=="rank" or x[0]=="file") and
                               (x[1]==0 or x[1]==7)))],
    "corner": [(noun, lambda x: (x[0]=="square" and
                                 (x[1]==0 or x[1]==7) and
                                 (x[2]==0 or x[2]==7)))],
    "black": [(adjective,
               lambda noun:(
                   lambda x: (noun(x) and
                              (True if x[0]=="black"
                            else False if x[0]=="white"
                            else (x[1]+x[2])%2==1 if x[0]=="square"
                               # this implements a semantic constraint
                            else None))))],
    "white": [(adjective,
               lambda noun:(
                   lambda x: (noun(x) and
                              (False if x[0]=="black"
                            else True if x[0]=="white"
                            else (x[1]+x[2])%2==0 if x[0]=="square"
                               # this implements a semantic constraint
                            else None))))],
    "every": [(determiner,
               lambda noun: (
                   lambda noun1: (
                       all(((not noun(x)) or noun1(x)) for x in objects))))],
    "some": [(determiner,
              lambda noun: (
                  lambda noun1: (
                      any((noun(x) and noun1(x)) for x in  objects))))],
    "the": [(determiner,
             lambda noun: (
                 lambda noun1: (
                     (noun1(filter(noun, objects)[0])
                     if len(filter(noun, objects))==1
                      # this implements a semantic constraint
                     else None))))],
    "of": [(preposition,
            lambda np: (
                lambda noun: lambda x: noun(x) and np(lambda y: of(x, y))))],
    "on": [(preposition,
            lambda np: (
                lambda noun: lambda x: noun(x) and np(lambda y: on(x, y))))],
    "is": [(verb_np,
            lambda object_np: (
                lambda subject_np: (
                    subject_np(lambda x: object_np(lambda y: x==y))))),
           (verb_np,
            lambda object_np: (
                lambda subject_np: (
                    object_np(lambda x: subject_np(lambda y: x==y))))),
           (verb_pp,
            lambda object_pp: (
                lambda subject_np: subject_np(object_pp(lambda x: True)))),
           (verb_pp,
            lambda object_pp: (
                lambda subject_np: (
                    subject_np(
                        object_pp(lambda y: subject_np(lambda x: x==y))))))]}

def top_down(words):
    n = len(words)
    if n==1:
        if words[0] in lexicon:
            return lexicon[words[0]]
        else:
            return []
    else:
        results = []
        for k in range(1, n):
            for B, left in top_down(words[0:k]):
                for C, right in top_down(words[k:n]):
                    if (isinstance(B, tuple) and
                        B[1]=="->" and
                        B[0]==C):
                        result = left(right)
                        if result is not None:
                            results.append((B[2], result))
                    if (isinstance(C, tuple) and
                        C[1]=="<-" and
                        C[2]==B):
                        result = right(left)
                        if result is not None:
                            results.append((C[0], result))
        return results

def meaning(words):
    truths = [truth
              for category, truth in top_down(words)
              if category=="boolean"]
    if len(truths)==0:
        return "ungrammatical"
    elif True in truths and False in truths:
        return "ambiguous"
    elif True in truths:
        return True
    elif False in truths:
        return False
    else:
        raise RuntimeError("This shouldn't happen")

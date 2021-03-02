debug = True

def top_down_s(words):
    if debug:
        print words, "s"
    n = len(words)
    if n!=1:
        for k in range(1, n):
            if (top_down_np(words[0:k]) and
                top_down_vp(words[k:n])):
                return True
    return False

def top_down_np(words):
    if debug:
        print words, "np"
    n = len(words)
    if n!=1:
        for k in range(1, n):
            if (top_down_d(words[0:k]) and
                top_down_nb(words[k:n])):
                return True
            if (top_down_d(words[0:k]) and
                top_down_n(words[k:n])):
                return True
    return False

def top_down_nb(words):
    if debug:
        print words, "nb"
    n = len(words)
    if n!=1:
        for k in range(1, n):
            if (top_down_a(words[0:k]) and
                top_down_nb(words[k:n])):
                return True
            if (top_down_a(words[0:k]) and
                top_down_n(words[k:n])):
                return True
            if (top_down_n(words[0:k]) and
                top_down_pp(words[k:n])):
                return True
    return False

def top_down_pp(words):
    if debug:
        print words, "pp"
    n = len(words)
    if n!=1:
        for k in range(1, n):
            if (top_down_p(words[0:k]) and
                top_down_np(words[k:n])):
                return True
    return False

def top_down_vp(words):
    if debug:
        print words, "vp"
    n = len(words)
    if n!=1:
        for k in range(1, n):
            if (top_down_v(words[0:k]) and
                top_down_np(words[k:n])):
                return True
            if (top_down_v(words[0:k]) and
                top_down_pp(words[k:n])):
                return True
    return False

def top_down_n(words):
    if debug:
        print words, "n"
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
            return True
    return False

def top_down_a(words):
    if debug:
        print words, "a"
    n = len(words)
    if n==1:
        if (words[0]=="black" or words[0]=="white"):
            return True
    return False

def top_down_d(words):
    if debug:
        print words, "d"
    n = len(words)
    if n==1:
        if (words[0]=="every" or words[0]=="some" or words[0]=="the"):
            return True
    return False

def top_down_v(words):
    if debug:
        print words, "v"
    n = len(words)
    if n==1:
        if (words[0]=="is"):
            return True
    return False

def top_down_p(words):
    if debug:
        print words, "p"
    n = len(words)
    if n==1:
        if (words[0]=="of" or words[0]=="on"):
            return True
    return False

print top_down_s(("some", "pawn", "is", "on", "some", "square"))

print top_down_s(("some", "pawn", "is", "on", "some"))

print top_down_s(("some", "pawn", "is", "on", "some", "square", "square"))

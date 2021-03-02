debug = True

chart_s = {}

def top_down_s(words):
    if words in chart_s:
        return chart_s[words]
    else:
        if debug:
            print words, "s"
        n = len(words)
        if n!=1:
            for k in range(1, n):
                if (top_down_np(words[0:k]) and
                    top_down_vp(words[k:n])):
                    chart_s[words] = True
                    return True
        chart_s[words] = False
        return False

chart_np = {}

def top_down_np(words):
    if words in chart_np:
        return chart_np[words]
    else:
        if debug:
            print words, "np"
        n = len(words)
        if n!=1:
            for k in range(1, n):
                if (top_down_d(words[0:k]) and
                    top_down_nb(words[k:n])):
                    chart_np[words] = True
                    return True
                if (top_down_d(words[0:k]) and
                    top_down_n(words[k:n])):
                    chart_np[words] = True
                    return True
        chart_np[words] = False
        return False

chart_nb = {}

def top_down_nb(words):
    if words in chart_nb:
        return chart_nb[words]
    else:
        if debug:
            print words, "nb"
        n = len(words)
        if n!=1:
            for k in range(1, n):
                if (top_down_a(words[0:k]) and
                    top_down_nb(words[k:n])):
                    chart_nb[words] = True
                    return True
                if (top_down_a(words[0:k]) and
                    top_down_n(words[k:n])):
                    chart_nb[words] = True
                    return True
                if (top_down_n(words[0:k]) and
                    top_down_pp(words[k:n])):
                    chart_nb[words] = True
                    return True
        chart_nb[words] = False
        return False

chart_pp = {}

def top_down_pp(words):
    if words in chart_pp:
        return chart_pp[words]
    else:
        if debug:
            print words, "pp"
        n = len(words)
        if n!=1:
            for k in range(1, n):
                if (top_down_p(words[0:k]) and
                    top_down_np(words[k:n])):
                    chart_pp[words] = True
                    return True
        chart_pp[words] = False
        return False

chart_vp = {}

def top_down_vp(words):
    if words in chart_vp:
        return chart_vp[words]
    else:
        if debug:
            print words, "vp"
        n = len(words)
        if n!=1:
            for k in range(1, n):
                if (top_down_v(words[0:k]) and
                    top_down_np(words[k:n])):
                    chart_vp[words] = True
                    return True
                if (top_down_v(words[0:k]) and
                    top_down_pp(words[k:n])):
                    chart_vp[words] = True
                    return True
        chart_vp[words] = False
        return False

chart_n = {}

def top_down_n(words):
    if words in chart_n:
        return chart_n[words]
    else:
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
                chart_n[words] = True
                return True
        chart_n[words] = False
        return False

chart_a = {}

def top_down_a(words):
    if words in chart_a:
        return chart_a[words]
    else:
        if debug:
            print words, "a"
        n = len(words)
        if n==1:
            if (words[0]=="black" or words[0]=="white"):
                chart_a[words] = True
                return True
        chart_a[words] = False
        return False

chart_d = {}

def top_down_d(words):
    if words in chart_d:
        return chart_d[words]
    else:
        if debug:
            print words, "d"
        n = len(words)
        if n==1:
            if (words[0]=="every" or words[0]=="some" or words[0]=="the"):
                chart_d[words] = True
                return True
        chart_d[words] = False
        return False

chart_v = {}

def top_down_v(words):
    if words in chart_v:
        return chart_v[words]
    else:
        if debug:
            print words, "v"
        n = len(words)
        if n==1:
            if (words[0]=="is"):
                chart_v[words] = True
                return True
        chart_v[words] = False
        return False

chart_p = {}

def top_down_p(words):
    if words in chart_p:
        return chart_p[words]
    else:
        if debug:
            print words, "p"
        n = len(words)
        if n==1:
            if (words[0]=="of" or words[0]=="on"):
                chart_p[words] = True
                return True
        chart_p[words] = False
        return False

print top_down_s(("some", "pawn", "is", "on", "some", "square"))

print top_down_s(("some", "pawn", "is", "on", "some"))

print top_down_s(("some", "pawn", "is", "on", "some", "square", "square"))

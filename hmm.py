from numpy import sum, array, zeros, ones
from numpy.random import choice, uniform

def check1(w, a, b, c):
    I = len(w)
    J = len(b)
    K = c.shape[1]
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(c.shape)!=2 or c.shape[0]!=J:
        raise RuntimeError("c has wrong shape")
    for wi in w:
        if not type(wi)==int or wi<0 or wi>=K:
            raise RuntimeError("w has bad word")
    return I, J, K

def check(w, a, b, c):
    L = len(w)
    I = [len(w[l]) for l in range(L)]
    Imax = max(I)
    J = len(b)
    K = c.shape[1]
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(c.shape)!=2 or c.shape[0]!=J:
        raise RuntimeError("c has wrong shape")
    for wl in w:
        for wli in wl:
            if not type(wli)==int or wli<0 or wli>=K:
                raise RuntimeError("w has bad word")
    return I, Imax, J, K, L

def sample(a, b, c, I):
    J = len(b)
    K = c.shape[1]
    j = choice(range(J), 1, p=b)[0]
    w = []
    for i in range(1, I+1):
        w.append(int(choice(range(K), 1, p=c[j, :])[0]))
        j = choice(range(J), 1, p=a[j, :])[0]
    return w

def samples(a, b, c, I, L):
    return [sample(a, b, c, I) for l in range(L)]

def state_sequence_probability(w, t, a, b, c):
    I, _, _ = check1(w, a, b, c)
    p = b[t[0]]*c[t[0], w[0]]
    for i in range(1, I):
        p *= a[t[i-1], t[i]]*c[t[i], w[i]]
    return p

def viterbi(w, a, b, c):
    I, J, _= check1(w, a, b, c)
    delta = zeros([I, J])
    index = zeros([I, J], dtype=int)
    best_state = zeros([I], dtype=int)
    for j in range(J):
        delta[0, j] = b[j]*c[j, w[0]]
    for i in range(1, I):
        for j in range(J):
            previous = -1
            for j_prime in range(J):
                this = delta[i-1, j_prime]*a[j_prime, j]
                if this>=delta[i, j]:
                    delta[i, j] = this
                    previous = j_prime
            index[i, j] = previous
            delta[i, j] *= c[j, w[i]]
    best = 0
    best_index = -1
    for j in range(J):
        this = delta[I-1, j]
        if this>=best:
            best = this
            best_index = j
    for i in range(I-1, -1, -1):
        best_state[i] = best_index
        best_index = index[i, best_index]
    return best, best_state

def calculate_alpha(w, a, b, c):
    I, Imax, J, _, L = check(w, a, b, c)
    alpha = zeros([L, Imax, J])
    for l in range(L):
        for j in range(J):
            alpha[l, 0, j] = b[j]*c[j, w[l][0]]
        for i in range(1, I[l]):
            for j in range(J):
                for j_prime in range(J):
                    alpha[l, i, j] += alpha[l, i-1, j_prime]*a[j_prime, j]
                alpha[l, i, j] *= c[j, w[l][i]]
    return alpha

def calculate_beta(w, a, b, c):
    I, Imax, J, _, L = check(w, a, b, c)
    beta = zeros([L, Imax, J])
    for l in range(L):
        for j in range(J):
            beta[l, I[l]-1, j] = 1
        for i in range(I[l]-2, -1, -1):
            for j in range(J):
                for j_prime in range(J):
                    beta[l, i, j] += (a[j, j_prime]*
                                      c[j_prime, w[l][i+1]]*
                                      beta[l, i+1, j_prime])
    return beta

def e_step(w, a, b, c):
    I, Imax, J, _, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    beta = calculate_beta(w, a, b, c)
    gamma = zeros([L, Imax, J])
    psi = zeros([L, Imax-1, J, J])
    for l in range(L):
        likelihood = 0
        for j in range(J):
            likelihood += alpha[l, I[l]-1, j]
        for i in range(I[l]):
            for j in range(J):
                gamma[l, i, j] = alpha[l, i, j]*beta[l, i, j]/likelihood
        for i in range(I[l]-1):
            for j in range(J):
                for j_prime in range(J):
                    psi[l, i, j, j_prime] = (
                        alpha[l, i, j]*
                        a[j, j_prime]*
                        c[j_prime, w[l][i+1]]*
                        beta[l, i+1, j_prime]/
                        likelihood)
    return gamma, psi

def normalize(a, b, c):
    J = len(b)
    for j in range(J):
        a[j, :] /= sum(a[j, :])
        c[j, :] /= sum(c[j, :])
    b /= sum(b)

def m_step(w, gamma, psi):
    J = gamma.shape[2]
    K = 0
    L = len(w)
    for wl in w:
        for wli in wl:
            if not type(wli)==int:
                raise RuntimeError("w has bad word")
            K = max(K, wli+1)
    a = zeros([J, J])
    b = zeros([J])
    c = zeros([J, K])
    for j in range(J):
        for j_prime in range(J):
            for l in range(L):
                for i in range(len(w[l])-1):
                    a[j, j_prime] += psi[l, i, j, j_prime]
        for l in range(L):
            b[j] += gamma[l, 0, j]
        for k in range(K):
            for l in range(L):
                for i in range(len(w[l])):
                    if w[l][i]==k:
                        c[j, k] += gamma[l, i, j]
    normalize(a, b, c)
    return a, b, c

def likelihood(w, a, b, c):
    I, _, J, _, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    p = 1
    for l in range(L):
        pl = 0
        for j in range(J):
            pl += alpha[l, I[l]-1, j]
        p *= pl
    return p

def alternate_likelihood(w, a, b, c):
    _, _, J, _, L = check(w, a, b, c)
    beta = calculate_beta(w, a, b, c)
    p = 1
    for l in range(L):
        pl = 0
        for j in range(J):
            pl += b[j]*c[j, w[l][0]]*beta[l, 0, j]
        p *= pl
    return p

def uniform_model(J, K):
    a = ones([J, J])
    b = ones([J])
    c = ones([J, K])
    normalize(a, b, c)
    return a, b, c

def sequence(J, K):
    a = zeros([J, J])
    b = zeros([J])
    c = ones([J, K])
    for j in range(J):
        # allow to stay in same state
        a[j, j] = 1
        # all except last state can transition to next state
        if j!=J-1:
            a[j, j+1] = 1
    # start in first state
    b[0] = 1
    normalize(a, b, c)
    return a, b, c

def random_model(J, K):
    a = array([[uniform(0, 1) for _ in range(J)] for _ in range(J)])
    b = array([uniform(0, 1) for _ in range(J)])
    c = array([[uniform(0, 1) for _ in range(K)] for _ in range(J)])
    normalize(a, b, c)
    return a, b, c

def baum_welch_step(w, a, b, c):
    gamma, psi = e_step(w, a, b, c)
    a, b, c = m_step(w, gamma, psi)
    return a, b, c

def baum_welch(w, J, K):
    a, b, c = random_model(J, K)
    p = likelihood(w, a, b, c)
    print(p)
    while True:
        a, b, c = baum_welch_step(w, a, b, c)
        new_p = likelihood(w, a, b, c)
        print(new_p)
        if new_p<=p:
            return a, b, c
        p = new_p

def model():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    c = array([[1, 0], [0, 1]])
    return a, b, c

def model2():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    c = array([[0.5, 0.5], [0.5, 0.5]])
    return a, b, c

def model3():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    c = array([[0.75, 0.25], [0.25, 0.75]])
    return a, b, c

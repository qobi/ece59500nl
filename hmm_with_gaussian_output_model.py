from numpy.linalg import inv, det
from numpy import pi, sqrt, exp, dot, sum, outer, array, zeros, eye
from numpy.random import choice, multivariate_normal, uniform

def check1(w, a, b, means, variances):
    I = len(w)
    J = len(b)
    K = len(w[0][0])
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(means.shape)!=2 or means.shape[0]!=J or means.shape[1]!=K:
        raise RuntimeError("means has wrong shape")
    for wi in w:
        if len(wi)!=K:
            raise RuntimeError("w has bad word")
    return I, J, K

def check(w, a, b, means, variances):
    L = len(w)
    I = [len(w[l]) for l in range(L)]
    Imax = max(I)
    J = len(b)
    K = len(w[0][0])
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(means.shape)!=2 or means.shape[0]!=J or means.shape[1]!=K:
        raise RuntimeError("means has wrong shape")
    for wl in w:
        for wli in wl:
            if len(wli)!=K:
                raise RuntimeError("w has bad word")
    return I, Imax, J, K, L

def sample(a, b, means, variances, I):
    J = len(b)
    K = means.shape[1]
    j = choice(range(J), 1, p=b)[0]
    w = []
    for i in range(1, I+1):
        w.append(multivariate_normal(means[j], variances[j]))
        j = choice(range(J), 1, p=a[j, :])[0]
    return w

def samples(a, b, means, variances, I, L):
    return [sample(a, b, means, variances, I) for l in range(L)]

def distance(x, mean, variance):
    return dot((x-mean), dot(inv(variance), (x-mean)))

def gaussian(x, mean, variance):
    coefficient = 1/sqrt((2*pi)**len(x)*det(variance))
    return coefficient*exp(-0.5*distance(x, mean, variance))

def state_sequence_probability(w, t, a, b, means, variances):
    I, _, _ = check1(w, a, b, means, variances)
    p = b[t[0]]*gaussian(w[0], means[t[0]], variances[t[0]])
    for i in range(1, I):
        p *= a[t[i-1], t[i]]*gaussian(w[i], means[t[i]], variances[t[i]])
    return p

def viterbi(w, a, b, means, variances):
    I, J, _= check1(w, a, b, means, variances)
    delta = zeros([I, J])
    index = zeros([I, J], dtype=int)
    best_state = zeros([I], dtype=int)
    for j in range(J):
        delta[0, j] = b[j]*gaussian(w[0], means[j], variances[j])
    for i in range(1, I):
        for j in range(J):
            previous = -1
            for j_prime in range(J):
                this = delta[i-1, j_prime]*a[j_prime, j]
                if this>=delta[i, j]:
                    delta[i, j] = this
                    previous = j_prime
            index[i, j] = previous
            delta[i, j] *= gaussian(w[i], means[j], variances[j])
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

def calculate_alpha(w, a, b, means, variances):
    I, Imax, J, _, L = check(w, a, b, means, variances)
    alpha = zeros([L, Imax, J])
    for l in range(L):
        for j in range(J):
            alpha[l, 0, j] = b[j]*gaussian(w[l][0], means[j], variances[j])
        for i in range(1, I[l]):
            for j in range(J):
                for j_prime in range(J):
                    alpha[l, i, j] += alpha[l, i-1, j_prime]*a[j_prime, j]
                alpha[l, i, j] *= gaussian(w[l][i], means[j], variances[j])
    return alpha

def calculate_beta(w, a, b, means, variances):
    I, Imax, J, _, L = check(w, a, b, means, variances)
    beta = zeros([L, Imax, J])
    for l in range(L):
        for j in range(J):
            beta[l, I[l]-1, j] = 1
        for i in range(I[l]-2, -1, -1):
            for j in range(J):
                for j_prime in range(J):
                    beta[l, i, j] += (
                        a[j, j_prime]*
                        gaussian(w[l][i+1], means[j_prime], variances[j_prime])*
                        beta[l, i+1, j_prime])
    return beta

def e_step(w, a, b, means, variances):
    I, Imax, J, _, L = check(w, a, b, means, variances)
    alpha = calculate_alpha(w, a, b, means, variances)
    beta = calculate_beta(w, a, b, means, variances)
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
                        gaussian(w[l][i+1], means[j_prime], variances[j_prime])*
                        beta[l, i+1, j_prime]/
                        likelihood)
    return gamma, psi

def normalize(a, b):
    J = len(b)
    for j in range(J):
        a[j, :] /= sum(a[j, :])
    b /= sum(b)

def m_step(w, gamma, psi):
    J = gamma.shape[2]
    K = len(w[0][0])
    L = len(w)
    for wl in w:
        for wli in wl:
            if len(wli)!=K:
                raise RuntimeError("w has bad word")
    a = zeros([J, J])
    b = zeros([J])
    means = zeros([J, K])
    variances = zeros([J, K, K])
    for j in range(J):
        for j_prime in range(J):
            for l in range(L):
                for i in range(len(w[l])-1):
                    a[j, j_prime] += psi[l, i, j, j_prime]
        for l in range(L):
            b[j] += gamma[l, 0, j]
        for l in range(L):
            for i in range(len(w[l])):
                means[j, :] += gamma[l, i, j]*w[l][i]
        means[j, :] /= sum(gamma[:, :, j])
        for l in range(L):
            for i in range(len(w[l])):
                point = w[l][i]-means[j, :]
                variances[j, :] += gamma[l, i, j]*outer(point, point)
        variances[j, :] /= sum(gamma[:, :, j])
    normalize(a, b)
    return a, b, means, variances

def likelihood(w, a, b, means, variances):
    I, _, J, _, L = check(w, a, b, means, variances)
    alpha = calculate_alpha(w, a, b, means, variances)
    p = 1
    for l in range(L):
        pl = 0
        for j in range(J):
            pl += alpha[l, I[l]-1, j]
        p *= pl
    return p

def alternate_likelihood(w, a, b, means, variances):
    _, _, J, _, L = check(w, a, b, means, variances)
    beta = calculate_beta(w, a, b, means, variances)
    p = 1
    for l in range(L):
        pl = 0
        for j in range(J):
            pl += b[j]*gaussian(w[l][0], means[j], variances[j])*beta[l, 0, j]
        p *= pl
    return p

def uniform_model(J, K):
    a = ones([J, J])
    b = ones([J])
    means = zeros([J, K])
    variances = array([eye(K) for _ in range(J)])
    normalize(a, b)
    return a, b, means, variances

def sequence(J, K):
    a = zeros([J, J])
    b = zeros([J])
    means = zeros([J, K])
    variances = array([eye(K) for _ in range(J)])
    for j in range(J):
        # allow to stay in same state
        a[j, j] = 1
        # all except last state can transition to next state
        if j!=J-1:
            a[j, j+1] = 1
    # start in first state
    b[0] = 1
    normalize(a, b)
    return a, b, means, variances

def random_model(J, K):
    a = array([[uniform(0, 1) for _ in range(J)] for _ in range(J)])
    b = array([uniform(0, 1) for _ in range(J)])
    means = zeros([J, K])
    variances = array([eye(K) for _ in range(J)])
    normalize(a, b)
    return a, b, means, variances

def baum_welch_step(w, a, b, means, variances):
    gamma, psi = e_step(w, a, b, means, variances)
    a, b, means, variances = m_step(w, gamma, psi)
    return a, b, means, variances

def baum_welch(w, J, K):
    a, b, means, variances = random_model(J, K)
    p = likelihood(w, a, b, means, variances)
    print(p)
    while True:
        a, b, means, variances = baum_welch_step(w, a, b, means, variances)
        new_p = likelihood(w, a, b, means, variances)
        print(new_p)
        if new_p<=p:
            return a, b, means, variances
        p = new_p

def model():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    means = array([[0, 0], [1, 1]])
    variances = array([[[1, 0], [0, 1]], [[1, 0], [0, 1]]])
    return a, b, means, variances

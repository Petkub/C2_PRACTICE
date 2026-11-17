# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200011)
MAXN, MAXL, MAXC = 200_000, 1000, 1000
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] (1 <= i < n) is a node in 0..i-1; node 0 is the root"""
    par = [-1] * n
    h = max(1, n // 2)
    s = max(1, int(n ** 0.5))
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # long and thin, short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "spider":                  # about sqrt(n) legs of length about sqrt(n) at the root
            par[i] = 0 if (i - 1) % s == 0 else i - 1
        elif kind == "twopaths":                # two long chains below the root
            par[i] = 0 if i <= 2 else i - 2
        elif kind == "midstar":                 # a path whose middle node has many leaves
            par[i] = i - 1 if i < h else h // 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    """a random numbering 1..n of the nodes 0..n-1 (node 0 gets root if given)"""
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def edge_list(par, lab):
    """edges (lab[u], lab[v]) of the tree in random order and orientation"""
    r = _rnd
    es = [(lab[par[i]], lab[i]) if r() < 0.5 else (lab[i], lab[par[i]]) for i in range(1, len(par))]
    shuf(es)
    return es


def shape_ok(par, lab):
    """par[i] < i for every node and lab is a numbering 1..n: the edges form a tree"""
    n = len(par)
    return (par[0] == -1 and all(0 <= par[i] < i for i in range(1, n))
            and len(set(lab)) == n and min(lab) == 1 and max(lab) == n)


def is_tree(n, es):
    if len(es) != n - 1:
        return False
    d = list(range(n + 1))

    def find(x):
        while d[x] != x:
            d[x] = d[d[x]]
            x = d[x]
        return x
    for u, v in es:
        if not (1 <= u <= n and 1 <= v <= n and u != v):
            return False
        a, b = find(u), find(v)
        if a == b:
            return False
        d[a] = b
    return True


def add(c, p, l, checked=False):
    """c = [c_1..c_N], p = [p_2..p_N], l = [l_2..l_N]"""
    n = len(c)
    assert 1 <= n <= MAXN and len(p) == n - 1 and len(l) == n - 1
    assert 1 <= min(c) and max(c) <= MAXC
    assert n == 1 or (1 <= min(l) and max(l) <= MAXL)
    assert checked or is_tree(n, [(i + 2, p[i]) for i in range(n - 1)])
    tests.append(f"{n}\n" + " ".join(map(str, c)) + "\n" + "".join(f"{p[i]} {l[i]}\n" for i in range(n - 1)))


def bushes_shape(n, k):
    """a random tree on n // (k + 1) nodes, each node with about k extra leaves"""
    m = max(1, n // (k + 1))
    par = [-1] + [int(_rnd() * i) for i in range(1, m)]
    while len(par) < n:
        par.append(ri(0, m - 1))
    return par


def build(n, kind, cval, lval, k=0, top=0):
    """cval(i, depth) and lval(i, depth) for the i-th created house; node 0 is house 1;
    top > 0: a chain of top houses from house 1, the shape of n - top houses below its end"""
    m = n - top
    sub = bushes_shape(m, k) if kind == "bushes" else shape(m, kind)
    par = [i - 1 for i in range(top)] + [top - 1 if j == 0 else top + sub[j] for j in range(m)]
    par[0] = -1
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n, root=1)
    assert shape_ok(par, lab)
    c = [0] * (n + 1)
    p = [0] * (n + 1)
    l = [0] * (n + 1)
    for i in range(n):
        c[lab[i]] = cval(i, dep[i])
        if i:
            p[lab[i]] = lab[par[i]]
            l[lab[i]] = lval(i, dep[i])
    add(c[1:], p[2:], l[2:], checked=True)


def uni(lo, hi):
    return lambda i, d: ri(lo, hi)


def skew(i, d):
    """mostly small with a few large values: neither the shortest nor the heaviest branch is always first"""
    return ri(1, 10) if _rnd() < 0.7 else ri(300, 1000)


# samples
add([4, 5, 1, 2, 3], [1, 1, 3, 3], [3, 1, 2, 1])
add([1, 1, 1], [1, 1], [10, 1])
add([7], [], [])
add([1, 3, 1, 1, 8], [1, 1, 3, 3], [2, 1, 1, 5])
add([2, 1, 4, 6, 1, 3, 5], [1, 2, 1, 3, 1, 6], [4, 1, 2, 3, 1, 2])
# hidden: small
add([MAXC, MAXC], [1], [MAXL])
build(6, "star", skew, skew)
build(8, "random", skew, skew)
build(9, "random", uni(1, 5), uni(1, 5))
build(9, "binary", skew, uni(1, 3))
build(200, "random", skew, skew)
build(2000, "deep", skew, skew)
build(3000, "binary", uni(1, MAXC), uni(1, MAXL))
build(3000, "random", skew, skew)
# hidden: maximum size (all but the path hang below a chain of 50 000 to 60 000 houses)
N = MAXN


def T():
    return ri(50_000, 60_000)


build(N, "star", skew, skew, 0, T())
build(N, "path", uni(MAXC, MAXC), uni(MAXL, MAXL))     # the largest answer
build(N, "random", skew, skew, 0, T())
build(N, "random", uni(1, MAXC), uni(1, MAXL), 0, T())
build(N, "bushes", skew, skew, 50, T())
build(N, "bushes", uni(1, MAXC), skew, 7, T())
build(N, "cater", skew, skew, 0, T())
build(N, "spider", skew, skew, 0, T())
build(N, "binary", skew, skew, 0, T())
build(N, "deep", skew, skew, 0, T())

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

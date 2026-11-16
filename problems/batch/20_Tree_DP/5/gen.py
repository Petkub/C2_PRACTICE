# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200005)
MAXN, MAXV = 5000, 5000
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


def add(p, rg, checked=False):
    """p = [p_2, ..., p_N], rg = [(l_1, r_1), ...]"""
    n = len(rg)
    assert 1 <= n <= MAXN and len(p) == n - 1
    assert all(1 <= l <= r <= MAXV for l, r in rg)
    assert checked or is_tree(n, [(i + 2, p[i]) for i in range(n - 1)])
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n" + "".join(f"{l} {r}\n" for l, r in rg))


def build(n, kind, rng):
    """rng(i, depth) gives (l, r) of the i-th created node; node 0 is employee 1"""
    par = shape(n, kind)
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n, root=1)
    p = [0] * (n + 1)
    rg = [None] * (n + 1)
    for i in range(n):
        rg[lab[i]] = rng(i, dep[i])
        if i:
            p[lab[i]] = lab[par[i]]
    assert shape_ok(par, lab)
    add(p[2:], rg[1:], checked=True)


def wide(i, d):
    return (ri(1, 50), ri(MAXV - 50, MAXV))


def full(i, d):
    return (1, MAXV)


def sub(lo, hi):
    def f(i, d):
        a, b = ri(lo, hi), ri(lo, hi)
        return (min(a, b), max(a, b))
    return f


def falling(i, d):
    """deeper employees get lower ranges, overlapping their bosses' ranges"""
    top = max(1, MAXV - d * 3)
    return (max(1, top - ri(500, 3000)), top)


# samples
add([1, 1, 2], [(2, 3), (1, 3), (2, 2), (1, 2)])
add([1], [(1, 2), (3, 4)])
add([], [(1, 5000)])
add([1, 2], [(1, 3), (1, 3), (1, 3)])
add([1, 2, 3, 4, 5], [(1, 5000)] * 6)
# hidden: small
add([1, 1], [(5000, 5000), (5000, 5000), (1, 5000)])
build(5, "random", sub(1, 4))
build(7, "deep", sub(1, 3))
build(8, "random", sub(1, 5))
build(30, "random", falling)
build(200, "binary", sub(1, 300))
build(500, "spider", wide)
build(1000, "random", sub(2000, 2100))          # many zero factors
# hidden: maximum size
N = MAXN
build(N, "path", full)
build(N, "path", wide)
build(N, "path", falling)
build(N, "star", full)
build(N, "random", wide)
build(N, "random", falling)
build(N, "binary", full)
build(N, "deep", wide)
build(N, "cater", full)
build(N, "spider", falling)
build(N, "broom", wide)
build(N, "random", sub(1, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

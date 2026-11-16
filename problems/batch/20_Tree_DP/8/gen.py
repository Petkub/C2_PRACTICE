# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(200008)
MAXN = 200_000
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


def add(n, es, checked=False):
    assert 1 <= n <= MAXN
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind):
    par = shape(n, kind)
    lab = labels(n)
    assert shape_ok(par, lab)
    add(n, edge_list(par, lab), checked=True)


def comb(n, legs, leg):
    """a path of n - legs * leg nodes, with `legs` paths of `leg` nodes hanging at random spine nodes"""
    spine = n - legs * leg
    par = [-1] + [i - 1 for i in range(1, spine)]
    for _ in range(legs):
        at = ri(0, spine - 1)
        for j in range(leg):
            par.append(at if j == 0 else len(par) - 1)
    lab = labels(n)
    assert shape_ok(par, lab)
    add(n, edge_list(par, lab), checked=True)


def bushes(n, k):
    """a random tree on n // (k + 1) nodes, each node with k extra leaves: many equally good partners"""
    m = n // (k + 1)
    par = [-1] + [int(_rnd() * i) for i in range(1, m)]
    while len(par) < n:
        par.append(ri(0, m - 1))
    lab = labels(n)
    assert shape_ok(par, lab)
    add(n, edge_list(par, lab), checked=True)


# samples
add(8, [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (6, 7), (6, 8)])
add(3, [(1, 2), (2, 3)])
add(1, [])
add(5, [(1, 2), (1, 3), (1, 4), (1, 5)])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5)])
add(10, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8), (7, 9), (9, 10)])
# hidden: small
add(2, [(2, 1)])
build(9, "random")
build(13, "random")
build(16, "deep")
build(20, "cater")
build(20, "binary")
build(400, "random")
build(3000, "spider")
bushes(3000, 2)
# hidden: maximum size
N = MAXN
build(N, "path")
build(N - 1, "path")
build(N, "star")
build(N, "random")
build(N, "deep")
build(N, "binary")
build(N, "spider")
build(N, "broom")
comb(N, 60000, 2)
bushes(N, 2)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

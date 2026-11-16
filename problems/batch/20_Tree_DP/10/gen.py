# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200010)
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


def add(D, n, es, checked=False):
    assert 1 <= n <= MAXN and 0 <= D <= n - 1
    assert checked or is_tree(n, es)
    tests.append(f"{n} {D}\n" + "".join(f"{u} {v}\n" for u, v in es))


def legs_shape(n, leg):
    """many legs of length `leg` hanging from a short random core"""
    core = max(1, n // (leg * 20))
    par = [-1] + [int(_rnd() * i) for i in range(1, core)]
    while len(par) < n:
        i = len(par)
        if (i - core) % leg == 0:
            par.append(ri(0, core - 1))
        else:
            par.append(i - 1)
    return par


def build(n, D, kind, leg=0):
    par = legs_shape(n, leg) if kind == "legs" else shape(n, kind)
    lab = labels(n)
    assert shape_ok(par, lab)
    add(D, n, edge_list(par, lab), checked=True)


# samples
add(2, 7, [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7)])
add(1, 4, [(1, 2), (2, 3), (3, 4)])
add(0, 3, [(2, 1), (3, 2)])
add(2, 6, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])
add(3, 10, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (1, 7), (7, 8), (8, 9), (8, 10)])
# hidden: small
add(0, 1, [])
build(8, 1, "random")
build(12, 3, "random")
build(14, 2, "cater")
build(16, 4, "deep")
build(16, 5, "binary")
build(300, 6, "random")
build(2000, 40, "legs", 15)
build(2000, 300, "deep")
build(2000, 1999, "random")                   # nothing to remove
# hidden: maximum size
N = MAXN
build(N, 50_000, "path")
build(N, 1, "path")
build(N, 30_000, "deep")
build(N, 70_000, "twopaths")
build(N, 60_000, "broom")
build(N, 20_000, "cater")
build(N, 3_000, "legs", 2000)
build(N, 10, "random")
build(N, 2, "random")
build(N, 10_000, "deep")
build(N, 12, "binary")
build(N, 15_000, "legs", 20_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

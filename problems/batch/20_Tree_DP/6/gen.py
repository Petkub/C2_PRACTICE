# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200006)
MAXN, MAXW = 100_000, 10**9
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


def add(w, es, checked=False):
    n = len(w)
    assert 1 <= n <= MAXN and 1 <= min(w) and max(w) <= MAXW
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + " ".join(map(str, w)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind, val, hub=0):
    """val(i, depth, children) gives the value of the i-th created node;
    hub > 0: the shape gets n - hub nodes and a random node of it gets hub more leaves"""
    par = shape(n - hub, kind)
    at = ri(0, n - hub - 1)
    par += [at] * hub
    dep = [0] * n
    nch = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
        nch[par[i]] += 1
    lab = labels(n)
    w = [0] * n
    for i in range(n):
        w[lab[i] - 1] = val(i, dep[i], nch[i])
    assert shape_ok(par, lab)
    add(w, edge_list(par, lab), checked=True)


def uni(lo, hi):
    return lambda i, d, k: ri(lo, hi)


def leafy(i, d, k):
    """leaves are worth a lot: the plain independent set would take many siblings"""
    return ri(MAXW // 2, MAXW) if k == 0 else ri(1, MAXW // 3)


def lvl(i, d, k):
    return ri(MAXW // 2, MAXW) if d % 2 == 0 else ri(1, 1000)


# samples
add([4, 3, 5, 6, 2, 1, 7], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7)])
add([1, 5, 6, 7], [(1, 2), (1, 3), (1, 4)])
add([8], [])
add([5, 1, 1, 5, 1, 1, 5], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
add([2, 9, 3, 4, 8, 1, 6, 5], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)])
# hidden: small
add([MAXW, MAXW], [(1, 2)])
build(9, "random", uni(1, 10))
build(13, "random", leafy)
build(16, "deep", uni(1, 20))
build(20, "cater", leafy)
build(300, "random", uni(1, 100))
build(2000, "binary", lvl)
build(8000, "spider", leafy)
build(20000, "random", uni(1, MAXW))
# hidden: maximum size (every one has a node of degree >= 70 000)
N = MAXN


def H():
    return ri(72_000, 78_000)


build(N, "path", uni(MAXW, MAXW), H())          # the largest answer
build(N, "path", uni(1, MAXW), H())
build(N, "star", leafy)
build(N, "random", uni(1, MAXW), H())
build(N, "random", leafy, H())
build(N, "binary", lvl, H())
build(N, "binary", leafy, H())
build(N, "cater", leafy, H())
build(N, "deep", uni(1, MAXW), H())
build(N, "spider", lvl, H())
build(N, "broom", leafy, H())
build(N, "midstar", uni(1, MAXW), H())

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

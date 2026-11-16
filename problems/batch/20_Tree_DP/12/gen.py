# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200012)
MAXN, MAXW = 5000, 100_000
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
            and sorted(lab) == list(range(1, n + 1)))


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


def add(K, n, es, checked=False):
    """es = [(u, v, w), ...]"""
    assert 2 <= n <= MAXN and 1 <= K <= n - 1
    assert all(1 <= w <= MAXW for _, _, w in es)
    assert checked or is_tree(n, [(u, v) for u, v, _ in es])
    tests.append(f"{n} {K}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in es))


def blocks_shape(n, k):
    """the root has many children, each heading a block of about k nodes"""
    par = [-1]
    for i in range(1, n):
        j = (i - 1) % k
        par.append(0 if j == 0 else i - ri(1, min(j, 3)))
    return par


def hubs_shape(n, m):
    """a path of m nodes; every other node is a leaf of one of three hubs on the path"""
    par = [-1] + [i - 1 for i in range(1, m)]
    hubs = [0, m // 2, m - 1]
    while len(par) < n:
        par.append(hubs[ri(0, 2)])
    return par


def build(n, K, kind, wval, k=0):
    par = blocks_shape(n, k) if kind == "blocks" else hubs_shape(n, k) if kind == "hubs" else shape(n, kind)
    lab = labels(n)
    assert shape_ok(par, lab)
    es = [(u, v, wval()) for u, v in edge_list(par, lab)]
    add(K, n, es, checked=True)


def uni(lo, hi):
    return lambda: ri(lo, hi)


def skew():
    return ri(1, 10) if _rnd() < 0.8 else ri(MAXW // 2, MAXW)


# samples
add(2, 5, [(1, 2, 1), (2, 3, 2), (2, 4, 1), (4, 5, 3)])
add(1, 3, [(1, 2, 5), (2, 3, 1)])
add(1, 2, [(2, 1, 7)])
add(3, 6, [(1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 1)])
add(4, 8, [(1, 2, 3), (2, 3, 1), (3, 4, 4), (2, 5, 2), (5, 6, 1), (1, 7, 5), (7, 8, 2)])
# hidden: small
add(1, 2, [(1, 2, MAXW)])
build(8, 3, "random", uni(1, 10))
build(10, 5, "random", skew)
build(12, 4, "deep", uni(1, 5))
build(14, 7, "cater", skew)
build(15, 2, "binary", uni(1, 100))
build(300, 120, "random", skew)
build(800, 400, "blocks", uni(1, MAXW), 40)
build(1500, 300, "deep", skew)
# hidden: maximum size
N = MAXN
build(N, N // 2, "path", uni(MAXW, MAXW))           # the largest answer
build(N, N // 2, "blocks", uni(1, MAXW), 300)       # worst case for the merging work
build(N, 2000, "blocks", skew, 120)
build(N, N // 2, "random", uni(1, MAXW))
build(N, 1700, "random", skew)
build(N, N - 1, "random", uni(1, MAXW))
build(N, 1, "random", uni(1, MAXW))
build(N, N // 2, "star", uni(1, MAXW))
build(N, 2400, "binary", skew)
build(N, 2600, "deep", uni(1, MAXW))
build(N, N // 3, "cater", skew)
build(N, N // 2, "spider", uni(1, MAXW))
build(N, 2200, "broom", skew)
build(N, 2000, "midstar", uni(1, MAXW))
build(N, 1200, "star", skew)
build(N, N // 2, "hubs", uni(1, MAXW), 600)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

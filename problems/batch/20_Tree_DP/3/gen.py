# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200003)
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


def add(p, d, checked=False):
    """p = [p_2, ..., p_N], d = [d_1, ..., d_N]"""
    n = len(d)
    assert 1 <= n <= MAXN and len(p) == n - 1
    assert 1 <= min(d) and max(d) <= n
    assert checked or is_tree(n, [(i + 2, p[i]) for i in range(n - 1)])       # connected, so every chain reaches 1
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n" + " ".join(map(str, d)) + "\n")


def build(n, kind, dval, top=0):
    """dval(i, depth, n) gives d of the i-th created node; node 0 is employee 1;
    top > 0: a chain of top employees (d between n / 2 and n) on top, the shape of n - top nodes below it"""
    m = n - top
    sub = shape(m, kind)
    par = [i - 1 for i in range(top)] + [top - 1 if j == 0 else top + sub[j] for j in range(m)]
    par[0] = -1
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n, root=1)
    p = [0] * (n + 1)
    d = [0] * (n + 1)
    for i in range(n):
        d[lab[i]] = ri(n // 2, n) if i < top else dval(i - top, dep[i] - top, n)
        if i:
            p[lab[i]] = lab[par[i]]
    assert shape_ok(par, lab)
    add(p[2:], d[1:], checked=True)


def small_d(i, dep, n):
    return ri(1, min(3, n))


def big_d(i, dep, n):
    return ri(n // 2, n)


def mixed(i, dep, n):
    r = _rnd()
    return ri(1, min(2, n)) if r < 0.6 else ri(1, min(20, n)) if r < 0.9 else ri(1, n)


# samples
add([1, 2, 3, 1, 5], [2, 2, 1, 1, 1, 1])
add([1, 2], [1, 1, 1])
add([1, 1, 1, 1], [1, 4, 2, 3, 5])
add([1, 2, 3, 4, 5, 6], [3, 1, 1, 2, 1, 1, 1])
add([1, 1, 2, 2, 3, 5, 5], [1, 2, 1, 1, 2, 1, 1, 1])
# hidden: small
add([], [1])
build(9, "random", small_d)
build(12, "deep", mixed)
build(40, "random", mixed)
build(300, "binary", small_d)
build(3000, "cater", mixed)
build(20000, "random", small_d)
build(20000, "path", lambda i, dep, n: n if i % 7 == 3 else 1)
# hidden: maximum size
N = MAXN
T = 80_000                                                  # a long chain of bosses above the shape
build(N, "path", lambda i, dep, n: n)                      # only the last employee loses, and it is far away
build(N, "path", lambda i, dep, n: n if i % 7 == 3 else 1, T)
build(N, "path", lambda i, dep, n: 2, T)
build(N, "deep", big_d, T)
build(N, "deep", mixed, T)
build(N, "broom", big_d)
build(N, "twopaths", lambda i, dep, n: ri(n // 3, n))
build(N, "star", big_d, T)
build(N, "random", mixed, T)
build(N, "spider", big_d)
build(N, "cater", lambda i, dep, n: ri(1, 4), T)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

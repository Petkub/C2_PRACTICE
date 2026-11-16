# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(200002)
MAXN, MAXH = 100_000, 10**9
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


def add(h, es, checked=False):
    n = len(h)
    assert 1 <= n <= MAXN and 1 <= min(h) and max(h) <= MAXH
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind, val):
    """val(i, depth, par) gives the height of the i-th created node (parents are created first)"""
    par = shape(n, kind)
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n)
    hs = [0] * n
    for i in range(n):
        hs[i] = val(i, dep[i], hs[par[i]] if i else None)
    h = [0] * n
    for i in range(n):
        h[lab[i] - 1] = hs[i]
    assert shape_ok(par, lab)
    add(h, edge_list(par, lab), checked=True)


def uni(lo, hi):
    return lambda i, d, ph: ri(lo, hi)


def updown(p_up, step):
    """each node is above its parent with probability p_up, else below (rarely equal)"""
    def f(i, d, ph):
        if ph is None:
            return MAXH // 2
        r = _rnd()
        if r < 0.03:
            return ph
        x = ph + ri(1, step) if r < p_up else ph - ri(1, step)
        return min(MAXH, max(1, x))
    return f


def bydepth(i, d, ph):
    return 1 + d * 5000 + ri(0, 4999)


def middle_low(i, d, ph):
    """a path whose middle node is the lowest: heights rise on one side, fall... towards the other"""
    return 1 + abs(i - MAXN // 2) * 7


# samples
add([3, 1, 5, 4, 7], [(1, 2), (1, 3), (3, 4), (3, 5)])
add([2, 2, 3], [(1, 2), (2, 3)])
add([1, 2, 3, 4, 5], [(1, 2), (2, 3), (3, 4), (4, 5)])
add([4, 1, 7, 5, 2, 9, 3, 8], [(4, 1), (1, 2), (4, 3), (3, 6), (2, 5), (4, 7), (7, 8)])
add([5, 3, 8, 1, 4, 9, 6], [(1, 2), (2, 4), (2, 5), (1, 3), (3, 6), (3, 7)])
add([6, 6, 6, 6], [(1, 2), (1, 3), (1, 4)])
# hidden: small
add([7], [])
add([1, MAXH], [(1, 2)])
build(10, "random", uni(1, 4))
build(12, "deep", updown(0.5, 3))
build(60, "random", updown(0.6, 10))
build(500, "binary", bydepth)
build(3000, "spider", updown(0.5, 1000))
build(10000, "random", uni(1, 50))
# hidden: maximum size
N = MAXN
build(N, "path", lambda i, d, ph: i + 1)                         # every pair counts
build(N, "path", lambda i, d, ph: MAXH - 2 * i)
build(N, "path", lambda i, d, ph: 1 + abs(i - N // 2) * 7)      # lowest in the middle
build(N, "twopaths", lambda i, d, ph: 1 + d)
build(N, "spider", bydepth)
build(N, "star", uni(1, MAXH))
build(N, "random", bydepth)
build(N, "random", updown(0.5, 10**6))
build(N, "deep", bydepth)
build(N, "broom", bydepth)
build(N, "path", lambda i, d, ph: 1 + i // 2)                   # equal neighbours break the runs

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(200001)
MAXN, MAXA = 100_000, 10**9
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
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
        elif kind == "deep":
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "spider":
            par[i] = 0 if (i - 1) % s == 0 else i - 1
        elif kind == "twopaths":
            par[i] = 0 if i <= 2 else i - 2
        elif kind == "midstar":
            par[i] = i - 1 if i < h else h // 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def edge_list(par, lab):
    r = _rnd
    es = [(lab[par[i]], lab[i]) if r() < 0.5 else (lab[i], lab[par[i]]) for i in range(1, len(par))]
    shuf(es)
    return es


def shape_ok(par, lab):
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


def add(a, es, checked=False):
    n = len(a)
    assert 1 <= n <= MAXN and -MAXA <= min(a) and max(a) <= MAXA
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind, val):
    par = shape(n, kind)
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n)
    a = [0] * n
    for i in range(n):
        a[lab[i] - 1] = val(i, dep[i])
    assert shape_ok(par, lab)
    add(a, edge_list(par, lab), checked=True)


def uni(lo, hi):
    return lambda i, d: ri(lo, hi)


def bait(i, d):
    return -ri(MAXA // 2, MAXA) if d % 3 == 1 else ri(0, MAXA)


def mostly_neg(i, d):
    return ri(1, MAXA) if _rnd() < 0.1 else -ri(1, MAXA)


add([3, -2, 5, -6, 4, 1, -1], [(1, 2), (2, 3), (2, 4), (4, 5), (1, 6), (6, 7)])
add([-5, -2, -7], [(1, 2), (3, 1)])
add([10], [])
add([4, -1, -1, 4, -10], [(1, 2), (2, 3), (3, 4), (4, 5)])
add([2, -3, 6, 1, -4, 5, -1, 3], [(1, 2), (1, 3), (2, 4), (2, 5), (5, 6), (3, 7), (7, 8)])

add([-MAXA], [])
add([MAXA, MAXA], [(2, 1)])
build(9, "random", uni(-10, 10))
build(12, "deep", bait)
build(40, "random", mostly_neg)
build(300, "cater", uni(-100, 100))
build(2000, "random", bait)
build(5000, "spider", uni(-MAXA, MAXA))
build(20000, "binary", uni(-1000, 1000))

N = MAXN
build(N, "path", uni(MAXA, MAXA))
build(N, "path", bait)
build(N, "star", uni(-MAXA, MAXA))
build(N, "random", uni(-MAXA, MAXA))
build(N, "random", bait)
build(N, "deep", bait)
build(N, "binary", mostly_neg)
build(N, "spider", bait)
build(N, "twopaths", uni(-MAXA, MAXA // 2))
build(N, "random", uni(-MAXA, -1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

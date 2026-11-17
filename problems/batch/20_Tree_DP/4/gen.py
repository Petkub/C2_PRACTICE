# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(200004)
MAXN, MAXC = 100_000, 10**9
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


def add(c, es, checked=False):
    n = len(c)
    assert 1 <= n <= MAXN and 1 <= min(c) and max(c) <= MAXC
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + " ".join(map(str, c)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind, val, hub=0):
    par = shape(n - hub, kind)
    at = ri(0, n - hub - 1)
    par += [at] * hub
    dep = [0] * n
    nch = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
        nch[par[i]] += 1
    lp = [False] * n
    for i in range(1, n):
        if nch[i] == 0:
            lp[par[i]] = True
    lab = labels(n)
    c = [0] * n
    for i in range(n):
        c[lab[i] - 1] = val(i, dep[i], nch[i] == 0 and i > 0, lp[i])
    assert shape_ok(par, lab)
    add(c, edge_list(par, lab), checked=True)


def uni(lo, hi):
    return lambda i, d, leaf, lp: ri(lo, hi)


def bait(i, d, leaf, lp):
    if lp:
        return ri(MAXC // 2, MAXC)
    return ri(1, 1000) if leaf else ri(1, MAXC // 4)


def levels(i, d, leaf, lp):
    return ri(1, 10) if d % 3 == 0 else ri(10**6, MAXC)


add([2, 5, 10, 3, 4, 1], [(1, 2), (1, 3), (3, 4), (3, 5), (5, 6)])
add([3, 10, 3], [(1, 2), (2, 3)])
add([7], [])
add([1, 1, 1, 1, 1, 1, 1], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)])
add([9, 2, 2, 2, 2, 8, 6, 4], [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (6, 7), (6, 8)])

add([MAXC, MAXC], [(1, 2)])
build(8, "random", uni(1, 10))
build(12, "random", bait)
build(15, "deep", levels)
build(18, "cater", uni(1, 20))
build(20, "random", uni(1, 3))
build(500, "random", bait)
build(3000, "binary", levels)
build(10000, "spider", uni(1, MAXC))

N = MAXN


def H():
    return ri(72_000, 78_000)


build(N, "path", uni(MAXC, MAXC), H())
build(N, "path", uni(1, MAXC), H())
build(N, "path", levels, H())
build(N, "star", uni(1, MAXC))
build(N, "star", lambda i, d, leaf, lp: MAXC if i == 0 else ri(1, 10**4))
build(N, "random", uni(1, MAXC), H())
build(N, "random", bait, H())
build(N, "binary", levels, H())
build(N, "cater", bait, H())
build(N, "deep", uni(1, 100), H())
build(N, "spider", bait, H())
build(N, "broom", uni(1, 1), H())

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(200007)
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


def add(n, es, checked=False):
    assert 1 <= n <= MAXN
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in es))


def build(n, kind, hub=0):
    par = shape(n - hub, kind)
    at = ri(0, n - hub - 1)
    par += [at] * hub
    lab = labels(n)
    assert shape_ok(par, lab)
    add(n, edge_list(par, lab), checked=True)


def comb(n, legs, leg, hub=0):
    spine = n - legs * leg - hub
    par = [-1] + [i - 1 for i in range(1, spine)]
    for _ in range(legs):
        at = ri(0, spine - 1)
        for j in range(leg):
            par.append(at if j == 0 else len(par) - 1)
    par += [ri(0, spine - 1)] * hub
    lab = labels(n)
    assert shape_ok(par, lab)
    add(n, edge_list(par, lab), checked=True)


add(6, [(1, 2), (1, 3), (3, 4), (4, 5), (4, 6)])
add(3, [(1, 2), (2, 3)])
add(1, [])
add(6, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])
add(10, [(1, 2), (2, 3), (2, 4), (4, 5), (1, 6), (6, 7), (7, 8), (7, 9), (9, 10)])

add(2, [(2, 1)])
build(8, "random")
build(12, "deep")
build(15, "random")
build(18, "binary")
build(20, "cater")
build(500, "random")
build(5000, "spider")
build(20000, "deep")

N = MAXN


def H():
    return ri(40_000, 45_000)


build(N, "path", H())
build(N, "star")
build(N, "random", H())
build(N, "deep", H())
build(N, "binary", H())
build(N, "cater", H())
build(N, "spider", H())
build(N, "broom")
comb(N, 30000, 3, H())
comb(N, 50000, 1, H())

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

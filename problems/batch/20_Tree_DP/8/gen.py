# Test generator of this problem (the judge runs it to rebuild the big tests).
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


def add(D, n, es, checked=False):
    assert 1 <= n <= MAXN and 0 <= D <= n - 1
    assert checked or is_tree(n, es)
    tests.append(f"{n} {D}\n" + "".join(f"{u} {v}\n" for u, v in es))


def legs_shape(n, leg):
    core = max(1, n // (leg * 20))
    par = [-1] + [int(_rnd() * i) for i in range(1, core)]
    while len(par) < n:
        i = len(par)
        if (i - core) % leg == 0:
            par.append(ri(0, core - 1))
        else:
            par.append(i - 1)
    return par


def fan_shape(n, legs, leg):
    spine = n - legs * leg
    par = [-1] + [i - 1 for i in range(1, spine)]
    for _ in range(legs):
        for j in range(leg):
            par.append(spine - 1 if j == 0 else len(par) - 1)
    return par


def build(n, D, kind, leg=0, legs=0):
    if kind == "legs":
        par = legs_shape(n, leg)
    elif kind == "fan":
        par = fan_shape(n, legs, leg)
    else:
        par = shape(n, kind)
    lab = labels(n)
    assert shape_ok(par, lab)
    add(D, n, edge_list(par, lab), checked=True)


add(2, 7, [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7)])
add(1, 4, [(1, 2), (2, 3), (3, 4)])
add(0, 3, [(2, 1), (3, 2)])
add(2, 6, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])
add(3, 10, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (1, 7), (7, 8), (8, 9), (8, 10)])

add(0, 1, [])
build(8, 1, "random")
build(12, 3, "random")
build(14, 2, "cater")
build(16, 4, "deep")
build(16, 5, "binary")
build(300, 6, "random")
build(2000, 40, "legs", 15)
build(2000, 300, "deep")
build(2000, 1999, "random")
build(3000, 10, "random")
build(3000, 2, "random")
build(4095, 12, "binary")

N = MAXN
build(N, 50_000, "path")
build(N, 150_000, "path")
build(N, 30_000, "deep")
build(N, 70_000, "twopaths")
build(N, 60_000, "broom")
build(N, 20_000, "cater")
build(N, 35_000, "fan", 60_000, 3)
build(N, 28_000, "fan", 45_000, 4)
build(N, 60_000, "deep")
build(N, 10_000, "deep")
build(N, 25_000, "legs", 40_000)
build(N, 15_000, "legs", 20_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(200008)
MAXN, MAXW = 100000, 10 ** 9
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


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
    assert 1 <= n <= MAXN and len(es) == n - 1
    assert 1 <= min(w) and max(w) <= MAXW
    assert checked or is_tree(n, es)
    tests.append(f"{n}\n" + " ".join(map(str, w)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


class Tree:

    def __init__(self, w0):
        self.par, self.w = [-1], [w0]

    def node(self, p, w):
        assert 0 <= p < len(self.par)
        self.par.append(p)
        self.w.append(w)
        return len(self.par) - 1

    def size(self):
        return len(self.par)

    def emit(self):
        n = self.size()
        assert n == 1 or (min(self.par[1:]) >= 0 and all(map(int.__lt__, self.par[1:], range(1, n))))
        lab = list(range(1, n + 1))
        shuf(lab)
        w = [0] * n
        for i in range(n):
            w[lab[i] - 1] = self.w[i]
        par, r = self.par, _rnd
        es = [(lab[par[i]], lab[i]) if r() < 0.5 else (lab[i], lab[par[i]]) for i in range(1, n)]
        shuf(es)
        add(w, es, checked=True)


def unit():
    return 1


def small():
    return ri(1, 10)


def logw():
    return min(MAXW, int(10 ** (9 * _rnd())))


def top():
    return MAXW


def high():
    return ri(MAXW - 1000, MAXW)


def gadget(t, p, k, base=30, scale=MAXW):
    v = t.node(p, max(1, scale // base ** (k - 1)))
    for j in range(1, k):
        gadget(t, v, j, base, scale)
    return v


def grow(t, m, kind, wf, at=None):
    start = t.size()
    for i in range(m):
        cur = t.size()
        if kind == "random":
            p = ri(0, cur - 1) if at is None else (at if i == 0 else ri(start, cur - 1))
        elif kind == "path":
            p = cur - 1 if i else (at if at is not None else cur - 1)
        elif kind == "deep":
            p = ri(max(start, cur - 3), cur - 1) if i else (at if at is not None else cur - 1)
        elif kind == "binary":
            p = start + (i - 1) // 2 if i else (at if at is not None else 0)
        elif kind == "leaves":
            p = at
        else:
            raise ValueError(kind)
        t.node(p, wf())


def plant(t, cnt, k, lo=0, base=30):
    for _ in range(cnt):
        gadget(t, ri(lo, t.size() - 1), k, base, scale=ri(MAXW // 2, MAXW))


def fill(t, n, wf, at):
    assert 0 <= at < t.size()
    m = n - t.size()
    t.par += [at] * m
    t.w += [wf() for _ in range(m)]


add([5, 2, 3, 4, 1], [(1, 2), (1, 3), (1, 4), (4, 5)])
add([10, 1, 1, 1], [(2, 1), (1, 3), (4, 1)])
add([7], [])
add([3, 9, 2, 8, 1, 6], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
add([5, 2, 6, 5, 1, 6, 2, 5], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)])
add([1, 1, 1, 1, 1, 1], [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6)])


add([MAXW, MAXW], [(1, 2)])
add([100, 1, 1, 100], [(1, 2), (2, 3), (3, 4)])
t = Tree(1)
gadget(t, 0, 3)
t.node(0, 10 ** 9)
t.emit()
t = Tree(5)
for k in (1, 2, 3, 4):
    gadget(t, 0, k, base=10, scale=10 ** 6)
t.emit()
t = Tree(logw())
grow(t, 299, "random", logw)
t.emit()
t = Tree(1)
grow(t, 349, "random", unit)
t.emit()
t = Tree(small())
grow(t, 200, "deep", small)
plant(t, 10, 4)
t.emit()
t = Tree(logw())
grow(t, 3000, "random", logw)
plant(t, 60, 5)
grow(t, 2000, "leaves", logw, at=7)
t.emit()


N = MAXN

t = Tree(logw())
fill(t, N, logw, 0)
t.emit()

t = Tree(1)
while t.size() + 7 <= N:
    for k in (1, 2, 3):
        gadget(t, 0, k)
fill(t, N, top, 0)
t.emit()

t = Tree(logw())
grow(t, 40000, "random", logw)
plant(t, 1500, 4)
hub = ri(0, t.size() - 1)
fill(t, N, logw, hub)
t.emit()

t = Tree(logw())
grow(t, 49999, "path", logw)
fill(t, N, logw, t.size() - 1)
t.emit()

t = Tree(1)
grow(t, 45000, "random", unit)
fill(t, N, unit, ri(0, 1000))
t.emit()

t = Tree(MAXW)
grow(t, 30000, "random", top)
fill(t, N, top, 5)
t.emit()

t = Tree(logw())
grow(t, 30000, "binary", logw)
plant(t, 600, 5)
fill(t, N, logw, ri(0, 100))
t.emit()

t = Tree(logw())
grow(t, 20000, "path", logw)
for _ in range(20000):
    t.node(ri(0, 19999), logw())
fill(t, N, logw, 10000)
t.emit()

t = Tree(1)
while t.size() + 15 <= N:
    for k in (1, 2, 3, 4):
        gadget(t, 0, k, base=40)
fill(t, N, top, 0)
t.emit()

t = Tree(high())
h2 = t.node(0, high())
for i in range(N - 2):
    t.node(0 if i % 2 else h2, small())
t.emit()

t = Tree(logw())
grow(t, 40000, "deep", logw)
plant(t, 1000, 4)
fill(t, N, logw, ri(0, 40000))
t.emit()

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

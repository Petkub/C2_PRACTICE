# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(141616)
MAXN, MAXM, MAXQ = 100_000, 150_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.groups = n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def unite(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        self.groups -= 1
        return True


def bounds(n, roads):
    d0, d1, d2 = DSU(n), DSU(n), DSU(n)
    for u, v, p in roads:
        d0.unite(u, v)
        (d1 if p == 1 else d2).unite(u, v)
    return d0.groups == 1, d2.groups - 1, n - d1.groups


def add(n, roads, ks, mix=True):
    roads = list(roads)
    if mix:
        shuffle(roads)
    m, q = len(roads), len(ks)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM and 1 <= q <= MAXQ
    for u, v, p in roads:
        assert 1 <= u <= n and 1 <= v <= n and u != v and p in (1, 2)
    assert all(0 <= k <= n - 1 for k in ks)
    tests.append(f"{n} {m} {q}\n" + "".join(f"{u} {v} {p}\n" for u, v, p in roads) + " ".join(map(str, ks)) + "\n")


def part_roads(n, groups, p, extra, shape="random"):
    who = list(range(1, n + 1))
    shuffle(who)
    pos = list(range(1, n))
    shuffle(pos)
    cut = sorted(pos[:groups - 1])
    parts = [who[a:b] for a, b in zip([0] + cut, cut + [n])]
    res = []
    for g in parts:
        for i in range(1, len(g)):
            j = i - 1 if shape == "path" else ri(0, i - 1)
            res.append((g[i], g[j], p))
    big = [g for g in parts if len(g) > 1]
    for _ in range(extra):
        if not big:
            break
        g = big[ri(0, len(big) - 1)]
        a, b = g[ri(0, len(g) - 1)], g[ri(0, len(g) - 1)]
        if a != b:
            res.append((a, b, p))
    return res


def queries(n, q, lo, hi, near=0.5):
    ks = []
    spots = [lo - 2, lo - 1, lo, lo + 1, hi - 1, hi, hi + 1, hi + 2, 0, n - 1]
    for _ in range(q):
        if random.random() < near:
            k = spots[ri(0, len(spots) - 1)] + ri(-3, 3)
        else:
            k = ri(0, n - 1)
        ks.append(min(n - 1, max(0, k)))
    return ks


def build(n, m, q, g1, g2, share1=0.5, shape="random", connect=True, near=0.5):
    base1 = n - g1
    base2 = n - g2
    assert base1 + base2 + (min(g1, g2) if connect else 0) <= m, "too many roads for these groups"
    extra = max(0, m - base1 - base2 - (min(g1, g2) if connect else 0))
    e1 = int(extra * share1)
    roads = part_roads(n, g1, 1, e1, shape) + part_roads(n, g2, 2, extra - e1, shape)
    if connect:
        d = DSU(n)
        for u, v, p in roads:
            d.unite(u, v)
        roots = sorted(set(d.find(x) for x in range(1, n + 1)))
        for i in range(1, len(roots)):
            roads.append((roots[i], roots[ri(0, i - 1)], ri(1, 2)))
    ok, lo, hi = bounds(n, roads)
    return n, roads, queries(n, q, lo, hi, near)


def split(n, m, q):
    h = n // 2
    a = build(h, m // 2, 1, max(1, h // 2), max(1, h // 3))[1]
    b = build(n - h, m - m // 2, 1, max(1, h // 3), max(1, h // 2))[1]
    roads = a + [(u + h, v + h, p) for u, v, p in b]
    return n, roads, [ri(0, n - 1) for _ in range(q)]


add(5, [(1, 2, 1), (2, 3, 2), (3, 4, 1), (4, 5, 2), (5, 1, 2), (1, 3, 2)], [0, 1, 2, 3], mix=False)
add(4, [(1, 2, 1), (2, 1, 2), (3, 4, 1)], [0, 1, 2], mix=False)
add(4, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (3, 4, 2), (1, 4, 1)], [3, 2], mix=False)
add(2, [(1, 2, 2), (2, 1, 2)], [0, 1], mix=False)
add(6, [(1, 2, 1), (2, 3, 2), (3, 1, 1), (4, 5, 2), (5, 6, 2), (6, 4, 1), (3, 4, 1), (2, 5, 2)], [4, 1, 5, 3],
    mix=False)

add(2, [(1, 2, 1)], [0, 1])
add(3, [(1, 2, 1), (2, 3, 1), (3, 1, 2)], [0, 1, 2])
add(4, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (1, 2, 2), (3, 4, 2), (1, 4, 1)], [0, 1, 2, 3])
add(*build(7, 12, 7, 3, 3))
add(*build(8, 14, 8, 2, 4, share1=0.7))
add(*build(9, 18, 9, 5, 2, share1=0.3))
add(*build(40, 120, 40, 6, 9))
add(*build(60, 200, 60, 20, 4, share1=0.8))
add(*split(50, 150, 50))
add(*build(300, 900, 600, 40, 70))

N, M, Q = MAXN, MAXM, MAXQ
add(*build(N, M, Q, 60_000, 20_000))
add(*build(70_000, M, Q, 1, 1))
add(*build(N, M, Q, 50_000, 1_000, share1=0.9))
add(*build(N, M, Q, 2_000, 60_000, share1=0.1))
add(*split(N, M, Q))
add(*build(N, M, Q, 70_000, 70_000, shape="path"))
add(*build(N, M, Q, 10, 90_000, near=0.8))
add(*build(N, M, Q, 90_000, 10, near=0.8))
add(*build(N, M, Q, 40_000, 55_000, share1=0.5, near=0.9))
add(*build(70_000, M, Q, 5_000, 5_000, share1=0.5, near=0.2))
add(*build(N, M, Q, 25_000, 75_000, share1=0.6, shape="path"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

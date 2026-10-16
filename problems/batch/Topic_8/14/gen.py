# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(81414)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True, relabel=True):
    """relabel: intersections other than 1 get random numbers; each road gets a random orientation"""
    edges = list(edges)
    if relabel:
        p = list(range(2, n + 1))
        random.shuffle(p)
        p = [0, 1] + p
        edges = [(p[a], p[b], w) if random.random() < 0.5 else (p[b], p[a], w) for a, b, w in edges]
    if shuffle:
        random.shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and 1 <= w <= MAXW for a, b, w in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges))


def rnd(n, m, wlo, whi, ploop=0.0):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b or random.random() < ploop:
            res.append((a, b, ri(wlo, whi)))
    return res


def tree(n, wlo, whi, deep=False):
    e = []
    for v in range(2, n + 1):
        par = ri(max(1, v - 3), v - 1) if deep else ri(1, v - 1)
        e.append((par, v, ri(wlo, whi)))
    return e


def grid(r, c, wfun):
    e = []
    for i in range(r):
        for j in range(c):
            v = i * c + j + 1
            if j + 1 < c:
                e.append((v, v + 1, wfun(True)))
            if i + 1 < r:
                e.append((v, v + c, wfun(False)))
    return r * c, e


# samples
add(4, [(1, 2, 2), (2, 4, 3), (1, 3, 4), (3, 4, 2), (2, 3, 1)], False, False)
add(3, [(1, 2, 5), (2, 2, 1)], False, False)
add(4, [(1, 2, 3), (1, 2, 3), (2, 3, 1), (1, 3, 4)], False, False)
add(3, [(2, 3, 7)], False, False)
add(3, [(1, 2, MAXW), (2, 3, MAXW)], False, False)
# hidden: small
add(2, [(1, 2, 1)])
add(2, [(1, 1, 4)])
add(5, [(1, 2, 3), (1, 3, 3), (2, 4, 2), (3, 4, 2), (4, 5, 1)])
for n, m, whi, pl in ((5, 6, 3, 0.1), (8, 12, 5, 0.0), (10, 15, 2, 0.05), (12, 20, 10, 0.0), (30, 50, 20, 0.02)):
    add(n, rnd(n, m, 1, whi, pl))
add(30, tree(30, 1, 5))
add(40, tree(40, 1, 1))
n, e = grid(6, 7, lambda h: 1)
add(n, e)
n, e = grid(10, 12, lambda h: ri(1, 3))
add(n, e)
add(200, rnd(200, 400, 1, 10**6))
add(300, tree(300, 1, 10, True) + rnd(300, 50, 1, 10))
add(150, rnd(100, 300, 1, 5))                                                   # intersections 101..150 cut off
# hidden: maximum size
N, M = MAXN, MAXM
add(N, rnd(N, M, 1, MAXW))
add(50_000, rnd(50_000, M, 1, 3))                                               # many ties
add(N, tree(N, 1, MAXW, True))                                                  # only back-and-forth detours
add(N, tree(N, MAXW, MAXW, True), True, False)                                  # lengths near 10^14
n, e = grid(200, 250, lambda h: 1)
add(n, e)
n, e = grid(10_000, 5, lambda h: ri(1, 10) if h else ri(10**8, MAXW))            # cheap rows, costly columns
add(n, e)
e = [(i, i + 1, 2) for i in range(1, N)]                                         # a path with parallel roads
e += [(i, i + 1, 2 + random.choice((0, 1, 2))) for i in range(1, N - 1, 10)]
add(N, e[:M], True, False)
add(70_000, rnd(60_000, M, 1, 10**4, 0.01))                                      # some intersections cut off
e = tree(N - 1, 1, 10**4, True) + [(v, v, ri(1, 3)) for v in range(1, N, 1000)]      # self-loops, one isolated
add(N, e[:M])
add(N, [(1, v, ri(1, MAXW)) for v in range(2, N + 1)] + [(2, 3, 1)])               # a star
n, e = grid(220, 225, lambda h: ri(1, 1000))
add(n, e[:M])
e = [(i, i + 1, ri(1, 100)) for i in range(1, 50_000)]                           # long thin band
while len(e) < M:
    a = ri(1, 49_999)
    e.append((a, min(50_000, a + ri(1, 10)), ri(1, 100)))
add(50_000, e)
add(30_000, rnd(30_000, M, 1, 2, 0.001))
e = []
for b in range(25_000):                                                          # blocks of two equal routes
    a, x, y, z = 3 * b + 1, 3 * b + 2, 3 * b + 3, 3 * b + 4
    e += [(a, x, 1), (x, z, 1), (a, y, 1), (y, z, 1)]
add(75_001, e)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

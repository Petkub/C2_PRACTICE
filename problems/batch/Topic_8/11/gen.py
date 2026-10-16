# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(81111)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True, relabel=True):
    """relabel: intersections other than 1 and n get random numbers; each road gets a random orientation"""
    edges = list(edges)
    if relabel:
        p = list(range(2, n))
        random.shuffle(p)
        p = [0, 1] + p + [n]
        edges = [(p[a], p[b], w) if random.random() < 0.5 else (p[b], p[a], w) for a, b, w in edges]
    if shuffle:
        random.shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= w <= MAXW for a, b, w in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges))


def rnd(n, m, wlo, whi):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b, ri(wlo, whi)))
    return res


def grid(r, c, wfun):
    """r x c grid, corner (0, 0) is intersection 1 and the opposite corner is intersection r * c"""
    e = []
    for i in range(r):
        for j in range(c):
            v = i * c + j + 1
            if j + 1 < c:
                e.append((v, v + 1, wfun()))
            if i + 1 < r:
                e.append((v, v + c, wfun()))
    return r * c, e


def chain(n, wlo, whi, extra, xlo, xhi):
    e = [(i, i + 1, ri(wlo, whi)) for i in range(1, n)]
    return e + rnd(n, extra, xlo, xhi)


def diamonds(k, wmax):
    """k blocks in a row; each block: two routes, sometimes of equal length, plus a useless cross road"""
    e, cur, nxt = [], 1, 2
    for _ in range(k):
        x, y, z = nxt, nxt + 1, nxt + 2
        nxt += 3
        s = ri(2, wmax)
        t = ri(1, s - 1)
        s2 = s if random.random() < 0.6 else s + ri(1, 3)
        t2 = ri(1, s2 - 1)
        e += [(cur, x, t), (x, z, s - t), (cur, y, t2), (y, z, s2 - t2), (x, y, abs(t - t2) + ri(1, 2))]
        cur = z
    return cur, e


def band(n, m, width, wlo, whi):
    """intersections on a line, roads join close intersections only, so routes have many roads"""
    e = [(i, i + 1, ri(wlo, whi)) for i in range(1, n)]
    while len(e) < m:
        a = ri(1, n - 1)
        b = min(n, a + ri(1, width))
        e.append((a, b, ri(wlo, whi)))
    return n, e


# samples
add(5, [(1, 2, 3), (2, 5, 4), (1, 3, 2), (3, 5, 5), (3, 4, 1), (4, 5, 6), (2, 3, 1)], False, False)
add(4, [(1, 2, 5), (3, 4, 1), (2, 1, 7)], False, False)
add(4, [(4, 2, 2), (2, 1, 2), (1, 3, 3), (3, 4, 1), (1, 4, 5)], False, False)
add(3, [(1, 2, 1), (1, 2, 1), (1, 2, 2), (2, 3, 4), (3, 1, 6)], False, False)
add(4, [(1, 2, MAXW), (2, 3, MAXW), (3, 4, MAXW), (1, 3, MAXW), (2, 4, MAXW)], False, False)
# hidden: small
add(2, [(1, 2, 1)])
add(2, [(2, 1, 7), (1, 2, 7), (1, 2, 8)])
for n, m, whi in ((6, 10, 3), (8, 16, 2), (10, 25, 5), (30, 60, 10), (50, 150, 4), (200, 600, 20)):
    add(n, rnd(n, m, 1, whi))
n, e = grid(5, 6, lambda: ri(1, 2))
add(n, e)
n, e = diamonds(30, 8)
add(n, e)
add(9, rnd(8, 12, 1, 3))                                                        # intersection 9 unreachable
add(300, chain(300, 1, 5, 400, 1, 600))
n, e = grid(15, 20, lambda: 1)
add(n, e)
# hidden: maximum size
N, M = MAXN, MAXM
add(*band(40_000, M, 20, 1, 3))
add(N, rnd(N, M, 1, MAXW))
n, e = grid(200, 250, lambda: 1)                                                 # very many shortest routes
add(n, e)
n, e = grid(200, 250, lambda: ri(1, 3))
add(n, e)
add(N, chain(N, 1, 1000, 1, 10**8, MAXW), True, False)                           # one long route
add(N, chain(N, MAXW, MAXW, 1, MAXW, MAXW), True, False)                         # lengths near 10^14
n, e = diamonds(20_000, 10**6)
add(n, e)
e = rnd(N - 1, M - 1, 1, 100) + [(N - 2, N - 1, 5)]                              # intersection n unreachable
add(N, e, True, False)
n, e = grid(10_000, 5, lambda: 0)
e = [(a, b, ri(1, 10) if b == a + 1 else ri(10**8, MAXW)) for a, b, _ in e]      # cheap rows, costly columns
add(n, e)
n = 85_000
add(n, chain(n, 1, 3, 0, 1, 1) + [(i, i + 2, ri(2, 6)) for i in range(1, n - 1, 7)], True, False)
add(*band(50_000, M, 5, 1, 2))
e = []
for i in range(1, 50_000):                                                       # parallel roads, some of equal length
    x = ri(1, 10**6)
    e += [(i, i + 1, x), (i, i + 1, x + random.choice((0, 0, 1, 5)))]
add(50_000, e, True, False)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

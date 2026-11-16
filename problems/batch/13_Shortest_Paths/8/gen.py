# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80808)
MAXN, MAXM, MAXC = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True):
    edges = list(edges)
    if shuffle:
        random.shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= c <= MAXC for a, b, c in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in edges))


def rnd_edges(n, m, clo, chi):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b, ri(clo, chi)))
    return res


def perm(n):
    """random order of the cities 2..n after city 1"""
    p = list(range(2, n + 1))
    random.shuffle(p)
    return [1] + p


def chain(n, clo, chi, extra, xlo, xhi):
    """a long path 1 -> ... (cheap) plus extra random flights (expensive)"""
    p = perm(n)
    e = [(p[i], p[i + 1], ri(clo, chi)) for i in range(n - 1)]
    return e + rnd_edges(n, extra, xlo, xhi)


def gadgets(k):
    """k copies of: a cheap route with two equal flights vs. one long flight; the coupon prefers the long one"""
    e, nxt = [], 2
    hub = 1
    for _ in range(k):
        mid, end = nxt, nxt + 1
        nxt += 2
        x = ri(1000, 10**6)
        e += [(hub, mid, x), (mid, end, x), (hub, end, 2 * x + ri(1, x - 2))]
        hub = end if random.random() < 0.97 else ri(1, nxt - 1)
    return nxt - 1, e


def grid(r, c, chi):
    """r x c grid of cities, flights between neighbours in random directions"""
    idx = list(range(2, r * c + 1))
    random.shuffle(idx)
    idx = [1] + idx
    e = []
    for i in range(r):
        for j in range(c):
            v = idx[i * c + j]
            if j + 1 < c:
                e.append((v, idx[i * c + j + 1], ri(1, chi)))
            if i + 1 < r:
                e.append((v, idx[(i + 1) * c + j], ri(1, chi)))
    e = [(a, b, w) if random.random() < 0.75 else (b, a, w) for a, b, w in e]
    return r * c, e


def ladder(r, c):
    """tall r x c grid, flights both ways; cheap along the rows, expensive between rows"""
    idx = list(range(2, r * c + 1))
    random.shuffle(idx)
    idx = [1] + idx
    e = []
    for i in range(r):
        for j in range(c):
            v = idx[i * c + j]
            if j + 1 < c:
                w = ri(1, 10)
                e += [(v, idx[i * c + j + 1], w), (idx[i * c + j + 1], v, w)]
            if i + 1 < r:
                w = ri(10**8, MAXC)
                e += [(v, idx[(i + 1) * c + j], w), (idx[(i + 1) * c + j], v, w)]
    return r * c, e


# samples
add(4, [(1, 2, 8), (2, 4, 8), (1, 3, 3), (3, 4, 16)], False)
add(4, [(1, 2, 7), (3, 1, 4), (2, 3, 1)], False)
add(3, [(1, 2, 1), (1, 2, 5), (2, 3, 3), (1, 3, 9)], False)
add(6, [(1, 2, 4), (2, 3, 6), (3, 6, 2), (1, 4, 9), (4, 5, 1), (5, 6, 1), (2, 5, 11), (6, 1, 3)], False)
add(4, [(1, 2, MAXC), (2, 3, MAXC), (3, 4, MAXC)], False)
# hidden: small
add(2, [(2, 1, 5)])
add(2, [(1, 2, 1)])
for n, m, chi in ((5, 8, 10), (8, 20, 100), (10, 30, 5), (30, 80, 10**9), (60, 200, 50)):
    add(n, rnd_edges(n, m, 1, chi))
n, e = gadgets(20)
add(n, e)
add(40, chain(40, 1, 5, 60, 10, 100))
n, e = grid(6, 7, 30)
add(n, e)
add(300, rnd_edges(300, 1500, 1, 10**9))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, rnd_edges(N, M, 1, MAXC))
add(N, chain(N, 1, 1000, M - N + 1, 10**6, MAXC))
add(N, [(i, i + 1, MAXC) for i in range(N - 1, 0, -1)] + [(N, 1, MAXC)], False)   # sums near 10^14
add(N, chain(N, 1, MAXC, M - N + 1, 1, MAXC))
n, e = gadgets(30_000)
add(n, e + rnd_edges(n, M - len(e), 10**7, MAXC))
n, e = ladder(2500, 10)
add(n, e)
n, e = ladder(5000, 5)
add(n, e)
add(N, chain(N, 1, 1, M - N + 1, 2, 3))
p = perm(N)
e = [(p[i], p[i + 1], 2 * ri(1, 10**4) + 1) for i in range(N // 2)]  # about half of the cities unreachable
while len(e) < M:
    a, b = ri(0, N // 2), ri(0, N - 1)                          # flights into the first half
    if random.random() < 0.5:
        a, b = ri(N // 2 + 1, N - 1), ri(N // 2 + 1, N - 1)    # or inside the second half
    if a != b:
        e.append((p[b], p[a], ri(1, MAXC)))
add(N, e)
e = [(1, v, ri(5 * 10**8, MAXC)) for v in range(2, N + 1)]     # every city one expensive flight away
add(N, e + rnd_edges(N, M - len(e), 1, 10**4))
add(N, chain(N, 10**8, MAXC, M - N + 1, 1, 10**9))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

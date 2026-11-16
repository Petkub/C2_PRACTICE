# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(8007)
MAXN, MAXM, MAXW, MAXQ, MAXX = 400, 80_000, 10**9, 1000, 10**12
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads, xs):
    m, q = len(roads), len(xs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in roads)
    assert all(0 <= x <= MAXX for x in xs)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads)
                 + f"{q}\n" + " ".join(map(str, xs)) + "\n")


def relabel(n, roads):
    p = list(range(1, n + 1))
    random.shuffle(p)
    p = [0] + p
    res = [(p[u], p[v], w) if random.random() < 0.5 else (p[v], p[u], w) for u, v, w in roads]
    random.shuffle(res)
    return res


def rnd_roads(n, m, wmax=MAXW, wmin=1):
    res = []
    while len(res) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            res.append((u, v, ri(wmin, wmax)))
    return res


def dists(n, roads, src):
    """O(n^2) Dijkstra on the matrix of shortest roads"""
    inf = float("inf")
    adj = [dict() for _ in range(n + 1)]
    for u, v, w in roads:
        if w < adj[u].get(v, inf):
            adj[u][v] = adj[v][u] = w
    d = [inf] * (n + 1)
    done = [False] * (n + 1)
    d[src] = 0
    for _ in range(n):
        u, best = -1, inf
        for v in range(1, n + 1):
            if not done[v] and d[v] < best:
                u, best = v, d[v]
        if u < 0:
            break
        done[u] = True
        for v, w in adj[u].items():
            if best + w < d[v]:
                d[v] = best + w
    return [x for x in d[1:] if x != inf and x > 0]


def thresholds(n, roads, q, sources=4):
    """exact distances (and one less) from a few towns, plus random values"""
    pool = []
    for _ in range(sources):
        pool += dists(n, roads, ri(1, n))
    if not pool:
        pool = [1]
    res = [0, MAXX]
    while len(res) < q:
        t = random.random()
        if t < 0.4:
            res.append(random.choice(pool))
        elif t < 0.7:
            res.append(max(0, random.choice(pool) - 1))
        else:
            res.append(ri(0, max(pool)))
    random.shuffle(res)
    return res[:q]


def chain(n, w):
    return [(i, i + 1, w if w else ri(1, MAXW)) for i in range(1, n)]


# samples
add(4, [(1, 2, 7), (2, 3, 2), (3, 4, 2), (2, 4, 3)], [2, 9, 0])
add(5, [(3, 4, 2), (4, 5, 2), (5, 3, 2), (1, 2, 7)], [2, 1])
add(6, [(1, 2, 4), (2, 3, 4), (3, 4, 4), (4, 5, 4), (5, 6, 4), (1, 6, 1)], [4, 5, 8, 12])
add(3, [(2, 3, MAXW), (1, 3, MAXW), (2, 3, 1)], [1, MAXW])
add(1, [], [0, 5])
# hidden: small
add(3, [(2, 3, MAXW), (1, 3, MAXW), (2, 3, 1)], [1, MAXW, 2 * MAXW, MAXX])
add(2, [], [0, 1, MAXX])
add(2, [(1, 2, 5), (2, 1, 3)], [2, 3, 4])
r = rnd_roads(8, 12, 20)
add(8, r, thresholds(8, r, 20))
r = relabel(20, chain(20, 3))
add(20, r, thresholds(20, r, 30))
r = rnd_roads(40, 100, 1000)
add(40, r, thresholds(40, r, 50))
r = relabel(60, chain(60, 0) + rnd_roads(60, 40, MAXW, MAXW // 2))
add(60, r, thresholds(60, r, 100))
r = rnd_roads(100, 150, 10)
add(100, r, thresholds(100, r, 200))
# hidden: large
N, M, Q = MAXN, MAXM, MAXQ
r = rnd_roads(N, M)
add(N, r, thresholds(N, r, Q))
r = rnd_roads(N, M, 5)                                     # many equal distances and counts
add(N, r, thresholds(N, r, Q))
r = relabel(N, [(i, i + 1, ri(1, 1000)) for i in range(1, N)] + rnd_roads(N, M - N + 1, MAXW, 10**8))
# (above: shortest ways along a long chain)
add(N, r, thresholds(N, r, Q))
r = chain(N, MAXW)                                         # the largest distances (many parallel roads)
r = relabel(N, r + [(i, i + 1, MAXW) for i in (ri(1, N - 1) for _ in range(M - N + 1))])
add(N, r, thresholds(N, r, Q))
r = chain(N, 0)                                            # a chain: the ends are often the most isolated
r += [(i, i + 1, ri(1, MAXW)) for i in (ri(1, N - 1) for _ in range(M - N + 1))]
add(N, r, thresholds(N, r, Q))
r = [(u, v, ri(1, MAXW)) for u in range(1, N + 1) for v in range(u + 1, N + 1)]
random.shuffle(r)
r = r[:M]
add(N, r, thresholds(N, r, Q))
r = []                                                     # groups of different sizes, not connected
start = 1
for size in (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 169):
    grp = list(range(start, start + size))
    if size > 1:
        r += [(grp[i], grp[i + 1], ri(1, 1000)) for i in range(size - 1)]
        r += [(random.choice(grp), random.choice(grp), ri(1, 1000)) for _ in range(size * 3)]
    start += size
r = [(u, v, w) for u, v, w in r if u != v]
add(N, relabel(N, r), thresholds(N, r, Q, 10))
r = relabel(N, [(1, i, ri(1, 10**6)) for i in range(2, N + 1)])  # a star
add(N, r, thresholds(N, r, Q))
r = relabel(N, chain(N, 1) + rnd_roads(N, M - N + 1, MAXW, 10**8))
add(N, r, thresholds(N, r, Q))
r = rnd_roads(N, 1200, 10**6)                              # sparse
add(N, r, thresholds(N, r, Q))
r = [(i, ri(max(1, i - 3), i - 1), ri(1, 100)) for i in range(2, N + 1)]   # a thin tree of short roads
r = relabel(N, r + rnd_roads(N, M - N + 1, MAXW, 10**7))
add(N, r, thresholds(N, r, Q))
r = []                                                     # a 5 x 80 grid of short roads, long roads elsewhere
for i in range(5):
    for j in range(80):
        v = i * 80 + j + 1
        if j < 79:
            r.append((v, v + 1, ri(1, 10)))
        if i < 4:
            r.append((v, v + 80, ri(1, 10)))
r = relabel(N, r + rnd_roads(N, M - len(r), MAXW, 10**4))
add(N, r, thresholds(N, r, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

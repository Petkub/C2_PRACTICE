# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80200)
MAXN, MAXM, MAXQ, MAXW, MAXH = 400, 40_000, 100_000, 10**9, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, h, roads, qs):
    m, q = len(roads), len(qs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= q <= MAXQ and len(h) == n
    assert all(1 <= x <= MAXH for x in h)
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= w <= MAXW for a, b, w in roads)
    assert all(1 <= u <= n and 1 <= v <= n and 0 <= k <= MAXH for u, v, k in qs)
    tests.append(f"{n} {m} {q}\n" + " ".join(map(str, h)) + "\n"
                 + "".join(f"{a} {b} {w}\n" for a, b, w in roads)
                 + "".join(f"{u} {v} {k}\n" for u, v, k in qs))


def rnd_roads(n, m, wlo, whi, conn=True):
    roads = []
    if conn:
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        roads = [(perm[i], perm[ri(0, i - 1)], ri(wlo, whi)) for i in range(1, n)]
    while len(roads) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            roads.append((a, b, ri(wlo, whi)))
    random.shuffle(roads)
    return roads


def rnd_q(n, q, h, mode="mix"):
    """thresholds: around the levels of the towns (each value of k makes a different set of towns usable)"""
    lv = sorted(h)
    qs = []
    for _ in range(q):
        u, v = ri(1, n), ri(1, n)
        r = random.random()
        if mode == "mix" and r < 0.1:
            k = ri(0, MAXH)
        elif mode == "mix" and r < 0.15:
            k = 0
        else:
            k = max(0, random.choice(lv) - ri(0, 1))
        qs.append((u, v, k))
    return qs


# samples
add(4, [5, 1, 3, 2], [(1, 2, 4), (2, 4, 4), (1, 3, 1), (3, 4, 2)], [(1, 4, 0), (1, 4, 1), (1, 4, 3)])
add(3, [1, 9, 1], [(1, 2, 3), (2, 3, 3)], [(1, 3, 8), (1, 3, 9), (1, 2, 0)])
add(1, [7], [], [(1, 1, 0)])
add(3, [3, 3, 3], [(1, 2, 2), (2, 3, 2), (3, 1, 5)], [(3, 1, 3)])
add(2, [9, 9], [(1, 2, 5)], [(2, 2, 0), (2, 1, 0)])
# hidden: small
add(4, [5, 1, 3, 2], [(1, 2, 4), (2, 4, 4), (1, 3, 1), (3, 4, 2), (1, 4, 10)],
    [(1, 4, 0), (1, 4, 1), (1, 4, 3), (4, 1, 2), (2, 3, 5), (2, 3, 4)])
add(5, [2, 4, 6, 8, 10], [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (1, 5, 9), (2, 4, 3)],
    [(1, 5, 8), (1, 5, 7), (5, 2, 8), (5, 2, 6), (3, 1, 3)])
add(4, [3, 3, 3, 3], [(1, 2, 2), (2, 3, 2), (3, 1, 5), (1, 2, 1)], [(3, 1, 2), (3, 1, 3), (4, 1, 3), (2, 2, 1)])
add(2, [MAXH, MAXH], [(1, 2, MAXW), (2, 1, MAXW - 1)], [(1, 2, 0), (2, 1, MAXH), (2, 2, 5)])
for n, m, q, wmax, hmax in ((6, 9, 30, 10, 5), (10, 20, 60, 20, 10), (20, 40, 100, 100, 1000), (50, 120, 300, 10**4, 50)):
    h = [ri(1, hmax) for _ in range(n)]
    add(n, h, rnd_roads(n, m, 1, wmax), rnd_q(n, q, h))
n = 30                                                            # a path: the order of levels matters
h = [ri(1, 100) for _ in range(n)]
add(n, h, [(i, i + 1, ri(1, 9)) for i in range(1, n)], rnd_q(n, 200, h))
n = 120
h = [ri(1, MAXH) for _ in range(n)]
add(n, h, rnd_roads(n, 500, 1, MAXW), rnd_q(n, 2000, h))
n = 200
h = [ri(1, MAXH) for _ in range(n)]
add(n, h, rnd_roads(n, 300, 1, 1000, conn=False), rnd_q(n, 1500, h))
# hidden: largest
N, M, Q = MAXN, MAXM, MAXQ
h = [ri(1, MAXH) for _ in range(N)]
add(N, h, rnd_roads(N, M, 1, MAXW), rnd_q(N, Q, h))
h = [ri(1, MAXH) for _ in range(N)]
add(N, h, rnd_roads(N, 30_000, 1, MAXW), rnd_q(N, Q, h))
h = [ri(1, 20) for _ in range(N)]                                 # many equal levels
add(N, h, rnd_roads(N, M, 1, 1000), rnd_q(N, Q, h))
h = [ri(1, MAXH) for _ in range(N)]                               # a path with the largest lengths
add(N, h, [(i, i + 1, MAXW) for i in range(1, N)], [(1, N, MAXH)] * 10 + rnd_q(N, Q - 10, h))
h = list(range(1, N + 1))                                         # a path, levels rise along it
qs = []
for _ in range(Q):
    u = ri(1, 200)
    v = ri(u, N)
    qs.append((u, v, max(0, v - ri(0, 3))) if random.random() < 0.8 else (v, u, ri(0, N)))
roads = [(i, i + 1, ri(1, 1000)) for i in range(1, N)] + [(1, N, MAXW)] + rnd_roads(N, 25_000, 10**8, MAXW, conn=False)
random.shuffle(roads)
add(N, h, roads, qs)
h = [ri(1, MAXH) for _ in range(N)]                               # only roads from a hub to everybody
hub = ri(1, N)
h[hub - 1] = MAXH
roads = [(hub, v, ri(1, MAXW)) for v in range(1, N + 1) if v != hub] + rnd_roads(N, 300, MAXW // 2, MAXW, conn=False)
add(N, h, roads, rnd_q(N, Q // 2, h) + [(ri(1, N), ri(1, N), MAXH - ri(0, 1)) for _ in range(Q // 2)])
h = [ri(1, MAXH) for _ in range(N)]                               # complete graph, lengths almost equal
roads = [(a, b, ri(10**8, 10**8 + 1000)) for a in range(1, N + 1) for b in range(a + 1, N + 1)]
random.shuffle(roads)
add(N, h, roads[:M], rnd_q(N, Q, h))
h = [ri(1, MAXH) for _ in range(N)]                               # two groups of towns joined by few roads
roads = rnd_roads(N // 2, M // 2 - 5, 1, 10**6) + [(a + N // 2, b + N // 2, w) for a, b, w in rnd_roads(N // 2, M // 2 - 5, 1, 10**6)]
roads += [(ri(1, N // 2), ri(N // 2 + 1, N), ri(1, 10**6)) for _ in range(10)]
add(N, h, roads, rnd_q(N, Q, h))
h = [ri(1, MAXH) for _ in range(N)]
add(N, h, rnd_roads(N, M, 1, 10), rnd_q(N, Q, h, "levels"))
h = [ri(1, MAXH) for _ in range(N)]                               # every k below all levels: direct roads only
add(N, h, rnd_roads(N, M, 1, MAXW), [(ri(1, N), ri(1, N), ri(0, min(h) - 1)) for _ in range(Q)])
h = [ri(1, MAXH) for _ in range(N)]                               # every k above all levels: plain shortest paths
add(N, h, rnd_roads(N, 1000, 1, MAXW), [(ri(1, N), ri(1, N), ri(max(h), MAXH)) for _ in range(Q)])
# a grid of 20 x 20 towns
h = [ri(1, MAXH) for _ in range(N)]
roads = []
for r in range(20):
    for c in range(20):
        v = r * 20 + c + 1
        if c + 1 < 20:
            roads.append((v, v + 1, ri(1, 10**6)))
        if r + 1 < 20:
            roads.append((v, v + 20, ri(1, 10**6)))
add(N, h, roads, [(1, N, ri(0, MAXH)) for _ in range(Q // 2)] + rnd_q(N, Q // 2, h))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

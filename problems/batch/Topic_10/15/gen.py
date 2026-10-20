# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import heapq, os, random

random.seed(80150)
MAXN, MAXM, MAXK, MAXW, MAXC = 100_000, 100_000, 100_000, 10**6, 10**12
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads, shel):
    m, k = len(roads), len(shel)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= k <= MAXK
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in roads)
    assert all(1 <= s <= n and 0 <= c <= MAXC for s, c in shel)
    tests.append(f"{n} {m} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads)
                 + "".join(f"{s} {c}\n" for s, c in shel))


def dist_to(n, roads, s):
    """shortest time from every town to town s (Dijkstra on reversed roads)"""
    rev = [[] for _ in range(n + 1)]
    for u, v, w in roads:
        rev[v].append((u, w))
    d = [None] * (n + 1)
    d[s] = 0
    pq = [(0, s)]
    while pq:
        x, v = heapq.heappop(pq)
        if x != d[v]:
            continue
        for u, w in rev[v]:
            if d[u] is None or x + w < d[u]:
                d[u] = x + w
                heapq.heappush(pq, (d[u], u))
    return d


def rnd_roads(n, m, wmax, conn=True):
    roads = []
    if conn:                                   # a random spanning structure towards random earlier towns
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        for i in range(1, n):
            a, b = perm[i], perm[ri(0, i - 1)]
            roads.append((a, b, ri(1, wmax)) if random.random() < 0.8 else (b, a, ri(1, wmax)))
    while len(roads) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            roads.append((u, v, ri(1, wmax)))
    random.shuffle(roads)
    return roads[:m]


def cyc_roads(n, m, wmax):
    """one big directed cycle through all towns in random order plus random chords (strongly connected)"""
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    roads = [(perm[i], perm[(i + 1) % n], ri(1, wmax)) for i in range(n)]
    while len(roads) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            roads.append((u, v, ri(1, wmax)))
    random.shuffle(roads)
    return roads


def rnd_shel(n, k, clo, chi):
    return [(ri(1, n), ri(clo, chi)) for _ in range(k)]


# samples
add(6, [(1, 2, 3), (2, 5, 4), (1, 3, 2), (3, 4, 6), (4, 5, 1)], [(5, 20), (4, 9)])
add(4, [(1, 2, 5), (2, 3, 4), (4, 3, 8)], [(3, 8), (4, 0)])
add(3, [(1, 2, 7), (1, 2, 3), (3, 1, 5)], [(2, 10), (2, 4)])
add(4, [(1, 2, 5), (2, 1, 5), (3, 4, 1)], [(2, 100)])
add(1, [], [(1, MAXC)])
# hidden: small
add(2, [(1, 2, 1)], [(2, 0)])                                    # town 1 is one minute too late
add(2, [(2, 1, MAXW)], [(1, MAXW)])                              # exactly on time: 0
for n, m, k, wmax in ((8, 14, 2, 9), (30, 60, 5, 20), (200, 500, 20, 100), (1000, 3000, 50, 1000)):
    roads = rnd_roads(n, m, wmax, conn=(n != 30))
    add(n, roads, rnd_shel(n, k, 0, wmax * 6))
n = 2000                                                          # answers exactly 0 or -1 for many towns
roads = rnd_roads(n, 5000, 1000)
d = dist_to(n, roads, 1)
far = max(x for x in d[1:] if x is not None)
add(n, roads, [(1, far // 2)])
roads = [(i, i + 1, ri(1, MAXW)) for i in range(1, 1000)]       # town 1 has exactly 0 minutes to spare
add(1000, roads, [(1000, sum(w for _, _, w in roads)), (500, 1)])
n = 3000
roads = rnd_roads(n, 6000, 10**4)
add(n, roads, rnd_shel(n, 1500, 0, 4 * 10**4))                  # many shelters, also several in one town
# hidden: large
N = MAXN
roads = [(i, i + 1, MAXW) for i in range(1, N)]                  # one long chain, largest times
add(N, roads, [(N, MAXC)])
roads = [(i, i + 1, ri(1, 10)) for i in range(1, N)]             # chain, a shelter in every town:
c, shel = 0, []                                                  # each new one beats the earlier ones
for i in range(1, N + 1):
    c += 20
    shel.append((i, c))
add(N, roads, shel)
roads = [(i + 1, i, ri(1, MAXW)) for i in range(1, N)]           # chain the other way, decreasing times
shel = [(i, MAXC - (i - 1) * 9 * 10**6) for i in range(1, N + 1, 2)]
add(N, roads, shel)
roads = [(i, i + 1, 10) for i in range(1, N)]                   # chain, shelters listed by decreasing time:
add(N, roads, [(i, 5 * i) for i in range(N, 0, -1)])             # every town is best served by its own shelter
roads = cyc_roads(70_000, MAXM, MAXW)
add(70_000, roads, rnd_shel(70_000, 35_000, 0, 3 * 10**9))
roads = cyc_roads(N, MAXM, 1000)
add(N, roads, rnd_shel(N, 20_000, 0, 10**6))
roads = cyc_roads(80_000, MAXM, MAXW)
add(80_000, roads, rnd_shel(80_000, 60_000, MAXC - 10**10, MAXC))
roads = cyc_roads(N, MAXM, MAXW)
add(N, roads, rnd_shel(N, 1, 2 * 10**10, 4 * 10**10))
roads = [(i, 1, ri(1, MAXW)) for i in range(2, N + 1)]           # star into town 1
roads += [(1, ri(2, N), ri(1, MAXW)) for _ in range(MAXM - len(roads))]
random.shuffle(roads)
add(N, roads, [(1, ri(0, MAXW))] + rnd_shel(N, 999, 0, 2 * MAXW))
# near shelters close early, far shelters close late
roads = cyc_roads(N, MAXM, 100)
shel = [(v, ri(0, 50)) for v in random.sample(range(1, N + 1), 30_000)]
shel += [(v, ri(10**6, 2 * 10**6)) for v in random.sample(range(1, N + 1), 30)]
random.shuffle(shel)
add(N, roads, shel)
# layered graph: every town of a layer goes to several towns of the next one
L, W = 200, N // 200
roads = []
for a in range(L - 1):
    for b in range(W):
        u = a * W + b + 1
        for _ in range(2):
            roads.append((u, (a + 1) * W + ri(0, W - 1) + 1, ri(1, 10**4)))
roads = roads[:MAXM]
shel = [((L - 1) * W + b + 1, ri(0, 3 * 10**6)) for b in range(W)]
shel += rnd_shel(N, 20_000, 0, 10**6)
add(N, roads, shel)
roads = rnd_roads(N, MAXM, MAXW, conn=False)                    # many towns reach nothing
add(N, roads, rnd_shel(N, 50_000, 0, MAXC))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

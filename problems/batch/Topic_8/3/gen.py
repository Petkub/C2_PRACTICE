# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(8003)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, st, roads):
    m, k = len(roads), len(st)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= k <= n
    assert len(set(st)) == k and all(1 <= s <= n for s in st)
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n} {m} {k}\n" + " ".join(map(str, st)) + "\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def relabel(n, st, roads):
    """random intersection numbers, random order and direction of roads, random order of stations"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    p = [0] + p
    res = [(p[u], p[v], w) if random.random() < 0.5 else (p[v], p[u], w) for u, v, w in roads]
    random.shuffle(res)
    s = [p[x] for x in st]
    random.shuffle(s)
    return n, s, res


def stations(n, k):
    return random.sample(range(1, n + 1), k)


def rnd_roads(n, m, wmax=MAXW):
    return [(ri(1, n), ri(1, n), ri(1, wmax)) for _ in range(m)]


def connected(n, m, wmax=MAXW, depth=0):
    """a random tree (thin when depth > 0) plus random extra roads"""
    if depth:
        roads = [(i, ri(max(1, i - depth), i - 1), ri(1, wmax)) for i in range(2, n + 1)]
    else:
        roads = [(i, ri(1, i - 1), ri(1, wmax)) for i in range(2, n + 1)]
    return roads + rnd_roads(n, m - (n - 1), wmax)


def grid(r, c, wmax):
    roads = []
    for i in range(r):
        for j in range(c):
            v = i * c + j + 1
            if j + 1 < c:
                roads.append((v, v + 1, ri(1, wmax)))
            if i + 1 < r:
                roads.append((v, v + c, ri(1, wmax)))
    return roads


def broom(n, m, k, rest):
    """stations 1..k all joined to one centre, a larger station number is closer to it; the town hangs off the centre"""
    c = k + 1
    roads = [(i, c, k - i + 1) for i in range(1, k + 1)]
    sub = rest(n - k, m - k)                     # roads among c..n (renumbered from 1..n-k)
    roads += [(u + k, v + k, w) for u, v, w in sub]
    p = list(range(c + 1, n + 1))                # shuffle the town, keep the station numbers
    random.shuffle(p)
    p = list(range(0, c + 1)) + p
    roads = [(p[u], p[v], w) for u, v, w in roads]
    random.shuffle(roads)
    st = list(range(1, k + 1))
    return n, st, roads


# samples
add(6, [5, 2], [(1, 2, 4), (2, 3, 3), (3, 4, 2), (4, 5, 3), (5, 6, 1), (1, 6, 3)])
add(5, [4], [(4, 3, 7), (3, 4, 2), (1, 2, 5)])
add(7, [7, 1], [(i, i + 1, 2) for i in range(1, 7)])
add(5, [3, 1, 5], [(1, 2, 6), (2, 3, 4), (2, 4, 1), (4, 5, 3), (3, 5, 9), (2, 2, 1)])
add(1, [1], [])
# hidden: small
add(2, [2], [(1, 2, MAXW), (1, 2, MAXW)])
add(3, [1, 2, 3], [(1, 2, 1), (2, 3, 1)])
add(10, stations(10, 3), rnd_roads(10, 12, 3))
add(40, stations(40, 5), connected(40, 60, 4))
add(60, stations(60, 8), grid(6, 10, 1))
add(300, stations(300, 20), rnd_roads(300, 400, 10))
add(*relabel(1000, list(range(1, 11)), [(i, i + 1, 1) for i in range(1, 1000)]))
add(2000, stations(2000, 50), connected(2000, 3000, 1000, 3))
# hidden: large
N, M = MAXN, MAXM
add(N, stations(N, 1), connected(N, M))
add(N, stations(N, 1000), connected(N, M, 10, 3))
add(N, stations(N, N // 2), connected(N, M, 3))                       # many ties
add(N, list(range(1, N + 1)), rnd_roads(N, M))                      # every intersection has a station
add(N, list(range(1, N // 2 + 1)), [(i, i + 1, 1) for i in range(1, N)])   # chain, stations on the left half
add(N, list(range(N // 2, 0, -1)), [(i, i + 1, 1) for i in range(N - 1, 0, -1)])
add(*relabel(N, list(range(1, N // 2 + 1)), [(i, i + 1, ri(1, 3)) for i in range(1, N)]))
add(*relabel(N, stations(N, 2000), grid(250, 400, 1)[:M]))          # grid, equal roads: ties everywhere
add(N, stations(N, 5000), grid(250, 400, MAXW)[:M])
add(N, stations(N, 300), rnd_roads(N, M))                           # many intersections unreachable
add(*broom(N, M, 1000, lambda n, m: connected(n, m, 100, 3)))
add(*broom(N, M, 300, lambda n, m: connected(n, m, 1000)))
add(*broom(N, M, 3000, lambda n, m: grid(97, n // 97, 5)[:m] + rnd_roads(n, max(0, m - len(grid(97, n // 97, 5))), 5)))
roads = [(i, i + 1, MAXW) for i in range(1, N)]                      # one station at the end: largest distances
add(N, [N], roads)
n = N - 1                                                            # exact tie in the middle (n odd); the
path = [1] + list(range(n - 1, 1, -1)) + [n]                         # side of station 1 has the large numbers
add(n, [n, 1], [(path[i], path[i + 1], MAXW) for i in range(n - 1)])
k, leaves = 30_000, M - 60_000                                       # one hub improved many times
roads = []
for i in range(2, k + 2):
    roads.append((1, i, i))
    roads.append((i, N, 3 * k + 10 - 2 * i))
roads += [(N, x, ri(1, 5)) for x in range(k + 2, k + 2 + leaves)]
add(N, [1] + list(range(N - 99, N)), roads)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

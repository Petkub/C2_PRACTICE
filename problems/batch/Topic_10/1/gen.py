# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(8001)
MAXN, MAXM, MAXW, MAXC = 100_000, 100_000, 10**6, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, c, roads):
    m = len(roads)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and len(c) == n
    assert all(0 <= x <= MAXC for x in c)
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n} {m}\n" + " ".join(map(str, c)) + "\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def relabel(n, roads):
    """random numbers for intersections 2..n (the warehouse stays 1), random order and direction of roads"""
    p = list(range(2, n + 1))
    random.shuffle(p)
    p = [0, 1] + p
    res = [(p[u], p[v], w) if random.random() < 0.5 else (p[v], p[u], w) for u, v, w in roads]
    random.shuffle(res)
    return res


def rnd_c(n, hi=MAXC):
    return [ri(0, hi) for _ in range(n)]


def rnd_roads(n, m, wmax=MAXW):
    return [(ri(1, n), ri(1, n), ri(1, wmax)) for _ in range(m)]


def connected(n, m, wmax=MAXW):
    """a random tree plus random extra roads"""
    roads = [(i, ri(1, i - 1), ri(1, wmax)) for i in range(2, n + 1)]
    return roads + rnd_roads(n, m - (n - 1), wmax)


def deep(n, m, wsmall, wbig):
    """a long thin tree with short roads plus random long roads (shortest paths have many roads)"""
    roads = [(i, ri(max(1, i - 3), i - 1), ri(1, wsmall)) for i in range(2, n + 1)]
    roads += [(ri(1, n), ri(1, n), ri(wbig // 2, wbig)) for _ in range(m - (n - 1))]
    return relabel(n, roads)


def hub(k, leaves):
    """many paths improve one hub again and again; the hub has many neighbours"""
    n = k + leaves + 2                           # 2..k+1 middle, k+2..n-1 leaves, n hub
    roads, H, B = [], n, 3 * k + 10
    for i in range(2, k + 2):
        roads.append((1, i, i))                  # reached in the order 2, 3, ..., k+1
        roads.append((i, H, B - 2 * i))          # each one gives the hub a smaller distance B - i
    for x in range(k + 2, n):
        roads.append((H, x, ri(1, 5)))
    return n, [0] * n, roads


# samples
add(5, [7, 1, 10, 2, 3], [(1, 2, 3), (2, 3, 2), (1, 3, 1), (3, 4, 4), (2, 4, 9), (4, 5, 1)])
add(4, [0, 5, 0, 1], [(1, 2, 4), (2, 1, 2), (2, 2, 1), (3, 3, 5)])
add(5, [4, 0, 6, 1, 2], [(1, 2, 5), (1, 3, 1), (3, 2, 1), (2, 4, 2), (3, 4, 6), (4, 5, 1)])
add(5, [1, 2, 3, 4, 5], [(5, 4, 1), (4, 3, 1), (3, 2, 1), (2, 1, 1), (1, 5, 9)])
add(1, [9], [(1, 1, 3)])
# hidden: small
add(3, [MAXC] * 3, [(1, 2, MAXW), (2, 3, MAXW)])
add(2, [5, 5], [(2, 2, 1)])
add(2, [0, 0], [(2, 1, 7), (1, 2, 3), (1, 2, 5)])
add(8, rnd_c(8, 10), rnd_roads(8, 10, 10))
add(30, rnd_c(30, 20), connected(30, 45, 20))
add(60, [0] * 60, relabel(60, [(i, i + 1, 1) for i in range(1, 60)] + rnd_roads(60, 30, 60)))
add(300, rnd_c(300), rnd_roads(300, 400))
add(2000, rnd_c(2000, 100), connected(2000, 3000, 100))
add(3000, rnd_c(3000, 5), relabel(3000, [(i, i + 1, ri(1, 3)) for i in range(1, 3000)] + rnd_roads(3000, 500, 3000)))
# hidden: large
N = MAXN
add(N, rnd_c(N), [(i, i + 1, ri(1, MAXW)) for i in range(N - 1, 0, -1)])   # chain listed from the far end
add(N, [MAXC] * N, relabel(N, [(i, i + 1, MAXW) for i in range(1, N)]))   # the largest distances
add(N, rnd_c(N), connected(N, MAXM))
add(N, rnd_c(N, 10), deep(N, MAXM, 10, 1000))                             # many equal distances
add(N, [0] * N, deep(N, MAXM, 1, 1))                                      # all equal weights
add(N, rnd_c(N, 1000), deep(N, MAXM, 1000, MAXW))
n, c, roads = hub(30_000, MAXM - 60_000)
add(n, c, roads)
c = rnd_c(N, 100)
side = 250                                                                # 250 x 400 grid
grid = []
for r in range(side):
    for q in range(N // side):
        v = r * (N // side) + q + 1
        if q + 1 < N // side:
            grid.append((v, v + 1, ri(1, MAXW)))
        if r + 1 < side:
            grid.append((v, v + N // side, ri(1, 10)))
add(N, c, relabel(N, grid[:MAXM]))
k = 300                                                                   # a dense part and a long tail
roads = [(ri(1, k), ri(1, k), ri(1, MAXW)) for _ in range(MAXM - (N - k))]
roads += [(i, i + 1, ri(1, 1000)) for i in range(k, N)]
add(N, rnd_c(N), relabel(N, roads))
roads = [(1, i, 3 * i) for i in range(2, N // 2 + 2)]                    # star: shortcuts lose to the chain
roads += [(i, i + 1, 1) for i in range(N // 2, 1, -1)]
add(N, [0] * N, roads)
add(N, rnd_c(N), rnd_roads(N, MAXM))                                      # several components
roads = deep(N // 2, MAXM - N // 4, 100, MAXW)                           # half the town unreachable
roads += [(ri(N // 2 + 1, N), ri(N // 2 + 1, N), ri(1, MAXW)) for _ in range(N // 4)]
add(N, rnd_c(N, 100), roads)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

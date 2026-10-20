# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7002)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads):
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n for u, v in roads)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v}\n" for u, v in roads))


def relabel(n, roads, keep_order=False):
    """random numbers for intersections 2..n (home stays 1), random order of roads"""
    p = list(range(2, n + 1))
    random.shuffle(p)
    p = [1] + p
    res = [(p[u - 1], p[v - 1]) for u, v in roads]
    if not keep_order:
        random.shuffle(res)
    return res


def rnd_roads(n, m, loops=True):
    res = []
    while len(res) < m:
        u, v = ri(1, n), ri(1, n)
        if loops or u != v:
            res.append((u, v))
    return res


# samples
add(5, [(2, 1), (3, 2), (1, 4), (4, 3), (5, 4)])
add(4, [(1, 2), (2, 3), (3, 1)])
add(1, [])
add(3, [(2, 2), (3, 1), (3, 1), (1, 2)])
add(6, [(4, 1), (2, 4), (2, 5), (5, 6), (6, 1), (3, 2), (1, 3)])
add(4, [])
# hidden: small
add(1, [(1, 1), (1, 1)])
add(2, [(1, 2)])                                     # only away from home
add(2, [(2, 1), (1, 2), (2, 1)])
add(8, [(i, i + 1) for i in range(1, 8)])            # all roads point away from home
add(8, [(i + 1, i) for i in range(1, 8)])
add(10, rnd_roads(10, 12))
add(30, rnd_roads(30, 40))
add(60, relabel(60, [(i + 1, i) for i in range(1, 60)] + rnd_roads(60, 30)))
add(300, rnd_roads(300, 450))
add(3000, rnd_roads(3000, 4000))
add(5000, relabel(5000, [(i + 1, i) for i in range(1, 5000)]))
# hidden: large
N = MAXN
add(N, [(i + 1, i) for i in range(N - 1, 0, -1)])    # chain N -> ... -> 1, roads listed from the far end
add(N, relabel(N, [(i + 1, i) for i in range(1, N)]))
add(N, relabel(N, [(i, i + 1) for i in range(1, N)] + [(N, 1)]))   # one big cycle through home
add(N, [(i, 1) for i in range(2, N + 1)])            # everyone is one road from home
add(N, [(1, i) for i in range(2, N + 1)])            # nobody can come back
add(N, rnd_roads(N, MAXM))
add(N, rnd_roads(N, N // 2 * 3 // 2))
tree = [(i, ri(max(1, i - 3), i - 1)) for i in range(2, N + 1)]     # a long thin tree pointing home
add(N, relabel(N, tree))
half = N // 2                                        # long chain home, the other half pointing away
add(N, relabel(N, [(i + 1, i) for i in range(1, half)] + [(i, i + 1) for i in range(half, N)]
              + [(ri(1, N), ri(1, N)) for _ in range(MAXM - N + 1)]))
add(N, relabel(N, [(i + 1, i) for i in range(N - 1, 0, -1)], keep_order=True))  # far end first, random numbers
add(N, [(ri(1, N), ri(1, N)) for _ in range(MAXM - N // 2)] + [(v, v) for v in range(1, N // 2 + 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

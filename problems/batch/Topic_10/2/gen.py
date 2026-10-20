# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(8002)
MAXN, MAXM, MAXQ, MAXT = 400, 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, routes, qs):
    m, q = len(routes), len(qs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= t <= MAXT for a, b, t in routes)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {t}\n" for a, b, t in routes)
                 + f"{q}\n" + "".join(f"{u} {v}\n" for u, v in qs))


def perm(n, routes):
    """random stop numbers and random order of routes"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    p = [0] + p
    res = [(p[a], p[b], t) for a, b, t in routes]
    random.shuffle(res)
    return res


def rnd_routes(n, m, tmax=MAXT, tmin=1):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b, ri(tmin, tmax)))
    return res


def rnd_qs(n, q):
    return [(ri(1, n), ri(1, n)) for _ in range(q)]


def chain_heavy(n, m, tsmall, tbig):
    """a hidden chain (in both directions) of short routes plus random long routes"""
    res = [(i, i + 1, ri(1, tsmall)) for i in range(1, n)] + [(i + 1, i, ri(1, tsmall)) for i in range(1, n)]
    return perm(n, res + rnd_routes(n, m - len(res), tbig, tbig // 2))


# samples
add(4, [(1, 2, 5), (2, 3, 3), (1, 3, 10), (3, 1, 2)], [(1, 3), (3, 2), (4, 1)])
add(3, [(1, 2, 7), (1, 2, 4), (2, 1, 1)], [(1, 2), (1, 3), (3, 3)])
add(2, [], [(1, 2), (2, 2)])
add(3, [(1, 2, MAXT), (2, 3, MAXT)], [(1, 3), (3, 1)])
add(5, [(4, 1, 3), (1, 2, 1), (2, 5, 1), (1, 5, 4), (5, 4, 1)], [(4, 5), (5, 2)])
# hidden: small
add(1, [], [(1, 1)])
add(2, [(1, 2, 3), (2, 1, 3), (1, 2, 1)], [(1, 2), (2, 1), (1, 1), (2, 2)])
add(8, rnd_routes(8, 12, 10), [(u, v) for u in range(1, 9) for v in range(1, 9)])
add(20, rnd_routes(20, 40, 50), rnd_qs(20, 200))
add(30, chain_heavy(30, 100, 10, 1000), rnd_qs(30, 300))
add(60, rnd_routes(60, 300, 10**6), rnd_qs(60, 500))
add(100, perm(100, [(i, i + 1, MAXT) for i in range(1, 100)]), rnd_qs(100, 500))
add(150, chain_heavy(150, 3000, 100, 10**5), rnd_qs(150, 1000))
# hidden: large
N, M, Q = MAXN, MAXM, MAXQ
add(N, rnd_routes(N, M), rnd_qs(N, Q))
add(N, rnd_routes(N, M, 10), rnd_qs(N, Q))                    # many equal times
add(N, chain_heavy(N, M, 1000, MAXT), rnd_qs(N, Q))           # fastest ways use many stops
add(N, chain_heavy(N, M, 1, 2), rnd_qs(N, Q))
add(N, perm(N, [(i, i + 1, MAXT) for i in range(1, N)] + rnd_routes(N, M - N + 1, MAXT, MAXT)),
    rnd_qs(N, Q))                                             # the largest times
r = [(i, i + 1, MAXT) for i in range(1, N)]                   # one-way chain: half of the questions are -1
r += [(a, b, MAXT) for a, b, t in rnd_routes(N, M - N + 1) if a < b]
add(N, perm(N, r), rnd_qs(N, Q))
h = N // 2                                                    # two halves, only one way across
r = [(ri(1, h), ri(1, h), ri(1, MAXT)) for _ in range(M // 2)] + [(ri(h + 1, N), ri(h + 1, N), ri(1, MAXT))
                                                                  for _ in range(M // 2 - 5)]
r = [(a, b, t) for a, b, t in r if a != b] + [(ri(1, h), ri(h + 1, N), ri(1, MAXT)) for _ in range(5)]
add(N, perm(N, r), rnd_qs(N, Q))
add(N, chain_heavy(N, 2 * N + 200, 10**6, MAXT), rnd_qs(N, Q))  # few routes
add(N, [(a, b, ri(1, MAXT)) for a in range(1, N + 1) for b in range(1, N + 1) if a != b][:M], rnd_qs(N, Q))
add(N, chain_heavy(N, M, 10**5, MAXT), [(1, N)] * Q)
add(N, rnd_routes(N, M, MAXT, MAXT - 10), [(u, u) for u in range(1, N + 1)] * (Q // N))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

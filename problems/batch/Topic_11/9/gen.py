# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90901)
MAXN, MAXM, MAXQ, MAXC = 100_000, 100_000, 100_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads, qs):
    m, q = len(roads), len(qs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= c <= MAXC for (u, v, c) in roads)
    assert all(1 <= v <= n and 1 <= w <= MAXC for (v, w) in qs)
    tests.append(f"{n} {m} {q}\n" + "".join(f"{u} {v} {c}\n" for (u, v, c) in roads)
                 + "".join(f"{v} {w}\n" for (v, w) in qs))


def relabel(n, roads):
    p = list(range(1, n + 1))
    random.shuffle(p)
    res = [(p[u - 1], p[v - 1], c) if random.random() < 0.5 else (p[v - 1], p[u - 1], c) for (u, v, c) in roads]
    random.shuffle(res)
    return res


def tree(n, cmax=MAXC, cmin=1):
    return [(ri(1, v - 1), v, ri(cmin, cmax)) for v in range(2, n + 1)]


def extra(n, k, cmax=MAXC, cmin=1):
    res = []
    while len(res) < k:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            res.append((u, v, ri(cmin, cmax)))
    return res


def queries(n, q, roads, low=1, high=MAXC, near=0.3):
    cs = [c for (_, _, c) in roads] or [1]
    res = []
    for _ in range(q):
        if random.random() < near:
            w = min(MAXC, max(1, random.choice(cs) + ri(0, 1)))   # exactly a limit or one more
        else:
            w = ri(low, high)
        res.append((ri(1, n), w))
    return res


# samples
add(5, [(1, 2, 5), (2, 3, 3), (3, 4, 8), (4, 5, 2), (2, 5, 6)], [(1, 4), (1, 3), (4, 9)])
add(3, [(1, 2, 2), (1, 2, 7), (3, 2, 4)], [(1, 7), (3, 5), (3, 4)])
add(4, [], [(2, 1), (4, 1000000)])
add(4, [(1, 2, 10), (2, 3, 20), (3, 4, 10), (4, 1, 30)], [(1, 30), (3, 11), (4, 10)])
add(3, [(1, 3, 5), (3, 2, 5)], [(2, 5), (2, 6)])
# hidden: small
add(1, [], [(1, 1)])
add(2, [(1, 2, 1000000)], [(1, 1000000), (2, 1), (1, 999999)])
n = 8
r = relabel(n, tree(n, 10) + extra(n, 6, 10))
add(n, r, queries(n, 30, r, 1, 11))
n = 50
r = relabel(n, tree(n, 100) + extra(n, 40, 100))
add(n, r, queries(n, 200, r, 1, 101))
n = 300
r = relabel(n, extra(n, 250, 1000))
add(n, r, queries(n, 1000, r, 1, 1000))
n = 2000
r = relabel(n, [(i, i + 1, ri(1, MAXC)) for i in range(1, n)])
add(n, r, queries(n, 3000, r))
n = 3000
r = relabel(n, tree(n, 5) + extra(n, 3000, 5))                 # many equal limits
add(n, r, queries(n, 5000, r, 1, 6, 0.5))
# hidden: maximum size
N, M, Q = MAXN, MAXM, MAXQ
r = relabel(N, tree(N) + extra(N, M - N + 1))
add(N, r, queries(N, Q, r, 1, 10**5))                          # light trucks: huge reachable areas
r = relabel(N, [(i, i + 1, ri(1, MAXC)) for i in range(1, N)])
add(N, r, queries(N, Q, r, 1, 2000, 0.1))
r = relabel(N, [(i, i + 1, MAXC - i) for i in range(1, N)])    # limits fall along a path
add(N, r, queries(N, Q, r, MAXC - N, MAXC))
r = relabel(N, [(1, v, ri(1, MAXC)) for v in range(2, N + 1)])  # star
add(N, r, queries(N, Q, r, 1, 3000, 0.2))
r = relabel(N, tree(N, 1, 1))                                  # every limit 1
add(N, r + [(1, 2, 1)], [(ri(1, N), ri(1, 2)) for _ in range(Q)])
r = relabel(N, tree(N, 10) + extra(N, M - N + 1, 10))          # limits 1..10
add(N, r, queries(N, Q, r, 1, 11))
r = relabel(N, tree(N) + extra(N, M - N + 1))
add(N, r, queries(N, Q, r))
r = []
for k in range(0, N, 1000):                                    # 100 separate groups
    for v in range(k + 2, k + 1001):
        r.append((ri(k + 1, v - 1), v, ri(1, MAXC)))
r = relabel(N, r)
add(N, r, queries(N, Q, r, 1, 10**5))
r = relabel(N, tree(N, MAXC, MAXC - 1000))                     # the largest limits
add(N, r, queries(N, Q, r, MAXC - 1100, MAXC, 0.5))
r = relabel(N, [(i, i + 1, ri(1, 10)) for i in range(1, N)])   # long path with few distinct limits
add(N, r, [(ri(1, N), 1) for _ in range(Q // 2)] + queries(N, Q // 2, r, 1, 11))
r = relabel(N, [(ri(1, 10), ri(11, N), ri(1, MAXC)) for _ in range(M)])   # parallel roads to few hubs
add(N, r, queries(N, Q, r, 1, 10**5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

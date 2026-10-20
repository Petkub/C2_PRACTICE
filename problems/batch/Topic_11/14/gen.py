# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(91401)
MAXN, MAXM, MAXA, MAXW = 100_000, 50_000, 10**6, 2 * 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, b, offers):
    n, m = len(a), len(offers)
    assert 1 <= n <= MAXN and len(b) == n and 0 <= m <= MAXM
    assert all(1 <= x <= MAXA for x in a + b)
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for (u, v, w) in offers)
    tests.append(f"{n} {m}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"
                 + "".join(f"{u} {v} {w}\n" for (u, v, w) in offers))


def pair(n):
    u = ri(1, n)
    v = ri(1, n - 1)
    return (u, v + 1 if v >= u else v)


def offers_rnd(n, m, lo, hi):
    return [pair(n) + (ri(lo, hi),) for _ in range(m)]


def offers_cheap_tree(n, m, a, frac):
    """offers a bit cheaper than the normal cable, many of them along a random tree"""
    res = []
    for _ in range(m):
        if random.random() < frac:
            v = ri(2, n)
            u = ri(1, v - 1)
        else:
            u, v = pair(n)
        w = max(1, a[u - 1] + a[v - 1] - ri(0, 2 * MAXA // 3))
        res.append((u, v, w))
    return res


# samples
add([1, 5, 3, 4], [10, 10, 2, 10], [(2, 4, 3)])
add([10, 10, 10], [3, 4, 25], [])
add([7], [9], [])
add([2, 2, 9, 4], [50, 50, 50, 1], [(1, 2, 9), (3, 1, 1), (3, 1, 20), (4, 2, 3)])
add([6, 3, 8, 3, 5, 9], [20, 30, 5, 40, 12, 7], [(1, 5, 4), (6, 3, 11), (2, 6, 13)])
# hidden: small
add([1, 1], [1, 1], [(1, 2, 1)])
add([MAXA, MAXA], [MAXA, MAXA], [(2, 1, MAXW)])
n = 8
add([ri(1, 20) for _ in range(n)], [ri(1, 60) for _ in range(n)], offers_rnd(n, 6, 1, 30))
n = 50
a = [ri(1, 100) for _ in range(n)]
add(a, [ri(1, 300) for _ in range(n)], offers_cheap_tree(n, 60, a, 0.5))
n = 500
add([ri(1, 1000) for _ in range(n)], [ri(500, 5000) for _ in range(n)], offers_rnd(n, 500, 1, 2000))
n = 2000
a = [ri(1, MAXA) for _ in range(n)]
add(a, [ri(1, MAXA) for _ in range(n)], offers_cheap_tree(n, 2000, a, 0.7))
n = 3000
add([ri(1, 10) for _ in range(n)], [ri(1, 30) for _ in range(n)], offers_rnd(n, 3000, 1, 15))
# hidden: maximum size
N, M = MAXN, MAXM
a = [ri(1, MAXA) for _ in range(N)]
add(a, [ri(1, MAXA) for _ in range(N)], offers_rnd(N, M, 1, MAXW))
a = [ri(1, MAXA) for _ in range(N)]
add(a, [MAXA] * N, offers_cheap_tree(N, M, a, 0.8))                 # plants are expensive
a = [ri(MAXA // 2, MAXA) for _ in range(N)]
add(a, [ri(1, MAXA // 2) for _ in range(N)], offers_rnd(N, M, 1, MAXW))   # plants are cheap: many plants
add([MAXA] * N, [MAXA] * N, [pair(N) + (MAXW,) for _ in range(M)])  # all values at the maximum
add([ri(1, 10) for _ in range(N)], [ri(1, 10**4) for _ in range(N)], offers_rnd(N, M, 1, 20))
a = [ri(1000, MAXA) for _ in range(N)]
a[-1] = 1                                                        # the cheapest village is the last one
add(a, [ri(1, MAXA) for _ in range(N)], offers_rnd(N, M, 1, 3000))
a = [ri(1, MAXA) for _ in range(N)]
add(a, [ri(1, MAXA) for _ in range(N)], [])                         # no offers
a = [ri(1, MAXA) for _ in range(N)]
add(a, [ri(MAXA // 3, MAXA) for _ in range(N)], [(u, v, a[u - 1] + a[v - 1] + ri(0, 5))
                                                   for (u, v) in (pair(N) for _ in range(M))])   # useless offers
a = [5] * N                                                      # every village equally cheap
add(a, [ri(9, 15) for _ in range(N)], offers_rnd(N, M, 1, 12))
a = [ri(1, MAXA) for _ in range(N)]
b = [ri(1, MAXA) for _ in range(N)]
b[ri(0, N - 1)] = 1                                              # one very cheap plant
add(a, b, offers_cheap_tree(N, M, a, 1.0))
a = [ri(1, 100) for _ in range(N)]
add(a, [ri(50, 400) for _ in range(N)], offers_cheap_tree(N, M, a, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(170101)
MAXN, MAXQ, MAXA, MAXG, MAXH = 200_000, 200_000, 10**9, 10**6, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, g, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(g) == n
    assert all(1 <= v <= MAXA for v in a) and all(1 <= v <= MAXG for v in g)
    assert any(t == 2 for t, _, _ in ops)
    lines = []
    for t, x, y in ops:
        if t == 1:
            assert 1 <= x <= n and 1 <= y <= MAXH
        else:
            assert t == 2 and 1 <= x <= y <= n
        lines.append(f"{t} {x} {y}")
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, g)) + "\n" + "\n".join(lines) + "\n")


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def ops_of(a, g, q, pcut, rng, cut_ok=0.7, late=0.0):
    """pcut: share of cuts; rng() -> (l, r); cut_ok: share of cuts that really shorten the bamboo;
    late: share of the days (at the start) that have no cut, so the cuts come when g * day is large"""
    n = len(a)
    base = a[:]
    ops = []
    for day in range(1, q + 1):
        if day > late * q and random.random() < pcut:
            i = ri(1, n)
            cur = base[i - 1] + g[i - 1] * day
            if cur > 1 and random.random() < cut_ok:
                h = ri(1, min(cur - 1, MAXH)) if random.random() < 0.5 else max(1, min(cur - 1, MAXH) - ri(0, 20))
            else:
                h = min(MAXH, cur + ri(0, 50)) if cur <= MAXH else MAXH
            if h < cur:
                base[i - 1] = h - g[i - 1] * day
            ops.append((1, i, h))
        else:
            ops.append((2,) + rng())
    return ops


# samples
add([5, 2, 7], [1, 3, 2], [(2, 1, 3), (1, 3, 4), (2, 2, 3), (1, 2, 20), (2, 1, 3)])
add([10, 1], [5, 1], [(1, 1, 3), (2, 1, 2), (1, 1, 3), (2, 1, 1)])
add([MAXA], [MAXG], [(2, 1, 1), (1, 1, 1), (2, 1, 1)])
add([3, 1, 4], [9, 2, 6], [(1, 1, 10), (2, 1, 3), (2, 2, 2)])
add([1, 1, 1, 1], [1, 1, 1, 1], [(1, 2, 5), (1, 4, 1), (2, 1, 4)])
# hidden: small (the brute force checks these)
for n, q, amax, gmax, pcut in ((1, 6, 5, 3, 0.5), (3, 20, 10, 2, 0.4), (8, 60, 50, 10, 0.4), (30, 300, 1000, 100, 0.3),
                               (100, 800, MAXA, MAXG, 0.3), (300, 1500, 100, 5, 0.5), (200, 3000, 10, MAXG, 0.4)):
    a = [ri(1, amax) for _ in range(n)]
    g = [ri(1, gmax) for _ in range(n)]
    add(a, g, ops_of(a, g, q, pcut, lambda: any_rng(n)))
n = 50                                                      # many cuts that change nothing (h at or above the height)
a = [ri(1, 100) for _ in range(n)]
g = [ri(1, 3) for _ in range(n)]
add(a, g, ops_of(a, g, 2000, 0.5, lambda: any_rng(n), cut_ok=0.2))
# hidden: maximum size (inputs kept near 3 MB: small values where the counts are large)
N = MAXN
a = [ri(1, 1000) for _ in range(N)]
g = [ri(1, 9) for _ in range(N)]
add(a, g, ops_of(a, g, 120_000, 0.3, lambda: long_rng(N, 50)))
a = [ri(1, 1000) for _ in range(N)]
g = [ri(1, 9) for _ in range(N)]
add(a, g, ops_of(a, g, 120_000, 0.05, lambda: long_rng(N, 50)))
n = 150_000                                                 # fast growth, cuts late
a = [ri(1, 100) for _ in range(n)]
g = [ri(50_000, MAXG) for _ in range(n)]
add(a, g, ops_of(a, g, 90_000, 0.4, lambda: long_rng(n, 100), late=0.3))
n = 100_000                                                 # every value at the maximum
a = [MAXA] * n
g = [MAXG] * n
add(a, g, ops_of(a, g, 80_000, 0.3, lambda: long_rng(n, 10)))
a = [ri(1, 10_000) for _ in range(N)]                       # cut down to almost nothing, then regrow
g = [1] * N
ops = []
for day in range(1, 120_001):
    ops.append((1, ri(1, N), 1) if day % 2 else (2,) + long_rng(N, 30))
add(a, g, ops)
n = 160_000
a = [ri(1, 10**6) for _ in range(n)]
g = [ri(1, 1000) for _ in range(n)]
add(a, g, ops_of(a, g, 80_000, 0.3, lambda: long_rng(n, 20_000)))
a = [ri(1, 1000) for _ in range(N)]                         # every question asks the whole row
g = [ri(1, 99) for _ in range(N)]
add(a, g, [(2, 1, N)] * 110_000)
n = 150_000                                                 # a few fast bamboos among slow ones, cut late
g = [ri(1, 9) for _ in range(n)]
for i in random.sample(range(n), 3000):
    g[i] = ri(500_000, MAXG)
a = [ri(1, 100) for _ in range(n)]
add(a, g, ops_of(a, g, 90_000, 0.3, lambda: long_rng(n, 200), late=0.5))
n = 130_000                                                 # the fast bamboos are the ones that get cut
a = [ri(1, 1000) for _ in range(n)]
g = [MAXG if i % 2 else 1 for i in range(n)]
ops = []
for day in range(1, 90_001):
    if day > 30_000 and day % 3 == 0:
        ops.append((1, 2 * ri(1, n // 2), ri(1, MAXH)))
    else:
        ops.append((2,) + long_rng(n, 100))
add(a, g, ops)
# hidden: many short questions
n = 1000
a = [ri(1, MAXA) for _ in range(n)]
g = [ri(1, MAXG) for _ in range(n)]
add(a, g, ops_of(a, g, MAXQ, 0.5, lambda: any_rng(n)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

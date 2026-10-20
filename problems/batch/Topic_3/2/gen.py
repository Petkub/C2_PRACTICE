# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random
from itertools import accumulate

random.seed(20202)
MAXN = 200_000
MAXD = 10**9
MAXX = 10**15
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(d, xs):
    n, q = len(d), len(xs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    assert all(0 <= v <= MAXD for v in d)
    assert all(1 <= x <= MAXX for x in xs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, d)) + "\n" + " ".join(map(str, xs)) + "\n")


def goals(d, q, late=False, missing=0.0):
    """mix of goals exactly on a total, one above a total, and above the grand total"""
    pre = list(accumulate(d))
    total = pre[-1]
    lo = len(d) * 9 // 10 if late else 0
    res = []
    for _ in range(q):
        if random.random() < missing:
            res.append(min(MAXX, total + ri(1, 10**6)))
            continue
        v = pre[ri(lo, len(d) - 1)] + random.choice((0, 0, 1, -1))
        res.append(min(MAXX, max(1, v)))
    return res


# samples
add([3, 0, 4, 1, 5], [3, 4, 13, 14, 1])
add([0, 0, 2, 0, 2], [2, 3, 4, 5])
add([MAXD] * 3, [3 * MAXD, 1, 2 * MAXD + 1])
add([0], [1])
add([5, 2, 0, 0, 7, 1], [8, 7, 15, 6, 16, 14])
add([0, 0, 0, 9], [9, 10, 1])
# hidden: small
add([7], [7, 8, 1, MAXX])
add([0] * 10, [1, 2])
d = [ri(0, 3) for _ in range(30)]
add(d, list(range(1, sum(d) + 3)))
d = [random.choice((0, 0, 0, ri(1, 100))) for _ in range(500)]
add(d, goals(d, 500, missing=0.1))
d = [ri(0, MAXD) for _ in range(3000)]
add(d, goals(d, 3000, missing=0.1))
d = [MAXD] * 4000
add(d, goals(d, 4000) + [MAXX])
# hidden: maximum size (goals near the end or above the total, so scanning day by day is slow)
N = MAXN
d = [ri(0, 50_000) for _ in range(N)]                   # totals pass 2^31
add(d, goals(d, N, late=True, missing=0.2))
d = [random.choice((0, 0, 0, 0, ri(1, 50_000))) for _ in range(N)]   # many repeated totals
add(d, goals(d, N, late=True, missing=0.1))
d = [0] * (N - 1) + [MAXD]                             # every goal reached only on the last day
add(d, [ri(1, MAXD) for _ in range(N)])
d = [ri(0, 50_000) for _ in range(N)]
add(d, [MAXX] * 120_000)                                   # never reached
d = [MAXD] * N                                         # the largest totals
add(d, goals(d, 80_000, late=True, missing=0.1))
d = [ri(0, 9) for _ in range(N)]
add(d, goals(d, N, late=True))
d = [ri(0, 50_000) for _ in range(N)]
add(d, goals(d, N, missing=0.3))
d = [1] * N
add(d, [N - ri(0, 1000) for _ in range(N - 1)] + [N + 1])  # answers near the end and one -1
d = [ri(0, 1) * ri(0, 99_999) for _ in range(N)]
add(d, goals(d, N, late=True, missing=0.05))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

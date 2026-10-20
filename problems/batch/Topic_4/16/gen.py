# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30316)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(jobs):
    n = len(jobs)
    assert 1 <= n <= MAXN
    lines = [f"{n}\n"]
    for a, b in jobs:
        assert 1 <= a <= MAXV and 1 <= b <= MAXV
        lines.append(f"{a} {b}\n")
    tests.append("".join(lines))


def rnd(n, alo, ahi, blo, bhi):
    return [(ri(alo, ahi), ri(blo, bhi)) for _ in range(n)]


def near(n, lo, hi, d):
    """a and b close to each other"""
    res = []
    for _ in range(n):
        a = ri(lo, hi)
        b = min(MAXV, max(1, a + ri(-d, d)))
        res.append((a, b))
    return res


# samples
add([(3, 2), (1, 4), (2, 5)])
add([(4, 1), (2, 3)])
add([(5, 7)])
add([(2, 2), (2, 2), (2, 2), (2, 2)])
add([(6, 2), (1, 1), (4, 9), (3, 3), (7, 5)])
add([(10, 1), (8, 2), (9, 3), (1, 7), (2, 6), (3, 5)])
# hidden (small, checked by the exact subset DP)
add([(1, 1)])
add([(MAXV, MAXV)] * 20)
add(rnd(8, 1, 10, 1, 10))
add(rnd(12, 1, 100, 1, 100))
add(rnd(15, 1, 3, 1, 3))
add(near(16, 1, 50, 3))
add(rnd(18, 1, MAXV, 1, MAXV))
add(rnd(10, 1, 20, 50, 100) + rnd(10, 50, 100, 1, 20))
add(rnd(20, 1, 1000, 1, 1000))
# large
N = MAXN
add(rnd(N, 1, MAXV, 1, MAXV))
add(rnd(N, 1, 10, 1, 10))
add(rnd(N, 1, MAXV // 2, 1, MAXV))           # most signs have a < b
add(rnd(N, 1, MAXV, 1, MAXV // 2))           # most signs have a > b
add([(MAXV, MAXV)] * N)
add(near(N, 1, MAXV, 1000))
add(near(N, 1, 1000, 2))
add(rnd(N, 1, MAXV, 1, 1000))                # the painter is fast
add(rnd(N // 2, 1, 1000, 1, MAXV) + rnd(N // 2, 1, MAXV, 1, 1000))
add(sorted(rnd(N, 1, MAXV, 1, MAXV), key=lambda x: x[0] - x[1]))
add(rnd(N // 2, 1, 1000, 1, 1100) + rnd(N // 2, MAXV - 1000, MAXV, MAXV - 1100, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

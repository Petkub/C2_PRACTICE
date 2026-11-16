# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30319)
MAXN = 200_000
MAXH = 10**9
MAXD = 10**4
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(D, h):
    n = len(h)
    assert 1 <= n <= MAXN
    assert 0 <= D <= MAXD
    assert all(0 <= x <= MAXH for x in h)
    tests.append(f"{n} {D}\n" + " ".join(map(str, h)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def clip(x):
    return min(MAXH, max(0, x))


def near(n, D, base, noise):
    """almost a valid staircase: base + i * D plus noise"""
    return [clip(base + i * D + ri(-noise, noise)) for i in range(n)]


def walk(n, start, step):
    res, x = [], start
    for _ in range(n):
        x = clip(x + ri(-step, step))
        res.append(x)
    return res


# samples
add(0, [3, 1, 2, 5, 4])
add(2, [5, 5, 5, 5])
add(1, [1, 2, 4, 8, 16])
add(7, [42])
add(1, [4, 9, 2, 6, 3, 8, 7])
add(3, [10, 0, 10, 0, 10, 0])
# hidden (small)
add(MAXD, [MAXH, 0])
add(0, [MAXH, 0])
add(0, rnd(10, 0, 5))
add(1, rnd(10, 0, 20))
add(2, near(12, 2, 3, 3))
add(5, rnd(60, 0, 100))
add(0, rnd(300, 0, MAXH))
add(37, walk(2000, 10**5, 300))
add(MAXD, rnd(3000, 0, MAXH))
add(1, near(5000, 1, 10**6, 20))
add(0, rnd(20_000, 0, 1000))
# large
N = MAXN
add(0, rnd(N, 0, MAXH))
add(1, rnd(N, 0, MAXH))
add(MAXD, rnd(N, 0, MAXH))
add(0, list(range(MAXH, MAXH - N, -1)))                 # strictly decreasing
add(MAXD, [MAXH] * N)                                   # all equal, but each step must rise by D
add(MAXD, [0] * (N // 2) + [MAXH] * (N - N // 2))
add(MAXD, [MAXH - i * 4000 for i in range(N)])          # decreasing against a large D
add(3, near(N, 3, 1000, 50))
add(5000, near(N, 4999, 0, 10**6))
add(0, walk(N, MAXH // 2, 10**6))
add(0, [MAXH if i % 2 else 0 for i in range(N)])
add(1, rnd(N, 0, 10))
add(100, sorted(rnd(N, 0, MAXH)))                       # rising, but often by less than D

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

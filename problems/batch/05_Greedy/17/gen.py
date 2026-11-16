# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30317)
MAXN = 200_000
MAXP = 10**9
MAXF = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(F, p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert 0 <= F <= MAXF
    assert all(1 <= x <= MAXP for x in p)
    tests.append(f"{n} {F}\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def walk(n, start, step, lo, hi):
    """random walk clipped to [lo, hi]"""
    res, x = [], start
    for _ in range(n):
        x = min(hi, max(lo, x + ri(-step, step)))
        res.append(x)
    return res


def waves(n, period, lo, hi, jitter):
    """prices going down and up again and again (many bars held at the bottoms)"""
    res = []
    for i in range(n):
        t = i % period
        frac = abs(2 * t - period) / period         # 1 -> 0 -> 1
        v = lo + int((hi - lo) * frac) + ri(-jitter, jitter)
        res.append(min(hi, max(lo, v)))
    return res


# samples
add(1, [2, 8, 8, 3, 9, 9])
add(3, [5, 7, 4, 8])
add(1, [9, 7, 7, 4, 2])
add(0, [3, 1, 4, 1, 5, 9, 2, 6])
add(2, [10, 1, 7, 3, 9, 4, 12])
add(4, [6, 6, 6, 10, 10, 10])
# hidden (small)
add(0, [1])
add(MAXF, [1, MAXP])
add(MAXF - 2, [1, MAXP, 1, MAXP])               # each sale earns exactly 1
add(0, rnd(10, 1, 10))
add(3, rnd(12, 1, 10))
add(5, waves(40, 10, 1, 30, 2))
add(100, rnd(300, 1, 1000))
add(10**6, walk(2000, 5 * 10**8, 10**7, 1, MAXP))
add(50, waves(5000, 1000, 1, 10**4, 30))
add(7, walk(20_000, 5000, 20, 1, 10**4))
add(0, rnd(20_000, 1, MAXP))
# large
N = MAXN
add(ri(0, 10**7), rnd(N, 1, MAXP))
add(0, rnd(N, 1, 10**6))
add(1000, walk(N, 5 * 10**5, 3000, 1, 10**6))
add(0, list(range(N // 2, 0, -1)) + list(range(1, N // 2 + 1)))    # one deep valley
add(10, waves(N, 50_000, 1, 10**6, 5))
add(0, [MAXP if i % 2 else 1 for i in range(N)])
add(MAXP - 1, [MAXP if i % 2 else 1 for i in range(N)])     # nothing pays
add(1, list(range(1, N + 1)))
add(0, [5] * (N - 1) + [MAXP])
add(500, waves(N, 2000, 1, 10**6, 400))
add(ri(10**5, 10**6), walk(N, 5 * 10**8, 10**6, 1, MAXP))
add(3, list(range(N, 0, -1)))
add(20, [ri(1, 50) if i < N // 2 else ri(10**6 - 50, 10**6) for i in range(N)])  # buy early, sell late

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

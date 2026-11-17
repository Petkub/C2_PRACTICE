# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(180004)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(d, qs):
    n, q = len(d), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXV <= v <= MAXV for v in d)
    assert all(0 <= l < r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, d)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_q(n):
    l = ri(0, n - 1)
    return (l, ri(l + 1, n))


def long_q(n):
    l = ri(0, max(0, n // 10))
    return (l, ri(max(l + 1, n - n // 10), n))


def queries(n, q, long_frac):
    return [long_q(n) if random.random() < long_frac else rnd_q(n) for _ in range(q)]


add([3, -2, 4, -6, 1], [(0, 3), (2, 5), (3, 4)])
add([MAXV] * 3, [(0, 3), (1, 2)])
add([-5], [(0, 1)])
add([1, -1, 1, -1, 1, -1], [(0, 6), (1, 2), (2, 5), (5, 6), (0, 1)])
add([-4, 2, 2, 7, -3, -3, -3], [(0, 7), (1, 4), (3, 7), (4, 6), (6, 7)])

add([ri(-5, 5) for _ in range(10)], [(l, r) for l in range(10) for r in range(l + 1, 11)])
add([ri(-100, 100) for _ in range(100)], queries(100, 500, 0.3))
add([ri(-MAXV, MAXV) for _ in range(2000)], queries(2000, 3000, 0.3))
add([-MAXV] * 1000, queries(1000, 1000, 0.5))
add([ri(-10, 12) for _ in range(5000)], queries(5000, 5000, 0.4))

N = MAXN
add([MAXV] * N, queries(N, 50_000, 0.9))
add([-MAXV] * (N // 2) + [MAXV] * (N // 2), queries(N, 50_000, 0.9))
add([ri(-9999, 9999) for _ in range(N)], queries(N, 130_000, 0.9))
add([ri(-9999, 10_200) for _ in range(N)], queries(N, 130_000, 0.9))
add([ri(-10_200, 9999) for _ in range(N)], queries(N, 130_000, 0.9))
add([(-1) ** i * 99_999 for i in range(N)], queries(N, 130_000, 0.9))
d = [ri(1, 999) if (i // 5000) % 2 == 0 else -ri(1, 999) for i in range(N)]
add(d, queries(N, 140_000, 0.7))
add([ri(-99_999, 99_999) for _ in range(N)], [(0, N)] * 1000 + queries(N, 120_000, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

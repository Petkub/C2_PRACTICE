# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(180020)
MAXN, MAXQ, MAXH = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h, qs):
    n, q = len(h), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXH for v in h)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_q(n):
    l = ri(1, n)
    return (l, ri(l, n))


def long_q(n):
    l = ri(1, max(1, n // 10))
    return (l, ri(max(l, n - n // 10), n))


def queries(n, q, long_frac):
    return [long_q(n) if random.random() < long_frac else rnd_q(n) for _ in range(q)]


add([8, 7, 2, 2, 2, 9, 5], [(3, 6), (1, 3), (1, 2), (4, 4)])
add([5, 5, 5, 5], [(1, 4), (2, 3)])
add([0, 1000, 0, 1000, 1000], [(1, 5), (1, 4), (2, 5), (3, 3)])
add([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], [(1, 10), (2, 6), (5, 9), (6, 7), (8, 10), (4, 4)])
add([MAXH, 0], [(1, 2), (2, 2)])

h = [ri(0, 9) for _ in range(10)]
add(h, [(l, r) for l in range(1, 11) for r in range(l, 11)])
add([ri(0, MAXH) for _ in range(100)], queries(100, 1000, 0.3))
add([ri(0, 3) for _ in range(300)], queries(300, 1000, 0.3))
add([ri(MAXH - 1000, MAXH) for _ in range(500)], queries(500, 500, 0.5))
add([MAXH * (i % 2) for i in range(1000)], queries(1000, 500, 0.5))
add([ri(0, 10**6) for _ in range(3000)], queries(3000, 300, 0.5))

N, Q = MAXN, 120_000
add([ri(0, 999_999) for _ in range(N)], queries(N, Q, 0.9))
add([ri(0, 999_999) for _ in range(N)], queries(N, Q, 0.5))
add([MAXH] * N, queries(N, 50_000, 0.9))
add([MAXH * (i % 2) for i in range(N)], queries(N, 60_000, 0.9))
add([i * 4 for i in range(1, N + 1)], queries(N, Q, 0.9))
add([(N - i) * 4 for i in range(N)], queries(N, Q, 0.9))
h = [ri(0, 10) for _ in range(N)]
for _ in range(30):
    h[ri(0, N - 1)] = 999_999
add(h, queries(N, Q, 0.9))
h = [ri(999_990, 999_999) for _ in range(N)]
for _ in range(30):
    h[ri(0, N - 1)] = 0
add(h, queries(N, Q, 0.9))
add([ri(0, 3) for _ in range(N)], queries(N, 150_000, 0.9))
add([0] * (N // 2) + [999_999] * (N - N // 2 - 1), queries(N - 1, Q, 0.9))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

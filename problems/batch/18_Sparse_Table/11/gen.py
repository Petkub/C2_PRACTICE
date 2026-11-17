# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(180010)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
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


def blocks_of_distinct(n, lo, hi):
    a = []
    while len(a) < n:
        m = ri(lo, hi)
        a.extend(random.sample(range(1, 10 * m + 1), m))
    return a[:n]


add([1, 2, 1, 3, 4, 2, 5, 3], [(1, 8), (1, 4), (4, 8), (6, 6), (3, 5)])
add([7, 7, 7, 7], [(1, 4), (2, 3)])
add([MAXV], [(1, 1)])
add([1, 2, 3, 1, 2, 3, 4], [(1, 7), (1, 3), (2, 5), (4, 7), (3, 4)])
add([5, 1, 5, 2, 6, 3, 2, 1, 4], [(1, 9), (1, 3), (2, 6), (4, 9), (6, 9), (5, 5)])

a = [ri(1, 4) for _ in range(10)]
add(a, [(l, r) for l in range(1, 11) for r in range(l, 11)])
add([ri(1, 20) for _ in range(300)], queries(300, 500, 0.3))
add(blocks_of_distinct(1000, 1, 60), queries(1000, 1000, 0.4))
add([ri(1, MAXV) for _ in range(1500)], queries(1500, 1500, 0.3))
add([ri(1, 2) for _ in range(3000)], queries(3000, 3000, 0.3))

N = MAXN
add(list(range(1, N + 1)), queries(N, 120_000, 0.9))
add([i % 50_000 + 1 for i in range(N)], queries(N, 120_000, 0.9))
add(blocks_of_distinct(N, 1000, 30_000), queries(N, 120_000, 0.9))
add([ri(1, 300_000) for _ in range(N)], queries(N, 120_000, 0.9))
add([ri(1, 999_999) for _ in range(N)], queries(N, 120_000, 0.9))
a = list(range(1, N + 1))
for i in range(0, N, 40_000):
    a[i] = 1
add(a, queries(N, 120_000, 0.9))
a = list(range(1, N // 2 + 1)) * 2
add(a, queries(N, 120_000, 0.7))
add([ri(1, 5) for _ in range(N)], queries(N, 150_000, 0.9))
add(blocks_of_distinct(N, 50, 5000), [(ri(1, N), N) for _ in range(120_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180001)
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


def blocks(n, base_choices, mult_hi):
    """runs of planks sharing a block factor, so many ranges have a gcd > 1"""
    a = []
    while len(a) < n:
        g = random.choice(base_choices)
        for _ in range(ri(1, max(1, n // 5))):
            a.append(g * ri(1, mult_hi))
    return a[:n]


# samples
add([12, 18, 30, 7, 14], [(1, 3), (3, 4), (2, 2)])
add([MAXV] * 3, [(1, 3), (2, 3)])
add([1], [(1, 1)])
add([8, 4, 12, 16, 6, 9], [(1, 4), (1, 6), (5, 6), (4, 4), (2, 3)])
add([35, 49, 14, 21, 70, 28, 63], [(1, 7), (3, 6), (5, 5), (1, 2), (4, 7)])
# hidden: small
add([ri(1, 30) for _ in range(10)], queries(10, 40, 0.2))
add([6 * ri(1, 20) for _ in range(50)], queries(50, 100, 0.3))
add(blocks(300, [2, 3, 4, 6, 10, 12], 50), queries(300, 500, 0.3))
add([2**ri(0, 29) for _ in range(1000)], queries(1000, 2000, 0.3))            # powers of two
add(blocks(5000, [999_983, 2 * 3 * 5 * 7, 2**20], 900), queries(5000, 5000, 0.4))
add([ri(1, MAXV) for _ in range(2000)], queries(2000, 3000, 0.2))              # gcd mostly 1
# hidden: maximum size (values kept short so the input stays <= 3 MB)
N = MAXN
add([2 * 3 * 5 * 7 * ri(1, 4000) for _ in range(N)], queries(N, 120_000, 0.9))   # gcd never 1
add([MAXV] * N, queries(N, 60_000, 0.9))                                          # all equal, maximal
add([720_720] * (N - 1) + [360_360], queries(N, 130_000, 0.8))
add(blocks(N, [2, 6, 30, 210, 64], 9000), queries(N, 120_000, 0.7))
add([2**ri(10, 19) for _ in range(N)], queries(N, 140_000, 0.9))
add([ri(1, 999_999) for _ in range(N)], queries(N, 120_000, 0.5))
a = [12 * ri(1, 80_000) for _ in range(N)]
a[N // 2] = 11                                                                     # one plank breaks the middle
add(a, queries(N, 120_000, 0.9))
add([5 * ri(1, 199_999) for _ in range(N)], [(1, N)] * 1000 + queries(N, 110_000, 0.95))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

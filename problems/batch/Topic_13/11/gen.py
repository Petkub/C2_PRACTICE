# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110011)
MAXN, MAXQ, MAXV = 300_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n and 1 <= x <= MAXV for (l, r, x) in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r} {x}\n" for (l, r, x) in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def queries(a, q, xs, long_frac=0.9):
    """xs(): a random cap"""
    n = len(a)
    res = []
    for _ in range(q):
        if random.random() < long_frac:
            l = ri(1, max(1, n // 20))
            r = ri(max(l, n - n // 20), n)
        else:
            l = ri(1, n)
            r = ri(l, n)
        res.append((l, r, xs()))
    return res


def from_values(a):
    """a cap equal to some value, or one more / one less"""
    return lambda: max(1, random.choice(a) + ri(-1, 1))


# samples
add([3, 8, 5, 1, 10], [(1, 5, 6), (2, 3, 4), (4, 4, 100), (1, 5, 1)])
add([2, 2, 2], [(1, 3, 5), (2, 3, 2)])
add([7], [(1, 1, 7), (1, 1, 3)])
add([4, 9, 1, 6, 6, 2], [(1, 6, 5), (2, 5, 6), (3, 3, 1), (1, 4, 10)])
add([5, 12, 3, 8, 20, 7, 1, 9], [(1, 8, 8), (2, 6, 4), (5, 8, 15), (3, 7, 1), (1, 1, 2)])
# hidden: small
add([MAXV], [(1, 1, MAXV), (1, 1, 1)])
a = [ri(1, 10) for _ in range(10)]
add(a, [(l, r, ri(1, 11)) for l in range(1, 11) for r in range(l, 11)])
a = [ri(1, 100) for _ in range(200)]
add(a, queries(a, 400, from_values(a), 0.3))
a = [ri(1, MAXV) for _ in range(2000)]
add(a, queries(a, 3000, lambda: ri(1, MAXV), 0.3))
a = [ri(1, 1000) for _ in range(10000)]
add(a, queries(a, 8000, from_values(a), 0.4))
a = sorted(ri(1, 10**6) for _ in range(5000))
add(a, queries(a, 5000, from_values(a), 0.5))
# hidden: maximum size
N = 250_000
a = [ri(1, 9999) for _ in range(N)]
add(a, queries(a, 75_000, lambda: ri(1, 10**4)))
a = [ri(1, 9999) for _ in range(N)]
add(a, queries(a, 75_000, from_values(a)))
a = [ri(1, 9999) for _ in range(N)]
add(a, queries(a, 75_000, lambda: ri(1, 50)))                         # almost everything is capped
a = [ri(1, 9999) for _ in range(N)]
add(a, queries(a, 75_000, lambda: ri(9990, 99999)))                   # almost nothing is capped
a = sorted(ri(1, 9999) for _ in range(N))
add(a, queries(a, 75_000, from_values(a)))
a = sorted((ri(1, 9999) for _ in range(N)), reverse=True)
add(a, queries(a, 75_000, from_values(a)))
add([5000] * N, queries([5000] * N, 75_000, lambda: ri(4999, 5001)))  # equal values, caps at the boundary
a = [ri(1, 99) for _ in range(300_000)]
add(a, queries(a, 80_000, from_values(a)))
a = [MAXV - ri(0, 9) for _ in range(200_000)]
add(a, queries(a, 30_000, lambda: MAXV - ri(0, 12)))                   # sums up to 2 * 10^14
a = [ri(1, MAXV) for _ in range(180_000)]
add(a, queries(a, 30_000, lambda: ri(1, MAXV)))
a = [9999 - ri(0, 9) for _ in range(300_000)]
add(a, queries(a, 75_000, lambda: ri(9995, 99999), 0.95))              # sums above 2^31 with short numbers
a = [ri(1, 9999) if i % 2 else ri(1, 9) for i in range(N)]           # small and large values alternate
add(a, queries(a, 75_000, from_values(a), 0.95))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

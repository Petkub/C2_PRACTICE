# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250010)
MAXN, MAXQ, MAXV = 200_000, 100_000, (1 << 20) - 1
tests = []


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    assert all(1 <= l <= r <= n and 0 <= x <= MAXV for l, r, x in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r} {x}\n" for l, r, x in qs))


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def qlong(n, q, xlo=0, xhi=MAXV):
    """mostly long ranges"""
    qs = []
    for _ in range(q):
        l = random.randint(1, max(1, n // 10))
        r = random.randint(max(l, n - n // 10), n)
        qs.append((l, r, random.randint(xlo, xhi)))
    return qs


def qany(n, q, xlo=0, xhi=MAXV):
    qs = []
    for _ in range(q):
        l = random.randint(1, n)
        qs.append((l, random.randint(l, n), random.randint(xlo, xhi)))
    return qs


# samples
add([1, 6, 3, 7, 2], [(1, 5, 4), (2, 4, 1), (1, 2, 0), (5, 5, 7)])
add([0], [(1, 1, 0), (1, 1, MAXV)])
add([5, 5, 9, 5], [(1, 2, 12), (2, 4, 12), (4, 4, 5)])
add([8, 1, 15, 2, 4, 11], [(1, 6, 7), (2, 5, 7), (3, 3, 3), (4, 6, 9), (1, 2, 9)])
add([3, 12, 10, 6, 1, 0, 13], [(2, 7, 5), (1, 3, 1), (5, 6, 14), (6, 7, 2)])
# hidden: small
add(rnd(10, 0, 15), qany(10, 20, 0, 15))
add(rnd(100, 0, 255), qany(100, 300, 0, 255))
add(rnd(1000, 0, MAXV), qany(1000, 1000))
add(rnd(3000, 0, 7), qany(3000, 2000, 0, 7))
add(rnd(5000, 0, MAXV), qlong(5000, 3000))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(rnd(N, 0, MAXV), qlong(N, Q))
add(rnd(N, 0, MAXV), qany(N, Q))
a = rnd(N, 0, (1 << 10) - 1)                     # the far values sit outside most ranges
for i in range(0, N, 5000):
    a[i] = random.randint(1 << 19, MAXV)
add(a, qlong(N, Q, 0, (1 << 10) - 1))
add(sorted(rnd(N, 0, MAXV)), qlong(N, Q))
add([MAXV] * N, qlong(N, Q))
a = rnd(N, 0, MAXV)
qs = []
for _ in range(60_000):                          # short ranges at random places (fewer: any scan is fast here)
    l = random.randint(1, N - 50)
    qs.append((l, l + random.randint(0, 50), random.randint(0, MAXV)))
add(a, qs)
a = rnd(N, 0, MAXV)
qs = []
for _ in range(Q):                               # ranges of about half the row at random places
    l = random.randint(1, N // 2)
    qs.append((l, l + random.randint(N // 3, N // 2 - 1), random.randint(0, MAXV)))
add(a, qs)
a = rnd(N, 0, MAXV)
add(a, [(1, N, random.randint(0, MAXV)) for _ in range(Q)])
qs = []
for _ in range(60_000):                          # left ends far right: old indices must not be used
    r = random.randint(N - 1000, N)
    l = random.randint(max(1, r - 2000), r)
    qs.append((l, r, random.randint(0, MAXV)))
a = [MAXV ^ random.randint(0, 1) for _ in range(N - 3000)] + rnd(3000, 0, 1023)
add(a, qs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40113)
MAXN, MAXD = 120_000, 10**4
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, b):
    """a, b: lists of (free, busy)"""
    n, m = len(a), len(b)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN
    for (f, x) in a + b:
        assert 0 <= f <= MAXD and 1 <= x <= MAXD
    la = " ".join(f"{f} {x}" for (f, x) in a)
    lb = " ".join(f"{f} {x}" for (f, x) in b)
    tests.append(f"{n} {m}\n{la}\n{lb}\n")


def rnd(k, flo, fhi, blo, bhi):
    return [(ri(flo, fhi), ri(blo, bhi)) for _ in range(k)]


# samples
add([(1, 3), (2, 2)], [(2, 5)])
add([(0, 5)], [(5, 3), (4, 1)])
add([(0, 10000)], [(0, 10000)])
add([(3, 1), (1, 1), (1, 1), (1, 1)], [(2, 2), (0, 3), (2, 6)])
add([(4, 2), (0, 3), (10, 5)], [(1, 4), (1, 1), (0, 2), (9, 1)])
# hidden: small
add([(0, 1)], [(1, 1)])
add([(7, 2)], [(0, 8)])
add(rnd(5, 0, 5, 1, 5), rnd(6, 0, 5, 1, 5))
add(rnd(40, 0, 20, 1, 20), rnd(30, 0, 20, 1, 30))
add(rnd(500, 0, 100, 1, 100), rnd(700, 0, 80, 1, 50))
add(rnd(3000, 0, MAXD, 1, MAXD), rnd(2000, 0, MAXD, 1, MAXD))
add(rnd(8000, 0, 3, 1, 3), rnd(9000, 0, 2, 1, 2))
add(rnd(5000, 0, 0, 1, MAXD), rnd(4000, MAXD, MAXD, 1, 1))     # first always busy, second rarely
# hidden: maximum size
N = MAXN
add(rnd(N, 0, MAXD, 1, MAXD), rnd(N, 0, MAXD, 1, MAXD))
add(rnd(N, 8000, MAXD, 8000, MAXD), rnd(N, 8000, MAXD, 8000, MAXD))   # ends beyond 2^31
add(rnd(N, MAXD, MAXD, MAXD, MAXD), rnd(N, MAXD, MAXD, MAXD, MAXD))   # identical, times beyond 2^31
add(rnd(N, 0, 0, MAXD, MAXD), rnd(N, 0, 0, MAXD, MAXD))               # both busy all the time
add(rnd(N, MAXD - 100, MAXD, 1, 100), rnd(N, 0, 100, MAXD - 100, MAXD))
add(rnd(N, 9000, MAXD, 9000, MAXD), rnd(N, 9000, MAXD, 9000, MAXD))
add(rnd(N, 0, 9, 1, 9), rnd(N, 0, 9, 1, 9))                           # short pieces, ends near 2 * 10^6
add(rnd(N, 0, MAXD, 1, MAXD), rnd(N // 2, MAXD, MAXD, MAXD, MAXD))
add(rnd(N, 9000, 9000, 9000, 9000), rnd(N, 9000, 9000, 9000, 9000))   # same rhythm, phase shift 0
add([(0, 9000)] + rnd(N - 1, 9000, 9000, 9000, 9000), rnd(N, 9000, 9000, 9000, 9000))   # exactly out of phase
add(rnd(N, 0, MAXD, MAXD - 10, MAXD), rnd(N, 0, 10, 1, MAXD))
add(rnd(10, 0, 0, MAXD, MAXD), rnd(N, 0, MAXD, 1, MAXD))              # first busy only at the start
add(rnd(N, 1, MAXD, 8000, MAXD), rnd(N, 1, MAXD, 8000, MAXD))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

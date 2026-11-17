# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(50505)
MAXN, MAXP = 100_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert all(len(d) == 3 and all(-MAXP <= x <= MAXP for x in d) for d in p)
    tests.append(f"{n}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in p))


def rnd(n, lo, hi):
    return [(ri(lo, hi), ri(lo, hi), ri(lo, hi)) for _ in range(n)]


# samples
add([(5, 1, 0), (10, 0, 0), (2, 6, 3)])
add([(-3, -5, -2), (-1, -4, -6)])
add([(4, -7, 9)])
add([(3, 3, 3)] * 4)
add([(10**9, -10**9, 0), (10**9, 10**9, 10**9), (10**9, 0, -10**9)])
add([(7, 2, 4), (8, 9, 1), (6, 3, 3), (1, 5, 8), (9, 9, 2)])
# hidden: small (the brute force checks these)
add([(-10**9, -10**9, -10**9)])
add([(0, 0, 0), (0, 0, 0)])
add(rnd(8, -10, 10))
add(rnd(10, 0, 100))
add(rnd(11, -MAXP, MAXP))
add(rnd(12, -100, -1))                      # every point negative
add([(1, 0, 0)] * 12)                       # the same activity is best every day
add([(5, 5, 0), (9, 0, 0), (0, 9, 0)] * 4)
# hidden: maximum size
N = MAXN
add(rnd(N, -MAXP, MAXP))
add(rnd(N, 0, MAXP))
add([(MAXP, MAXP, MAXP)] * N)               # the largest total
add([(-MAXP, -MAXP, -MAXP)] * (N - 10_000))   # the smallest total
add(rnd(N, -MAXP, -1))
add([(MAXP, MAXP - 1, -MAXP)] * N)          # the best activity is never allowed twice
add([(ri(0, 5), ri(0, 5), ri(0, 5)) for _ in range(N)])
add([(MAXP, ri(-MAXP, MAXP), -MAXP) if i % 2 else (MAXP - ri(0, 3), 0, 0) for i in range(N)])
add(rnd(N, -10, 10))
add([(-1, -1, -MAXP)] * N)
add(rnd(N, -MAXP, MAXP // 10))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

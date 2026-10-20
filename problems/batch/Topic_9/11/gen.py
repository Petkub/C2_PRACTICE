# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(131101)
MAXN = 200000
MAXA = 10**9
MAXLR = 10**15
tests = []


def add(a, lo, hi):
    assert 1 <= len(a) <= MAXN and all(-MAXA <= x <= MAXA for x in a)
    assert -MAXLR <= lo <= hi <= MAXLR
    tests.append(f"{len(a)} {lo} {hi}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def walk(n, drift, step):
    """values around drift: prefix sums wander like a random walk"""
    return [max(-MAXA, min(MAXA, drift + random.randint(-step, step))) for _ in range(n)]


# samples
add([3, -1, 2, -4, 5], 2, 3)
add([-5, 2, -5], -4, -1)
add([0, 0, 0, 0], 0, 0)
add([1, 2, 3], 7, 100)
add([MAXA] * 3, 2 * MAXA, 3 * MAXA)
add([4, -7, 1, 0, 6, -2, -3, 5], -2, 2)
# hidden: small and medium (the brute force checks these)
add([5], 5, 5)
add([-MAXA], -MAXLR, MAXLR)
add(rnd(10, -5, 5), -3, 3)
add(rnd(300, -10, 10), 0, 0)
add(rnd(2000, -MAXA, MAXA), -10**10, 10**10)
add(rnd(3000, -3, 3), -5, 2)
add(rnd(20000, -MAXA, MAXA), 0, 10**11)
add(rnd(20000, 1, 100), 500, 1000)
# hidden: large
N = MAXN
add(rnd(N, -MAXA, MAXA), -10**12, 10**12)
add(rnd(N, -MAXA, MAXA), 3 * 10**11, 2 * 10**12)
add(rnd(N, -MAXA, MAXA), 777, 777)
add(rnd(N, -3, 3), -1, 1)
add(rnd(N, -1, 1), 0, 0)
add([0] * N, 0, 0)                                                  # every period counts
add([MAXA] * N, 5 * 10**13, 5 * 10**13)                             # periods of one exact length
add([-MAXA] * N, -MAXLR, -10**14)
add(rnd(N, -MAXA, MAXA), -MAXLR, MAXLR)
add(rnd(N, 0, MAXA), 10**13, 10**14)
add(walk(N, 3, 1000), -10**5, 10**6)
add(walk(N, -50, 100), -10**6, -10**4)
add([MAXA if i % 2 == 0 else -MAXA for i in range(N)], 0, MAXA)
add(rnd(N, -MAXA, MAXA), 10**15 - 1, MAXLR)                         # nothing
add([random.choice((-MAXA, MAXA)) for _ in range(N)], -2 * MAXA, 2 * MAXA)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

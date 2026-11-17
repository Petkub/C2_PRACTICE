# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(50303)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(1, [5, 1, 2, 10, 6, 2])
add(2, [5, 1, 2, 10, 6, 2])
add(4, [3, 9, 4, 1])
add(1, [8])
add(1, [10**9, 1, 10**9, 1, 10**9])
add(1, [4, 7, 4, 1, 2, 8, 3])
# hidden: small (the brute force checks these)
add(1, [3, 3])
add(2, [1, 5, 1])
add(1, rnd(18, 1, 10))
add(3, rnd(20, 1, 100))
add(2, rnd(22, 1, MAXA))
add(5, rnd(22, 1, 50))
add(1, [1, 2] * 11)
add(4, [2, 1, 1, 1, 2, 1, 1, 1, 2, 9, 9, 9, 9, 2])
# hidden: maximum size
N = MAXN
add(1, rnd(N, 1, MAXA))
add(1, [MAXA] * N)                      # the largest total
add(2, rnd(N, 1, MAXA))
add(3, rnd(N, 1, 10))
add(7, rnd(N, 1, MAXA))
add(50, rnd(N, 1, MAXA))
add(1, [MAXA if i % 3 == 0 else MAXA - 1 for i in range(N)])
add(2, list(range(1, N + 1)))
add(1, [ri(1, 3) for _ in range(N)])
add(1000, rnd(N, 1, MAXA))
add(N, rnd(N, 1, MAXA))                 # only one lot can be taken
add(N - 1, rnd(N, 1, MAXA))
add(10, [1] * N)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

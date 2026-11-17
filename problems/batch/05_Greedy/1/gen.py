# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3006)
MAXN, MAXL = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXL for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([4, 3, 2, 6])
add([5, 5, 5, 5])
add([7])
add([1000000000, 1000000000])
add([8, 1, 3, 5, 2, 9, 4])
add([1, 1, 2, 4, 8, 16])
# hidden: small (every way is tried)
add([1])
add([3, 9])
add([1, 1, 1])
add([2, 2, 3, 3])
add([1] * 10)
add([10, 11, 12, 13, 14, 15])
add([1, 2, 3, 100, 101, 102, 103])
add(rnd(8, 1, 10))
add(rnd(10, 1, 100))
add(rnd(10, 1, MAXL))
add(rnd(7, 1, 5))
# hidden: medium
add(rnd(100, 1, 1000))
add(rnd(2000, 1, MAXL))
add(rnd(5000, 1, 10))
# hidden: maximum size
N = MAXN
add([MAXL] * N)                                   # the largest answer
add(rnd(N, 1, MAXL))
add(sorted(rnd(N, 1, MAXL)))
add(sorted(rnd(N, 1, MAXL), reverse=True))
add(rnd(N, 1, 3))                                 # many equal lengths
add(rnd(N, MAXL - 1000, MAXL))
add([1] * (N - 30) + [2 ** k for k in range(30)])  # many short ropes and a few doubling ones
a = rnd(N - 100, 1, 100) + rnd(100, 10**8, MAXL)
random.shuffle(a)
add(a)
add([ri(1, 9) * 10 ** ri(0, 8) for _ in range(N)])       # lengths of very different sizes
add(rnd(N - 1, 1, MAXL))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

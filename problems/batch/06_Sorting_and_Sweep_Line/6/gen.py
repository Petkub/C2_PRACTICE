# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40406)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([50, 80, 50, 100, 70])
add([7, 7, 7])
add([0])
add([0, MAXA])
add([5, 3, 5, 1, 3, 9])
add([10, 9, 8, 7])
# hidden: small
add([MAXA, MAXA])
add([1, 2, 2, 2, 3])
add(rnd(10, 0, 5))
add(rnd(50, 0, 100))
add(rnd(400, 0, 20))
add(rnd(2000, 0, MAXA))
add(rnd(5000, 0, 3))
add(list(range(3000)))
# hidden: large
N = MAXN
add(rnd(N, 0, MAXA))
add(rnd(N, 0, 1000))
add([ri(0, 1) * MAXA for _ in range(N)])        # two values, gap 10^9
add([123_456_789] * N)                          # everyone first
add([5] * (N - 1) + [6])                        # one leader, all others tied
add([6] + [5] * (N - 1))
add(list(range(N)))                             # all distinct, increasing
add(list(range(MAXA, MAXA - N, -1)))            # all distinct, decreasing, large
add([ri(0, 9) * 100_000_000 for _ in range(N)])  # ten groups of equal scores
a = rnd(N, 0, MAXA)
a[ri(0, N - 1)] = MAXA
add(a)
add(sorted(rnd(N, 0, 50_000), reverse=True))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(60006)
MAXN, MAXA = 300_000, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi, zero=0.0):
    return [0 if random.random() < zero else ri(lo, hi) for _ in range(n)]


# samples
add([2, 1, 3, 1])
add([3, 1, 0, 0, 2])
add([5])
add([6] * 6)
add([3, 0, 2, 4, 1, 1, 3, 2])
add([3, 1, 2, 0, 4, 1, 2, 3, 1, 2])
# hidden: small (every sequence is walked)
add([0])
add([1] * 20)                                         # one way only
add([2] * 22)                                         # Fibonacci
add([MAXA] * 22)                                      # every ordered sum: 2^21
add([0] + [5] * 15)                                   # stuck at the start
add(rnd(20, 1, 4, 0.1))
add(rnd(22, 1, 6))
add([22 - i for i in range(22)])
# hidden: medium (the square-by-square loop of brute.cpp checks them)
add(rnd(30_000, 0, 50_000, 0.01))
add(rnd(30_000, 1, 3))
# hidden: large
N = MAXN
add([MAXA] * N)                                       # every ordered sum, the slow way is O(N^2)
add([N - i for i in range(N)])                        # exactly to the end
add(rnd(N, N // 2, MAXA))
add(rnd(N, 1, MAXA, 0.001))
add(rnd(N, 1, N // 3))
add(rnd(N, 5, 10, 0.05))
add(rnd(N, 1, 2))                                     # Fibonacci-like, small ranges
a = [MAXA] * N
for i in range(0, N, 1000):                           # walls of zeros that big jumps fly over
    for j in range(i + 500, min(N, i + 520)):
        a[j] = 0
add(a)
a = [MAXA] * N
a[N - 1] = 0                                          # the last square before the end is a trap
add(a)
add([ri(N - i, MAXA) if i % 2 else 1 for i in range(N)])
M = N // 2
a = [ri(1, 1000) if i < M - 1000 else ri(1, M - i) if i < M else 0 if i == M else ri(1, 1000) for i in range(N)]
add(a)                                                # nobody passes square N / 2: answer 0
add(rnd(N - 7, 100_000, MAXA))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

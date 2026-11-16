# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160004)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


# samples
add([3, 1, 8, 2, 8, 6])
add([4, 4, 4])
add([9])
add([5, 4, 3, 2, 1])
add([2, 7, 1, 8, 2, 8, 1])
# hidden: small
add([1, 2])
add([ri(1, 3) for _ in range(12)])
add([ri(1, 6) for _ in range(300)])
add([ri(1, MAXH) for _ in range(2000)])
add([5000 - i for i in range(5000)])
add([ri(1, 2) for _ in range(20000)])
# hidden: maximum size
N = MAXN
add([MAXH] * N)                                       # all equal
h = [ri(MAXH - 1, MAXH) for _ in range(N)]
add(h)
add([N - i for i in range(N)])                        # decreasing: every answer wraps around
add([i + 1 for i in range(N)])                        # increasing
h = [7] * N                                           # one taller tower at the start
h[0] = 8
add(h)
h = [7] * N                                           # one taller tower at the end
h[-1] = 8
add(h)
add([ri(1, MAXH) for _ in range(N)])
add([N - abs(N // 2 - i) for i in range(N)])          # mountain
add([1 + abs(N // 3 - i) for i in range(N)])          # valley
add([MAXH - (i % 1000) for i in range(N)])            # repeated decreasing runs

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160001)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


# samples
add([4, 2, 5, 7, 5, 1, 3])
add([2, 2, 1, 2, 2])
add([7])
add([1, 2, 3, 4, 5])
add([3, 1, 4, 1, 5, 9])
# hidden: small
add([5, 5])
add([ri(1, 3) for _ in range(12)])
add([ri(1, 5) for _ in range(200)])
add([ri(1, MAXH) for _ in range(1000)])
add([ri(1, 20) for _ in range(5000)])
add([10 - abs(i - 15) % 10 for i in range(3000)])       # zigzag with many equal distances
add([ri(1, 2) for _ in range(20000)])
# hidden: maximum size
N = MAXN
add([MAXH] * N)                                          # nobody is lower
h = [MAXH] * N                                           # a few low houses far apart
for p in (1, N // 3, 2 * N // 3 + 7, N):
    h[p - 1] = 1
add(h)
h = [ri(MAXH - 1, MAXH) for _ in range(N)]
add(h)
add([N - abs(N // 2 - i) for i in range(N)])             # mountain
add([1 + abs(N // 2 - i) for i in range(N)])             # valley: lower house far for the middle
add([ri(1, MAXH) for _ in range(N)])
add([ri(1, 3) for _ in range(N)])
h = [MAXH] * N                                           # one low house in the middle, ties to both sides
h[N // 2] = 1
h[N // 2 - 50000] = 1
h[N // 2 + 50000] = 1
add(h)
add([(i % 2) + 1 for i in range(N)])                     # 1 2 1 2 ...: every tall house has a tie
add([N - i for i in range(N)])                            # decreasing

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

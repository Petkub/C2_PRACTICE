# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160108)
MAXN, MAXW = 200_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(w):
    n = len(w)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXW for x in w)
    tests.append(f"{n}\n" + " ".join(map(str, w)) + "\n")


# samples
add([6, 2, 4, 3])
add([3, 3, 3])
add([7])
add([1, 2, 3, 4, 5])
add([5, 1, 4, 1, 5, 9, 2])
# hidden: small (interval DP)
add([4, 9])
add([ri(1, 4) for _ in range(9)])
add([ri(1, 20) for _ in range(60)])
add([ri(1, MAXW) for _ in range(200)])
add([ri(1, 3) for _ in range(300)])
add([400 - abs(200 - i) for i in range(400)])          # mountain
add([1 + abs(200 - i) for i in range(400)])            # valley
# hidden: medium (pair simulation)
add([ri(1, MAXW) for _ in range(3000)])
# hidden: maximum size
N = MAXN
add([MAXW] * N)                                        # (N - 1) * 10^12
add([i % MAXW + 1 for i in range(N)])                  # increasing
add([MAXW - i for i in range(N)])                      # decreasing
add([ri(1, MAXW) for _ in range(N)])
add([ri(1, 3) for _ in range(N)])
add([MAXW - abs(N // 2 - i) * 5 for i in range(N)])    # mountain
add([1 + abs(N // 2 - i) * 5 for i in range(N)])       # valley
add([MAXW if i % 2 else ri(1, 10) for i in range(N)])  # heavy and light alternate
add([(i % 1000) * 1000 + 1 for i in range(N)])         # saw teeth
add([ri(MAXW - 100, MAXW) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160006)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


# samples
add([2, 3, 3, 1, 2])
add([2, 1, 2])
add([7])
add([1, 2, 3, 4])
add([3, 1, 3, 1, 3])
# hidden: small (checked by the exhaustive search)
add([5, 5, 5])
add([2, 1, 2, 1, 2, 1, 2, 1])
add([1, 3, 2, 3, 1, 3, 2])
add([ri(1, 4) for _ in range(8)])
add([ri(1, 3) * 10**8 for _ in range(10)])
add([3, 2, 1, 2, 3, 2, 1, 2])
# hidden: medium (checked by the slab recursion)
add([ri(1, 5) for _ in range(2000)])
add([ri(1, MAXH) for _ in range(5000)])
add([i % 50 + 1 for i in range(20000)])
# hidden: maximum size
N = MAXN
add([MAXH] * N)
add([i + 1 for i in range(N)])                    # staircase up
add([N - i for i in range(N)])                    # staircase down
add([ri(1, MAXH) for _ in range(N)])
add([ri(1, 3) for _ in range(N)])
add([ri(1, 50) for _ in range(N)])
add([N - abs(N // 2 - i) for i in range(N)])      # mountain
add([1 + abs(N // 2 - i) for i in range(N)])      # valley
add([MAXH if i % 2 else MAXH - 1 for i in range(N)])
h, cur = [], 1                                    # random walk
for _ in range(N):
    cur = max(1, min(MAXH, cur + ri(-3, 3)))
    h.append(cur)
add(h)
add([i * 1000 + ri(0, 3000) + 1 for i in range(N)])          # noisy ramp up
add([(N - i) * 1000 + ri(0, 3000) for i in range(N)])        # noisy ramp down
add([(i % 40000) * 20000 + ri(1, 9) for i in range(N)])      # five long ramps

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

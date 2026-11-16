# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(50101)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 2 <= n <= MAXN
    assert all(0 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([10, 30, 40, 20, 50, 30])
add([1, 2, 3, 4, 5])
add([7, 3])
add([5, 5, 5, 5, 5, 5, 5])
add([0, 1000000000, 1000000000, 0, 0, 1000000000])
add([3, 8, 2, 6, 6, 1, 4, 9])
# hidden: small (the brute force checks these)
add([4, 4])
add([2, 9, 2])
add(rnd(12, 0, 3))
add(rnd(20, 0, 10))
add(rnd(25, 0, MAXH))
add(list(range(30, 0, -1)))
add(rnd(30, 0, 2))
add([0, 0, 1, 1] * 7)
# hidden: maximum size
N = MAXN
add(rnd(N, 0, MAXH))
add(rnd(N, 0, 3))                               # many ties in effort
add(sorted(rnd(N, 0, MAXH)))                    # every way has the same effort
add(sorted(rnd(N, 0, MAXH), reverse=True))
add([MAXH] * N)                                 # effort 0, fewest jumps
add([0, 0, MAXH, MAXH] * (N // 4))              # effort near 10^14
add([0 if i % 2 == 0 else MAXH for i in range(N)])
add([(i * 7) % 5 for i in range(N)])
add([ri(0, 10) + (MAXH - 20) * (i // 2 % 2) for i in range(N)])
add([i // 3 for i in range(N)])                 # steps of equal stones
add(rnd(N - 1, 0, MAXH) + [0])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

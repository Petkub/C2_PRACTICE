# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(5114)
MAXN, MAXP = 300_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXP for x in p)
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def walk(n, step):
    x, out = MAXP // 2, []
    for _ in range(n):
        x = min(MAXP, max(1, x + ri(-step, step)))
        out.append(x)
    return out


# samples
add([2, 3, 4, 1, 3])
add([5, 4, 3])
add([7])
add([1, 3, 1, 3])
add([3, 1, 4, 1, 5, 9, 2, 6])
add([1, 10, 1, 1, 10, 1, 10])
# hidden: small (the brute force can check these)
add([1, MAXP])
add([MAXP, 1])
add(rnd(10, 1, 10))
add(rnd(14, 1, 100))
add(rnd(16, 1, MAXP))
add([1, 2] * 8)                                  # zigzag: resting decides everything
add([1, MAXP, MAXP, 1, MAXP, 1, MAXP, 1, 1, MAXP, 1, MAXP, MAXP, 1, MAXP, 1, MAXP])
add(list(range(1, 18)))
# hidden: large
N = MAXN
add([1, MAXP] * (N // 2))                        # zigzag with the largest swings
add([1, 1, MAXP] * (N // 3))                     # rest fits perfectly: largest profit
add(rnd(N, 1, MAXP))
add(walk(N, 1000))
add(walk(N, 10**7))
add(list(range(N, 0, -1)))                       # always falling: 0
add(list(range(1, N + 1)))                       # always rising: one trade
add([MAXP] * N)
add([ri(1, 3) for _ in range(N)])
add([1, 2, 3] * (N // 3))
add([MAXP - ri(0, 5) if i % 4 in (1, 2) else ri(1, 5) for i in range(N)])
add(rnd(N - 1, 1, MAXP))
add([ri(1, 1000) * (1 if i % 3 else 10**6) for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

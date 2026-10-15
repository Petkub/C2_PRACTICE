# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10114)
MAXN = 200_000
MAXV = 10**9
MAXD = 10**15
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(D, d):
    n = len(d)
    assert 2 <= n <= MAXN
    assert 1 <= D <= MAXD
    assert all(1 <= x <= MAXV for x in d)
    tests.append(f"{n} {D}\n" + " ".join(map(str, d)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(4, [1, 2, 3, 4, 2])
add(2, [1, 1, 1, 1])
add(3, [5, 4])
add(10, [3, 3, 3])
add(6, [2, 9, 1, 1, 3, 8])
add(1, [2, 2, 2, 2, 2])
# hidden (small)
add(1, [1, 1])
add(5, [5, 5])
add(3, [1] * 6)                     # opposite stops at distance 3 both ways
add(7, [1, 1, 1, 1, 1, 1, 1, 6])
d = rnd(40, 1, 10)
add(sum(d) // 4, d)
d = rnd(300, 1, 1000)
add(sum(d) // 3, d)
d = rnd(3000, 1, MAXV)
add(sum(d) // 2, d)                 # every pair is close
d = rnd(5000, 1, 100)
add(sum(d) // 2 - 1, d)
d = [2] * 4000
add(sum(d) // 2, d)
# large
N = MAXN
d = [1] * N
add(N // 2, d)                      # every pair, many with equal ways
add(N // 2 - 1, d)                  # every pair except the opposite ones
d = rnd(N, 1, MAXV)
add(sum(d) // 4, d)
d = rnd(N, 1, MAXV)
add(sum(d) // 2, d)                 # every pair
d = rnd(N, 1, MAXV)
add(sum(d) // 3, d)
d = rnd(N, 1, MAXV)
add(sum(d) // 10, d)
add(MAXD, [MAXV] * N)               # the largest ring, every pair
add(MAXV * (N // 2) - 1, [MAXV] * N)
d = rnd(N, 1, 10)
add(1000, d)
d = rnd(N - 1, 1, 2) + [MAXV]      # one long gap
add(50_000, d)
add(MAXV * 3, [1 if i % 2 else MAXV for i in range(N)])
d = rnd(N, 999_999_000, MAXV)
add(sum(d) // 2 - ri(0, 10**13), d)
add(1, rnd(N, 2, MAXV))             # no pair at all
d = rnd(N, 1, MAXV)
add(sum(d) // 2 - sum(d) // 1000, d)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

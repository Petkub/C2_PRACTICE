# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(6012)
MAXN, MAXV = 500_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(L, R, p):
    n = len(p)
    assert 2 <= n <= MAXN and 1 <= L <= R <= n - 1
    assert all(-MAXV <= x <= MAXV for x in p)
    tests.append(f"{n} {L} {R}\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(1, 2, [3, -5, -2, 4, -1, 2])
add(2, 2, [1, 2, 3, 4, 5, 6])
add(1, 1, [-7, 4])
add(1, 3, [-1, -8, -3, -9, -2, -6, -1])
add(2, 3, [5, 9, -4, 1, -2, 8, -6, 3])
add(3, 4, [6, -9, 7, -1, 2, 5, -3, 8, -5, 4])
# hidden: small (every jump sequence is tried)
add(1, 1, [MAXV, MAXV])
add(1, 2, [-MAXV, -MAXV, -MAXV])
add(2, 3, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
add(1, 17, rnd(18, -100, 100))
add(1, 4, rnd(18, -MAXV, MAXV))
add(2, 5, rnd(20, -10, 10))
add(3, 3, rnd(16, -50, 50))                    # 16 = 1 + 3 * 5: reachable
add(3, 3, rnd(17, -50, 50))                    # not reachable
add(4, 9, rnd(22, -MAXV, MAXV))
add(5, 7, rnd(9, 1, 9))                        # too short to land on cell N
add(1, 5, [-1] * 12)
# hidden: medium
add(3, 40, rnd(2000, -MAXV, MAXV))
add(1, 1000, rnd(5000, -1000, 100))
# hidden: maximum size
N = MAXN
M = 200_000                                    # the tests with 10-digit values are shorter (file size)
add(1, N - 1, rnd(N, -1000, 1000))
add(1, N // 2, rnd(N, -1000, 0))
add(N // 4, N // 2, rnd(N, -1000, 1000))
add(1000, 100_000, rnd(M, -MAXV, MAXV // 10))
add(1, 1, [MAXV] * M)                          # every cell is used
add(1, M - 1, [-MAXV] * M)                     # one jump
add(2, 2, rnd(N, -1000, 1000))                 # N even: never lands on cell N
add(3, 3, rnd(N - 1, -999, 999))               # N - 1 = 1 + 3k: one forced path
add(7, 150_000, [MAXV - i for i in range(M)])  # decreasing values
add(1, M - 1, [-(MAXV - i) for i in range(M)])
add(5, 300_000, rnd(N, -1000, 1000))
add(49_999, 50_001, rnd(M, -MAXV, MAXV))       # only 4 jumps fit
add(1, 250_000, rnd(N, -10, 1))
add(100_000, 400_000, rnd(N, -1000, 1000))
add(2, 200_000, rnd(N, -MAXV // 10**6, MAXV // 10**6))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

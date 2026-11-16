# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20208)
MAXN, MAXP = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(k, p):
    n = len(p)
    assert 1 <= k <= n <= MAXN
    assert all(1 <= x <= MAXP for x in p)
    tests.append(f"{n} {k}\n" + " ".join(map(str, p)) + "\n")


# samples
add(2, [3, 1, 4, 1, 5])
add(4, [2, 2, 2, 2, 2])
add(6, [5, 1, 1, 3, 2, 5])
add(1, [MAXP])
add(1, [7, 7, 7, 7])
add(3, [6, 2, 9, 4, 1, 8, 3])
# hidden: small
add(2, [1, 1])
add(3, [10, 1, 1, 1, 1, 1, 1, 1, 1])          # one long chapter decides W, fewer days than K
add(4, rnd(12, 1, 20))
add(5, rnd(40, 1, 1000))
add(7, [MAXP] * 30)
add(13, rnd(80, 1, MAXP))
add(40, rnd(150, 1, 10))
add(60, rnd(120, 1, 3))                      # W is a small number, many equal splits
# hidden: maximum size (the answer is far above max p_i and N K is huge)
N = MAXN
add(2, rnd(N, 1, MAXP))
add(3, [MAXP] * N)                            # W about 6.7 * 10^13
add(17, rnd(N, 1, MAXP))
add(1000, rnd(N, 1, MAXP))
add(N // 2, rnd(N, 1, MAXP))
add(N // 3, rnd(N, 1, MAXP))
add(N // 2 + 1, sorted(rnd(N, 1, MAXP)))
add(N // 10, sorted(rnd(N, 1, MAXP), reverse=True))
add(N - 1, rnd(N, 1, MAXP))
p = rnd(N, 1, 1000)
p[N // 2] = MAXP                              # one huge chapter, the rest tiny
add(5000, p)
add(N // 4, rnd(N, 999_000_000, MAXP))
add(N, rnd(N, 1, MAXP))
add(1, rnd(N, 1, MAXP))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

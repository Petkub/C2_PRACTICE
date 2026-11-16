# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180002)
MAXN, MAXQ, MAXV, M31 = 200_000, 15 * 10**6, 10**9, 2**31
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(q, s, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and 0 <= s < M31
    assert all(1 <= v <= MAXV for v in a)
    t = f"{n} {q} {s}\n" + " ".join(map(str, a)) + "\n"
    assert len(t) <= 3_100_000
    tests.append(t)


# samples
add(3, 7, [4, 9, 2, 7, 5])
add(4, 0, [MAXV])
add(1, 2_147_483_647, [3, 1, 2])
add(10, 12_345, [5, 1, 8, 8, 2, 6, 3])
add(20, 1, [2, 7, 1, 8, 2, 8, 1, 8, 2, 8])
# hidden: small (brute runs on these)
add(1000, ri(0, M31 - 1), [ri(1, 20) for _ in range(10)])
add(10**5, ri(0, M31 - 1), [ri(1, MAXV) for _ in range(100)])
add(10**5, ri(0, M31 - 1), list(range(1, 2001)))                     # increasing: the answer is a_r
add(50_000, ri(0, M31 - 1), [ri(1, MAXV) for _ in range(3000)])
add(MAXQ, 0, [MAXV])                                                  # N = 1: 1.5 * 10^16
add(MAXQ, ri(0, M31 - 1), [ri(1, MAXV), ri(1, MAXV)])
# hidden: maximum size
N = MAXN
add(MAXQ, ri(0, M31 - 1), [ri(1, MAXV) for _ in range(N)])
add(MAXQ, ri(0, M31 - 1), [ri(1, MAXV) for _ in range(N)])
add(MAXQ, ri(0, M31 - 1), [MAXV] * N)                                  # all maximal
add(MAXQ, ri(0, M31 - 1), [i * 5000 for i in range(1, N + 1)])        # increasing
add(MAXQ, ri(0, M31 - 1), [MAXV - i * 4999 for i in range(N)])        # decreasing
a = [ri(1, 10**6) for _ in range(N)]
a[ri(0, N - 1)] = MAXV                                                 # one huge peak
add(MAXQ, ri(0, M31 - 1), a)
a = [ri(1, MAXV) for _ in range(N - 1)] + [MAXV]
add(MAXQ, ri(0, M31 - 1), a)
add(MAXQ, ri(0, M31 - 1), [ri(1, 1000) for _ in range(N)])
add(MAXQ, ri(0, M31 - 1), [ri(1, MAXV) for _ in range(N - 7)])        # N not a power of two

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

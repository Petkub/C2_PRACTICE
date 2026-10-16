# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20214)
MAXN, MAXB = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(m, k, b):
    n = len(b)
    assert 1 <= n <= MAXN
    assert 1 <= m <= n and 1 <= k <= n
    assert all(1 <= x <= MAXB for x in b)
    tests.append(f"{n} {m} {k}\n" + " ".join(map(str, b)) + "\n")


# samples
add(2, 2, [3, 1, 4, 1, 5, 9, 2])
add(3, 2, [1, 2, 3, 4, 5])
add(1, 5, [5, 4, 3, 2, 1])
add(1, 1, [MAXB])
add(2, 3, [1, 1, 1, 9, 1, 1, 2, 1])
add(3, 2, [6, 2, 8, 3, 3, 7, 1, 9, 4, 4])
# hidden: small
add(1, 1, [7])
add(2, 2, [7, 3, 4])                           # M K > N
add(1, 2, [5, 5])
add(2, 2, [1, 9, 1, 1, 9, 1])                  # bloomed pairs split by late flowers
add(3, 3, rnd(9, 1, 5))
add(4, 3, rnd(20, 1, 30))
add(5, 4, rnd(60, 1, 1000))
add(7, 10, rnd(80, 1, MAXB))                   # M K = 70 <= 80
add(9, 10, rnd(80, 1, MAXB))                   # M K = 90 > 80
add(30, 3, rnd(150, 1, 50))
add(1, 300, rnd(300, 1, MAXB))
# hidden: maximum size (the answer is a late bloom day)
N = MAXN
add(N, 1, rnd(N, 1, MAXB))                     # every flower is needed
add(N // 2, 1, rnd(N, 1, MAXB))
add(1, N, rnd(N, 1, MAXB))
add(N // 1000, 1000, rnd(N, 1, MAXB))
add(N // 3, 3, rnd(N, 1, MAXB))
add(400, 400, rnd(N, 1, MAXB))
add(N // 2, 2, sorted(rnd(N, 1, MAXB)))
add(N // 7, 7, sorted(rnd(N, 1, MAXB), reverse=True))
add(N // 4, 4, rnd(N, 1, MAXB))
add(65536, 65536, rnd(N, 1, MAXB))              # M K = 2^32: impossible
add(N // 2 + 1, 2, rnd(N, 1, MAXB))            # impossible by one bouquet
add(N // 2, 2, [MAXB] * N)
add(N // 5, 4, rnd(N, 1, 100_000))              # many equal days
b = rnd(N, 1, MAXB // 2)
for i in range(0, N, 50):
    b[i] = MAXB - i                             # a late flower in every block of 50
add(N // 50, 49, b)
add(ri(1, N // 10), 10, rnd(N, 1, MAXB))
add(1, N // 2, rnd(N, 1, MAXB))
add(N - 5, 1, rnd(N, 1, MAXB))
add(N // 30, 25, rnd(N, 1, MAXB))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

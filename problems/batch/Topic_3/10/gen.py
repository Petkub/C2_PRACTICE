# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20210)
MAXN, MAXV = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(k, a, b):
    n, m = len(a), len(b)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN
    assert 1 <= k <= n * m
    assert all(1 <= x <= MAXV for x in a + b)
    tests.append(f"{n} {m} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


# samples
add(4, [5, 1, 3], [2, 4])
add(3, [1, 1], [1, 2])
add(1, [MAXV], [MAXV])
add(9, [7, 2, 9], [4, 4, 1])
add(1, [6, 3, 8, 3], [5, 2, 9])
add(7, [10, 20, 30, 40], [1, 2, 3])
# hidden: small
add(2, [1], [5, 1, 3])
add(5, [4, 4, 4], [4, 4])
add(33, rnd(7, 1, 20), rnd(9, 1, 20))
add(1000, rnd(40, 1, 1000), rnd(50, 1, 1000))
add(80_000, rnd(300, 1, MAXV), rnd(400, 1, MAXV))
add(250_000, rnd(500, 1, 50), rnd(700, 1, 50))      # many equal prices
add(2_000_000, rnd(2000, MAXV - 100, MAXV), rnd(1000, MAXV - 100, MAXV))
add(999 * 777, rnd(999, 1, MAXV), rnd(777, 1, MAXV))   # the largest price
# hidden: big (K far from both ends, so taking sums one by one is too slow)
B = 100_000
add(B * B // 2, rnd(B, 1, MAXV), rnd(B, 1, MAXV))
add(B * B // 3 + 12_345, rnd(B, 1, MAXV), rnd(B, 1, MAXV))
add(B * B - 1, rnd(B, 1, MAXV), rnd(B, 1, MAXV))
add(B * B, [MAXV] * B, [MAXV] * B)                     # 2 * 10^9 does not fit in int
add(B * B // 2 + 1, rnd(B, MAXV - 1000, MAXV), rnd(B, MAXV - 1000, MAXV))
add(5_000_000_000 - 7, rnd(B, 1, 10), rnd(B, 1, 10))   # huge numbers of equal sums
add(ri(1, B * B), rnd(B, 1, MAXV), rnd(B, 1, 1000))
add(ri(1, 2 * 10**10), rnd(2 * MAXN // 2, 1, 999_999), rnd(MAXN // 2, 1, 999_999))
add(ri(1, 10**10), sorted(rnd(B, 1, MAXV)), sorted(rnd(B, 1, MAXV), reverse=True))
add(MAXN * 1000 // 2, rnd(MAXN, 1, 999_999), rnd(1000, 1, MAXV))
add(ri(1, MAXN) * 7, [ri(1, 999_999) for _ in range(7)], rnd(MAXN, 1, 999_999))
add(3 * 10**9, [1 + 2 * i for i in range(B)], [2 + 2 * i for i in range(B)])
add(4 * 10**9, rnd(150_000, 1, 99_999), rnd(150_000, 1, 99_999))
add(1, rnd(B, 1, MAXV), rnd(B, 1, MAXV))
add(B * B // 4, rnd(B, 1, MAXV // 1000), rnd(B, 1, MAXV))
add(B * B // 4 + 99, rnd(B, MAXV // 2, MAXV), rnd(B // 2, 1, MAXV // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

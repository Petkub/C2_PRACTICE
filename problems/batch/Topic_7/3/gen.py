# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(60003)
MAXN, MAXA, MAXQ, MAXS = 100, 10**5, 10**5, 10**5
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, s):
    n, q = len(a), len(s)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= MAXA for x in a) and all(1 <= x <= MAXS for x in s)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + f"\n{q}\n" + " ".join(map(str, s)) + "\n")


def queries(q, lo, hi):
    return [ri(lo, hi) for _ in range(q)]


# samples
add([1, 2, 3, 4], [5, 10, 11])
add([2, 2, 2], [4, 6])
add([100000], [100000, 99999])
add([1, 1, 1, 1, 1], [1, 2, 3, 4, 5])
add([5, 3, 8, 3, 6, 1], [9, 14, 2, 26])
add([7, 12, 7, 20, 5, 12, 9, 3], [24, 31, 75, 1, 41])
# hidden: small (all sets are listed)
add([1], [1])
add([3, 5], [1, 2, 3, 4, 5, 8, 100000])
add([ri(1, 10) for _ in range(20)], list(range(1, 60)))
add([ri(1, 100) for _ in range(20)], queries(200, 1, 2000))
add([ri(1, MAXA) for _ in range(18)], queries(100, 1, MAXS))
add([1] * 20, list(range(1, 21)))
add([ri(40000, 60000) for _ in range(20)], queries(300, 90000, MAXS))
# hidden: large
N, Q = MAXN, MAXQ
add([1] * N, queries(Q, 1, 100))                          # binomial coefficients, huge counts
add([ri(1, 2000) for _ in range(N)], queries(Q, 1, MAXS))
add([ri(1, MAXA) for _ in range(N)], queries(Q, 1, MAXS))
add([ri(1, MAXA) for _ in range(N)], [MAXS] * Q)
add([ri(900, 1100) for _ in range(N)], queries(Q, 50000, MAXS))
add([1000 * ri(1, 3) for _ in range(N)], [1000 * ri(1, 100) for _ in range(Q)])
add([i + 1 for i in range(N)], queries(Q, 1, 5050))       # distinct parts
add([MAXA] * N, [MAXS] * (Q // 2) + [MAXS - 1] * (Q // 2))
add([ri(1, 50) for _ in range(N)], [ri(1, 2500) for _ in range(Q)])
add([ri(1, 10) for _ in range(N)], queries(Q, 1, 1200))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

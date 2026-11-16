# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(50404)
MAXM, MAXQ, MAXV = 100, 200_000, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(c, x):
    m, q = len(c), len(x)
    assert 1 <= m <= MAXM and 1 <= q <= MAXQ
    assert len(set(c)) == m and all(1 <= v <= MAXV for v in c)
    assert all(1 <= v <= MAXV for v in x)
    tests.append(f"{m} {q}\n" + " ".join(map(str, c)) + "\n" + "\n".join(map(str, x)) + "\n")


def coins(m, lo, hi):
    return random.sample(range(lo, hi + 1), m)


def queries(q, lo, hi):
    return [ri(lo, hi) for _ in range(q)]


# samples
add([1, 3, 4], [6, 7, 2])
add([5, 7], [3, 12, 23, 24])
add([2], [10, 7])
add([10, 1, 25], [30, 40, 63])
add([1000000], [1000000, 999999])
add([4, 9, 6], [15, 1, 26, 13, 8])
# hidden: small (the brute force checks these)
add([1], [1, 5, 30])
add([3, 5], list(range(1, 31)))
add([2, 6, 9], list(range(1, 41)))
add([1, 7, 10], list(range(1, 46)))
add(coins(4, 2, 12), queries(30, 1, 60))
add(coins(6, 3, 20), queries(30, 1, 80))
add([6, 10, 15], list(range(1, 61)))
add(coins(3, 40, 60), queries(20, 1, 200))
# hidden: maximum size
Q = MAXQ
add(coins(MAXM, 1, MAXV), queries(Q, 1, MAXV))
add(coins(MAXM, 1, 2000), queries(Q, 1, MAXV))
add(coins(MAXM, 1000, 5000), queries(Q, MAXV - 100_000, MAXV))
add([1], queries(Q - 1, 1, MAXV) + [MAXV])                     # largest answer
add([2 * v for v in coins(MAXM, 1, 20000)], queries(Q, 1, MAXV))  # every odd total is impossible
add(sorted(coins(MAXM, 100_000, MAXV)), queries(Q, 1, MAXV))    # mostly impossible
add([1] + [v * 50 + 1 for v in range(1, MAXM)], queries(Q, 1, MAXV))
add(list(range(MAXV, MAXV - MAXM, -1)), queries(Q, 1, MAXV))
add([997, 1000, 1003, 1] + coins(MAXM - 4, 1004, 3000), queries(Q, 1, MAXV))
add(coins(MAXM, 1, 100), list(range(MAXV, MAXV - Q, -1)))
add([999_983, 999_979], queries(Q, 1, MAXV))
add(coins(10, 1, 300), queries(Q, 1, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

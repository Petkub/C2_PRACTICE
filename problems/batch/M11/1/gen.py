# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511011)
MAXN = MAXQ = 100000
MAXD = 10 ** 9
MAXB = 10 ** 6
tests = []


def add(deliveries, qs, shuffle=True):
    n, q = len(deliveries), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= d <= MAXD and 1 <= b <= MAXB for d, b in deliveries) and all(1 <= t <= MAXD for t in qs)
    deliveries = list(deliveries)
    if shuffle:
        random.shuffle(deliveries)
    tests.append(f"{n} {q}\n" + "".join(f"{d} {b}\n" for d, b in deliveries) + " ".join(map(str, qs)) + "\n")


def spread(n, lo, hi, blo, bhi):
    return [(random.randint(lo, hi), random.randint(blo, bhi)) for _ in range(n)]


def dense(n, start, gap, blo, bhi):

    out, d = [], start
    for _ in range(n):
        out.append((d, random.randint(blo, bhi)))
        d = min(MAXD, d + random.randint(0, gap))
    return out


def high_queries(q, lo, hi):
    return [random.randint(lo, hi) for _ in range(q)]


add([(2, 3), (4, 1), (9, 2)], [1, 3, 5, 10], False)
add([(1, 1), (5, 2), (5, 1), (6, 10)], [4, 7, 100], False)
add([(MAXD, MAXB)], [MAXD], False)
add([(3, 5), (4, 5)], [2, 3, 12], False)
add([(1, 2), (4, 4), (6, 1), (15, 3), (16, 2)], [5, 9, 16, 17, 30, 3], False)

add([(1, 1)], [1, 2, 3])
add([(5, 2), (5, 2), (5, 2)], [4, 5, 9, 10, 11])
add(spread(6, 1, 30, 1, 5), high_queries(8, 1, 60))
add(spread(10, 1, 100, 1, 30), high_queries(10, 1, 200))
add(dense(20, 7, 3, 1, 9), high_queries(15, 1, 400))
add(spread(50, 1, 2000, 1, 100), high_queries(40, 1, 6000))
add(spread(300, 1, 10 ** 5, 1, 1000), high_queries(300, 1, 3 * 10 ** 5))
add(dense(1000, 1, 5, 1, 10), high_queries(500, 1, 10 ** 5))

add(spread(5000, 1, 10 ** 6, 1, 500), high_queries(5000, 1, 2 * 10 ** 6))
add(dense(4000, 100, 2, MAXB // 2, MAXB), high_queries(3000, 1, MAXD))
add(dense(3000, 1, 1, MAXB - 10, MAXB), high_queries(3000, 2000, 10 ** 7))

add(spread(MAXN, 1, MAXD, 1, MAXB), high_queries(MAXQ, MAXD // 2, MAXD))
add(dense(MAXN, 1, 3, MAXB - 1000, MAXB), high_queries(MAXQ, 2 * 10 ** 5, MAXD))
add(dense(MAXN, 1000, 20000, 1, 30000), high_queries(MAXQ, 10 ** 9 // 2, MAXD))
add(spread(MAXN, 1, MAXD, 1, 20000), [MAXD] * MAXQ)
add(dense(MAXN, 1, 1, 1, 3), high_queries(MAXQ, 10 ** 5, 3 * 10 ** 5))
add(spread(MAXN, 1, 10 ** 6, 1, MAXB), high_queries(MAXQ, 9 * 10 ** 5, MAXD))
add([(d, MAXB) for d in range(1, MAXN + 1)], high_queries(MAXQ, MAXN, MAXD))
add(dense(MAXN, 5, 40000, 1, 40000), high_queries(MAXQ, MAXD - 10 ** 8, MAXD))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

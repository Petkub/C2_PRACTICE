# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80110)
MAXT = 50_000
MAXB = 10 ** 6
MAXQ = 10 ** 12
tests = []


def add(qs):
    assert 1 <= len(qs) <= MAXT
    assert all(2 <= b <= MAXB and 1 <= p <= q <= MAXQ for b, p, q in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{b} {p} {q}\n" for b, p, q in qs))


def rng(lo, hi):
    a, b = random.randint(lo, hi), random.randint(lo, hi)
    return min(a, b), max(a, b)


def logb():
    """a base spread over all sizes"""
    return min(MAXB, max(2, int(10 ** random.uniform(0.3, 6))))


# samples
add([(10, 1, 25), (10, 95, 105)])
add([(2, 1, MAXQ), (16, 47, 49)])
add([(3, 1, 100), (1000, 999, 1001), (7, 49, 49)])
add([(10, 1, MAXQ), (36, 1000, MAXQ)])
add([(MAXB, 5, 5), (500_000, 1, 400_000), (40_000, 1, MAXQ)])

# hidden: small (the brute force adds every term)
add([(2, 1, 1)])
add([(random.randint(2, 12),) + rng(1, 3000) for _ in range(1000)])
edge = []
for b in [2, 3, 4, 5, 9, 10, 11, 16, 99, 100, 101, 255, 256, 997, 1000]:
    edge += [(b, 1, b - 1), (b, 1, b), (b, b, b), (b, b - 1, b + 1), (b, 1, b * b), (b, b * b, b * b),
             (b, b * b - 1, b * b + 1)]
add(edge)
add([(random.randint(46_342, MAXB),) + rng(1, 3 * 10 ** 6) for _ in range(10)])
add([(random.randint(2, MAXB),) + rng(1, 10 ** 6) for _ in range(30)])
add([(10,) + rng(1, 10 ** 5) for _ in range(300)])
pw = []
for b in range(2, 21):
    x = b
    while x <= MAXQ:
        pw += [(b, x, x), (b, x - 1, x), (b, x, min(x + 1, MAXQ))]
        x *= b
add(pw)
add([(logb(), x, x) for x in (random.randint(1, MAXQ) for _ in range(1000))])
add([(b, b * k, b * k + 2) for b, k in ((random.randint(46_342, MAXB), random.randint(1, 10 ** 6)) for _ in range(1000))])
# hidden: largest (every test has many ranges of length about 10^12)
add([(random.randint(2, MAXB), random.randint(1, 10 ** 6), random.randint(MAXQ - 10 ** 6, MAXQ)) for _ in range(MAXT)])
add([(random.randint(2, 10), 1, MAXQ) for _ in range(MAXT)])
add([(MAXB, 1, MAXQ)] * MAXT)
add([(random.randint(MAXB - 100, MAXB),) + rng(1, MAXQ) for _ in range(MAXT)])
add([(random.randint(46_342, MAXB),) + rng(1, MAXQ) for _ in range(MAXT)])
add([(random.randint(2, 1000),) + rng(1, MAXQ) for _ in range(MAXT)])
add([(logb(), random.randint(1, 1000), MAXQ) for _ in range(MAXT)])
add([(logb(),) + rng(1, MAXQ) for _ in range(MAXT)])
add([(random.choice([2, 3, 10, 999_999, MAXB]), 1, random.randint(MAXQ - 1000, MAXQ)) for _ in range(MAXT)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

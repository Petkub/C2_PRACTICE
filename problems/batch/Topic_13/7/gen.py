# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13007)
MAXB = 10 ** 11
MAXQ = 10_000
tests = []


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    assert all(0 <= a <= b < MAXB for a, b in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b}\n" for a, b in qs))


def rq(lo, hi, q):
    out = []
    for _ in range(q):
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        out.append((min(a, b), max(a, b)))
    return out


def near_pow(hi, q):
    """ends close to powers of two and to 2^k - 1"""
    out = []
    top = hi.bit_length()
    for _ in range(q):
        ends = []
        for _ in range(2):
            k = random.randint(0, top)
            x = (1 << k) + random.randint(-2, 2)
            if random.random() < 0.3:
                x = (1 << k) - (1 << random.randint(0, k)) + random.randint(-1, 1)
            ends.append(min(max(x, 0), hi))
        out.append((min(ends), max(ends)))
    return out


# samples
add([(0, 5), (3, 4)])
add([(0, 0), (4, 4)])
add([(7, 7), (8, 8), (0, 15)])
add([(0, 99_999_999_999), (1023, 1024)])
add([(10, 20), (1000, 1023), (12345, 67890)])
# hidden: small (the brute force builds the rows)
add([(0, 0)])
add([(r, r) for r in range(64)])
add(rq(0, 300, 1000))
add(near_pow(4000, 500))
add([(0, 4999), (4999, 4999), (4096, 4999), (0, 4095)] + rq(0, 4999, 20))
add(rq(2000, 4000, 300))
# hidden: medium (rows up to 10^7)
add(rq(0, 10 ** 7, 5))
add([(0, 10 ** 7 - 1)])
# hidden: large
add(rq(0, MAXB - 1, MAXQ))
add([(0, MAXB - 1)] * MAXQ)
add(near_pow(MAXB - 1, MAXQ))
add([(0, random.randint(MAXB // 2, MAXB - 1)) for _ in range(MAXQ)])
add(rq(MAXB - 10 ** 6, MAXB - 1, MAXQ))
add([(random.randint(0, 10 ** 6), random.randint(MAXB - 10 ** 6, MAXB - 1)) for _ in range(MAXQ)])
add(rq(10 ** 10, MAXB - 1, MAXQ))
add([(0, (1 << 36) - 1), (1 << 36, MAXB - 1), (0, MAXB - 1), (MAXB - 1, MAXB - 1)] + rq(0, MAXB - 1, 100))
add([(0, (1 << k) - 1) for k in range(37)] + [((1 << k) - 1, (1 << k) - 1) for k in range(37)] + [(0, 0)])
add([(0, MAXB - 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

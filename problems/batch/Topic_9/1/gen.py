# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13001)
MAXQ = 50_000
MAXA = MAXB = 10 ** 18
MAXM = 10 ** 9
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, b, m in qs:
        assert 1 <= a <= MAXA and 0 <= b <= MAXB and 1 <= m <= MAXM
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b} {m}\n" for a, b, m in qs))


MODS = [999_999_937, 999_999_929, 999_999_893, 998_244_353, 999_999_751]
MODS = [p for p in MODS if p <= MAXM]

# samples
add([(2, 10, 1000), (3, 4, 100), (10, 5, 7)])
add([(7, 0, 10), (6, 1, 4), (12, 2, 12)])
add([(2, 1_000_000_000_000_000_000, 999_999_937)])
add([(123_456_789_012_345_678, 3, 1000), (5, 3, 1)])
add([(1, 999, 13), (9, 9, 9), (2, 30, 1_000_000_000), (3, 3, 26)])
# hidden: small (the brute force loops b times)
add([(1, 0, 1)])
add([(ri(1, 50), ri(0, 30), ri(1, 100)) for _ in range(300)])
add([(ri(1, MAXA), ri(0, 1000), ri(1, MAXM)) for _ in range(2000)])
add([(ri(1, MAXA), ri(0, 1000), 1) for _ in range(200)] + [(ri(1, MAXA), 0, ri(1, MAXM)) for _ in range(200)])
add([(MAXA, ri(0, 2000), ri(MAXM - 1000, MAXM)) for _ in range(1000)])
add([(m * ri(1, 10 ** 8), ri(0, 1000), m) for m in [ri(2, MAXM) for _ in range(500)]])  # a is a multiple of m
add([(ri(1, MAXA), ri(10 ** 5, 10 ** 6), ri(1, MAXM)) for _ in range(40)])
add([(MAXM - 1, ri(1, 3000), MAXM) for _ in range(3000)])               # products near 10^18
# hidden: large (b up to 10^18)
add([(ri(1, MAXA), ri(MAXB // 2, MAXB), ri(1, MAXM)) for _ in range(MAXQ)])
add([(ri(1, MAXA), MAXB, random.choice(MODS)) for _ in range(MAXQ)])
add([(MAXA, MAXB, MAXM)] * MAXQ)
add([(MAXA - ri(0, 10 ** 6), MAXB - ri(0, 10 ** 6), MAXM - ri(0, 10 ** 3)) for _ in range(MAXQ)])
add([(ri(1, MAXM), ri(1, MAXB), ri(MAXM // 2, MAXM)) for _ in range(MAXQ)])
add([(ri(1, MAXA), ri(0, MAXB), random.choice([1, 2, 3, ri(1, MAXM)])) for _ in range(MAXQ)])
add([(ri(1, MAXA), (1 << 59) - 1 if i % 2 else ri(1, MAXB), random.choice(MODS)) for i in range(MAXQ)])
add([(2, ri(1, MAXB), random.choice(MODS)) for _ in range(MAXQ)])
add([(ri(1, 10 ** 9), ri(1, MAXB), ri(1, MAXM)) for _ in range(MAXQ)])
add([(ri(1, MAXA), ri(10 ** 17, MAXB), 1 if i % 1000 == 0 else ri(MAXM - 10 ** 6, MAXM)) for i in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

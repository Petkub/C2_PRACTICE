# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(141101)
MAXQ = 10_000
MAXA = MAXB = 10 ** 18
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, b, k in qs:
        assert 0 <= a <= MAXA and 1 <= b <= MAXB and 1 <= k <= 18
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b} {k}\n" for a, b, k in qs))


def near_border(k):
    # a^b close to 10^k from either side
    a = ri(2, 99)
    b = 1
    while a ** (b + 1) < 10 ** k:
        b += 1
    return (a, b + ri(0, 1), k)


# samples
add([(2, 10, 3), (2, 10, 5), (7, 2, 2)])
add([(0, 5, 3), (1, MAXB, 18), (10, 3, 3)])
add([(2, MAXB, 18)])
add([(MAXA - 1, MAXB - 1, 18), (MAXA, 1, 18)])
add([(5, 3, 3), (12345, 1, 3), (3, 40, 1), (13, 2, 2)])
# hidden: small b (the brute force multiplies b times)
add([(ri(0, 20), ri(1, 30), ri(1, 18)) for _ in range(500)])
add([(ri(0, MAXA), ri(1, 300), ri(1, 18)) for _ in range(300)])
add([near_border(ri(1, 18)) for _ in range(1000)])
add([(10 ** ri(0, 18), ri(1, 20), ri(1, 18)) for _ in range(500)])
add([(ri(0, 1), ri(1, MAXB), ri(1, 18)) for _ in range(200)] + [(MAXA - ri(0, 9), ri(1, 2), 18) for _ in range(200)])
add([(ri(MAXA // 10, MAXA), ri(1000, 3000), 18) for _ in range(30)])
add([(ri(2, 9) * 10 ** ri(0, 3), ri(1000, 20000), ri(10, 18)) for _ in range(5)])
# hidden: large (b up to 10^18)
add([(ri(0, MAXA), ri(1, MAXB), ri(1, 18)) for _ in range(MAXQ)])
add([(ri(MAXA - 10 ** 9, MAXA), ri(MAXB - 10 ** 9, MAXB), 18) for _ in range(MAXQ)])
add([(ri(2, MAXA), ri(MAXB // 2, MAXB), ri(10, 18)) for _ in range(MAXQ)])
add([(MAXA - 1, MAXB, 18)] * MAXQ)
add([(random.choice([2, 3, 7, 999_999_999_999_999_999, 123_456_789_123_456_789]), ri(1, MAXB), ri(13, 18)) for _ in range(MAXQ)])
add([(ri(1, 10 ** 6) * random.choice([1, 2, 5, 10, 16, 625]), ri(10 ** 15, MAXB), ri(1, 18)) for _ in range(MAXQ)])
add([(ri(0, MAXA), ri(1, MAXB), 18) if i % 3 else (ri(0, 1), ri(1, MAXB), ri(1, 18)) for i in range(MAXQ)])
add([(ri(2, MAXA), ri(10 ** 17, MAXB), ri(1, 9)) if i % 2 else (ri(2, MAXA), ri(10 ** 17, MAXB), ri(10, 18)) for i in range(MAXQ)])
add([near_border(ri(1, 18)) if i % 2 else (ri(10 ** 17, MAXA), ri(10 ** 17, MAXB), ri(16, 18)) for i in range(MAXQ)])
add([(ri(3, 10 ** 6) | 1, MAXB - ri(0, 1000), 18) for _ in range(MAXQ)])
# a^b just past 10^K with a big base: a check that multiplies before comparing overflows here
add([(ri(10 ** 9, MAXA), ri(2, 4), ri(10, 18)) if i % 2 else (ri(3 * 10 ** 9, MAXA), 2, 18) for i in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

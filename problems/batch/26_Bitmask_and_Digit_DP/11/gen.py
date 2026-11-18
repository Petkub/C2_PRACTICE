# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(26009)
MAXV, MAXQ = 10**18, 50_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, b, k in qs:
        assert 1 <= a <= b <= MAXV and 1 <= k <= 10
    t = f"{len(qs)}\n" + "".join(f"{a} {b} {k}\n" for a, b, k in qs)
    assert len(t) <= 3_000_000
    tests.append(t)


def logu(lo, hi):
    d = ri(len(str(lo)), len(str(hi)))
    return max(lo, min(hi, ri(10 ** (d - 1), 10 ** d - 1)))


def few_digit_number(nd, digits):
    first = [d for d in digits if d > 0] or [ri(1, 9)]
    s = str(random.choice(first)) + "".join(str(random.choice(digits)) for _ in range(nd - 1))
    return int(s)


def short_range(span, k=None):
    a = logu(1, MAXV - span)
    return (a, a + ri(0, span), k or ri(1, 10))


def long_range(k=None):
    a, b = logu(1, MAXV), logu(1, MAXV)
    a, b = min(a, b), max(a, b)
    return (a, b, k or ri(1, 10))


def edge_range(k=None):
    nd1, nd2 = ri(1, 18), ri(1, 18)
    a = few_digit_number(nd1, random.sample(range(10), ri(1, 4)))
    b = few_digit_number(nd2, random.sample(range(10), ri(1, 4)))
    if random.random() < 0.1:
        b = MAXV
    a, b = min(a, b), max(a, b)
    return (a, b, k or ri(1, 5))


add([(10, 30, 1), (100, 130, 2)])
add([(1, 1000, 1)])
add([(1, MAXV, 2), (1, MAXV, 1), (9, 10, 1)])
add([(999999999999999000, MAXV, 3), (777777777777777777, 888888888888888888, 1), (55, 55, 1)])
add([(1, 99999, 10), (5, 5, 1), (123, 4567, 2)])

add([(1, 1, 1), (MAXV, MAXV, 1), (MAXV, MAXV, 10), (MAXV - 1, MAXV, 1), (1, 9, 1), (10, 10, 1)])
add([(ri(1, 2000), ri(2000, 5000), ri(1, 10)) for _ in range(300)])
add([short_range(1000) for _ in range(500)])
add([short_range(100000, ri(1, 3)) for _ in range(60)])
add([(10 ** e - ri(0, 50000), 10 ** e + ri(0, 50000), ri(1, 4)) for e in range(5, 18)])
add([(1, 2_000_000, k) for k in range(1, 11)])

add([long_range() for _ in range(2000)] + [edge_range() for _ in range(2000)])
add([(1, MAXV, k) for k in range(1, 11)] + [(1, MAXV - 1, k) for k in range(1, 11)]
    + [(10 ** e, 10 ** (e + 1) - 1, k) for e in range(18) for k in range(1, 11)])

add([long_range() for _ in range(MAXQ)])
add([long_range(ri(3, 10)) for _ in range(MAXQ)])
add([edge_range() for _ in range(MAXQ)])
add([(logu(1, 10**6), logu(10**17, MAXV), ri(1, 10)) for _ in range(MAXQ)])
add([(1, logu(10**17, MAXV), ri(4, 10)) for _ in range(MAXQ)])
add([long_range(1) for _ in range(MAXQ // 2)] + [long_range(2) for _ in range(MAXQ // 2)])
add([short_range(10 ** ri(1, 12)) for _ in range(MAXQ)])
add([(ri(1, 10**9), MAXV - ri(0, 10**9), ri(1, 10)) for _ in range(MAXQ)])
add([edge_range(ri(1, 10)) if i % 2 else long_range() for i in range(MAXQ)])
add([(1, MAXV, 10)] * MAXQ)
add([long_range() for _ in range(MAXQ - 1)] + [(1, MAXV, 5)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(26002)
MAXV, MAXQ, MAXP = 10**18, 30_000, 18
tests = []


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, b, p in qs:
        assert 1 <= a <= b <= MAXV
        assert 1 <= len(p) <= MAXP and all(c in "0123456789" for c in p)
    t = "%d\n" % len(qs) + "".join("%d %d %s\n" % q for q in qs)
    assert len(t) <= 3_000_000
    tests.append(t)


def rand_p(lo=1, hi=MAXP, zero_share=25):
    n = random.randint(lo, hi) if random.randint(0, 2) == 0 else random.randint(lo, min(hi, max(lo, 5)))
    p = [random.randint(0, 9) for _ in range(n)]
    if random.randint(1, 100) <= zero_share:
        p[0] = 0
    return "".join(map(str, p))


def logu(lo, hi):
    d = random.randint(len(str(lo)), len(str(hi)))
    return max(lo, min(hi, random.randint(10 ** (d - 1), 10 ** d - 1)))


def holder(p, nd):
    pos = sorted(random.sample(range(1, nd), len(p)))
    s = [random.randint(0, 9) for _ in range(nd)]
    s[0] = random.randint(1, 9)
    for i, c in zip(pos, p):
        s[i] = int(c)
    v = int("".join(map(str, s)))
    assert 1 <= v <= MAXV
    return v


def lucky_a(p, hi_digits=18):
    nd = random.randint(len(p) + 1, max(len(p) + 1, hi_digits))
    return holder(p, min(nd, 18))


def big_query(zero_share=25, lucky_share=40):
    p = rand_p(1, MAXP, zero_share)
    if len(p) < 18 and random.randint(1, 100) <= lucky_share:
        a = lucky_a(p)
        b = random.randint(a, MAXV) if random.randint(0, 1) else min(MAXV, a + logu(1, 10**17))
    else:
        a, b = sorted((logu(1, MAXV), logu(1, MAXV)))
    return (a, b, p)


def small_query(span, zero_share=30, lucky_share=40, maxd=18):
    p = rand_p(1, 4, zero_share)
    if random.randint(1, 100) <= lucky_share:
        a = holder(p, random.randint(len(p) + 1, max(len(p) + 1, min(18, maxd))))
    else:
        a = logu(1, 10 ** maxd - 1)
    b = min(MAXV, a + random.randint(0, span))
    return (a, b, p)


add([(1, 200, "168"), (1600, 1700, "168")])
add([(1, 120, "10")])
add([(5, 1000, "7"), (2, 99999, "2026"), (3, 3000, "33"), (12, 345, "123456")])
add([(2, MAXV, "9"), (2, MAXV, "168"), (2, MAXV, "123456789012345678"), (2, 99, "999")])
add([(31415926, 271828182845, "520"), (6, 10**12, "1000"), (11, 10**18 - 1, "89898989")])

add([(a, b, p) for a in range(1, 60, 7) for b in (a, a + 30, a + 300) for p in ("0", "1", "00", "01", "10", "11", "05")])
add([small_query(600, 30, 40, 4) for _ in range(500)])
add([small_query(1000, 50, 50, 18) for _ in range(400)])
add([(max(1, 10 ** e - random.randint(0, 300)), min(MAXV, 10 ** e + random.randint(0, 300)), rand_p(1, 3, 40))
     for e in range(1, 19) for _ in range(10)])
ps = [rand_p(10, 17, 30) for _ in range(150)]
add([(a, min(MAXV, a + random.randint(0, 2000)), p) for p in ps for a in [holder(p, random.randint(len(p) + 1, 18))]])
add([(MAXV - random.randint(0, 3000), MAXV, rand_p(1, 18, 30)) for _ in range(200)])
add([(a, a, p) for p in (rand_p(1, 6, 40) for _ in range(800)) for a in [lucky_a(p) if random.randint(0, 1) else logu(1, MAXV)]])

add([big_query() for _ in range(2000)])
add([big_query(60, 60) for _ in range(2000)])

add([big_query() for _ in range(MAXQ)])
add([big_query(50, 50) for _ in range(MAXQ)])
add([big_query(25, 80) for _ in range(MAXQ)])
add([(1, MAXV, rand_p(1, 18, 30)) if i % 2 else big_query(30, 60) for i in range(MAXQ)])
add([(lucky_a(p), MAXV, p) for p in (rand_p(1, 6, 35) for _ in range(MAXQ))])
add([big_query(30, 50) if i % 3 else (2, MAXV, "0" * random.randint(1, 18)) for i in range(MAXQ)])
add([(a, min(MAXV, a + logu(10**6, 10**15)), p) for p in (rand_p(8, 17, 30) for _ in range(MAXQ))
     for a in [lucky_a(p)]])
add([(10 ** random.randint(0, 16) + random.randint(0, 1), 10 ** random.randint(17, 18) - random.randint(0, 1),
      rand_p(1, 4, 40)) for _ in range(MAXQ)])
add([big_query(40, 40) for _ in range(MAXQ)])
add([big_query(20, 70) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert 18 <= len(tests) <= 30
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open("tests/%02d.in" % i, "w") as f:
        f.write(t)

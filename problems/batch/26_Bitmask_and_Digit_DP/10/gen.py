# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(26011)
MAXA, MAXK, MAXQ = 10**17, 2 * 10**14, 60_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, k in qs:
        assert 0 <= a <= MAXA and 1 <= k <= MAXK
    t = f"{len(qs)}\n" + "".join(f"{a} {k}\n" for a, k in qs)
    assert len(t) <= 3_000_000
    tests.append(t)


def logu(lo, hi):
    d = ri(len(str(lo)), len(str(hi)))
    return max(lo, min(hi, ri(10 ** (d - 1), 10 ** d - 1)))


def zig(nd):
    while True:
        s = [ri(1, 9)]
        up = random.random() < 0.5
        ok = True
        for _ in range(nd - 1):
            p = s[-1]
            if (up and p == 9) or (not up and p == 0):
                ok = False
                break
            s.append(ri(p + 1, 9) if up else ri(0, p - 1))
            up = not up
        if ok:
            return int("".join(map(str, s)))


def rand_a():
    r = random.random()
    if r < 0.5:
        return zig(ri(1, 17))
    if r < 0.6:
        return 10 ** ri(0, 17) - ri(0, 1)
    return logu(1, MAXA)


add([(0, 1), (11, 3), (99, 3)])
add([(122, 5)])
add([(0, 100000), (123456, 777777), (98765, 1)])
add([(MAXA, MAXK), (0, MAXK), (MAXA, 1)])
add([(31415926535, 2718281828), (8088, 2), (11, 1)])

add([(a, k) for a in range(0, 130) for k in (1, 2, 5)])
add([(zig(ri(1, 6)), ri(1, 300)) for _ in range(500)])
add([(logu(1, 10**9), ri(1, 100)) for _ in range(500)])
add([(zig(ri(7, 17)), ri(1, 20)) for _ in range(300)])
add([(10 ** e - 1, k) for e in range(1, 18) for k in (1, 3)] + [(10 ** e, 2) for e in range(18)])
add([(MAXA - ri(0, 10**6), ri(1, 5)) for _ in range(100)])

add([(rand_a(), logu(1, MAXK)) for _ in range(5000)])
add([(rand_a(), logu(1, 10**6)) for _ in range(5000)])

add([(rand_a(), logu(1, MAXK)) for _ in range(MAXQ)])
add([(zig(ri(1, 17)), logu(1, MAXK)) for _ in range(MAXQ)])
add([(zig(17), ri(1, MAXK)) for _ in range(MAXQ)])
add([(logu(1, MAXA), ri(MAXK // 2, MAXK)) for _ in range(MAXQ)])
add([(0, logu(1, MAXK)) for _ in range(MAXQ // 2)] + [(MAXA, logu(1, MAXK)) for _ in range(MAXQ // 2)])
add([(rand_a(), ri(10**6, 10**9)) for _ in range(MAXQ)])
add([(zig(ri(10, 17)), ri(1, 10**4)) if i % 2 else (rand_a(), MAXK) for i in range(MAXQ)])
add([(MAXA, MAXK)] * (MAXQ // 2) + [(zig(16), MAXK) for _ in range(MAXQ // 2)])
add([(rand_a(), logu(1, MAXK)) for _ in range(MAXQ)])
add([(10 ** ri(0, 17) - ri(0, 1), logu(1, MAXK)) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

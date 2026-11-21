# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(106172)
MAXN, MAXF, MAXM, MAXP = 10 ** 9, 100, 10000, 10 ** 6
tests = []


def ri(a, b):
    k = b - a + 1
    bits = k.bit_length()
    while True:
        r = random.getrandbits(bits)
        if r < k:
            return a + r


def add(n, F, A, matches):
    assert 1 <= n <= MAXN and 1 <= F <= MAXF and 1 <= A <= F
    assert 0 <= len(matches) <= min(n, MAXM)
    last = 0
    for d, p, c in matches:
        assert isinstance(d, int) and last < d <= n
        assert isinstance(p, int) and 1 <= p <= MAXP
        assert isinstance(c, int) and 1 <= c <= F
        last = d
    tests.append(f"{n} {F} {A}\n{len(matches)}\n" + "".join(f"{d} {p} {c}\n" for d, p, c in matches))


def days_clustered(n, m, clusters, gapmax):
    sizes = [m // clusters + (1 if i < m % clusters else 0) for i in range(clusters)]
    steps = [[ri(1, gapmax + 1) for _ in range(s)] for s in sizes]
    free = n - sum(sum(s) for s in steps) - ri(0, 5)
    assert free >= 0
    days, d = [], 0
    for i in range(clusters):
        lead = free if i == clusters - 1 else ri(0, free // (clusters - i))
        free -= lead
        d += lead
        for s in steps[i]:
            d += s
            days.append(d)
    assert all(x < y for x, y in zip(days, days[1:])) and 1 <= days[0] and days[-1] <= n
    return days


def big(F, A, clusters, gapmax, plo, phi, clo, chi):
    days = days_clustered(MAXN, MAXM, clusters, gapmax)
    add(MAXN, F, A, [(d, ri(plo, phi), ri(clo, min(chi, F))) for d in days])


def bait(F, A, clusters, gapmax):
    days = days_clustered(MAXN, MAXM, clusters, gapmax)
    ms = []
    for d in days:
        if ri(0, 3) == 0:
            ms.append((d, ri(MAXP // 2, MAXP), ri(1, F)))
        else:
            ms.append((d, ri(1, MAXP // 20), ri(1, F)))
    add(MAXN, F, A, ms)


def small(n, F, A, m, phi=30):
    chosen = set()
    while len(chosen) < m:
        chosen.add(ri(1, n))
    add(n, F, A, [(d, ri(1, phi), ri(1, F)) for d in sorted(chosen)])


add(6, 8, 4, [(3, 4, 1), (4, 7, 6), (5, 7, 4)])
add(1000000000, 10, 4, [(3, 5, 2), (1000000000, 9, 10)])
add(5, 6, 6, [(1, 10, 3)])
add(7, 6, 3, [(3, 8, 1), (5, 9, 1), (7, 9, 3)])


add(1, 1, 1, [])
add(1, 1, 1, [(1, 5, 1)])
add(3, 100, 100, [(2, 1000000, 100), (3, 1000000, 1)])
add(4, 1, 1, [(2, 1000000, 1), (3, 1000000, 1), (4, 1000000, 1)])
add(12, 7, 5, [(2, 9, 3), (3, 1, 1), (5, 8, 3), (6, 7, 2), (9, 6, 6), (12, 9, 1)])
for _ in range(3):
    F = ri(4, 15)
    small(ri(6, 14), F, ri(2, F), ri(2, 6))
for _ in range(2):
    F = ri(20, 100)
    small(ri(3000, 20000), F, ri(2, F), ri(200, 2000), MAXP)
small(100000, 100, 37, 10000, MAXP)


bait(100, 31, 10, 3)
bait(100, 47, 3, 2)
bait(97, 13, 25, 6)
bait(100, 64, 1, 1)
big(100, 23, 8, 4, 1, MAXP, 1, 100)
big(100, 9, 40, 12, 1, MAXP, 1, 30)
big(100, 50, 5, 2, MAXP // 2, MAXP, 1, 100)
big(100, 2, 10, 60, 1, MAXP, 1, 100)
big(100, 100, 6, 3, 1, MAXP, 1, 100)
big(100, 1, 6, 5, 1, MAXP, 1, 100)
big(83, 29, 20, 3, 1, MAXP, 20, 83)
big(100, 41, 2, 8, MAXP - 1000, MAXP, 1, 10)
big(60, 17, 12, 2, 1, MAXP, 1, 60)
big(100, 7, 10000, 0, 1, MAXP, 1, 100)
big(1, 1, 3, 0, MAXP, MAXP, 1, 1)
big(100, 33, 1, 0, 1, MAXP, 1, 100)
bait(100, 19, 50, 4)

assert 25 <= len(tests) <= 35
os.makedirs("tests", exist_ok=True)
for i, s in enumerate(tests, 1):
    with open(os.path.join("tests", f"{i:02d}.in"), "w", newline="\n") as f:
        f.write(s)

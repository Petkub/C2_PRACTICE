# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(10519)
MAXN = 200_000
MAXX = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(T, gigs):
    n = len(gigs)
    assert 1 <= n <= MAXN and 0 <= T <= MAXX
    for c, s, e, p in gigs:
        assert c in (1, 2) and 0 <= s < e <= MAXX and 1 <= p <= MAXX
    tests.append(f"{n} {T}\n" + "".join(f"{c} {s} {e} {p}\n" for c, s, e, p in gigs))


def rnd(n, span, maxlen, maxp, minp=1):
    g = []
    for _ in range(n):
        s = ri(0, span - 1)
        e = min(span, s + ri(1, maxlen))
        g.append((ri(1, 2), s, e, ri(minp, maxp)))
    return g


def chain(n, T, maxp):
    g = []
    t = 0
    for _ in range(n):
        ln = ri(1, 3 * T + 3)
        c = ri(1, 2)
        g.append((c, t, t + ln, ri(1, maxp)))
        t += ln + random.choice([0, 0, T, T - 1 if T > 0 else 0, ri(0, T)])
    return g


add(2, [(1, 1, 3, 5), (2, 5, 8, 6), (1, 4, 9, 5), (2, 2, 4, 3), (2, 8, 10, 2)])
add(5, [(1, 0, 4, 6), (2, 6, 9, 6), (2, 4, 7, 5)])
add(0, [(2, 3, 9, 4)])
add(0, [(1, 0, 5, 3), (2, 5, 7, 3), (1, 6, 9, 3), (2, 7, 8, 1)])
add(10, [(1, 0, 1, MAXX), (1, 1, 2, MAXX), (1, 2, 3, MAXX)])
add(3, [(1, 0, 2, 4), (2, 0, 3, 5), (2, 4, 6, 4), (1, 5, 8, 6), (2, 9, 12, 5), (1, 11, 12, 2)])

add(MAXX, [(1, 0, MAXX, MAXX)])
add(1, [(2, 0, 1, 1), (1, 1, 2, 1), (2, 2, 3, 1), (1, 3, 4, 1)])
add(4, rnd(12, 40, 8, 20))
add(0, rnd(14, 30, 6, 10))
add(7, chain(15, 7, 9))
add(MAXX, rnd(15, 50, 10, 30))
add(2, rnd(15, 25, 3, 5))
add(1, [(ri(1, 2), 0, 10, ri(1, 9)) for _ in range(10)])
add(3, chain(16, 3, MAXX))

add(10, rnd(MAXN, 10**5, 50, 99))
add(0, rnd(150_000, 10**6, 100, 999))
add(MAXX, rnd(150_000, 10**5, 30, 999))
add(30, chain(140_000, 30, 99))
add(1, chain(150_000, 1, 999))
add(10**4, [(c, s, e, p if random.random() < 0.9 else ri(MAXX - 1000, MAXX))
            for c, s, e, p in rnd(140_000, 10**6, 1000, 99)])
add(50, [(1 + i % 2, 2 * i, 2 * i + 1, ri(1, 99)) for i in range(150_000)])
add(1, [(1 + i % 2, 2 * i, 2 * i + 1, ri(1, 99)) for i in range(150_000)])
add(500, [(ri(1, 2), 0, MAXX, ri(1, MAXX)) for _ in range(50_000)])
add(20, [(ri(1, 2), i, MAXX - i, ri(1, MAXX)) for i in range(50_000)])
add(7, rnd(180_000, 10**6, 20, 99))
add(3 * 10**4, [(c, s, e, p if random.random() < 0.8 else ri(1, MAXX))
                for c, s, e, p in rnd(140_000, 10**7, 10**4, 999)])
add(200, [(1, s, e, p) for _, s, e, p in rnd(75_000, 10**6, 500, 999)]
    + [(2, s, e, p) for _, s, e, p in rnd(75_000, 10**6, 500, 999)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXM, MAXQ, MAXT, ENC = 100_000, 60_000, 60_000, 10 ** 6, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(n, slots, a, b, x, y):
    ok = set(c for s, e, c in slots if x <= s and e <= y)
    for c in range(a, b + 1):
        if c not in ok:
            return c
    return -1


def add(n, slots, qs):
    m = len(slots)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= len(qs) <= MAXQ
    assert all(1 <= s <= e <= MAXT and 1 <= c <= n for s, e, c in slots)
    assert all(0 <= pa < ENC and 0 <= pb < ENC and 1 <= x <= y <= MAXT for pa, pb, x, y in qs)
    tests.append(f"{n} {m} {len(qs)}\n" + "".join(f"{s} {e} {c}\n" for s, e, c in slots)
                 + "".join(f"{pa} {pb} {x} {y}\n" for pa, pb, x, y in qs))


def crafted(n, slots, real):
    last, qs = 0, []
    for a, b, x, y in real:
        assert 1 <= a <= b <= n
        qs.append(((a - 1) ^ last, (b - 1) ^ last, x, y))
        ans = answer(n, slots, a, b, x, y)
        last = 0 if ans == -1 else ans
    add(n, slots, qs)


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def big(n, m, q, p_fail, extra, p_wide, tmax=MAXT):
    slots = []
    lo, hi = int(tmax * 0.4), int(tmax * 0.55)
    for c in range(1, n + 1):
        if len(slots) >= m:
            break
        if random.random() >= p_fail:
            s = ri(lo, hi)
            slots.append((s, min(tmax, s + ri(0, tmax // 20)), c))
        if random.random() < extra and len(slots) < m:
            s = ri(tmax // 10, tmax // 5)
            slots.append((s, ri(int(tmax * 0.95), tmax), c))
    while len(slots) < m:
        s = ri(1, tmax)
        slots.append((s, min(tmax, s + ri(0, tmax // 10)), ri(1, n)))
    shuffle(slots)
    qs = []
    for _ in range(q):
        if random.random() < p_wide:
            x, y = ri(1, tmax // 10), ri(int(tmax * 0.7), tmax)
        else:
            x, y = ri(1, tmax), ri(1, tmax)
            x, y = min(x, y), max(x, y)
        qs.append((ri(0, RANDENC - 1), ri(0, RANDENC - 1), x, y))
    add(n, slots, qs)


random.seed(301201)

crafted(4, [(2, 5, 1), (4, 6, 2), (1, 3, 3), (7, 9, 4)], [(1, 4, 1, 9), (1, 4, 2, 6), (2, 4, 1, 6), (3, 4, 2, 8)])
crafted(3, [(5, 5, 2), (1, 10, 3)], [(2, 3, 1, 10), (1, 3, 5, 5), (2, 2, 4, 6)])
crafted(1, [(1, 1000000, 1)], [(1, 1, 1, 1000000), (1, 1, 2, 1000000)])
crafted(5, [(3, 4, 1), (3, 4, 2), (3, 4, 3), (3, 4, 4), (2, 6, 5)], [(1, 5, 3, 4), (1, 5, 2, 6), (2, 3, 4, 9)])
crafted(6, [(10, 20, 2), (15, 16, 4), (1, 30, 6), (12, 14, 1)], [(1, 6, 10, 20), (1, 1, 12, 14), (2, 6, 1, 30), (3, 5, 15, 16)])

big(1, 1, 5, 0.3, 0.5, 0.5, 10)
big(3, 5, 30, 0.3, 0.5, 0.5, 10)
big(10, 20, 200, 0.2, 0.5, 0.6, 50)
big(50, 120, 500, 0.1, 0.4, 0.7, 1000)
big(300, 500, 1000, 0.05, 0.3, 0.8)
big(2000, 3000, 3000, 0.01, 0.3, 0.8)
big(10000, 12000, 10000, 0.001, 0.2, 0.9)

for n, p_fail, extra, p_wide in [(48000, 0.00002, 0.2, 0.97), (40000, 0.00005, 0.4, 0.98), (53000, 0.0, 0.1, 0.95),
                                 (30000, 0.0, 0.9, 0.97), (50000, 0.00004, 0.15, 0.99), (45000, 0.00002, 0.3, 0.97),
                                 (57000, 0.0, 0.03, 0.98), (34000, 0.00003, 0.7, 0.97), (59000, 0.0, 0.0, 0.97),
                                 (49000, 0.00002, 0.2, 0.96)]:
    assert n * (1 + extra) <= MAXM * 0.99
    big(n, MAXM, MAXQ, p_fail, extra, p_wide)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

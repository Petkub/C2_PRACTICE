# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(51605)
MAXN = 200_000
MAXH = 10**6
MAXM = 1000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(camps):
    n = len(camps)
    assert 1 <= n <= MAXN
    assert all(1 <= h <= MAXH and 1 <= m <= MAXM for h, m in camps)
    tests.append(f"{n}\n" + "".join("%d %d\n" % c for c in camps))


def rnd(n, hlo, hhi, mlo, mhi):
    return [(ri(hlo, hhi), ri(mlo, mhi)) for _ in range(n)]


def small_buffs(n):
    return [(ri(1, MAXH), random.choice((1, 2, 2, 2, 3, 3, 4, 5, 6))) for _ in range(n)]


def equal_keys(n):
    out = []
    for _ in range(n):
        if random.random() < 0.1:
            out.append((ri(1, MAXH), 1))
            continue
        m = random.choice((2, 3, 4, 5, 6))
        K = 60 * ri(1, 16000)
        out.append((K * (m - 1) // m, m))
    return out


def big_vs_small(n):
    out = []
    for _ in range(n):
        if random.random() < 0.5:
            out.append((ri(MAXH // 2, MAXH), ri(500, MAXM)))
        else:
            out.append((ri(1, MAXH // 1000), ri(2, 3)))
    return out


def mixed_ones(n, share):
    return [(ri(1, MAXH), 1) if random.random() < share else (ri(1, MAXH), ri(2, 40)) for _ in range(n)]


add([(12, 1), (10, 3), (9, 2)])
add([(12, 3), (6, 1), (9, 2)])
add([(7, 4)])
add([(25, 2), (5, 1), (19, 1), (1, 5), (15, 3)])
add([(19, 1), (27, 2), (1, 3), (15, 2)])
add([(1, 5), (15, 5), (18, 2), (12, 1), (16, 3)])

add([(3, 2), (4, 2)])
add([(10, 2), (6, 3), (14, 2), (5, 1), (9, 4), (2, 2), (20, 3), (11, 5)])
add([(8, 2), (12, 3), (6, 1), (9, 2), (16, 4), (20, 5), (3, 1), (15, 6)])
add(rnd(7, 1, 50, 1, 6))
add([(1, 1), (MAXH, 2), (MAXH, MAXM), (1, MAXM), (MAXH, 1)])

add(small_buffs(2000))
add(equal_keys(1500))
add(rnd(2000, 1, MAXH, 1, MAXM))

add(rnd(MAXN, 1, MAXH, 1, MAXM))
add(small_buffs(MAXN))
add(small_buffs(MAXN))
add(equal_keys(MAXN))
add(big_vs_small(MAXN))
add(mixed_ones(MAXN, 0.5))
add(rnd(MAXN, 1, MAXH, 2, 3))
add([(ri(MAXH - 1000, MAXH), MAXM - ri(0, 3)) for _ in range(MAXN)])
add(mixed_ones(MAXN, 0.02))
add(sorted(rnd(MAXN, 1, MAXH, 1, 10), key=lambda c: (-c[0], c[1])))
add([(ri(1, MAXH), 1) for _ in range(MAXN)])
add(rnd(MAXN, 1, 1000, 2, MAXM))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

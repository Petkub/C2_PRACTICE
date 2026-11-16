# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131501)
MAXQ = 50_000
MAXA = MAXM = 10**9
MAXN = 10**18
tests = []


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    for a, n, m in qs:
        assert 1 <= a <= MAXA and 1 <= n <= MAXN and 1 <= m <= MAXM
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {n} {m}\n" for a, n, m in qs))


def ri(lo, hi):
    return random.randint(lo, hi)


def rand_m(big):
    """a modulus of a random kind: prime-like, power of two, highly composite, tiny, or 1"""
    k = ri(0, 9)
    if k == 0:
        return 1
    if k == 1:
        return 2 ** ri(1, 29)
    if k == 2:
        return random.choice([10**9, 999_999_937, 735_134_400, 600_000_000, 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23])
    if k == 3:
        return ri(2, 30)
    return ri(1, MAXM) if big else ri(1, 10**6)


def rand_a(m):
    """a multiplier, often congruent to 0, 1 or -1 modulo m"""
    k = ri(0, 7)
    if k == 0:
        r = 1
    elif k == 1:
        r = 0
    elif k == 2:
        r = m - 1
    else:
        return ri(1, MAXA)
    a = r + m * ri(0, (MAXA - r) // m)
    return a if a >= 1 else m * ri(1, MAXA // m)


def query(nmax, big):
    m = rand_m(big)
    return (rand_a(m), ri(1, nmax), m)


# samples
add([(2, 10, 1000), (3, 4, 100), (10, 5, 7)])
add([(7, 6, 10), (1, 25, 7)])
add([(10**9, 10**18, 999_999_937), (999_999_999, 10**18 - 1, 10**9), (2, 10**18, 10**9)])
add([(5, 1, 1), (5, 1, 3), (10**9, 1, 10**9), (4, 3, 4)])
add([(6, 13, 35), (12, 100, 66), (3, 20, 2), (31, 7, 30), (9, 11, 1000)])
# hidden: small n (the brute force adds the terms one by one)
add([(a, n, m) for a in range(1, 7) for n in range(1, 9) for m in range(1, 13)])
add([query(100, False) for _ in range(2000)])
add([query(10_000, False) for _ in range(3000)])
add([query(100_000, True) for _ in range(500)])
add([(rand_a(m), 10**6 - ri(0, 10), m) for m in (2, 4, 6, 8, 9, 10, 12, 16, 1024, 10**9, 999_999_937, 1)])
add([(m + 1, ri(1, 10**6), m) for m in (2, 3, 1000, 65536, 10**9 - 1)] +
    [(ri(1, 10**3) * m, ri(1, 10**6), m) for m in (3, 7, 100, 10**6)])
add([(10**9, 4 * 10**6, 10**9), (999_999_999, 4 * 10**6, 10**9), (2, 3 * 10**6, 2**29), (3, 3 * 10**6, 2 * 3**18)])
# hidden: large (n up to 10^18)
add([query(MAXN, True) for _ in range(MAXQ)])
add([(ri(1, MAXA), ri(MAXN // 2, MAXN), ri(MAXM // 2, MAXM)) for _ in range(MAXQ)])
add([(ri(1, MAXA), MAXN - ri(0, 1000), rand_m(True)) for _ in range(MAXQ)])
add([(ri(1, MAXA), 2 ** ri(50, 59) - 1, ri(1, MAXM)) for _ in range(MAXQ)])     # many odd steps
add([(1, ri(1, MAXN), ri(1, MAXM)) for _ in range(MAXQ)])                        # a = 1
add([(m * ri(1, MAXA // m) + 1, ri(1, MAXN), m) for m in (ri(2, MAXM) for _ in range(MAXQ))])   # a = 1 mod m
add([(ri(1, MAXA), ri(1, MAXN), 2 ** ri(20, 29)) for _ in range(MAXQ)])          # even moduli
add([(MAXA, MAXN, MAXM)] * MAXQ)
add([(MAXA - ri(0, 5), MAXN - ri(0, 5), MAXM - ri(0, 5)) for _ in range(MAXQ)])
add([(m - 1, ri(1, MAXN), m) for m in (ri(2, MAXM) for _ in range(MAXQ))])       # a = -1 mod m
add([(ri(1, MAXA), ri(1, MAXN), random.choice([735_134_400, 10**9, 999_999_937, 223_092_870]))
     for _ in range(MAXQ)])
add([query(MAXN, True) if i % 2 else query(10**6, True) for i in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

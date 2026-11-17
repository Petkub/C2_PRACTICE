# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(14002)
MAXT = 100_000
MAXP = 10 ** 18
MAXQ = 10 ** 6
SUMQ = 2_000_000
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(pq):
    assert 1 <= len(pq) <= MAXT
    assert all(0 <= p <= MAXP and 1 <= q <= MAXQ for p, q in pq)
    assert sum(q for _, q in pq) <= SUMQ
    tests.append(f"{len(pq)}\n" + "".join(f"{p} {q}\n" for p, q in pq))


def isprime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def full_reptend(n):

    if not isprime(n) or n in (2, 5):
        return False
    m, fs, f = n - 1, [], 2
    while f * f <= m:
        if m % f == 0:
            fs.append(f)
            while m % f == 0:
                m //= f
        f += 1
    if m > 1:
        fs.append(m)
    return all(pow(10, (n - 1) // f, n) != 1 for f in fs)


def reptend_below(n, cnt):
    res = []
    while len(res) < cnt:
        if full_reptend(n):
            res.append(n)
        n -= 1
    return res


R1M = reptend_below(MAXQ, 4)
R100K = reptend_below(100_000, 20)
R10K = reptend_below(10_000, 200)
R250K = reptend_below(250_000, 1)[0]
R125K = reptend_below(125_000, 1)[0]


add([(1, 6), (22, 7), (1, 4)])
add([(9, 3), (1, 3)])
add([(1, 81), (5, 12), (0, 5), (13, 8)])
add([(10 ** 18, 3), (1, 28), (7, 1)])
add([(1, 17), (123, 990), (1, 1_000_000)])

add([(0, 1)])
add([(ri(0, MAXP), ri(1, 200)) for _ in range(2000)])
add([(ri(0, 1000), ri(1, 60)) for _ in range(3000)])
add([(q * ri(0, 10 ** 12), q) for q in [ri(1, 3000) for _ in range(500)]] + [(MAXP // 999_999 * 999_999, 999_999)])
add([(ri(0, MAXP), 2 ** a * 5 ** b) for a in range(20) for b in range(9) if 2 ** a * 5 ** b <= 100_000] + [(1, 524_288)])
add([(ri(1, MAXP), 2 ** a * 5 ** b * c) for a in range(4) for b in range(3) for c in (3, 7, 11, 13, 37, 41, 101)])
add([(ri(0, MAXP), q) for q in R10K[:40]] + [(1, 999_999), (MAXP, 531_441)])
add([(ri(0, MAXP), 7 ** 7), (ri(0, MAXP), 8 * R125K), (MAXP, 1)])

add([(ri(0, MAXP), R1M[0]), (ri(0, MAXP), R1M[1])])
add([(1, R1M[2]), (MAXP, R1M[3])])
add([(MAXP, R1M[0]), (1, 4 * R250K)])
add([(ri(0, MAXP), q) for q in R100K])
add([(ri(0, MAXP), q) for q in R10K])
add([(ri(0, MAXP), 7 ** 7), (ri(0, MAXP), 8 * R125K)])
add([(ri(0, MAXP), 3 ** 12), (MAXP - 1, 5 * 3 ** 11), (MAXP, 999)])
add([(ri(0, MAXP), ri(1, 20)) for _ in range(MAXT)])
add([(R1M[1] * 5, R1M[1]), (ri(0, MAXP), R1M[0]), (ri(0, MAXP), 7)])
add([(ri(1, R1M[0] - 1), R1M[0]), (ri(0, MAXP), 4 * 5 * 3 * R10K[0])])
add([(ri(0, MAXP), ri(900_000, MAXQ)), (ri(0, MAXP), ri(900_000, MAXQ))])
add([(ri(0, MAXP), q) for q in R100K[:10]] + [(ri(0, MAXP), q) for q in R10K[:100]])
add([(ri(0, MAXP), ri(15_000, 20_000)) for _ in range(100)])
add([(ri(0, 10 ** 6), random.choice([7, 17, 19, 23, 29, 13, 3, 6, 12, 28, 39])) for _ in range(MAXT)])
add([(ri(0, MAXP), ri(1, 20)) for _ in range(MAXT)])
add([(ri(0, 10 ** 9), ri(1, 30)) for _ in range(66_000)])
add([(ri(0, MAXP), random.choice([17, 19, 23, 29, 47, 49, 6, 1, 2, 50])) for _ in range(40_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

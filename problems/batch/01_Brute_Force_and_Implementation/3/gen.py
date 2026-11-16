# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(120303)
MAXQ, MAXR = 10 ** 5, 10 ** 9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(qs):
    assert 1 <= len(qs) <= MAXQ
    assert all(1 <= l <= r <= MAXR for l, r in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{l} {r}\n" for l, r in qs))


def is_prime(n):
    """Miller-Rabin, exact for n < 3 * 10^9 with these bases"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


pal = []
for length in range(1, 10):
    h = (length + 1) // 2
    for half in range(10 ** (h - 1), 10 ** h):
        t = str(half)
        pal.append(int(t + t[::-1][length % 2:]))
pal.sort()
palprime = [x for x in pal if (len(str(x)) % 2 == 1 or x == 11) and is_prime(x)]


def q_uniform():
    l, r = ri(1, MAXR), ri(1, MAXR)
    return (min(l, r), max(l, r))


def q_log():
    l, r = int(10 ** (random.random() * 9)), int(10 ** (random.random() * 9))
    l, r = max(1, min(l, MAXR)), max(1, min(r, MAXR))
    return (min(l, r), max(l, r))


def q_point():
    x = random.choice(palprime) + random.choice((0, 0, 0, -1, 1))
    if random.random() < 0.3:
        x = random.choice(pal)
    x = max(1, min(x, MAXR))
    return (x, x)


def q_near():
    """both ends on or next to palindromic primes"""
    i, j = sorted((ri(0, len(palprime) - 1), ri(0, len(palprime) - 1)))
    l = palprime[i] + random.choice((0, 1))
    r = palprime[j] - random.choice((0, 1))
    if l > r:
        l, r = r, l
    return (max(1, l), min(r, MAXR))


def q_full():
    return (ri(1, 20), MAXR - ri(0, 30))


def mix(q, kinds):
    return [random.choice(kinds)() for _ in range(q)]


# samples
add([(1, 20), (100, 160)])
add([(1, 1), (11, 11), (200, 300)])
add([(12345, 678901), (999000000, 1000000000)])
add([(2, 2), (3, 5), (12, 100), (99999, 1000000)])
add([(10301, 10301), (10302, 10500), (98689, 98689)])
# hidden: small and medium (the brute force checks these)
add([(1, 1)])
add([(MAXR, MAXR), (999999999, MAXR), (999727999, MAXR), (999727998, 999727999)])
add([(10 ** 7, 10 ** 8 - 1), (10 ** 5, 10 ** 6 - 1), (1000, 10 ** 4 - 1), (10, 99), (10 ** 8, MAXR)])
add([(1, 10 ** k) for k in range(10)] + [(10 ** k, MAXR) for k in range(10)])
add(mix(2000, (q_uniform, q_log, q_point, q_near, q_full)))
add(mix(12000, (q_uniform, q_log)))
add(mix(12000, (q_point, q_near)))
add(mix(12000, (q_full,)))
# hidden: large
add(mix(MAXQ, (q_full,)))
add([(1, MAXR)] * MAXQ)
add(mix(MAXQ, (q_uniform,)))
add(mix(MAXQ, (q_log,)))
add(mix(MAXQ, (q_point,)))
add(mix(MAXQ, (q_near,)))
add(mix(MAXQ, (q_uniform, q_log, q_point, q_near, q_full)))
add([(ri(1, 10 ** 8), ri(9 * 10 ** 8, MAXR)) for _ in range(MAXQ)])
add([(ri(10 ** 8, 2 * 10 ** 8), ri(8 * 10 ** 8, MAXR)) for _ in range(MAXQ)])
add(mix(MAXQ, (q_near, q_full)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

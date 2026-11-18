# Test generator of this problem (the judge runs it to rebuild the big tests).
import math, os, random

random.seed(310008)
MAXN = 100_000
LIMIT = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffled(p):
    p = list(p)
    for i in range(len(p) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        p[i], p[j] = p[j], p[i]
    return p


def add(ms):
    n = len(ms)
    assert 1 <= n <= MAXN
    assert all(k >= 1 for x, y, k in ms)
    assert sum(k * (abs(x) + abs(y)) for x, y, k in ms) <= LIMIT
    tests.append(f"{n}\n" + "".join(f"{x} {y} {k}\n" for x, y, k in ms))


D = 10**18
PI = 3141592653589793238


def cos_sin(num, den):
    num %= den
    q = 4 * num // den
    phi = (2 * PI * (4 * num - q * den)) // (4 * den)
    c, s = D, 0
    t, k = D, 0
    while t:
        k += 1
        t = t * phi // (D * k)
        if k % 4 == 1:
            s += t
        elif k % 4 == 2:
            c -= t
        elif k % 4 == 3:
            s -= t
        else:
            c += t
    for _ in range(q):
        c, s = -s, c
    return c, s


def round_set(n, budget, kmax=1, jitter=0):
    per = budget // n
    out = []
    for i in range(n):
        c, s = cos_sin(i * 10**6 + jitter * ri(0, 10**4), n * 10**6)
        k = ri(1, kmax)
        f = 97_000 + ri(0, 3_000)
        den = k * (abs(c) + abs(s)) * 100_000
        x = abs(per * c * f) // den
        y = abs(per * s * f) // den
        out.append((x if c >= 0 else -x, y if s >= 0 else -y, k))
    return shuffled(out)


def random_small(n, c, kmax):
    out = []
    for _ in range(n):
        x, y = ri(-c, c), ri(-c, c)
        out.append((x, y, ri(1, kmax)))
    s = sum(k * (abs(x) + abs(y)) for x, y, k in out)
    if s > LIMIT:
        out = [(x, y, max(1, k * LIMIT // s - 1)) for x, y, k in out]
    while sum(k * (abs(x) + abs(y)) for x, y, k in out) > LIMIT:
        out = [(x, y, max(1, k // 2)) for x, y, k in out]
    return out


add([(2, 0, 3), (-1, 2, 1), (0, -1, 2)])
add([(1, 1, 1), (-1, -1, 1)])
add([(0, 0, 5)])
add([(3, -1, 2), (-2, -2, 1), (1, 4, 1), (0, 0, 7), (-3, 1, 1)])
add([(4, 0, 1), (-2, 1, 2), (0, -3, 1), (1, 1, 2)])

add([(ri(-3, 3), ri(-3, 3), ri(1, 3)) for _ in range(8)])
add([(ri(-10**6, 10**6), ri(-10**6, 10**6), ri(1, 100)) for _ in range(18)])
add(round_set(20, 20_000))
add(round_set(18, LIMIT))
add([(1, 0, 1)] * 5 + [(-1, 0, 1)] * 5 + [(0, 0, 3)] * 3 + [(0, 2, 2)] * 4)
add([(LIMIT, 0, 1)])
add([(LIMIT // 4, -LIMIT // 4, 2)])

add(round_set(2_000, LIMIT, 3, 50))

add(round_set(MAXN, LIMIT))
add(round_set(MAXN, LIMIT, 4, 90))
add(round_set(MAXN // 2, LIMIT * 2 // 3, 1, 30) + round_set(MAXN // 2, LIMIT // 3, 2, 70))
add(random_small(MAXN, 3000, 3))
add(random_small(MAXN, 20, 400))
p = round_set(MAXN - 20_000, LIMIT * 9 // 10)
p += [(x, y, 1) for x, y in ((1, 2), (-1, -2), (2, -1), (0, 0)) for _ in range(5_000)]
add(shuffled(p))
p = [(ri(-30, 30), ri(-30, 30), 1) for _ in range(500)]
add(shuffled([p[ri(0, 499)] for _ in range(MAXN)]))
add(round_set(MAXN, LIMIT, 1, 100))
add(round_set(MAXN, LIMIT // 2, 7, 20))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

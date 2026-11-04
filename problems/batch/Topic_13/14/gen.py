# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13014)
MAXN, MAXQ, MAXA = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXA for v in a)
    lines = []
    for t, x, y in ops:
        if t == 1:
            assert 1 <= x <= n and 1 <= y <= MAXA
        else:
            assert t == 2 and 1 <= x <= y <= n
        lines.append(f"{t} {x} {y}")
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "\n".join(lines) + "\n")


def multiples(g, n, ones, cmax):
    """values g * c with c = 1 at a share `ones` of the positions, else 2..cmax (all <= MAXA)"""
    cmax = max(2, min(cmax, MAXA // g))
    return [g if random.random() < ones else g * ri(2, cmax) for _ in range(n)]


def ops_of(n, q, upd, value, rng):
    """upd: share of updates; value(i) -> new value of a_i; rng() -> (l, r)"""
    ops = []
    for _ in range(q):
        if random.random() < upd:
            i = ri(1, n)
            ops.append((1, i, value(i)))
        else:
            ops.append((2,) + rng())
    return ops


def any_rng(n):
    def f():
        l = ri(1, n)
        return l, ri(l, n)
    return f


def long_rng(n, slack):
    def f():
        return ri(1, slack), ri(n - slack + 1, n)
    return f


def short_rng(n, d):
    def f():
        l = ri(1, n)
        return l, min(n, l + ri(0, d))
    return f


# samples
add([2, 4, 2, 6, 3, 2], [(2, 1, 3), (2, 1, 5), (1, 5, 8), (2, 1, 6), (2, 4, 4)])
add([5, 5, 5], [(2, 1, 3), (1, 2, 10), (2, 1, 3), (1, 1, 7), (2, 1, 3), (2, 2, 2)])
add([1], [(2, 1, 1), (1, 1, MAXA), (2, 1, 1)])
add([6, 4, 6, 4, 8], [(2, 1, 5), (2, 2, 5), (2, 4, 5), (1, 3, 4), (2, 2, 5)])
add([MAXA, MAXA // 2, MAXA - 1], [(2, 1, 2), (2, 1, 3), (1, 3, 1), (2, 1, 3), (2, 2, 3)])
# hidden: small (the brute force checks these)
for n, q, g, ones, cmax, upd in ((1, 5, 3, 0.5, 3, 0.4), (4, 20, 2, 0.4, 4, 0.3), (8, 40, 6, 0.4, 6, 0.3),
                                 (20, 200, 12, 0.3, 10, 0.3), (60, 500, 1, 0.2, 12, 0.3),
                                 (200, 1000, 10**6, 0.4, 900, 0.3), (300, 1500, 7, 0.5, 3, 0.4)):
    a = multiples(g, n, ones, cmax)
    add(a, ops_of(n, q, upd, lambda i: random.choice((g, g, g * ri(2, cmax), ri(1, 30))), any_rng(n)))
n = 300                                                     # the minimum occurs but does not divide (6, 10, 15)
a = [random.choice((6, 10, 15, 30, 60)) * 1000 for _ in range(n)]
add(a, ops_of(n, 1500, 0.3, lambda i: random.choice((6, 10, 15, 30)) * 1000, any_rng(n)))
# hidden: maximum size (inputs kept near 3 MB)
N, Q = MAXN, MAXQ
a = [MAXA] * 120_000                                        # all equal: every position counts
add(a, ops_of(120_000, 150_000, 0.05, lambda i: MAXA if random.random() < 0.7 else MAXA // 2, long_rng(120_000, 30)))
a = multiples(7, 150_000, 0.3, 10**5)                       # min = gcd almost always, counts in the tens of thousands
add(a, ops_of(150_000, 150_000, 0.2, lambda i: 7 * random.choice((1, 1, 2, ri(2, 10**5))), long_rng(150_000, 100)))
a = multiples(2**20, 150_000, 0.5, 900)                     # many minima, updates that break the gcd now and then
add(a, ops_of(150_000, 120_000, 0.3, lambda i: random.choice((2**20, 2**21, 3 * 2**19, 2**19)), long_rng(150_000, 2000)))
n, m = 150_000, 6 * 10**7                                  # the minimum appears many times but the values at the
a = [m * random.choice((1, 1, ri(2, 16))) for _ in range(n)]  # end are odd multiples of 3 * 10^7: it never divides
for i in range(n - 1500, n):
    a[i] = 3 * 10**7 * random.choice((3, 5, 7, 9, 11))
add(a, ops_of(n, 150_000, 0.1, lambda i: m * ri(1, 16) if i < n - 1500 else 9 * 10**7, long_rng(n, 50)))
n = 150_000                                                 # one bad value near the end spoils the long ranges
a = multiples(1000, n, 0.6, 10**6)
a[n - n // 10] = 999
add(a, ops_of(n, 150_000, 0.2, lambda i: 1000 if i != n - n // 10 else random.choice((999, 1000, 2000)),
              long_rng(n, n // 3)))
a = [ri(1, MAXA) for _ in range(N)]                         # random values: the answer is almost always 0
add(a, ops_of(N, Q // 3, 0.2, lambda i: ri(1, MAXA), any_rng(N)))
n = 150_000                                                 # small values: many ranges whose gcd is 1 with a 1 inside
a = [ri(1, 6) for _ in range(n)]
add(a, ops_of(n, Q, 0.3, lambda i: ri(1, 6), any_rng(n)))
a = multiples(3, N, 0.4, 5)                                 # short ranges, many updates
add(a, ops_of(N, Q * 3 // 4, 0.5, lambda i: 3 * ri(1, 5), short_rng(N, 30)))
a = multiples(1, 150_000, 0.001, 10**9)                     # few ones far apart
add(a, ops_of(150_000, 120_000, 0.1, lambda i: 1 if random.random() < 0.01 else ri(2, MAXA), long_rng(150_000, 5000)))
n = 150_000                                                 # values 12, 24, 36 coming and going, a rare 6
a = [12] * n
add(a, ops_of(n, 150_000, 0.5, lambda i: random.choice((12, 12, 24, 36)) if random.random() < 0.995 else 6,
              long_rng(n, 10)))
a = multiples(999_983, 150_000, 0.1, 1000)                  # a large prime gcd, few minima
add(a, ops_of(150_000, 120_000, 0.1, lambda i: 999_983 * random.choice((1, ri(2, 1000))), long_rng(150_000, 500)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

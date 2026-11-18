# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33002)
MAXN, MAXQ, MAXV = 100_000, 100_000, 1_000_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert 2 <= k <= 2 * MAXV
    assert all(1 <= x <= MAXV for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q} {k}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    tests.append(t)


def around(n, k, spread, half=0.0):
    a = []
    for _ in range(n):
        if k % 2 == 0 and random.random() < half:
            a.append(k // 2)
        else:
            a.append(min(MAXV, max(1, k // 2 + ri(-spread, spread))))
    return a


def any_q(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_q(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_q(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def queries(n, q, *makers):
    return [random.choice(makers)() for _ in range(q)]


add(10, [3, 7, 4, 6, 7, 2], [(1, 6), (2, 5), (5, 6)])
add(9, [4, 5, 5, 4, 1], [(1, 5), (2, 3)])
add(3, [1], [(1, 1)])
add(1_000_001, [1_000_000, 1, 999_999, 2, 500_000, 3, 999_998, 1], [(1, 8), (2, 4), (5, 5), (3, 8)])
add(8, [1, 7, 1, 7, 2, 3], [(1, 6), (2, 3), (5, 6)])

add(2, [1, 1], [(1, 1), (1, 2), (2, 2)])
add(2_000_000, [MAXV, MAXV, 1, MAXV], [(1, 4), (2, 3), (1, 2)])
for n, q, k, sp, h in ((10, 55, 10, 4, 0.3), (40, 400, 21, 10, 0.0), (300, 2000, 100, 8, 0.2),
                       (2000, 2000, 1_000_000, 50, 0.1), (3000, 3000, 999_999, 300, 0.0)):
    add(k, around(n, k, sp, h), queries(n, q, lambda: any_q(n), lambda: short_q(n, 10)))

N, Q = MAXN, MAXQ
add(2 * MAXV, [MAXV] * N, queries(N, Q, lambda: long_q(N, 1000), lambda: (1, N)))
add(1_000_001, [1 if i % 2 == 0 else MAXV for i in range(N)], queries(N, Q, lambda: long_q(N, 3000)))
add(500_000, around(N, 500_000, 20, 0.3), queries(N, Q, lambda: long_q(N, 20000), lambda: any_q(N)))
add(777_777, around(N, 777_777, 1000), queries(N, Q, lambda: long_q(N, 5000), lambda: short_q(N, 5)))
add(1_000_000, around(N, 1_000_000, 300_000, 0.05), queries(N, Q, lambda: any_q(N)))
add(2_000_000, [ri(1, MAXV) for _ in range(N)], queries(N, Q, lambda: long_q(N, 100)))
add(200, around(N, 200, 1, 0.9), queries(N, Q, lambda: long_q(N, 3000), lambda: short_q(N, 2)))
add(1_000_000, sorted(around(N, 1_000_000, 50, 0.9)), queries(N, Q, lambda: long_q(N, 2000), lambda: (ri(1, N), N)))
add(31, [random.choice((7, 24)) for _ in range(N)], queries(N, Q, lambda: (1, ri(N - 10, N)), lambda: short_q(N, 1)))
add(999_999, [random.choice((1, 999_998, 1, 999_998, 400_000)) for _ in range(N)],
    queries(N, Q, lambda: long_q(N, 500), lambda: any_q(N)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

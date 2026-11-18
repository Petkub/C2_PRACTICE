# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33004)
MAXN, MAXQ, MAXA = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= MAXA for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


def vals(n, k):
    pool = [ri(1, MAXA) for _ in range(max(1, k))]
    return [random.choice(pool) for _ in range(n)]


def band(n, k):
    base = ri(1, MAXA - k)
    return [base + ri(0, k - 1) for _ in range(n)]


def odd_even(n, k):
    base = 2 * ri(1, (MAXA - 4 * k) // 2)
    return [base + 2 * ri(0, k - 1) + ri(0, 1) for _ in range(n)]


def spread(n, k):
    a = vals(n, n)
    for _ in range(k):
        v = ri(1, MAXA - 1)
        for _ in range(ri(2, 4)):
            a[ri(0, n - 1)] = v + ri(0, 1)
    return a


def any_q(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_q(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_q(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def queries(q, *makers):
    return [random.choice(makers)() for _ in range(q)]


add([4, 9, 11, 1, 9, 5], [(2, 2), (2, 5), (1, 6)])
add([5, 9, 7, 10, 8, 10, 11, 6], [(2, 2), (1, 8), (2, 7)])
add([1], [(1, 1)])
add([11, 8, 7, 4, 4, 3, 11], [(1, 7), (3, 6), (2, 2)])
add([3, 12, 9, 10, 9, 10, 6, 10], [(2, 3), (3, 8), (3, 7)])

add(band(7, 4), [(l, r) for l in range(1, 8) for r in range(l, 8)])
add(odd_even(50, 30), queries(500, lambda: any_q(50), lambda: short_q(50, 4)))
add(spread(300, 20), queries(1000, lambda: any_q(300)))
add(band(2000, 1000), queries(2000, lambda: any_q(2000), lambda: short_q(2000, 50)))
add(spread(3000, 100), queries(3000, lambda: any_q(3000), lambda: long_q(3000, 500)))
add([MAXA - ri(0, 2) for _ in range(500)], queries(500, lambda: any_q(500)))

N, Q = MAXN, MAXQ
add(spread(N, 300), queries(Q, lambda: any_q(N)))
add(spread(N, 2000), queries(Q, lambda: long_q(N, 30000)))
add(odd_even(N, N // 10), queries(Q, lambda: long_q(N, 3000), lambda: short_q(N, 300)))
add(band(N, 3), queries(Q, lambda: long_q(N, 20000), lambda: any_q(N)))
add(band(N, N), queries(Q, lambda: long_q(N, 1000)))
add([MAXA - (i % 2) for i in range(N)], queries(Q, lambda: long_q(N, 20000), lambda: short_q(N, 0)))
add(spread(N, 50), queries(Q, lambda: (ri(1, N), N), lambda: (1, ri(1, N))))
add([1 + 2 * (i % 700) for i in range(N)], queries(Q, lambda: short_q(N, 1500), lambda: long_q(N, 20000)))
add(odd_even(N, 20000), queries(Q, lambda: short_q(N, 5000), lambda: any_q(N)))
add([1 + 3 * i for i in range(N // 2)] + [3 * i + 2 for i in range(N - N // 2)], queries(Q, lambda: long_q(N, 10000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33003)
MAXN, MAXQ, MAXP = 100_000, 100_000, 1_000_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, p, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(p) == n
    assert all(1 <= x <= n for x in a)
    assert all(1 <= x <= MAXP for x in p)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, p)) + "\n"
                 + "".join(f"{l} {r}\n" for l, r in qs))


def kinds(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def prices(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


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


add([2, 1, 2, 3, 2, 1], [5, 3, 10, 1, 1, 1], [(1, 6), (2, 4), (5, 5)])
add([1, 1, 1, 1], [7, 2, 2, 2], [(1, 4), (2, 3)])
add([1], [1000000], [(1, 1)])
add([3, 3, 1, 2, 3, 2, 1, 3], [4, 9, 6, 1, 1, 1, 1, 1], [(1, 8), (3, 5), (1, 2), (4, 7), (6, 8)])
add([4, 4, 4, 4, 4], [1, 1, 1, 1000000, 1], [(1, 5), (1, 3), (3, 5)])

add(kinds(6, 2), prices(6, 1, 9), [(l, r) for l in range(1, 7) for r in range(l, 7)])
add(kinds(40, 5), prices(40, 1, MAXP), queries(400, lambda: any_q(40)))
add(kinds(300, 30), prices(300, 1, 100), queries(1000, lambda: any_q(300), lambda: short_q(300, 10)))
add(kinds(2000, 3), prices(2000, MAXP - 10, MAXP), queries(2000, lambda: any_q(2000)))
add(kinds(3000, 1500), prices(3000, 1, MAXP), queries(3000, lambda: any_q(3000)))
add(kinds(3000, 1), prices(3000, MAXP, MAXP), queries(3000, lambda: long_q(3000, 100)))

N, Q = MAXN, MAXQ
add(kinds(N, N), prices(N, 1, MAXP), queries(Q, lambda: long_q(N, 2000)))
add(kinds(N, 1), prices(N, MAXP, MAXP), queries(Q, lambda: long_q(N, 5000), lambda: (1, N)))
add(kinds(N, 10), prices(N, MAXP // 2, MAXP), queries(Q, lambda: long_q(N, 20000), lambda: any_q(N)))
add(kinds(N, 300), prices(N, 1, MAXP), queries(Q, lambda: any_q(N)))
add(kinds(N, 2), [MAXP] * N, queries(Q, lambda: long_q(N, 30000), lambda: short_q(N, 100)))
add(kinds(N, 5000), prices(N, 1, 10), queries(Q, lambda: long_q(N, 1000)))
add([1 + i // 1000 for i in range(N)], prices(N, MAXP - 1000, MAXP), queries(Q, lambda: long_q(N, 10000)))
add(kinds(N, 40), prices(N, 1, MAXP), queries(Q, lambda: (ri(1, N), N), lambda: (1, ri(1, N))))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

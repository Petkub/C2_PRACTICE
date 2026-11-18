# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33007)
MAXN, MAXQ = 100_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


def kinds(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def skewed(n, k):
    a = []
    while len(a) < n:
        j = 1
        while j < k and random.random() < 0.5:
            j += 1
        a.append(j)
    return a


def blocks(n, k, run):
    a = []
    while len(a) < n:
        a += [ri(1, k)] * ri(1, run)
    return a[:n]


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


add([3, 3, 1, 2, 2, 4, 2, 3, 3, 4], [(3, 7), (2, 10), (1, 6)])
add([1, 3, 2, 3, 3, 1], [(2, 4), (1, 5), (2, 2), (1, 3)])
add([1], [(1, 1)])
add([4, 1, 2, 3, 2, 4, 1, 4, 3, 4], [(2, 10), (3, 7), (1, 3), (2, 9)])
add([2, 2, 3, 3, 1, 1], [(1, 1), (2, 5), (1, 6)])

add(kinds(7, 3), [(l, r) for l in range(1, 8) for r in range(l, 8)])
add(kinds(50, 5), queries(500, lambda: any_q(50)))
add(blocks(300, 10, 8), queries(1000, lambda: any_q(300), lambda: short_q(300, 20)))
add(skewed(2000, 30), queries(2000, lambda: any_q(2000)))
add(kinds(3000, 2), queries(3000, lambda: any_q(3000), lambda: long_q(3000, 300)))

N, Q = MAXN, MAXQ
add(kinds(N, N), queries(Q, lambda: long_q(N, 3000)))
add(kinds(N, 2), queries(Q, lambda: any_q(N)))
add(kinds(N, 300), queries(Q, lambda: long_q(N, 20000), lambda: short_q(N, 500)))
add(skewed(N, 40), queries(Q, lambda: any_q(N)))
add(blocks(N, 50, 2000), queries(Q, lambda: long_q(N, 30000), lambda: any_q(N)))
add([1] * N, queries(Q, lambda: long_q(N, 10000)))
add([1 + i % 1000 for i in range(N)], queries(Q, lambda: long_q(N, 2000), lambda: short_q(N, 999)))
add(kinds(N, 20), queries(Q, lambda: (ri(1, N), N), lambda: (1, ri(1, N))))
add(blocks(N, N, 3), queries(Q, lambda: long_q(N, 1000)))
add([1 + (i % 2) * ri(1, 1000) for i in range(N)], queries(Q, lambda: long_q(N, 40000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

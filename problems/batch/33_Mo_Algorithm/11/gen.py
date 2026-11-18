# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33011)
MAXN, MAXQ, MAXM = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(m, a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and 1 <= m <= MAXM
    assert all(0 <= x <= m for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {m} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


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


def band(n, m, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def clusters(n, m, k):
    centres = sorted(ri(0, m) for _ in range(k))
    w = max(1, m // (50 * k))
    return [min(m, max(0, random.choice(centres) + ri(-w, w))) for _ in range(n)]


add(20, [2, 18, 7, 1, 19, 12], [(1, 6), (1, 2), (3, 5)])
add(10, [5, 5, 1, 9], [(1, 4), (2, 4), (3, 4)])
add(MAXM, [1, MAXM - 1, MAXM // 2], [(1, 2), (1, 3)])
add(12, [0, 12, 6, 3, 9, 0, 12], [(1, 2), (1, 3), (3, 5), (4, 7), (1, 7)])
add(30, [4, 27, 15, 2, 22, 9, 28, 16], [(1, 8), (2, 6), (3, 7), (1, 4), (4, 8)])

add(1, [0], [(1, 1)])
add(5, [5, 0, 5, 3, 3], [(l, r) for l in range(1, 6) for r in range(l, 6)])
add(7, [ri(0, 7) for _ in range(9)], [(l, r) for l in range(1, 10) for r in range(l, 10)])
add(100, band(30, 100, 40, 60), queries(300, lambda: any_q(30), lambda: short_q(30, 2)))
add(MAXM, [ri(0, MAXM) for _ in range(200)], queries(2000, lambda: any_q(200)))
add(1000, clusters(400, 1000, 4), queries(3000, lambda: any_q(400), lambda: short_q(400, 5)))
add(50, [ri(0, 50) for _ in range(1500)], queries(1500, lambda: any_q(1500)))
add(MAXM, band(2000, MAXM, 0, 10**6) , queries(2000, lambda: any_q(2000), lambda: long_q(2000, 100)))

N, Q = MAXN, MAXQ
add(MAXM, [ri(0, MAXM) for _ in range(N)], queries(Q, lambda: long_q(N, 3000)))
add(MAXM, [ri(0, MAXM) for _ in range(N)], queries(Q, lambda: any_q(N)))
add(MAXM, clusters(N, MAXM, 30), queries(Q, lambda: long_q(N, 20000), lambda: short_q(N, 3)))
add(MAXM, band(N, MAXM, 4 * 10**8, 6 * 10**8), queries(Q, lambda: long_q(N, 1000)))
add(MAXM, sorted(ri(0, MAXM) for _ in range(N)), queries(Q, lambda: long_q(N, 5000)))
add(MAXM, sorted((ri(0, MAXM) for _ in range(N)), reverse=True), queries(Q, lambda: long_q(N, 5000), lambda: any_q(N)))
add(1000, [ri(0, 1000) for _ in range(N)], queries(Q, lambda: long_q(N, 30000)))
add(MAXM, [MAXM if i % 2 else 0 for i in range(N)], queries(Q, lambda: long_q(N, 100), lambda: short_q(N, 0)))
add(MAXM, [ri(0, 10) if i % 2 else MAXM - ri(0, 10) for i in range(N)] , queries(Q, lambda: long_q(N, 2000)))
add(MAXM, clusters(N, MAXM, 3), queries(Q, lambda: (ri(1, 50), N), lambda: (1, ri(N - 50, N))))
add(MAXM, [i * 10000 for i in range(N)], queries(Q, lambda: long_q(N, 40000)))
add(MAXM, [ri(0, MAXM) for _ in range(N)], queries(Q, lambda: (1, N), lambda: short_q(N, 300)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

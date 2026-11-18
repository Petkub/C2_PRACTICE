# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33005)
MAXN, MAXQ, MAXV = 100_000, 80_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n and 1 <= x <= y <= MAXV for l, r, x, y in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r} {x} {y}\n" for l, r, x, y in qs))


def vals(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def band(lo, hi, wide):
    if wide:
        x = ri(lo, lo + (hi - lo) // 4)
        return x, ri(hi - (hi - lo) // 4, hi)
    x = ri(lo, hi)
    return x, ri(x, min(hi, x + ri(0, 50)))


def any_r(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_r(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_r(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def queries(q, rng, lo, hi, wide_share):
    return [rng() + band(lo, hi, random.random() < wide_share) for _ in range(q)]


add([5, 3, 8, 3, 10, 6, 7, 2], [(1, 8, 4, 9), (2, 5, 6, 9), (6, 8, 1, 5)])
add([4, 4, 1, 9, 2], [(1, 5, 5, 10), (1, 3, 1, 3), (3, 5, 3, 8)])
add([100000], [(1, 1, 1, 99999)])
add([7, 1, 7, 3, 5, 11, 9, 13, 3, 5], [(1, 10, 8, 14), (4, 8, 2, 10), (2, 6, 2, 4), (9, 10, 1, 20)])
add([2, 2, 2, 6], [(1, 4, 3, 7), (1, 3, 4, 4)])

add(vals(6, 1, 4), [(l, r, x, y) for l in range(1, 7) for r in range(l, 7) for x, y in ((1, 2), (2, 4), (3, 3))])
add(vals(50, 1, 20), queries(500, lambda: any_r(50), 1, 20, 0.5))
add(vals(300, 1, MAXV), queries(1000, lambda: any_r(300), 1, MAXV, 0.7))
add(vals(2000, 1, 300), queries(2000, lambda: any_r(2000), 1, 300, 0.5))
add(vals(3000, MAXV - 500, MAXV), queries(3000, lambda: any_r(3000), MAXV - 600, MAXV, 0.5))

N, Q = MAXN, MAXQ
add(vals(N, 1, MAXV), queries(Q, lambda: long_r(N, 3000), 1, MAXV, 1.0))
add(vals(N, 1, 1000), queries(Q, lambda: long_r(N, 20000), 1, 1000, 0.6))
add(vals(N, 1, 50), queries(Q, lambda: any_r(N), 1, 60, 0.5))
add(vals(N, 1, MAXV), queries(Q, lambda: any_r(N), 1, MAXV, 0.8))
add([ri(1, 2) * 50000 for _ in range(N)], queries(Q, lambda: long_r(N, 1000), 1, MAXV, 0.5))
add(list(range(1, N + 1)), queries(Q, lambda: long_r(N, 30000), 1, MAXV, 0.9))
add(vals(N, 1, 30000), queries(Q, lambda: (ri(1, N), N), 1, 30000, 1.0))
add([1 + (i * 7) % 5000 for i in range(N)], queries(Q, lambda: long_r(N, 5000), 1, 6000, 0.7))
add(vals(N, 1, MAXV), [(l, r, 1, MAXV) for l, r in (long_r(N, 2000) for _ in range(Q))])
add(vals(N, 1, 10), queries(Q, lambda: long_r(N, 10000), 1, 10, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

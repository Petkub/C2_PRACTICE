# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33008)
MAXN, MAXQ = 70_000, 70_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rand_vals(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def perm(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def local_shuffle(n, w):
    a = list(range(1, n + 1))
    for i in range(0, n, w):
        part = a[i:i + w]
        random.shuffle(part)
        a[i:i + w] = part
    return a


def equal_runs(n, length, gap, copies):
    vals = []
    v = 1 + ri(0, gap)
    while v + length - 1 <= n and len(vals) < n:
        vals += list(range(v, v + length)) * copies
        v += length + gap
    while len(vals) < n:
        vals.append(random.choice(vals) if vals else 1)
    vals = vals[:n]
    random.shuffle(vals)
    return vals


def repeats_near(n, k):
    a, x = [], ri(1, k)
    for _ in range(n):
        x = min(k, max(1, x + random.choice((-1, 0, 1, 1, -1, 2, -2))))
        a.append(x)
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


add([3, 8, 2, 7, 4, 8, 6, 1], [(1, 8), (2, 6), (4, 7), (5, 5)])
add([6, 1, 2, 5, 6, 4], [(1, 6), (1, 4), (3, 5)])
add([1], [(1, 1)])
add([4, 7, 4, 2, 9, 3, 7, 10, 2, 8], [(1, 10), (2, 5), (3, 8), (6, 9), (5, 10), (1, 3)])
add([2, 3, 2, 2, 5, 4, 3], [(1, 7), (1, 4), (3, 5), (4, 4)])

add(rand_vals(6, 3), [(l, r) for l in range(1, 7) for r in range(l, 7)])
add(repeats_near(12, 6), [(l, r) for l in range(1, 13) for r in range(l, 13)])
add(rand_vals(50, 20), queries(500, lambda: any_q(50), lambda: short_q(50, 5)))
add(equal_runs(80, 3, 2, 2), queries(800, lambda: any_q(80)))
add(repeats_near(300, 40), queries(2000, lambda: any_q(300), lambda: long_q(300, 30)))
add(local_shuffle(2000, 40), queries(2000, lambda: any_q(2000), lambda: short_q(2000, 100)))
add(rand_vals(3000, 2500), queries(3000, lambda: any_q(3000), lambda: long_q(3000, 300)))

N, Q = MAXN, MAXQ
add(perm(N), queries(Q, lambda: long_q(N, 3000)))
add(rand_vals(N, N), queries(Q, lambda: long_q(N, 20000), lambda: any_q(N)))
add(local_shuffle(N, 300), queries(Q, lambda: long_q(N, 5000), lambda: short_q(N, 500)))
add(equal_runs(N, 7, 3, 2), queries(Q, lambda: long_q(N, 10000)))
add(equal_runs(N, 50, 1, 1), queries(Q, lambda: long_q(N, 25000), lambda: any_q(N)))
add(repeats_near(N, 2000), queries(Q, lambda: long_q(N, 2000)))
add(repeats_near(N, N), queries(Q, lambda: any_q(N), lambda: long_q(N, 1000)))
add(rand_vals(N, 60000), queries(Q, lambda: (ri(1, N // 2), N), lambda: (1, ri(N // 2, N))))
add(list(range(1, N + 1)), queries(Q, lambda: long_q(N, 30000)))
add([N - i if i % 2 == 0 else ri(1, N) for i in range(N)], queries(Q, lambda: long_q(N, 4000)))
add(rand_vals(N, 1000), queries(Q, lambda: long_q(N, 500), lambda: short_q(N, 300)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

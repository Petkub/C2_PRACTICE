# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33006)
MAXN, MAXQ, MAXA = 50_000, 30_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= MAXA for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rand_vals(n, hi):
    return [ri(1, hi) for _ in range(n)]


def falling(n, noise):
    a = [MAXA - 3 * i for i in range(n)]
    for _ in range(noise):
        i = ri(0, n - 2)
        a[i], a[i + 1] = a[i + 1], a[i]
    return a


def rising(n, noise):
    a = [1 + 7 * i for i in range(n)]
    for _ in range(noise):
        i, j = ri(0, n - 1), ri(0, n - 1)
        a[i], a[j] = a[j], a[i]
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


add([8, 8, 6, 3, 1], [(1, 4), (1, 5), (1, 3)])
add([5, 4, 5, 1, 8, 3, 7], [(3, 5), (1, 4), (1, 3)])
add([MAXA], [(1, 1)])
add([8, 1, 4, 9, 7, 5, 2, 8], [(6, 8), (1, 3), (1, 6)])
add([2, 9, 1, 3, 7, 7, 4], [(1, 5), (1, 3), (1, 7)])

for n, q, hi in ((1, 1, 5), (6, 21, 3), (12, 78, 100), (40, 300, 10), (200, 500, MAXA), (300, 600, 4)):
    a = rand_vals(n, hi)
    qs = [(l, r) for l in range(1, n + 1) for r in range(l, n + 1)]
    random.shuffle(qs)
    add(a, qs[:q])
add(falling(500, 30), queries(800, lambda: any_q(500), lambda: long_q(500, 20)))
add(rising(500, 40), queries(800, lambda: any_q(500)))

N, Q = MAXN, MAXQ
add(rand_vals(N, MAXA), queries(Q, lambda: any_q(N)))
add(rand_vals(N, MAXA), queries(Q, lambda: long_q(N, 3000)))
add(falling(N, 100), queries(Q, lambda: long_q(N, 2000), lambda: (1, N)))
add([MAXA - i for i in range(N)], queries(Q, lambda: long_q(N, 1500), lambda: short_q(N, 50)))
add(rand_vals(N, 5), queries(Q, lambda: any_q(N), lambda: long_q(N, 100)))
add([1000 - i // 70 for i in range(N)], queries(Q, lambda: long_q(N, 1000), lambda: any_q(N)))
add(rising(N, 2000), queries(Q, lambda: any_q(N)))
add([ri(1, 2) * MAXA // 2 for _ in range(N)], queries(Q, lambda: long_q(N, 20000)))
add([(i % 1000) + 1 + 1000 * ri(0, 3) for i in range(N)], queries(Q, lambda: any_q(N), lambda: short_q(N, 2000)))
add(falling(N, N // 2), queries(Q, lambda: long_q(N, 4000), lambda: any_q(N)))
add([MAXA] * (N // 2) + [1] * (N - N // 2), queries(Q, lambda: long_q(N, 2000)))
add([MAXA - 2 * 10**6 - 14000 * i + ri(0, 2 * 10**6) for i in range(N)], queries(Q, lambda: (ri(1, 100), N), lambda: (1, ri(N - 100, N))))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

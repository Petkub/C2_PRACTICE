# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33001)
MAXN, MAXQ = 100_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    tests.append(t)


def rand_vals(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def gaps(n, kinds):
    a = []
    pool = list(range(1, n + 1))
    random.shuffle(pool)
    pi = 0
    while len(a) < n:
        kind = random.choice(kinds)
        x, y, z = pool[pi % n], pool[(pi + 1) % n], pool[(pi + 2) % n]
        pi += 3
        a += {'xx': [x, x], 'xyx': [x, y, x], 'xyz': [x, y, z], 'xxx': [x, x, x],
              'xyxyx': [x, y, x, y, x], 'xyxx': [x, y, x, x]}[kind]
    return a[:n]


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


add([2, 1, 3, 4, 1, 1], [(1, 6), (5, 5), (1, 4)])
add([3, 3, 1, 4, 4, 3, 2], [(6, 7), (3, 3), (1, 7)])
add([1], [(1, 1)])
add([1, 2, 2, 3, 3, 1, 2, 2, 2], [(4, 9), (3, 3), (1, 2)])
add([3, 2, 4, 4, 2, 2], [(1, 6), (4, 5), (3, 4)])

for n, q, k in ((3, 6, 2), (6, 21, 3), (10, 55, 4), (14, 105, 5)):
    a = rand_vals(n, k)
    add(a, [(l, r) for l in range(1, n + 1) for r in range(l, n + 1)][:q])
add(gaps(12, ['xyx', 'xyz', 'xx', 'xyxyx']), [(l, r) for l in range(1, 13) for r in range(l, 13)])
add(rand_vals(40, 6), queries(40, 400, lambda: short_q(40, 13), lambda: any_q(40)))
add(gaps(60, ['xyx', 'xyz', 'xyxx', 'xxx']), queries(60, 600, lambda: short_q(60, 13), lambda: any_q(60)))
add(rand_vals(2000, 300), queries(2000, 2000, lambda: any_q(2000), lambda: short_q(2000, 12)))
add(gaps(3000, ['xyx', 'xyz', 'xx', 'xyxyx']), queries(3000, 3000, lambda: any_q(3000)))

N, Q = MAXN, MAXQ
add(rand_vals(N, N // 20), queries(N, Q, lambda: long_q(N, 2000)))
add(rand_vals(N, N // 3), queries(N, Q, lambda: long_q(N, 30000), lambda: any_q(N)))
add(gaps(N, ['xyx', 'xyz', 'xyz', 'xx']), queries(N, Q, lambda: long_q(N, 5000)))
add(gaps(N, ['xyx', 'xyxyx', 'xyxx']), queries(N, Q, lambda: long_q(N, 20000), lambda: short_q(N, 6)))
add(rand_vals(N, 3), queries(N, Q, lambda: long_q(N, 1000), lambda: short_q(N, 4)))
add([ri(1, N) for _ in range(N)], queries(N, Q, lambda: long_q(N, 100)))
add(gaps(N, ['xyz', 'xyz', 'xyz', 'xyx', 'xxx']), queries(N, Q, lambda: any_q(N)))
add([1 + (i % 2) * (i // 2 % N) + (1 - i % 2) * (i // 4 % N) for i in range(N)],
    queries(N, Q, lambda: long_q(N, 3000), lambda: (ri(1, N), N)))
add(rand_vals(N, 500), queries(N, Q, lambda: (1, ri(N - 10, N)), lambda: short_q(N, 1)))
add(gaps(N, ['xyx', 'xx']), queries(N, Q, lambda: long_q(N, 10000), lambda: short_q(N, 0)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

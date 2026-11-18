# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33012)
MAXN, MAXQ = 70_000, 70_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in a)
    assert any(t == 2 for t, _, _ in ops)
    for t, x, y in ops:
        assert (t == 1 and 1 <= x <= n and 1 <= y <= n) or (t == 2 and 1 <= x <= y <= n)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{t} {x} {y}\n" for t, x, y in ops))


def kinds(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def steps(n, k):
    a = []
    for j in range(1, k + 1):
        a += [j] * j
    a = (a * (n // max(1, len(a)) + 1))[:n]
    random.shuffle(a)
    return a


def ops_of(n, q, share, rng, val):
    ops = [(1, ri(1, n), val()) if random.random() < share else (2,) + rng() for _ in range(q)]
    if not any(o[0] == 2 for o in ops):
        ops[-1] = (2,) + rng()
    return ops


def any_r(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_r(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_r(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


add([3, 1, 4, 4, 1, 4, 2], [(1, 3, 2), (2, 2, 6), (2, 1, 6), (2, 6, 6)])
add([1, 1, 3, 4, 3, 1, 4, 3, 3, 1], [(1, 7, 2), (1, 6, 3), (2, 4, 10), (2, 9, 10), (2, 2, 6)])
add([1], [(2, 1, 1)])
add([4, 1, 1, 2, 1, 1, 4], [(2, 3, 5), (2, 2, 7), (2, 7, 7), (1, 1, 3), (2, 6, 7), (2, 1, 5)])
add([1, 2, 2, 4, 4, 2, 1, 2], [(2, 7, 7), (2, 4, 8), (1, 5, 1), (2, 2, 8), (1, 3, 3), (2, 5, 6)])

add(kinds(6, 3), ops_of(6, 40, 0.3, lambda: any_r(6), lambda: ri(1, 3)))
add(kinds(30, 4), ops_of(30, 300, 0.4, lambda: any_r(30), lambda: ri(1, 5)))
add(steps(200, 15), ops_of(200, 500, 0.3, lambda: any_r(200), lambda: ri(1, 15)))
add(kinds(500, 60), ops_of(500, 1000, 0.5, lambda: any_r(500), lambda: ri(1, 60)))
add(steps(2000, 40), ops_of(2000, 2000, 0.2, lambda: any_r(2000), lambda: ri(1, 40)))
add(kinds(3000, 2), ops_of(3000, 3000, 0.5, lambda: long_r(3000, 300), lambda: ri(1, 2)))

N, Q = MAXN, MAXQ
add(kinds(N, 30), ops_of(N, Q, 0.1, lambda: long_r(N, 5000), lambda: ri(1, 30)))
add(kinds(N, 300), ops_of(N, Q, 0.2, lambda: long_r(N, 8000), lambda: ri(1, 300)))
add(kinds(N, N), ops_of(N, Q, 0.15, lambda: long_r(N, 5000), lambda: ri(1, N)))
add(steps(N, 370), ops_of(N, Q, 0.1, lambda: long_r(N, 3000), lambda: ri(1, 440)))
add(steps(N, 200), ops_of(N, Q, 0.25, lambda: long_r(N, 6000), lambda: ri(1, 200)))
add(kinds(N, 2), ops_of(N, Q, 0.2, lambda: long_r(N, 4000), lambda: ri(1, 2)))
add([1] * N, ops_of(N, Q, 0.1, lambda: long_r(N, 5000), lambda: ri(1, 3)))
add(kinds(N, 5000), ops_of(N, Q, 0.05, lambda: long_r(N, 2000), lambda: ri(1, 5000)))
add(steps(N, 100), ops_of(N, Q, 0.2, lambda: long_r(N, 5000), lambda: ri(1, 100)))
add(kinds(N, 1000), ops_of(N, Q, 0.1, lambda: (ri(1, 3000), N), lambda: ri(1, 1000)))
add(kinds(N, 50), ops_of(N, Q, 0.3, lambda: long_r(N, 3000), lambda: ri(1, 50)))
add(kinds(N, N), ops_of(N, Q, 0.5, lambda: any_r(N), lambda: ri(1, N)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

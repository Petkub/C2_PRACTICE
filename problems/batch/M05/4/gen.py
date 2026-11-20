# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(450004)
MAXN = 6000
MAXK = 2500
MAXA = 10 ** 6
MAXB = 10 ** 4
tests = []


def add(k, a, b):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK and len(b) == k
    assert all(-MAXA <= x <= MAXA for x in a) and all(1 <= x <= MAXB for x in b)
    tests.append(f"{n} {k}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n")


def ra(n, lo=-MAXA, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]


def rb(k, lo=1, hi=MAXB):
    return [random.randint(lo, hi) for _ in range(k)]


add(2, [5, 7, 6, 3, -6, -4, -4], [1, 4])
add(2, [0, 2, 0, -6, -5, -5], [4, 3])
add(3, [6, 6, 4, 2, 4, 6], [3, 1, 3])
add(1, [-5], [7])
add(3, [9, -5, -2, -1, -6, 8, -4, -3], [3, 2, 1])

add(1, [4, -3], [2])
add(5, ra(12, -9, 9), rb(5, 1, 9))
add(3, ra(18, -20, 30), sorted(rb(3, 1, 20)))
add(4, ra(20, -50, 20), rb(4, 1, 50))
add(20, ra(16, -5, 9), rb(20, 1, 9))
add(2, [-MAXA] * 20, [MAXB, MAXB])

add(40, ra(2000, -1000, 1000), rb(40, 1, 100))
add(30, ra(1500), sorted(rb(30)))
add(60, ra(2500, -MAXA, MAXA // 3), sorted(rb(60), reverse=True))

add(MAXK, ra(MAXN), rb(MAXK))
add(MAXK, [MAXA] * MAXN, [MAXB] * MAXK)
add(MAXK, [-MAXA] * MAXN, rb(MAXK))
add(MAXK, [random.randint(0, MAXA) if random.random() < 0.9 else -MAXA for _ in range(MAXN)],
    sorted(rb(MAXK)))
add(MAXK, ra(MAXN, -MAXA // 10, MAXA), sorted(rb(MAXK), reverse=True))
add(MAXK, ra(MAXN, -5, 5), rb(MAXK, MAXB - 100, MAXB))
add(MAXK, ra(MAXN, -MAXA // 4, MAXA), [1] * (MAXK - 1) + [MAXB])
add(MAXK, [random.choice([MAXA, MAXA // 2, -MAXA]) for _ in range(MAXN)], rb(MAXK))
add(MAXK, ra(MAXN, -MAXA, MAXA // 3), rb(MAXK))
add(MAXK, [random.randint(-3, 3) * random.randint(0, MAXA // 3) for _ in range(MAXN)], rb(MAXK))
add(MAXK, [0 if random.random() < 0.8 else random.randint(-MAXA, MAXA) for _ in range(MAXN)], rb(MAXK))
add(MAXK, [MAXA - random.randint(0, 10)] * MAXN, rb(MAXK, 1, MAXB))
add(MAXK, [random.randint(1, MAXA) if (i // 7) % 2 == 0 else -random.randint(1, MAXA) for i in range(MAXN)],
    rb(MAXK))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

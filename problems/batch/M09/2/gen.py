# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490003)
MAXN = 100000
MAXK = 10 ** 9
MAXA = 10 ** 9
MAXQ = 50000
CAP = 400000
tests = []


def stacks_at_least(a, k):
    cur = list(a)
    while True:
        nxt = sum(k if x % k == 0 else 1 for x in cur)
        if nxt == len(cur) or nxt > CAP:
            return nxt
        new = []
        for x in cur:
            if x % k == 0:
                new.extend([x // k] * k)
            else:
                new.append(x)
        cur = new


def add(k, a, qs, top=None):
    n = len(a)
    assert 1 <= n <= MAXN and 2 <= k <= MAXK and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= MAXA for x in a)
    if top is None:
        top = stacks_at_least(a, k)
    assert all(1 <= l <= r <= top for l, r in qs)
    tests.append(f"{n} {k}\n{' '.join(map(str, a))}\n{len(qs)}\n" + "".join(f"{l} {r}\n" for l, r in qs))


def rnd(n, lo=1, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]


def plain(n, k, lo=1, hi=MAXA):
    out = []
    while len(out) < n:
        x = random.randint(lo, hi)
        if x % k:
            out.append(x)
    return out


def multiples(n, k, hi=MAXA):
    return [k * random.randint(1, hi // k) for _ in range(n)]


def pick(n, pool):
    return [random.choice(pool) for _ in range(n)]


def blend(a, b):
    return [x if random.random() < 0.5 else y for x, y in zip(a, b)]


def queries(top, q, mode="random"):
    out = []
    for _ in range(q):
        if mode == "end":
            l = random.randint(1, max(1, top // 50))
            r = random.randint(max(l, top - top // 50), top)
        elif mode == "point":
            l = r = random.randint(max(1, top - top // 3), top)
        else:
            l, r = sorted((random.randint(1, top), random.randint(1, top)))
        out.append((l, r))
    return out


def case(k, a, q, mode="random"):
    top = stacks_at_least(a, k)
    add(k, a, queries(top, q, mode), top)


ROUND = [10 ** 9, 5 * 10 ** 8, 2 * 10 ** 8, 3 * 10 ** 8, 64 * 10 ** 6, 10 ** 6, 120000, 7000, 990, 1]
POW = [536870912, 805306368, 268435456, 999999999, 1, 3]
SMALL = [5, 10, 25, 50, 125, 250, 625, 3, 7, 999999995]

add(2, [12, 5, 8, 6], [(1, 4), (3, 6), (5, 15)])
add(3, [18, 7, 9], [(8, 12), (10, 19)])
add(10 ** 9, [10 ** 9], [(1, 10 ** 9), (500000000, 500000000)])
add(5, [1, 2, 3, 4, 25], [(3, 3), (1, 29)])
add(2, [1000000000, 999999999], [(1, 513), (512, 513)])

case(2, rnd(6, 1, 480), 8)
case(3, rnd(5, 1, 1600), 8)
case(7, rnd(6, 1, 2400), 8, "point")
case(1000, pick(3, [1000, 999, 2000, 999000, 1]), 6)
case(4, rnd(4, 1, 10240), 8, "end")

case(2, rnd(2000, 1, 64000), 2000)
case(3, rnd(2000, 1, 3 ** 12), 2000, "end")

N, Q = MAXN, MAXQ
case(2, plain(70000, 2) + rnd(30000), Q)
case(2, plain(80000, 2) + pick(20000, POW), Q, "end")
case(3, plain(50000, 3) + rnd(50000), Q)
case(10 ** 9, [10 ** 9] * N, Q, "end")
a = rnd(N)
for i in random.sample(range(N), 12):
    a[i] = 999999937
case(999999937, a, Q)
case(5, plain(60000, 5) + pick(40000, SMALL), Q, "point")
case(31622, blend(rnd(N - 5), multiples(N - 5, 31622, 9 * 10 ** 8)) + [999950884] * 5, Q, "end")
case(10, plain(70000, 10) + pick(30000, ROUND), Q)
case(6, plain(50000, 6) + rnd(50000), Q, "end")
case(46341, blend(rnd(N), multiples(N, 46341)), Q)
case(2, plain(50000, 2) + multiples(50000, 2), Q)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

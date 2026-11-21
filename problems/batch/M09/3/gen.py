# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490003)
MAXN = 100000
MAXK = 10 ** 9
MAXA = 10 ** 9
MAXQ = 50000
tests = []


def add(k, parts, qs):
    n = len(parts)
    assert 1 <= n <= MAXN and 2 <= k <= MAXK and 1 <= len(qs) <= MAXQ
    a, total = [], 0
    for base, e in parts:
        assert base % k != 0
        v = base * k ** e
        assert 1 <= v <= MAXA
        a.append(v)
        total += k ** e
    assert all(1 <= l <= r <= total for l, r in qs)
    tests.append(f"{n} {k}\n{' '.join(map(str, a))}\n{len(qs)}\n" + "".join(f"{l} {r}\n" for l, r in qs))
    return total


def part(k, emax=None, bmax=MAXA):
    e_top = 0
    while k ** (e_top + 1) <= MAXA:
        e_top += 1
    e = random.randint(0, e_top if emax is None else min(emax, e_top))
    hi = min(bmax, MAXA // k ** e)
    while True:
        b = random.randint(1, hi)
        if b % k:
            return (b, e)


def stacks(k, parts):
    return sum(k ** e for _, e in parts)


def queries(total, q, mode="random"):
    out = []
    for _ in range(q):
        if mode == "end":
            l = random.randint(1, max(1, total // 50))
            r = random.randint(max(l, total - total // 50), total)
        elif mode == "point":
            l = r = random.randint(max(1, total - total // 3), total)
        else:
            l, r = sorted((random.randint(1, total), random.randint(1, total)))
        out.append((l, r))
    return out


def case(k, parts, q, mode="random"):
    add(k, parts, queries(stacks(k, parts), q, mode))


add(2, [(3, 2), (5, 0), (1, 3), (3, 1)], [(1, 4), (3, 6), (5, 15)])
add(3, [(2, 2), (7, 0), (1, 2)], [(8, 12), (10, 19)])
add(10 ** 9, [(1, 1)], [(1, 10 ** 9), (500000000, 500000000)])
add(5, [(1, 0), (2, 0), (3, 0), (4, 0), (1, 2)], [(3, 3), (1, 29)])
add(2, [(1953125, 9), (999999999, 0)], [(1, 513), (512, 513)])

case(2, [part(2, 4, 30) for _ in range(6)], 8)
case(3, [part(3, 3, 20) for _ in range(5)], 8)
case(7, [part(7, 2, 50) for _ in range(6)], 8, "point")
case(1000, [part(1000, 1, 999) for _ in range(3)], 6)
case(4, [part(4, 5, 10) for _ in range(4)], 8, "end")

case(2, [part(2, 6, 1000) for _ in range(2000)], 2000)
case(3, [part(3, 4) for _ in range(2000)], 2000, "end")

case(2, [part(2) for _ in range(MAXN)], MAXQ)
case(2, [part(2, None, 1) for _ in range(MAXN)], MAXQ, "end")
case(3, [part(3) for _ in range(MAXN)], MAXQ)
case(10 ** 9, [(1, 1)] * MAXN, MAXQ, "end")
case(999999937, [part(999999937, 0) for _ in range(MAXN)], MAXQ)
case(2, [random.choice([(1, 29), (3, 28), (1, 28)]) for _ in range(MAXN)], MAXQ, "end")
case(5, [part(5) for _ in range(MAXN)], MAXQ, "point")
case(31622, [part(31622) for _ in range(MAXN)], MAXQ, "end")
case(2, [part(2, 0) if i % 2 else part(2) for i in range(MAXN)], MAXQ)
case(6, [part(6) for _ in range(MAXN)], MAXQ, "end")
case(2, [part(2, 2) for _ in range(MAXN)], MAXQ)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

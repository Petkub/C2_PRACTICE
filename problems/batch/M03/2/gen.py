# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43002)
MAXN, MAXQ, MAXX = 200_000, 70_000, 10**15
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in a)
    assert all(1 <= l <= r <= n and 1 <= x <= MAXX for l, r, x in qs)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + f"\n{q}\n" + "".join(f"{l} {r} {x}\n" for l, r, x in qs))


def scores(a):
    n = len(a)
    s = []
    for k in range(1, n + 1):
        lo, hi = min(k, a[k - 1]), max(k, a[k - 1])
        s.append(sum(1 for i in range(1, n + 1) for j in range(i, n + 1) if i <= lo and hi <= j))
    return s


def query(s, kind):
    n = len(s)
    l = ri(1, n)
    r = ri(l, n)
    tot = sum(s[l - 1:r])
    if kind == "in":
        k = ri(l, r)
        x = sum(s[l - 1:k]) - (ri(0, s[k - 1] - 1) if s[k - 1] > 0 else 0)
        return l, r, min(max(1, x), MAXX)
    if kind == "edge":
        return l, r, min(max(1, tot + ri(0, 1)), MAXX)
    if kind == "over":
        rest = sum(s[l - 1:])
        if r < n and rest > tot:
            return l, r, min(MAXX, tot + ri(1, rest - tot))
        return l, r, min(MAXX, tot + 1)
    return l, r, ri(1, MAXX)


def mix(s, q, kinds):
    return [query(s, random.choice(kinds)) for _ in range(q)]


def big_query(n, cal, kind):
    total, head, tail, top = cal
    if kind == "long":
        return ri(1, 20), n, min(MAXX, total - head - ri(0, n))
    if kind == "all":
        return ri(1, 20), n, min(MAXX, total + ri(1, n))
    if kind == "in":
        return ri(1, n // 2), n, min(MAXX, ri(1, tail))
    if kind == "over":
        l = ri(1, n // 2 - 30)
        return l, l + ri(0, 20), min(MAXX, ri(21 * top + 1, tail))
    l = ri(1, n)
    return l, ri(l, n), ri(1, MAXX)


def big_mix(n, cal, q, kinds):
    return [big_query(n, cal, random.choice(kinds)) for _ in range(q)]


add([3, 5, 1, 2, 4], [(1, 5, 7), (2, 4, 6), (3, 5, 12), (4, 4, 4)])
add([2, 2, 2], [(1, 3, 8), (3, 3, 3), (1, 1, 1)])
add([1, 2, 3, 4, 5, 6], [(1, 6, 56), (1, 6, 57), (3, 4, 1)])
add([6, 5, 4, 3, 2, 1], [(2, 5, 13), (5, 6, 6), (1, 3, 14)])
add([5, 8, 2, 2, 7, 1, 6, 3], [(1, 8, 10**15), (2, 7, 40), (6, 8, 20)])


add([1], [(1, 1, 1), (1, 1, 2)])
for n, q in [(2, 6), (5, 20), (10, 40), (30, 60), (80, 200), (150, 300)]:
    a = [ri(1, n) for _ in range(n)]
    add(a, mix(scores(a), q, ["in", "edge", "over", "rand"]))
a = list(range(1, 151))
add(a, mix(scores(a), 300, ["in", "edge", "over"]))


N, Q = MAXN, MAXQ
C = 3 * N // 5
WALK = ["long"] * 5 + ["all"] * 2
shapes = []
a = [k if k <= C else N for k in range(1, N + 1)]
shapes.append((a, WALK + ["in", "over"]))
a = [min(N, max(1, k + ri(-30, 30))) if k <= C else 1 for k in range(1, N + 1)]
shapes.append((a, WALK + ["in"]))
a = list(range(1, N + 1))
random.shuffle(a)
shapes.append((a, WALK + ["over", "rand"]))
a = [N + 1 - k for k in range(1, N + 1)]
shapes.append((a, WALK + ["over"]))
a = [ri(1, N) for _ in range(N)]
shapes.append((a, WALK + ["in", "over", "rand"]))
a = [1 if ri(0, 1) else N for _ in range(N)]
shapes.append((a, WALK + ["over"]))
a = [1] * N
shapes.append((a, WALK + ["in"]))
a = [N if k <= 3 * N // 10 else k for k in range(1, N + 1)]
shapes.append((a, ["long"] * 8 + ["over"]))
a = [N] * N
shapes.append((a, ["long"]))
CAL = [
    (864024800080000, 41997340, 197348133380000, 10000100000),
    (863832382061729, 25797112, 197308055638232, 10000091444),
    (667845720940243, 21713235, 334309265848314, 9998145039),
    (666676666700000, 2870, 333338333350000, 10000000000),
    (666562217606244, 23325406, 333153102181098, 9998377888),
    (20015743269, 2000016, 10022858065, 200000),
    (20000100000, 3999810, 5000050000, 200000),
    (1045349133410000, 210, 666676666700000, 10000100000),
    (20000100000, 210, 15000050000, 200000),
]
assert len(CAL) == len(shapes)
for (a, kinds), cal in zip(shapes, CAL):
    add(a, big_mix(N, cal, Q, kinds))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

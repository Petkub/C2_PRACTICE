# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 70_000, 100_000, 10 ** 6, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(ab, l, r, k):
    seg = ab[l - 1:r]
    d = sorted((a + b for a, b in seg), reverse=True)
    return sum(a for a, _ in seg) - sum(d[:k])


def add(ab, qs):
    n = len(ab)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(1 <= a <= MAXV and 1 <= b <= MAXV for a, b in ab)
    assert all(0 <= v < ENC for t in qs for v in t)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{a} {b}\n" for a, b in ab) + "".join(f"{x} {y} {z}\n" for x, y, z in qs))


def crafted(ab, real):
    last, qs = 0, []
    for l, r, k in real:
        assert 1 <= l <= r <= len(ab) and 0 <= k <= r - l + 1
        qs.append(((l - 1) ^ last, (r - 1) ^ last, k ^ last))
        last = abs(answer(ab, l, r, k))
    add(ab, qs)


def rand_queries(q):
    return [(ri(0, RANDENC - 1), ri(0, RANDENC - 1), ri(0, RANDENC - 1)) for _ in range(q)]


def arr(n, kind):
    if kind == "rand":
        return [(ri(1, MAXV), ri(1, MAXV)) for _ in range(n)]
    if kind == "crossed":
        out = []
        for _ in range(n):
            a = ri(1, MAXV)
            out.append((a, max(1, MAXV - a - ri(0, 1000)) if random.random() < 0.5 else ri(1, MAXV)))
        return out
    if kind == "bigb":
        return [(ri(1, 1000), ri(1, MAXV)) for _ in range(n)]
    if kind == "equal":
        return [(MAXV, MAXV)] * n
    if kind == "few":
        return [(ri(1, 3) * 300_000, ri(1, 3) * 300_000) for _ in range(n)]
    if kind == "inc":
        x = sorted(ri(1, MAXV) for _ in range(n))
        return [(v, ri(1, MAXV)) for v in x]
    raise ValueError(kind)


random.seed(300601)

crafted([(5, 2), (3, 1), (8, 4), (1, 1), (6, 3)], [(1, 5, 2), (2, 4, 0), (1, 3, 3), (3, 5, 1)])
crafted([(10, 10), (2, 5), (7, 9)], [(1, 3, 1), (2, 3, 2), (1, 1, 0)])
crafted([(1000000, 1000000)], [(1, 1, 1), (1, 1, 0)])
crafted([(4, 4), (4, 4), (4, 4), (9, 1)], [(1, 4, 2), (1, 3, 3), (2, 4, 1)])
crafted([(2, 7), (3, 8), (1, 1), (6, 9), (5, 9), (4, 9)], [(1, 6, 3), (2, 5, 2), (4, 6, 1), (1, 2, 2), (3, 3, 1)])

add([(3, 5)], rand_queries(5))
add(arr(3, "rand"), rand_queries(30))
add(arr(10, "few"), rand_queries(200))
add(arr(50, "crossed"), rand_queries(500))
add(arr(300, "bigb"), rand_queries(1000))
add(arr(2000, "rand"), rand_queries(3000))
add(arr(5000, "inc"), rand_queries(5000))
add(arr(20000, "crossed"), rand_queries(20000))

for kind in ["rand", "crossed", "bigb", "equal", "few", "inc", "rand", "crossed", "bigb", "rand"]:
    add(arr(MAXN, kind), rand_queries(MAXQ))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

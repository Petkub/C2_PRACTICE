# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 150_000, 150_000, 10 ** 9, 2 ** 30
RANDENC = 2 ** 18


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def hindex(a, l, r):
    b = sorted(a[l - 1:r], reverse=True)
    h = 0
    while h < len(b) and b[h] >= h + 1:
        h += 1
    return h


def add(a, qs):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    assert all(0 <= v < ENC for t in qs for v in t)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{x} {y}\n" for x, y in qs))


def crafted(a, real):
    last, qs = 0, []
    for l, r in real:
        assert 1 <= l <= r <= len(a)
        qs.append(((l - 1) ^ last, (r - 1) ^ last))
        last = hindex(a, l, r)
    add(a, qs)


def rand_queries(q, long_share=0.0):
    out = []
    for _ in range(q):
        x = ri(0, RANDENC - 1)
        out.append((x, x ^ 131072 if random.random() < long_share else ri(0, RANDENC - 1)))
    return out


def arr(n, kind):
    if kind == "mid":
        return [ri(0, 30000) for _ in range(n)]
    if kind == "small":
        return [ri(0, 100) for _ in range(n)]
    if kind == "big":
        return [ri(n, 999_999) for _ in range(n)]
    if kind == "heavy":
        return [int(1.0 / (random.random() + 1e-9)) % (MAXV + 1) for _ in range(n)]
    if kind == "rand":
        return [ri(0, MAXV) if random.random() < 0.03 else ri(0, n) for _ in range(n)]
    if kind == "equal":
        return [40000] * n
    if kind == "zero":
        return [0 if random.random() < 0.9 else ri(0, 3) for _ in range(n)]
    raise ValueError(kind)


random.seed(300901)

crafted([3, 0, 6, 1, 5, 3], [(1, 6), (2, 4), (3, 6), (2, 2)])
crafted([10, 8, 5, 4, 3], [(1, 5), (3, 5), (2, 5)])
crafted([0, 0], [(1, 2), (2, 2)])
crafted([1000000000, 2, 2, 7], [(1, 4), (2, 3), (3, 4)])
crafted([4, 4, 4, 4, 1, 9, 3], [(1, 7), (5, 6), (2, 6), (4, 5)])

add([5], rand_queries(5))
add([1, 1, 1], rand_queries(20))
add([5, 5, 5], rand_queries(20))
add(arr(10, "small"), rand_queries(200))
add([ri(0, 60) for _ in range(60)], rand_queries(500))
add([ri(0, 300) for _ in range(300)], rand_queries(1000))
add(arr(2000, "heavy"), rand_queries(3000))
add([ri(0, 5000) for _ in range(5000)], rand_queries(5000))
add(arr(20000, "rand"), rand_queries(20000, 0.5))

for kind in ["mid", "small", "big", "heavy", "rand", "equal", "mid", "zero", "rand", "mid"]:
    add(arr(MAXN, kind), rand_queries(MAXQ, 0.8))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

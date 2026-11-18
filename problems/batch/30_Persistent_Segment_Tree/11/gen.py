# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 100_000, 10 ** 9, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(a, l, r):
    s = 0
    for c in sorted(a[l - 1:r]):
        if c > s + 1:
            break
        s += c
    return s + 1


def add(a, qs):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= MAXV for x in a)
    assert all(0 <= v < ENC for t in qs for v in t)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{x} {y}\n" for x, y in qs))


def crafted(a, real):
    last, qs = 0, []
    for l, r in real:
        assert 1 <= l <= r <= len(a)
        qs.append(((l - 1) ^ last, (r - 1) ^ last))
        last = answer(a, l, r)
    add(a, qs)


def rand_queries(q, long_share=0.0):
    out = []
    for _ in range(q):
        x = ri(0, RANDENC - 1)
        out.append((x, x ^ 65536 if random.random() < long_share else ri(0, RANDENC - 1)))
    return out


def arr(n, kind):
    if kind == "geo":
        return [min(MAXV, int(2 ** (random.random() * 30))) for _ in range(n)]
    if kind == "fib":
        f = [1, 2]
        while f[-1] + f[-2] <= MAXV:
            f.append(f[-1] + f[-2])
        return [f[int(random.random() * len(f))] for _ in range(n)]
    if kind == "pow2":
        return [2 ** ri(0, 29) for _ in range(n)]
    if kind == "ones":
        return [1 if random.random() < 0.5 else ri(MAXV // 2, MAXV) for _ in range(n)]
    if kind == "max":
        return [MAXV] * n
    if kind == "gap":
        return [ri(1, 50) if random.random() < 0.95 else ri(10 ** 6, MAXV) for _ in range(n)]
    if kind == "rand":
        return [ri(1, MAXV) for _ in range(n)]
    raise ValueError(kind)


random.seed(301101)

crafted([1, 2, 5, 1, 9, 3], [(1, 3), (1, 6), (3, 5), (2, 6)])
crafted([2, 1, 1, 7], [(1, 4), (2, 3), (4, 4)])
crafted([1000000000, 1], [(1, 2), (1, 1)])
crafted([1, 1, 1, 1, 1], [(1, 5), (2, 3), (5, 5)])
crafted([3, 1, 4, 1, 5, 9, 2, 6], [(1, 8), (1, 4), (5, 8), (2, 4), (3, 7)])

add([1], rand_queries(5))
add([2, 1, 3], rand_queries(20))
add(arr(10, "fib"), rand_queries(200))
add([ri(1, 5) for _ in range(60)], rand_queries(500))
add(arr(300, "geo"), rand_queries(1000))
add(arr(2000, "gap"), rand_queries(3000))
add(arr(5000, "pow2"), rand_queries(5000))
add(arr(20000, "fib"), rand_queries(20000, 0.5))

for kind in ["geo", "fib", "pow2", "ones", "gap", "geo", "fib", "max", "rand", "pow2"]:
    add(arr(MAXN, kind), rand_queries(MAXQ, 0.8))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

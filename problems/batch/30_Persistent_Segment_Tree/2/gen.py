# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 100_000, 10 ** 9, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(a, l, r, k):
    b = sorted(a[l - 1:r])
    return b[k - 1], b.count(b[k - 1])


def add(a, qs):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= MAXV for x in a)
    assert all(0 <= v < ENC for t in qs for v in t)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{x} {y} {z}\n" for x, y, z in qs))


def crafted(a, real):
    last, qs = 0, []
    for l, r, k in real:
        assert 1 <= l <= r <= len(a) and 1 <= k <= r - l + 1
        qs.append(((l - 1) ^ last, (r - 1) ^ last, (k - 1) ^ last))
        last = answer(a, l, r, k)[0]
    add(a, qs)


def rand_queries(q):
    return [(ri(0, RANDENC - 1), ri(0, RANDENC - 1), ri(0, RANDENC - 1)) for _ in range(q)]


def arr(n, kind, vmax=MAXV):
    if kind == "rand":
        return [ri(1, vmax) for _ in range(n)]
    if kind == "few":
        return [ri(1, 5) * 200_000_000 for _ in range(n)]
    if kind == "equal":
        return [MAXV] * n
    if kind == "inc":
        return sorted(ri(1, vmax) for _ in range(n))
    if kind == "dec":
        return sorted((ri(1, vmax) for _ in range(n)), reverse=True)
    if kind == "perm":
        a = list(range(1, n + 1))
        random.shuffle(a)
        return a
    if kind == "zigzag":
        return [i if i % 2 else MAXV - i for i in range(1, n + 1)]
    raise ValueError(kind)


random.seed(300101)

crafted([5, 2, 8, 2, 7, 3], [(1, 4, 2), (3, 6, 3), (1, 6, 1), (5, 6, 1)])
crafted([40, 10, 30, 10, 20], [(1, 5, 4), (3, 5, 1), (1, 3, 2)])
crafted([9, 1, 1, 1], [(1, 4, 3), (1, 4, 1)])
crafted([1000000000, 999999999, 1000000000], [(1, 3, 1), (1, 2, 1)])
crafted([9, 6, 4, 9, 4, 6, 1, 6], [(1, 8, 5), (4, 8, 4), (4, 7, 2), (2, 6, 2), (4, 8, 1)])

add([7], rand_queries(5))
add(arr(2, "rand", 3), rand_queries(20))
add(arr(10, "rand", 10), rand_queries(200))
add(arr(50, "few"), rand_queries(500))
add(arr(300, "perm"), rand_queries(1000))
add(arr(2000, "rand", 100), rand_queries(3000))
add(arr(5000, "zigzag"), rand_queries(5000))
add(arr(20000, "rand"), rand_queries(20000))

for kind in ["rand", "perm", "few", "equal", "inc", "dec", "zigzag", "rand", "perm"]:
    add(arr(MAXN, kind), rand_queries(MAXQ))
add(arr(MAXN, "rand", 1000), rand_queries(MAXQ))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

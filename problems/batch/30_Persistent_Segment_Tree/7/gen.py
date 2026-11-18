# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 100_000, 10 ** 9, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def mex(a, l, r):
    s = set(a[l - 1:r])
    m = 0
    while m in s:
        m += 1
    return m


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
        last = mex(a, l, r)
    add(a, qs)


def rand_queries(q, long_share=0.0):
    out = []
    for _ in range(q):
        x = ri(0, RANDENC - 1)
        out.append((x, x ^ 65536 if random.random() < long_share else ri(0, RANDENC - 1)))
    return out


def arr(n, kind):
    if kind == "perm":
        a = list(range(n)); shuffle(a); return a
    if kind == "permbig":
        a = list(range(n)); shuffle(a)
        return [x if random.random() < 0.999 else ri(n, MAXV) for x in a]
    if kind == "small":
        return [ri(0, 30) for _ in range(n)]
    if kind == "sqrt":
        m = int(n ** 0.5) * 4
        return [ri(0, m) for _ in range(n)]
    if kind == "rand":
        return [ri(0, MAXV) for _ in range(n)]
    if kind == "twice":
        a = list(range(n // 2)); shuffle(a); b = list(a); shuffle(b)
        return (a + b + [0])[:n]
    if kind == "inc":
        return [i if random.random() < 0.9999 else ri(n, MAXV) for i in range(n)]
    if kind == "permsmall":
        a = list(range(n)); shuffle(a)
        return [x if random.random() < 0.8 else ri(0, 2000) for x in a]
    if kind == "mix":
        return [ri(0, n - 1) if random.random() < 0.7 else ri(0, MAXV) for _ in range(n)]
    raise ValueError(kind)


random.seed(300701)

crafted([2, 0, 7, 1, 4, 3], [(1, 4), (2, 3), (1, 6), (3, 6)])
crafted([1, 0, 1000000000, 2], [(1, 2), (2, 4), (3, 3)])
crafted([0], [(1, 1), (1, 1)])
crafted([5, 1, 2, 0, 3, 4, 9], [(2, 5), (1, 6), (4, 4), (5, 7), (2, 6)])
crafted([3, 2, 1, 0, 2], [(1, 4), (2, 5), (4, 4)])

add([7], rand_queries(4))
add(arr(3, "small"), rand_queries(30))
add(arr(10, "perm"), rand_queries(200))
add(arr(60, "twice"), rand_queries(500))
add(arr(300, "sqrt"), rand_queries(1000))
add(arr(2000, "mix"), rand_queries(3000))
add(arr(5000, "permbig"), rand_queries(5000))
add(arr(20000, "small"), rand_queries(20000))

add(arr(50000, "inc"), rand_queries(50000, 0.5))
add(arr(50000, "sqrt"), rand_queries(50000, 0.5))
for kind in ["perm", "permbig", "twice", "permsmall", "mix", "permsmall", "perm", "rand", "twice", "permbig"]:
    add(arr(MAXN, kind), rand_queries(MAXQ, 0.9))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

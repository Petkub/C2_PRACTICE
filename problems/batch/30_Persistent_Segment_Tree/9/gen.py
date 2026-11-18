# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 100_000, 10 ** 9, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def answer(a, t, l, y):
    if t == 1:
        return len(set(a[l - 1:y]))
    s = set()
    for r in range(l, len(a) + 1):
        s.add(a[r - 1])
        if len(s) == y:
            return r
    return -1


def add(a, qs):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= MAXV for x in a)
    assert all(t in (1, 2) and 0 <= x < ENC and 0 <= y < ENC for t, x, y in qs)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{t} {x} {y}\n" for t, x, y in qs))


def crafted(a, real):
    last, qs = 0, []
    for t, l, y in real:
        assert 1 <= l <= len(a) and 1 <= y <= len(a) and (t == 2 or l <= y)
        qs.append((t, (l - 1) ^ last, (y - 1) ^ last))
        ans = answer(a, t, l, y)
        last = 0 if ans == -1 else ans
    add(a, qs)


def rand_queries(q, p1):
    return [(1 if random.random() < p1 else 2, ri(0, RANDENC - 1), ri(0, RANDENC - 1)) for _ in range(q)]


def arr(n, kinds, mode="rand"):
    ks = [ri(1, MAXV) for _ in range(kinds)]
    if mode == "rand":
        return [ks[int(random.random() * kinds)] for _ in range(n)]
    if mode == "blocks":
        a = []
        while len(a) < n:
            a += [ks[int(random.random() * kinds)]] * ri(1, 50)
        return a[:n]
    if mode == "cycle":
        return [ks[i % kinds] for i in range(n)]
    if mode == "late":
        return [ks[int(random.random() * min(kinds, 10))] if i < n // 2 else ks[int(random.random() * kinds)]
                for i in range(n)]
    raise ValueError(mode)


random.seed(300501)

crafted([3, 1, 3, 2, 1, 5, 2], [(1, 1, 5), (2, 2, 3), (1, 3, 7), (2, 1, 4), (2, 5, 4)])
crafted([7, 7, 8, 7, 9], [(2, 1, 2), (1, 2, 4), (2, 4, 2), (2, 2, 4)])
crafted([1000000000], [(1, 1, 1), (2, 1, 1)])
crafted([4, 4, 4, 4], [(2, 1, 1), (1, 1, 4), (2, 3, 2)])
crafted([5, 6, 5, 6, 7, 5, 8, 6], [(1, 2, 6), (2, 3, 4), (2, 1, 3), (1, 4, 8), (2, 6, 3), (2, 7, 3)])

add([1], rand_queries(5, 0.5))
add(arr(3, 2), rand_queries(30, 0.5))
add(arr(10, 4), rand_queries(200, 0.4))
add(arr(50, 50), rand_queries(500, 0.5))
add(arr(300, 30, "blocks"), rand_queries(1000, 0.5))
add(arr(2000, 1500, "cycle"), rand_queries(3000, 0.4))
add(arr(5000, 2000, "late"), rand_queries(5000, 0.5))
add(arr(20000, 20000), rand_queries(20000, 0.5))

for kinds, mode, p1 in [(100000, "rand", 0.5), (100000, "rand", 0.1), (60000, "cycle", 0.3), (2, "rand", 0.5),
                        (50000, "rand", 0.0), (1000, "blocks", 0.5), (100000, "late", 0.3), (30000, "rand", 1.0),
                        (90000, "cycle", 0.2), (100000, "blocks", 0.4)]:
    add(arr(MAXN, kinds, mode), rand_queries(MAXQ, p1))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110009)
MAXN, MAXQ, MAXV = 300_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n for (l, r) in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for (l, r) in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def queries(n, q, long_frac=0.9):
    res = []
    for _ in range(q):
        if random.random() < long_frac:
            l = ri(1, max(1, n // 20))
            res.append((l, ri(max(l, n - n // 20), n)))
        else:
            l = ri(1, n)
            res.append((l, ri(l, n)))
    return res


# samples
add([1, 2, 1, 3, 2, 2], [(1, 3), (2, 5), (6, 6), (1, 6)])
add([5, 5, 5, 5], [(1, 4), (2, 3)])
add([42], [(1, 1)])
add([9, 30, 9, 70000, 30], [(1, 5), (2, 3), (3, 4), (1, 2)])
add([4, 1, 4, 4, 2, 1, 3, 2], [(1, 8), (3, 4), (2, 6), (5, 8), (4, 7)])
# hidden: small
add([ri(1, 3) for _ in range(10)], [(l, r) for l in range(1, 11) for r in range(l, 11)])
add([ri(1, 20) for _ in range(100)], queries(100, 300, 0.3))
add(list(range(1, 501)), queries(500, 500, 0.3))                       # all different
add([MAXV] * 1000, queries(1000, 1000, 0.3))                            # all equal
add([ri(1, MAXV) if random.random() < 0.5 else ri(1, 50) for _ in range(5000)], queries(5000, 5000, 0.4))
add([ri(1, 2000) for _ in range(20000)], queries(20000, 10000, 0.3))
add([(i % 37) + 1 for i in range(10000)], queries(10000, 10000, 0.3))  # periodic
# hidden: maximum size
N = MAXN
add([ri(1, 9999) for _ in range(N)], queries(N, 100_000))
add([ri(1, 10) for _ in range(N)], queries(N, 160_000, 0.8))
add([ri(1, 999) for _ in range(N)], queries(N, 100_000))
p = list(range(1, N + 1))
random.shuffle(p)
add(p, queries(N, 50_000))                                              # all different
add([1] * N, queries(N, 120_000))                                       # all equal
add([(i % 5000) + 1 for i in range(N)], queries(N, 100_000))           # periodic
a = [ri(1, 9999) for _ in range(N // 2)]
add(a + a[::-1], queries(N, 100_000))                                   # mirrored halves
pool = [ri(1, MAXV) for _ in range(1000)]
add([random.choice(pool) for _ in range(200_000)], queries(200_000, 60_000))   # big values
add([ri(MAXV - 10**5, MAXV) for _ in range(200_000)], queries(200_000, 60_000))
a = []
while len(a) < N:                                                       # long runs of one value
    v, k = ri(1, 9999), ri(1, 100)
    a.extend([v] * k)
add(a[:N], queries(N, 100_000))
add([ri(1, 9999) for _ in range(N)], [(1, N)] * 20_000 + queries(N, 50_000, 0.0))
# the most queries on (almost) the whole street: short numbers keep the file under 3 MB
add([ri(1, 99) for _ in range(N)], [(ri(1, 99), ri(N - 99, N)) for _ in range(MAXQ)])
add([(i * 7919) % 300 + 1 for i in range(N)], [(ri(1, 99), ri(N - 99, N)) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

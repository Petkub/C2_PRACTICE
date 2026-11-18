# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


random.seed(270707)
MAXN = MAXM = MAXQ = 100_000


def add(n, c, ops, qs):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXM and 1 <= len(qs) <= MAXQ and len(c) == n + 1
    assert all(1 <= x <= n for x in c[1:])
    for a, b in ops:
        assert 1 <= a <= n and 1 <= b <= n
    for x, col in qs:
        assert 1 <= x <= n and 1 <= col <= n
    tests.append(f"{n} {len(ops)} {len(qs)}\n" + " ".join(map(str, c[1:])) + "\n"
                 + "".join(f"{a} {b}\n" for a, b in ops) + "".join(f"{x} {col}\n" for x, col in qs))


def make(n, m, q, k, kind, absent=0.3, early=0.0):
    k = min(k, n - 1)
    c = [0] + [ri(1, k) for _ in range(n)]
    perm = list(range(1, n + 1))
    shuffle(perm)
    ops = []
    if kind == "rand":
        ops = [(ri(1, n), ri(1, n)) for _ in range(m)]
    elif kind == "snow":
        for i in range(1, n):
            a, b = perm[i], perm[ri(0, i - 1)]
            ops.append((a, b) if random.random() < 0.5 else (b, a))
    else:
        step = 1
        while step < n and len(ops) < m:
            for s in range(0, n - step, 2 * step):
                ops.append((perm[s + ri(0, step - 1)], perm[s + step]))
            step *= 2
    while len(ops) < m:
        ops.append((ri(1, n), ri(1, n)))
    ops = ops[:m]
    qs = []
    for _ in range(q):
        x = perm[ri(0, max(0, int(early * n) - 1))] if random.random() < early else ri(1, n)
        r = random.random()
        if r < absent:
            col = ri(k + 1, n)
        elif r < absent + 0.05:
            col = c[x]
        else:
            col = ri(1, k)
        qs.append((x, col))
    add(n, c, ops, qs)


add(6, [0, 1, 2, 3, 1, 2, 4], [(1, 2), (3, 4), (2, 3), (6, 1)], [(1, 3), (2, 4), (2, 2), (5, 1)])
add(4, [0, 3, 2, 4, 4], [(4, 4), (1, 3), (4, 2), (4, 3)], [(3, 1), (4, 3), (1, 4), (3, 4)])
add(2, [0, 2, 2], [(1, 2)], [(1, 2), (2, 1)])
add(4, [0, 4, 4, 3, 1], [(2, 3), (1, 3), (1, 1)], [(2, 3), (1, 2), (1, 3)])
add(5, [0, 1, 5, 2, 2, 2], [(2, 3), (4, 5), (1, 3)], [(2, 1), (2, 2), (1, 3)])

make(8, 10, 12, 3, "rand")
make(20, 25, 30, 5, "snow")
make(50, 60, 80, 8, "pairs")
make(100, 150, 200, 20, "rand", 0.1)
make(300, 400, 400, 10, "snow", 0.5, 0.3)
make(1000, 1500, 2000, 100, "pairs")
make(3000, 3000, 3000, 30, "rand")
make(5000, 6000, 6000, 200, "snow", 0.4, 0.5)
make(30_000, 30_000, 30_000, 10_000, "pairs", 0.5, 0.0)

make(MAXN, MAXM, MAXQ, 1000, "snow", 0.9, 0.9)
make(MAXN, MAXM, MAXQ, 100, "snow", 0.6, 0.5)
make(MAXN, MAXM, MAXQ, 20_000, "snow", 0.3, 0.7)
make(MAXN, MAXM, MAXQ, 50_000, "snow", 0.5, 0.6)
make(MAXN, MAXM, MAXQ, 5, "snow", 0.95, 1.0)
make(MAXN, MAXM, MAXQ, 3000, "snow", 0.8, 0.4)
make(MAXN, MAXM, MAXQ, 90_000, "snow", 0.1, 0.8)
make(MAXN, MAXM, MAXQ, 10, "snow", 0.5, 0.3)
make(MAXN, MAXM, MAXQ, 500, "rand", 0.7, 0.0)
make(MAXN, MAXM, MAXQ, 70_000, "snow", 0.5, 0.9)
make(MAXN, MAXM, MAXQ, 2, "snow", 0.99, 0.99)

write_all()

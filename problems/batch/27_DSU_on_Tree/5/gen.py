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


random.seed(270909)
MAXN = MAXM = 200_000


def add(n, ops):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXM
    for a, b in ops:
        assert 1 <= a <= n and 1 <= b <= n
    tests.append(f"{n} {len(ops)}\n" + "".join(f"{a} {b}\n" for a, b in ops))


def make(n, m, kind, k=2):
    ops = []
    if kind == "rand":
        ops = [(ri(1, n), ri(1, n)) for _ in range(m)]
    elif kind == "snow":
        perm = list(range(1, n + 1))
        shuffle(perm)
        for i in range(1, n):
            a, b = perm[i], perm[ri(0, i - 1)]
            ops.append((a, b) if random.random() < 0.5 else (b, a))
    elif kind == "mod":
        for r in range(k):
            xs = list(range(r + 1, n + 1, k))
            shuffle(xs)
            for i in range(1, len(xs)):
                ops.append((xs[i], xs[ri(0, i - 1)]))
        heads = list(range(1, k + 1))
        shuffle(heads)
        for i in range(1, k):
            ops.append((heads[i], heads[ri(0, i - 1)]))
    elif kind == "blocks":
        starts = list(range(1, n + 1, k))
        for s in starts:
            for x in range(s + 1, min(n, s + k - 1) + 1):
                ops.append((x, x - 1) if random.random() < 0.5 else (x - 1, x))
        shuffle(starts)
        for i in range(1, len(starts)):
            ops.append((starts[i], starts[ri(0, i - 1)]))
    else:
        lo, hi = 1, n
        side = 0
        while lo < hi:
            if side:
                ops.append((lo + 1, 1))
                lo += 1
            else:
                ops.append((hi, 1))
                hi -= 1
            side ^= 1
    while len(ops) < m:
        ops.append((ri(1, n), ri(1, n)))
    add(n, ops[:m])


add(6, [(6, 3), (3, 2), (3, 1), (5, 1), (5, 1)])
add(5, [(5, 1), (4, 3), (5, 3), (1, 3)])
add(2, [(1, 1), (2, 1)])
add(7, [(2, 6), (2, 5), (6, 5), (1, 6), (1, 1), (2, 4)])
add(6, [(1, 5), (4, 3), (3, 3), (5, 4)])

make(8, 10, "rand")
make(20, 19, "mod", 2)
make(50, 60, "blocks", 4)
make(100, 120, "snow")
make(300, 300, "mod", 3)
make(1000, 1200, "sweep")
make(3000, 3000, "blocks", 50)
make(5000, 6000, "rand")

make(MAXN, MAXM, "snow")
make(MAXN, MAXM, "mod", 2)
make(MAXN, MAXM, "mod", 7)
make(MAXN, MAXM, "blocks", 3)
make(MAXN, MAXM, "blocks", 1000)
make(MAXN, MAXM, "sweep")
make(MAXN, MAXM, "rand")
make(MAXN, MAXM, "mod", 100)
make(MAXN, MAXM, "snow")
make(MAXN, MAXM, "blocks", 20)
make(MAXN, MAXM, "mod", 2000)

write_all()

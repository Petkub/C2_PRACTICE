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


random.seed(270303)
MAXN = 100_000
MAXM = 100_000
MAXH = 10 ** 9


def add(n, h, ops):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXM and len(h) == n + 1
    assert all(1 <= x <= MAXH for x in h[1:])
    for a, b in ops:
        assert 1 <= a <= n and 1 <= b <= n
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, h[1:])) + "\n" + "".join(f"{a} {b}\n" for a, b in ops))


def provinces(n, k, big=False):
    pool = [ri(1, MAXH) if big else ri(1, 3 * k + 5) for _ in range(k)]
    return [0] + [pool[ri(0, k - 1)] for _ in range(n)]


def rand_ops(n, m, same=0.1):
    ops = []
    for _ in range(m):
        if ops and random.random() < same:
            a, b = ops[ri(0, len(ops) - 1)]
            ops.append((b, a))
        else:
            ops.append((ri(1, n), ri(1, n)))
    return ops


def snowball(n, m, perm, reverse=False):
    ops = []
    for i in range(1, n):
        a, b = perm[i], perm[ri(0, i - 1)]
        ops.append((b, a) if reverse else (a, b))
    while len(ops) < m:
        ops.append((perm[ri(0, n - 1)], perm[ri(0, n - 1)]))
    return ops[:m]


def tworows(n, perm):
    half = n // 2
    ops = []
    for i in range(1, half):
        ops.append((perm[i], perm[i - 1]))
        ops.append((perm[half + i], perm[half + i - 1]))
    ops.append((perm[0], perm[half]))
    return ops


def make(n, m, k, kind, big=False):
    h = provinces(n, k, big)
    perm = list(range(1, n + 1))
    shuffle(perm)
    if kind == "rand":
        ops = rand_ops(n, m)
    elif kind == "snow":
        ops = snowball(n, m, perm)
    elif kind == "snowrev":
        ops = snowball(n, m, perm, True)
    else:
        ops = tworows(n, perm)[:m]
    add(n, h, ops)


add(6, [0, 3, 5, 3, 3, 5, 7], [(1, 2), (3, 4), (2, 3), (5, 6), (6, 1)])
add(4, [0, 10, 10, 10, 10], [(1, 2), (3, 4), (2, 4)])
add(2, [0, 1000000000, 1000000000], [(2, 1)])
add(7, [0, 1, 2, 1, 2, 1, 2, 1], [(1, 3), (2, 4), (5, 7), (6, 2), (3, 5), (4, 7)])
add(5, [0, 4, 8, 4, 9, 8], [(2, 5), (1, 5), (3, 4), (2, 3)])

make(8, 12, 2, "rand")
make(20, 30, 3, "snow")
make(50, 60, 5, "rand")
make(100, 150, 4, "snowrev", True)
make(300, 400, 10, "two")
make(1000, 1500, 30, "rand", True)
make(3000, 3000, 2, "snow")
make(5000, 6000, 100, "rand")

make(MAXN, MAXM, 1, "snow")
make(MAXN, MAXM, 2, "snow")
make(MAXN, MAXM, 50, "snow", True)
make(MAXN, MAXM, 3, "two")
make(MAXN, MAXM, MAXN, "snow", True)
make(MAXN, MAXM, 2, "snow", True)
make(MAXN, MAXM, 1, "snow", True)
make(MAXN, MAXM, 3, "snow")
make(MAXN, MAXM, 7, "snow")
make(MAXN, MAXM, 1, "two")

write_all()

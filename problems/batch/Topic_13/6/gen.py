# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13003)
MAXN = 60
MAXQ = 100_000
tests = []


def add(n, ks):
    assert 1 <= n <= MAXN and 1 <= len(ks) <= MAXQ
    assert all(1 <= k <= (1 << n) - 1 for k in ks)
    tests.append(f"{n} {len(ks)}\n" + "".join(f"{k}\n" for k in ks))


def rnd(n, q):
    return [random.randint(1, (1 << n) - 1) for _ in range(q)]


def special(n, q):
    """creases near powers of two and near the ends, plus random ones"""
    top = (1 << n) - 1
    ks = []
    while len(ks) < q:
        t = random.randint(0, 5)
        j = random.randint(0, n - 1)
        if t == 0:
            k = (1 << j) + random.randint(-2, 2)
        elif t == 1:
            k = top - random.randint(0, 3)
        elif t == 2:
            k = random.randint(1, top) | 1
        elif t == 3:
            k = random.randint(1, top) >> j << j
        elif t == 4:
            k = top - (1 << j) + random.randint(-1, 1)
        else:
            k = random.randint(1, top)
        if 1 <= k <= top:
            ks.append(k)
    return ks


# samples
add(2, [1, 2, 3])
add(3, [7, 4, 6])
add(1, [1])
add(60, [1 << 59, (1 << 60) - 1, 3])
add(10, [100, 512, 999, 1023])
# hidden: small (the brute force folds a real strip)
add(1, [1, 1])
add(2, [3, 2, 1])
add(3, list(range(1, 8)))
add(5, list(range(1, 32)))
add(10, list(range(1, 1024)))
add(12, rnd(12, 3000))
add(16, special(16, 5000))
add(18, special(18, 20000))
add(18, rnd(18, 20000))
# hidden: large
add(MAXN, rnd(MAXN, MAXQ))
add(MAXN, special(MAXN, MAXQ))
add(MAXN, special(MAXN, MAXQ))
add(MAXN, [(1 << MAXN) - 1 - i for i in range(MAXQ)])
add(MAXN, [(1 << 59) + random.randint(-MAXQ, MAXQ) for _ in range(MAXQ)])
add(59, rnd(59, MAXQ))
add(45, special(45, MAXQ))
add(40, rnd(40, MAXQ))
add(32, special(32, MAXQ))
add(30, rnd(30, MAXQ))
add(MAXN, [random.randint(1, (1 << random.randint(1, MAXN)) - 1) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

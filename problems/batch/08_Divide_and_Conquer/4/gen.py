# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13004)
MAXN = 60
MAXQ = 20_000
tests = []


def add(n, ks):
    assert 1 <= n <= MAXN and 1 <= len(ks) <= MAXQ
    assert all(0 <= k <= (1 << n) - 1 for k in ks)
    tests.append(f"{n} {len(ks)}\n" + "".join(f"{k}\n" for k in ks))


def rnd(n, q):
    return [random.randint(0, (1 << n) - 1) for _ in range(q)]


def special(n, q):
    """around the moves of the big disks, the ends, numbers made of few bits"""
    top = (1 << n) - 1
    ks = []
    while len(ks) < q:
        t = random.randint(0, 4)
        j = random.randint(0, n - 1)
        if t == 0:
            k = (1 << j) + random.randint(-2, 1)
        elif t == 1:
            k = top - random.randint(0, 3)
        elif t == 2:
            k = random.randint(0, 5)
        elif t == 3:
            k = sum(1 << b for b in random.sample(range(n), min(n, 3)))
        else:
            k = top ^ (1 << j)
        if 0 <= k <= top:
            ks.append(k)
    return ks


# samples
add(3, [3, 0, 7])
add(2, [1, 2])
add(1, [0, 1])
add(4, [5, 8, 10])
add(30, [536870912, 1073741823, 6])
# hidden: small (the brute force lists every move)
add(1, [1, 0, 1])
add(3, list(range(8)))
add(4, list(range(16)))
add(8, rnd(8, 300))
add(12, rnd(12, 2000))
add(16, special(16, 3000))
add(18, rnd(18, 5000))
add(18, special(18, 5000))
# hidden: large
add(MAXN, rnd(MAXN, MAXQ))
add(MAXN, rnd(MAXN, MAXQ))
add(MAXN, special(MAXN, MAXQ))
add(MAXN, [(1 << MAXN) - 1 - i for i in range(MAXQ)])
add(MAXN, [(1 << 59) - MAXQ // 2 + i for i in range(MAXQ)])
add(59, special(59, MAXQ))
add(50, rnd(50, MAXQ))
add(40, special(40, MAXQ))
add(33, rnd(33, MAXQ))
add(MAXN, [random.randint(0, (1 << random.randint(1, MAXN)) - 1) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

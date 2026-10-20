# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(13002)
MAXN = 300_000
tests = []


def add(a, b):
    n = len(a)
    assert 1 <= n <= MAXN and len(b) == n
    for p in (a, b):
        assert len(set(p)) == n and min(p) == 1 and max(p) == n
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def perm(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def near(a, swaps):
    """a copy of a with a few random swaps of nearby places"""
    b = a[:]
    n = len(b)
    for _ in range(swaps):
        i = random.randrange(n)
        j = min(n - 1, i + random.randint(1, 5))
        b[i], b[j] = b[j], b[i]
    return b


def blocks_reversed(a, k):
    """cut a into k blocks and reverse the order of the blocks (each block keeps its order)"""
    n = len(a)
    cuts = sorted(random.sample(range(1, n), k - 1))
    parts = [a[i:j] for i, j in zip([0] + cuts, cuts + [n])]
    return [x for part in reversed(parts) for x in part]


# samples
add([2, 4, 1, 3], [4, 1, 2, 3])
add([1, 2, 3], [1, 2, 3])
add([5, 4, 3, 2, 1], [1, 2, 3, 4, 5])
add([1], [1])
add([3, 6, 1, 5, 2, 4], [6, 3, 2, 1, 4, 5])
# hidden: small (checked by the brute force)
add([1, 2], [2, 1])
add([2, 1], [2, 1])
a = perm(10); add(a, perm(10))
a = perm(300); add(a, perm(300))
a = perm(2000); add(a, a[::-1])
a = perm(5000); add(a, near(a, 300))
a = perm(5000); add(a, blocks_reversed(a, 7))
a = perm(6000); add(a, perm(6000))
# hidden: large
N = MAXN
add(list(range(1, N + 1)), list(range(N, 0, -1)))       # every pair disagrees
a = perm(N); add(a, a[:])                               # no pair disagrees
a = perm(N); add(a, perm(N))
a = perm(N); add(a, perm(N))
a = perm(N); add(a, near(a, 1000))
a = perm(N); add(a, blocks_reversed(a, 2))
a = perm(N); add(a, blocks_reversed(a, 50))
a = perm(N); b = a[::-1]; add(a, near(b, 50_000))
add(list(range(N, 0, -1)), perm(N))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

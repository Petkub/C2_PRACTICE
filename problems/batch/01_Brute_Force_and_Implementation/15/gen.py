# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(20115)
MAXN = 200000
tests = []


def add(p):
    n = len(p)
    assert 1 <= n <= MAXN and sorted(p) == list(range(1, n + 1))
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n")


def shuffled(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def blocks(n, size, rev_inside=False):
    """values in increasing blocks, the blocks in random order"""
    bl = [list(range(i, min(n, i + size - 1) + 1)) for i in range(1, n + 1, size)]
    random.shuffle(bl)
    out = []
    for b in bl:
        out += b[::-1] if rev_inside else b
    return out


def nearly_sorted(n, swaps, rev=False):
    p = list(range(1, n + 1))
    for _ in range(swaps):
        i, j = random.randrange(n), random.randrange(n)
        p[i], p[j] = p[j], p[i]
    return p[::-1] if rev else p


# samples
add([3, 1, 2, 6, 4, 5])
add([8, 3, 4, 7, 2, 6, 1, 5])
add([2, 1, 4, 3])
add([1, 2, 3, 4, 5, 9, 7, 8, 6, 10, 11, 12])
add([16, 1, 8, 2, 9, 12, 3, 15, 10, 4, 6, 14, 5, 11, 13, 7])
# hidden: small
add([1])
add([2, 1])
add(list(range(1, 10)))
add(list(range(30, 0, -1)))
add(shuffled(60))
add(shuffled(200))
add(nearly_sorted(300, 20))
add(blocks(250, 7, True))
# hidden: large
add(list(range(1, MAXN + 1)))                    # every triple of values counts
add(list(range(MAXN, 0, -1)))
add(shuffled(MAXN))
add(shuffled(MAXN))
add(nearly_sorted(MAXN, 2000))
add(nearly_sorted(MAXN, 20000, rev=True))
add(blocks(MAXN, 450))
add(blocks(MAXN, 1000, True))
odd = list(range(1, MAXN + 1, 2))
even = list(range(2, MAXN + 1, 2))
add(odd + even[::-1])
add(shuffled(MAXN - 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

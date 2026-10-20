# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(91001)
MAXN, MAXX = 3000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, pts):
    n = len(pts)
    assert 2 <= n <= MAXN and 2 <= k <= n
    assert all(0 <= x <= MAXX and 0 <= y <= MAXX for (x, y) in pts)
    tests.append(f"{n} {k}\n" + "".join(f"{x} {y}\n" for (x, y) in pts))


def uniform(n, hi=MAXX):
    return [(ri(0, hi), ri(0, hi)) for _ in range(n)]


def blobs(n, c, spread, hi=MAXX):
    """n points around c centres"""
    cs = [(ri(spread, hi - spread), ri(spread, hi - spread)) for _ in range(c)]
    res = []
    for i in range(n):
        cx, cy = cs[i % c]
        res.append((cx + ri(-spread, spread), cy + ri(-spread, spread)))
    random.shuffle(res)
    return res


# samples
add(2, [(0, 0), (1, 0), (5, 0), (6, 1), (0, 3)])
add(3, [(2, 2), (2, 2), (4, 2), (2, 5)])
add(2, [(1000000000, 1000000000), (0, 0)])
add(4, [(0, 0), (3, 0), (0, 3), (3, 3), (1, 1), (8, 8)])
add(2, [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10)])
# hidden: small (every split is tried)
add(2, [(7, 7), (7, 7)])
add(3, [(5, 5)] * 3 + [(6, 6)] * 3)
add(9, uniform(9, 20))
add(4, uniform(9, 10))
add(2, blobs(9, 2, 3, 100))
add(5, [(i, 0) for i in range(9)])
# hidden: medium
add(10, blobs(200, 10, 1000, 10**6))
add(37, uniform(300, 10**4))
# hidden: maximum size
N = MAXN
add(2, uniform(N))
add(5, blobs(N, 5, 10**7))
add(40, blobs(N, 40, 10**6))
add(N // 2, uniform(N))
add(N, uniform(N))
add(100, [(ri(0, 54), ri(0, 54)) for _ in range(N)])        # many equal distances and duplicates
add(3, [(MAXX if i % 2 else 0, ri(0, MAXX)) for i in range(N)])   # two far lines: huge distances
add(2, [(ri(0, 1), ri(0, 1)) for _ in range(N)])         # four places only
add(777, [(i * 333_333, 0) for i in range(N)])               # equally spaced: every tree edge equal
add(2, [(MAXX, MAXX)] * (N - 1) + [(0, 0)])                  # the largest possible answer
add(N - 1, uniform(N))
add(11, blobs(N, 3, 10**8))
add(1000, blobs(N, 900, 10**5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

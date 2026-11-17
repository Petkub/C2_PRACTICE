# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60101)
MAXN, MAXC, MAXW = 100_000, 10**9, 40_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(shops):
    n = len(shops)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXC and 0 <= y <= MAXC and 1 <= w <= MAXW for (x, y, w) in shops)
    tests.append(f"{n}\n" + "".join(f"{x} {y} {w}\n" for (x, y, w) in shops))


def rnd(n, c=MAXC, wlo=1, whi=MAXW):
    return [(ri(0, c), ri(0, c), ri(wlo, whi)) for _ in range(n)]


def mirrored(n, c=MAXC, wlo=1, whi=MAXW):
    s = []
    for _ in range(n // 2):
        w = ri(wlo, whi)
        s.append((ri(0, c // 2), ri(0, c // 2), w))
        s.append((ri(c // 2 + 1, c), ri(c // 2 + 1, c), w))
    random.shuffle(s)
    return s


def heavy_far(n, k, c=MAXC):
    s = [(ri(0, c // 3), ri(0, c // 3), ri(1, 3)) for _ in range(n - k)]
    s += [(ri(c - c // 10, c), ri(c - c // 10, c), MAXW) for _ in range(k)]
    random.shuffle(s)
    return s


add([(1, 5, 2), (4, 1, 1), (6, 3, 3)])
add([(2, 2, 1), (7, 4, 5), (9, 9, 1)])
add([(10, 20, 7)])
add([(0, 0, 40000), (1000000000, 1000000000, 40000)])
add([(3, 3, 4), (3, 3, 1), (8, 1, 2), (0, 6, 2)])
add([(12, 10, 6), (5, 12, 4), (2, 4, 9), (11, 8, 2), (4, 1, 2), (10, 6, 6)])

add([(0, MAXC, MAXW)])
add([(5, 5, 3)] * 7)
add([(1, 1, 1), (2, 2, 1), (3, 3, 1), (100, 100, 4)])
add(rnd(8, 20, 1, 9))
add(mirrored(10, 30, 1, 5))
add(rnd(60, 1000))
add(heavy_far(200, 3, 10**6))
add(mirrored(2000))
add(rnd(5000, MAXC, 30000, MAXW))

N = MAXN
add(rnd(N, MAXC, 15000, MAXW))
add(rnd(N, MAXC, 25000, MAXW))
add([(ri(0, 1) * MAXC, ri(0, 1) * MAXC, MAXW) for _ in range(N)])
add(mirrored(N, MAXC, 30000, MAXW))
add(heavy_far(N, 30))
add(heavy_far(N, 8000))
add([(i * 9000, MAXC - i * 9000, ri(22000, MAXW)) for i in range(N)])
add([(ri(0, 50), ri(0, 50), ri(30000, MAXW)) for _ in range(N)])
s = mirrored(N - 1, MAXC, 25000, MAXW) + [(MAXC // 2, MAXC // 2, 1)]
add(s)
add(rnd(N, MAXC, MAXW, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

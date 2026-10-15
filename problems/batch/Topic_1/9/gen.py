# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10109)
MAXRC = 1000
MAXK = 100_000
MAXQ = 100_000
tests = []


def add(R, C, T, tarps, qs):
    assert 1 <= R <= MAXRC and 1 <= C <= MAXRC
    assert 1 <= len(tarps) <= MAXK and 1 <= len(qs) <= MAXQ
    assert 1 <= T <= len(tarps)
    for (r1, c1, r2, c2) in tarps + qs:
        assert 1 <= r1 <= r2 <= R and 1 <= c1 <= c2 <= C
    lines = [f"{R} {C} {len(tarps)} {T}"]
    lines += [f"{a} {b} {c} {d}" for (a, b, c, d) in tarps]
    lines.append(str(len(qs)))
    lines += [f"{a} {b} {c} {d}" for (a, b, c, d) in qs]
    tests.append("\n".join(lines) + "\n")


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rect(R, C, maxh=None, maxw=None):
    if maxh is None:
        a, b = sorted((ri(1, R), ri(1, R)))
    else:
        h = ri(1, min(maxh, R))
        a = ri(1, R - h + 1)
        b = a + h - 1
    if maxw is None:
        c, d = sorted((ri(1, C), ri(1, C)))
    else:
        w = ri(1, min(maxw, C))
        c = ri(1, C - w + 1)
        d = c + w - 1
    return (a, c, b, d)


def rects(n, R, C, maxh=None, maxw=None):
    return [rect(R, C, maxh, maxw) for _ in range(n)]


# samples
add(4, 5, 2, [(1, 1, 3, 3), (2, 2, 4, 5), (3, 1, 3, 5)], [(1, 1, 4, 5), (2, 2, 3, 3), (4, 1, 4, 5)])
add(3, 3, 2, [(1, 1, 2, 2), (2, 2, 3, 3)], [(1, 1, 3, 3), (1, 1, 1, 3)])
add(1, 1, 1, [(1, 1, 1, 1)], [(1, 1, 1, 1)])
add(1, 6, 2, [(1, 1, 1, 4), (1, 3, 1, 6), (1, 2, 1, 5)], [(1, 1, 1, 6)])
add(5, 5, 1, [(2, 2, 2, 2)], [(1, 1, 5, 5), (3, 3, 3, 3)])
# hidden (small)
add(1, 7, 2, [(1, 1, 1, 7), (1, 3, 1, 5), (1, 5, 1, 7)], [(1, i, 1, j) for i in range(1, 8) for j in range(i, 8)])
add(6, 1, 1, [(2, 1, 5, 1)], [(1, 1, 6, 1), (1, 1, 1, 1), (2, 1, 5, 1)])
add(8, 8, 3, rects(10, 8, 8), rects(30, 8, 8))
add(10, 12, 2, rects(25, 10, 12), rects(40, 10, 12))
add(30, 40, 5, rects(60, 30, 40), rects(200, 30, 40))
add(50, 50, 4, rects(300, 50, 50, 10, 10), rects(300, 50, 50))
add(100, 80, 40, rects(400, 100, 80), rects(500, 100, 80))
add(200, 200, 1, rects(2000, 200, 200, 20, 20), rects(2000, 200, 200))
add(200, 200, 2000, rects(2000, 200, 200), rects(500, 200, 200))     # T = K: only cells under every tarp
add(150, 300, 3, rects(3000, 150, 300, 15, 40), rects(3000, 150, 300))
R = C = MAXRC
full = (1, 1, R, C)
# large
add(R, C, MAXK // 8, rects(MAXK, R, C), rects(MAXQ, R, C))
add(R, C, 3, rects(MAXK, R, C, 60, 60), rects(MAXQ, R, C))
add(R, C, MAXK, [full] * MAXK, [full] * 30_000)                       # every cell has K layers
add(R, C, 1, rects(MAXK, R, C), rects(30_000, R, C))
add(R, C, MAXK, rects(MAXK, R, C), rects(30_000, R, C))               # nothing reaches T
add(R, C, 2, [(r, 1, r, C) for r in range(1, R + 1)] * 50 + [(1, c, R, c) for c in range(1, C + 1)] * 50,
    rects(MAXQ, R, C))                                                 # whole rows and whole columns
add(R, C, MAXK // 2, [(1 + i % 500, 1 + i % 500, R - i % 500, C - i % 500) for i in range(MAXK)],
    rects(30_000, R, C))                                               # nested frames
add(R, C, MAXK // 6, rects(MAXK, R, C), [full] * 30_000)
add(R, C, 7, rects(MAXK, R, C, 300, 300), [rect(R, C, 30, 30) for _ in range(MAXQ)])
add(R, C, MAXK // 10, rects(MAXK, R, C), rects(30_000, R, C))
add(R, C, 1, [(ri(1, R), ri(1, C)) * 2 for _ in range(MAXK)], rects(30_000, R, C))
add(R, C, 20, rects(MAXK, R, C, 500, 500), rects(30_000, R, C))
add(1000, 999, 20_000, rects(MAXK, 1000, 999), rects(30_000, 1000, 999))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

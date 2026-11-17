# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10007)
MAXCELLS, MAXH = 300000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g):
    r, c = len(g), len(g[0])
    assert r >= 1 and c >= 1 and r * c <= MAXCELLS
    assert all(len(row) == c and 1 <= min(row) and max(row) <= MAXH for row in g)
    tests.append(f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))


def rnd(r, c, lo=1, hi=MAXH):
    flat = random.choices(range(lo, hi + 1), k=r * c)
    return [flat[i * c:(i + 1) * c] for i in range(r)]


def slope(r, c):
    """height grows with i + j: every right/down staircase is a longest run (huge number of runs)"""
    return [[1 + (i + j) * 2 + ri(0, 1) for j in range(c)] for i in range(r)]


def snake(r, c, noise_rows=False):
    """one run covers the whole grid: boustrophedon order, heights 1..r*c along it"""
    g = [[0] * c for _ in range(r)]
    k = 1
    for i in range(r):
        cols = range(c) if i % 2 == 0 else range(c - 1, -1, -1)
        for j in cols:
            g[i][j] = k; k += 1
    return g


def comb(r, c):
    """rows in groups of three: a run row (one long run, dropping by 3 per cell, snaking down through the end
    columns), a row of dead-end cells just 1 below the run cell above them (between high walls), a wall row"""
    assert r >= 1 and c >= 5
    g = [[MAXH] * c for _ in range(r)]
    path = []
    for t in range((r + 2) // 3):
        cols = range(c) if t % 2 == 0 else range(c - 1, -1, -1)
        path += [(3 * t, j) for j in cols]
        end = c - 1 if t % 2 == 0 else 0
        if 3 * t + 3 < r:
            path += [(3 * t + 1, end), (3 * t + 2, end)]
    top = 3 * len(path) + 10
    assert top < MAXH
    for k, (i, j) in enumerate(path):
        g[i][j] = top - 3 * k
    for t in range((r + 2) // 3):
        if 3 * t + 1 < r:
            for j in range(2, c - 2, 2):
                if g[3 * t + 1][j] == MAXH:
                    g[3 * t + 1][j] = g[3 * t][j] - 1
    return g


def spiral(n):
    g = [[0] * n for _ in range(n)]
    i, j, di, dj = 0, 0, 0, 1
    for k in range(n * n, 0, -1):
        g[i][j] = k
        ni, nj = i + di, j + dj
        if not (0 <= ni < n and 0 <= nj < n and g[ni][nj] == 0):
            di, dj = dj, -di
            ni, nj = i + di, j + dj
        i, j = ni, nj
    return g


# samples
add([[9, 6, 3], [8, 7, 2], [5, 4, 1]])
add([[3, 3], [3, 3]])
add([[1, 5, 2, 8, 3]])
add([[4], [9], [7], [1]])
add([[7, 7, 6, 2], [8, 3, 5, 1], [9, 4, 4, 2], [1, 6, 8, 3]])
# hidden: small
add([[10, 12, 11, 30], [20, 14, 13, 25], [21, 15, 16, 22], [19, 18, 17, 23]])
add([[1]])
add(rnd(3, 4, 1, 5))
add(rnd(8, 8, 1, 20))
add(slope(12, 12))
add(snake(6, 7))
add(spiral(9))
add(rnd(50, 60, 1, 1000))
add(comb(30, 30))
# hidden: medium (random and flat grids have only short runs)
add(rnd(300, 300))
add(rnd(200, 400, 1, 100))                    # many equal neighbours
add([[MAXH] * 300 for _ in range(300)])        # nothing can move
# hidden: maximum size (every one has very long runs)
add(slope(547, 548))
add(slope(1, MAXCELLS))
add(snake(547, 548))
add(snake(2, 150000))
add(spiral(547))
add(snake(MAXCELLS, 1))
add([[MAXH - (i * 600 + j) % 1000 for j in range(500)] for i in range(600)])
add(comb(547, 548))
add(comb(3, 100000))
add(comb(60000, 5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7010)
MAXR = MAXC = 1000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC and r * c >= 2
    assert all(len(x) == c and set(x) <= set(".#ST") for x in rows)
    text = "".join(rows)
    assert text.count("S") == 1 and text.count("T") == 1
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def place(g, s=None, t=None):
    """put S and T on free cells (random ones unless given; T next to a wall or the border, so that
    the robot may stop there), return the rows as strings"""
    r, c = len(g), len(g[0])

    def blocked(i, j):
        return not (0 <= i < r and 0 <= j < c) or g[i][j] == "#"

    for ch, pos in (("S", s), ("T", t)):
        if pos is None:
            while True:
                i, j = ri(0, r - 1), ri(0, c - 1)
                if g[i][j] == "." and (ch == "S" or any(blocked(i + a, j + b)
                                                        for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0)))):
                    break
        else:
            i, j = pos
        g[i][j] = ch
    return ["".join(x) for x in g]


def solve(rows):
    """reference BFS (slow, small grids only)"""
    r, c = len(rows), len(rows[0])
    for i in range(r):
        for j in range(c):
            if rows[i][j] == "S":
                s = (i, j)
    dist = {s: 0}
    q = [s]
    for i, j in q:
        if rows[i][j] == "T":
            return dist[(i, j)]
        for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x, y = i, j
            while 0 <= x + a < r and 0 <= y + b < c and rows[x + a][y + b] != "#":
                x, y = x + a, y + b
            if (x, y) not in dist:
                dist[(x, y)] = dist[(i, j)] + 1
                q.append((x, y))
    return -1


def reachable_small(r, c, d):
    """random grid whose answer is not -1"""
    while True:
        rows = place(rnd(r, c, d))
        if solve(rows) >= 0:
            return rows


def corners(g):
    """S = first free cell of the top row, T = last free cell of the bottom row"""
    r, c = len(g), len(g[0])
    sj = next(j for j in range(c) if g[0][j] == ".")
    tj = next(j for j in range(c - 1, -1, -1) if g[r - 1][j] == ".")
    return place(g, (0, sj), (r - 1, tj))


def rnd(r, c, dens):
    return [["#" if random.random() < dens else "." for _ in range(c)] for _ in range(r)]


def serpentine(r, c):
    """corridors on even rows joined at alternating ends: the robot zigzags all the way down"""
    g = [["."] * c for _ in range(r)]
    for i in range(1, r, 2):
        for j in range(c):
            g[i][j] = "#"
        g[i][c - 1 if i % 4 == 1 else 0] = "."
    return g


# samples
add(["S..#.",
     "..#..",
     ".....",
     "#...T",
     "....#"])
add(["S....",
     "..T..",
     "....."])
add(["#S#",
     "#T.",
     "..."])
add(["S..T#."])
add(["..#...",
     "S...#.",
     "#.....",
     "...T.#"])
add(["T......",
     ".#####.",
     ".#...#.",
     ".#.S.#.",
     ".#...#.",
     ".......",
     ])
# hidden: small (checked by repeated relaxation)
add(["ST"])
add(["S", ".", "T"])
add(["S.T."])                                                  # T is passed over, never a stop
add(["T.S", "...", "..."])
for r, c, d in ((6, 6, 0.2), (8, 10, 0.3), (12, 12, 0.15), (15, 20, 0.35), (20, 20, 0.1),
                (30, 30, 0.25), (40, 50, 0.4), (60, 60, 0.05)):
    add(reachable_small(r, c, d))
add(place(rnd(30, 30, 0.3)))
add(place(serpentine(41, 30), (0, 0), (40, 29)))
add(reachable_small(150, 200, 0.3))
# hidden: large
R, C = MAXR, MAXC
add(place(rnd(R, C, 0.02), (0, 0), (R - 1, C - 1)))
add(corners(rnd(R, C, 0.1)))
add(corners(rnd(R, C, 0.2)))
add(corners(rnd(R, C, 0.25)))
add(corners(rnd(R, C, 0.08)))
add(corners(rnd(R, C, 0.4)))
add(place([["."] * C for _ in range(R)], (R // 2, C // 2), (R // 2 - 1, C // 2 + 7)))   # empty room: -1
add(place([["."] * C for _ in range(R)], (R // 2, C // 3), (R - 1, 0)))                 # empty room: 2
add(place(serpentine(R - 1, C), (0, 0), (R - 2, C - 1 if (R - 2) % 4 == 0 else 0)))
g = serpentine(R - 1, C)                                        # target in the middle of a corridor
add(place(g, (0, 0), (R // 2 + (R // 2) % 2, C // 2)))
g = rnd(R, C, 0.003)                                            # sparse posts: long slides
add(corners(g))
g = rnd(R, C, 0.1)
for j in range(C):                                              # a wall across the middle with few gaps
    g[R // 2][j] = "#"
for _ in range(4):
    j = ri(1, C - 1)
    for i in range(R):                                          # a clear column through each gap
        g[i][j] = "."
g[0][0] = "."
add(place(g, (0, 0), (R - 1, j)))
g = rnd(R, C, 0.25)
for j in range(C):                                              # a closed wall: unreachable half
    g[R // 2][j] = "#"
for (i, j) in ((ri(0, R // 2 - 1), ri(0, C - 1)), (ri(R // 2 + 1, R - 1), ri(0, C - 1))):
    g[i][j] = "."
s_pos = None
add(place(g))
g = [["."] * C for _ in range(R)]                               # a staircase: right and down move one cell each
for i in range(R - 2):
    g[i][i + 2] = "#"
    g[i + 2][i + 1] = "#"
add(place(g, (0, 0), (R - 1, C - 1)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

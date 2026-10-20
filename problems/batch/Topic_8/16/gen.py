# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(70016)
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
    tests.append(f"{r} {c}\n" + "\n".join(rows) + "\n")


def place(g, s=None, t=None):
    """put S and T on open cells (random ones unless given) and return the rows as strings"""
    opens = [(i, j) for i in range(len(g)) for j in range(len(g[0])) if g[i][j] == "."]
    if s is None:
        s = opens[ri(0, len(opens) - 1)]
    while t is None or t == s:
        t = opens[ri(0, len(opens) - 1)]
    g[s[0]][s[1]] = "S"
    g[t[0]][t[1]] = "T"
    return ["".join(x) for x in g]


def carve(g, s, t):
    """open a random monotone staircase path from s to t, so that T is reachable"""
    i, j = s
    g[i][j] = "."
    while (i, j) != t:
        di, dj = t[0] - i, t[1] - j
        if dj == 0 or (di != 0 and random.random() < abs(di) / (abs(di) + abs(dj))):
            i += 1 if di > 0 else -1
        else:
            j += 1 if dj > 0 else -1
        g[i][j] = "."
    return g


def corners(r, c):
    return (ri(0, r // 4), ri(0, c // 4)), (ri(r - 1 - r // 4, r - 1), ri(c - 1 - c // 4, c - 1))


def rnd_path(r, c, p):
    s, t = corners(r, c)
    return place(carve(rnd(r, c, p), s, t), s, t)


def rnd(r, c, p):
    w = [1 - p, p]
    return [random.choices(".#", w, k=c) for _ in range(r)]


def serpentine(r, c, width, noise):
    """horizontal walls every width+1 rows with a gap at alternating ends, some extra random blocks"""
    g = rnd(r, c, noise)
    k = 0
    for i in range(width, r, width + 1):
        g[i] = ["#"] * c
        gap = ri(0, 2) if k % 2 == 0 else c - 1 - ri(0, 2)
        g[i][gap] = "."
        if i + 1 < r:
            g[i + 1][gap] = "."
        g[i - 1][gap] = "."
        k += 1
    return g


def stairs(r, c):
    """only cells with j - i in {0, 1} (cut to the grid) are open: a long zigzag"""
    return [["." if 0 <= j - i <= 1 else "#" for j in range(c)] for i in range(r)]


def spiral(n):
    """a square spiral corridor"""
    g = [["#"] * n for _ in range(n)]
    i, j, d = 0, 0, 0
    dr, dc = (0, 1, 0, -1), (1, 0, -1, 0)
    g[0][0] = "."
    while True:
        moved = False
        for _ in range(2):
            ni, nj = i + 2 * dr[d], j + 2 * dc[d]
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == "#":
                g[i + dr[d]][j + dc[d]] = "."
                g[ni][nj] = "."
                i, j = ni, nj
                moved = True
                break
            d = (d + 1) % 4
        if not moved:
            return g, (i, j)


def rooms(r, c, step):
    """walls on a lattice of lines; each wall piece between two crossings gets one random door"""
    g = [["."] * c for _ in range(r)]
    for i in range(step, r, step):
        g[i] = ["#"] * c
    for j in range(step, c, step):
        for i in range(r):
            g[i][j] = "#"
    for i in range(step, r, step):                  # horizontal wall pieces
        for j in range(0, c, step):
            hi = min(c, j + step) - 1
            lo = j + 1 if j > 0 else 0
            if lo <= hi:
                g[i][ri(lo, hi)] = "."
    for j in range(step, c, step):                  # vertical wall pieces
        for i in range(0, r, step):
            hi = min(r, i + step) - 1
            lo = i + 1 if i > 0 else 0
            if lo <= hi:
                g[ri(lo, hi)][j] = "."
    return g


# samples
add(["S...#",
     ".##.#",
     ".#..T",
     "...#."])
add(["S.#..",
     "..#.T",
     "###..",
     "....."])
add(["S......T"])
add(["....",
     ".##.",
     "S#T.",
     "...."])
add(["S.....",
     "####..",
     "......",
     ".#####",
     "....T."])
add(["T.#S",
     "....",
     ".#.#"])
# hidden: small
add(["ST"])
add(["S", ".", "T"])
add(["S..#.T#", ".......", ".....#.", "#......", ".....#.", "##.....", "#....#."])
add(["...#T..", ".S.#.#.", ".......", "#.##...", "...#.#.", "....##.", "......."])
add([".##.#..", "#S.....", "...#..#", ".....##", "#.#....", "#.#...#", ".....T."])
add(["...###.", ".#...T#", ".......", ".......", "..#...#", "S.....#", "#..#.#."])
add(place(stairs(6, 7), (0, 0), (5, 6)))
add(place(serpentine(9, 4, 1, 0.0), (0, 0), (8, 3)))
add(rnd_path(40, 50, 0.35))
add(place(carve(serpentine(120, 80, 2, 0.15), (0, 0), (119, 79)), (0, 0), (119, 79)))
# hidden: large
R = C = 1000
add(place(rnd(R, C, 0.0), (0, 0), (R - 1, C - 1)))
add(place(rnd(R, C, 0.3)))
add(rnd_path(R, C, 0.42))
add(place(serpentine(R, C, 1, 0.0), (0, 0), (R - 1, C - 1)))
add(place(carve(serpentine(R, C, 3, 0.2), (0, 0), (R - 1, C - 1)), (0, 0), (R - 1, C - 1)))
add(place(stairs(R, C), (0, 0), (R - 1, C - 1)))
g, end = spiral(999)
add(place(g, (0, 0), end))
add(place(rooms(R, C, 10), (0, 0), (R - 2, C - 2)))
g = rnd(R, C, 0.1)                                   # T walled in: no path at all
for i in range(R // 2 - 1, R // 2 + 2):
    for j in range(C // 2 - 1, C // 2 + 2):
        g[i][j] = "#"
g[R // 2][C // 2] = "."
add(place(g, (0, 0), (R // 2, C // 2)))
for seed, p in ((8, 0.15), (6, 0.25), (10, 0.25), (6, 0.3)):
    # random S and T, many paths with equal turns (own generator so that these exact grids stay)
    rng = random.Random(seed)
    g = [rng.choices(".#", [1 - p, p], k=C) for _ in range(R)]
    s = (rng.randrange(R), rng.randrange(C))
    t = s
    while t == s:
        t = (rng.randrange(R), rng.randrange(C))
    g[s[0]][s[1]] = "S"
    g[t[0]][t[1]] = "T"
    add(["".join(x) for x in g])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

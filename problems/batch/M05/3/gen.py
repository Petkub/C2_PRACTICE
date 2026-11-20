# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45003)
SEEDS = [45003 * 100 + k for k in range(18)]
SEEDS[3] += 100
SEEDS[13] += 100
MAXR = MAXC = 300
KEYS, DOORS = "abcdef", "ABCDEF"
OK = set(".#SX" + KEYS + DOORS)
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g):
    if isinstance(g[0], list):
        g = ["".join(row) for row in g]
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(row) == c and set(row) <= OK for row in g)
    assert sum(row.count("S") for row in g) == 1 and sum(row.count("X") for row in g) == 1
    tests.append(f"{r} {c}\n" + "\n".join(g) + "\n")


def blank(r, c, ch="."):
    return [[ch] * c for _ in range(r)]


def put(g, i, j, ch):
    g[i][j] = ch


def free_cell(g, i0, i1, j0, j1):
    while True:
        i, j = ri(i0, i1), ri(j0, j1)
        if g[i][j] == ".":
            return i, j


def sprinkle(g, i0, i1, j0, j1, p, chars):
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            if g[i][j] == "." and random.random() < p:
                g[i][j] = random.choice(chars)


def strips(r, c, nwalls, cols, gaps, stands, wallp):
    g = blank(r, c)
    sprinkle(g, 0, r - 1, 0, c - 1, wallp, "#")
    rows = [(k + 1) * r // (nwalls + 1) for k in range(nwalls)]
    for w in rows:
        g[w] = ["#"] * c
        for _ in range(gaps):
            g[w][ri(0, c - 1)] = random.choice(cols.upper())
        for i in (w - 1, w + 1):
            for j in range(c):
                if g[w][j] != "#" and g[i][j] == "#":
                    g[i][j] = "."
    bounds = [-1] + rows + [r]
    for k in range(len(bounds) - 1):
        lo, hi = bounds[k] + 1, bounds[k + 1] - 1
        for _ in range(stands):
            i, j = free_cell(g, lo, hi, 0, c - 1)
            g[i][j] = random.choice(cols)
    i, j = free_cell(g, 0, bounds[1] - 1, 0, c - 1)
    g[i][j] = "S"
    i, j = free_cell(g, bounds[-2] + 1, r - 1, 0, c - 1)
    g[i][j] = "X"
    return g


def vwalls(r, c, step, col, wallp):
    g = blank(r, c)
    sprinkle(g, 0, r - 1, 0, c - 1, wallp, "#")
    cols = list(range(step, c - 1, step))
    for w in cols:
        for i in range(r):
            g[i][w] = "#"
        d = ri(r // 3, 2 * r // 3)
        g[d][w] = col.upper()
        g[d][w - 1] = g[d][w + 1] = "."
    bounds = [-1] + cols + [c]
    for k in range(len(bounds) - 1):
        lo, hi = bounds[k] + 1, bounds[k + 1] - 1
        i = 0 if k % 2 == 0 else r - 1
        g[i][ri(lo, hi)] = col
    i, j = free_cell(g, r // 3, 2 * r // 3, 0, bounds[1] - 1)
    g[i][j] = "S"
    i, j = free_cell(g, r // 3, 2 * r // 3, bounds[-2] + 1, c - 1)
    g[i][j] = "X"
    return g


def rooms(r, c, h, w, cols, pdoor, stands):
    g = blank(r, c, "#")
    rs = list(range(0, r - h + 1, h + 1))
    cs = list(range(0, c - w + 1, w + 1))
    for i0 in rs:
        for j0 in cs:
            for i in range(i0, i0 + h):
                for j in range(j0, j0 + w):
                    g[i][j] = "."
    for a, i0 in enumerate(rs):
        for b, j0 in enumerate(cs):
            if b + 1 < len(cs):
                ch = random.choice(cols.upper()) if random.random() < pdoor else "."
                g[ri(i0, i0 + h - 1)][j0 + w] = ch
            if a + 1 < len(rs):
                ch = random.choice(cols.upper()) if random.random() < pdoor else "."
                g[i0 + h][ri(j0, j0 + w - 1)] = ch
            for _ in range(stands):
                i, j = free_cell(g, i0, i0 + h - 1, j0, j0 + w - 1)
                g[i][j] = random.choice(cols)
    i, j = free_cell(g, 0, h - 1, 0, w - 1)
    g[i][j] = "S"
    i, j = free_cell(g, rs[-1], rs[-1] + h - 1, cs[-1], cs[-1] + w - 1)
    g[i][j] = "X"
    return g


def scatter(r, c, wallp, keyp, doorp, cols):
    g = blank(r, c)
    for i in range(r):
        for j in range(c):
            x = random.random()
            if x < wallp:
                g[i][j] = "#"
            elif x < wallp + keyp:
                g[i][j] = random.choice(cols)
            elif x < wallp + keyp + doorp:
                g[i][j] = random.choice(cols.upper())
    g[0][0] = "S"
    g[r - 1][c - 1] = "X"
    return g


def maze(r, c, cols, braid, pdoor, pkey):
    g = blank(r, c, "#")
    R2, C2 = (r + 1) // 2, (c + 1) // 2
    seen = [[False] * C2 for _ in range(R2)]
    stack = [(0, 0)]
    seen[0][0] = True
    g[0][0] = "."
    while stack:
        i, j = stack[-1]
        nb = [(i + di, j + dj) for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0))
              if 0 <= i + di < R2 and 0 <= j + dj < C2 and not seen[i + di][j + dj]]
        if not nb:
            stack.pop()
            continue
        a, b = random.choice(nb)
        seen[a][b] = True
        g[2 * a][2 * b] = "."
        g[i + a][j + b] = "."
        stack.append((a, b))
    for i in range(r):
        for j in range(c):
            if g[i][j] == "#" and (i + j) % 2 == 1 and random.random() < braid:
                g[i][j] = "."
    for i in range(r):
        for j in range(c):
            if g[i][j] == ".":
                x = random.random()
                if (i + j) % 2 == 1 and x < pdoor:
                    g[i][j] = random.choice(cols.upper())
                elif (i + j) % 2 == 0 and x < pkey:
                    g[i][j] = random.choice(cols)
    g[0][0] = "S"
    rr, cc = (r - 1) // 2 * 2, (c - 1) // 2 * 2
    g[rr][cc] = "X"
    return g


def lock_boss(g, ring):
    r, c = len(g), len(g[0])
    for i in range(r):
        for j in range(c):
            if g[i][j] == "X":
                g[i][j] = "."
    xi, xj = ri(2 * r // 3, r - 3), ri(2 * c // 3, c - 3)
    g[xi][xj] = "X"
    for di in range(-2, 3):
        for dj in range(-2, 3):
            i, j = xi + di, xj + dj
            if (di, dj) != (0, 0):
                g[i][j] = "#" if max(abs(di), abs(dj)) == 2 or (di, dj) not in [(a, b) for a, b, _ in ring] else "."
    for a, b, ch in ring:
        g[xi + a][xj + b] = ch
    return g


add(["S.aA.", "###.#", "X.Aa."])
add(["S.A..X", ".####B", ".ab..."])
add(["S#a.", ".A.X"])
add(["SaAaAX"])
add(["..c..", ".#C#.", "S#X#b", ".#B#.", "..a.."])
add(["S.a.#b.X", "#.#A#.#B", "c.C...a."])

add(["SX"])
add(["S", "a", "A", "A", "X"])
add(["Sa.", "AA.", "XAa"])
add(["S.aA", "#.#.", "XAb."])
for k, (r, c, cols) in enumerate(((5, 7, "ab"), (6, 6, "abc"), (8, 10, "abcd"))):
    random.seed(SEEDS[k])
    add(scatter(r, c, 0.15, 0.15, 0.2, cols))
random.seed(SEEDS[3])
add(strips(30, 40, 5, "ab", 3, 2, 0.1))
random.seed(SEEDS[4])
add(rooms(59, 59, 9, 9, "abc", 0.6, 2))

R = C = MAXR
big = [
    lambda: strips(R, C, 12, "ab", 4, 3, 0.12),
    lambda: strips(R, C, 20, "abc", 6, 4, 0.1),
    lambda: strips(R, C, 8, "abcdef", 10, 8, 0.15),
    lambda: vwalls(R, C, 25, "a", 0.15),
    lambda: vwalls(R, C, 14, "b", 0.08),
    lambda: rooms(R, C, 13, 13, "abcdef", 0.7, 3),
    lambda: rooms(R, C, 23, 23, "abc", 0.8, 2),
    lambda: scatter(R, C, 0.2, 0.005, 0.15, "abcdef"),
    lambda: scatter(R, C, 0.15, 0.008, 0.16, "ab"),
    lambda: scatter(R, C, 0.1, 0.002, 0.0, "abcdef"),
    lambda: maze(R, C, "abcdef", 0.25, 0.08, 0.1),
    lambda: lock_boss(scatter(R, C, 0.15, 0.05, 0.05, "abcde"), [(1, 0, "F")]),
    lambda: lock_boss(strips(R, C, 10, "abc", 6, 4, 0.1), [(-1, 0, "C"), (-2, 0, "C")]),
]
for k, make in enumerate(big):
    random.seed(SEEDS[5 + k])
    add(make())

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

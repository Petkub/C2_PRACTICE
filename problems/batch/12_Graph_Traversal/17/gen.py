# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(70017)
MAXR = MAXC = 300
KEYS, DOORS = "abcdef", "ABCDEF"
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(rows):
    if isinstance(rows[0], list):
        rows = ["".join(x) for x in rows]
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(x) == c and set(x) <= set(".#ST" + KEYS + DOORS) for x in rows)
    text = "".join(rows)
    assert text.count("S") == 1 and text.count("T") == 1
    tests.append(f"{r} {c}\n" + "\n".join(rows) + "\n")


def blank(r, c):
    return [["."] * c for _ in range(r)]


def rnd(r, c, p):
    return [random.choices(".#", [1 - p, p], k=c) for _ in range(r)]


def opens(g):
    return [(i, j) for i in range(len(g)) for j in range(len(g[0])) if g[i][j] == "."]


def sprinkle(g, letters, count):
    cells = opens(g)
    random.shuffle(cells)
    for (i, j) in cells[:count]:
        g[i][j] = random.choice(letters)
    return g


def put(g, ch, cell=None):
    if cell is None:
        cells = opens(g)
        cell = cells[ri(0, len(cells) - 1)]
    g[cell[0]][cell[1]] = ch
    return g


def maze(r, c, braid):
    g = [["#"] * c for _ in range(r)]
    g[0][0] = "."
    stack = [(0, 0)]
    while stack:
        i, j = stack[-1]
        nb = [(i + di, j + dj, di, dj) for di, dj in ((2, 0), (-2, 0), (0, 2), (0, -2))
              if 0 <= i + di < r and 0 <= j + dj < c and g[i + di][j + dj] == "#"]
        if not nb:
            stack.pop()
            continue
        ni, nj, di, dj = nb[ri(0, len(nb) - 1)]
        g[i + di // 2][j + dj // 2] = "."
        g[ni][nj] = "."
        stack.append((ni, nj))
    for i in range(r):
        for j in range(c):
            if g[i][j] == "#" and (i % 2) != (j % 2) and random.random() < braid:
                g[i][j] = "."
    return g


def vault(n, wall_p, copies, door_cnt):
    g = rnd(n, n, wall_p)
    mid = n // 2
    for i in range(mid - 20, mid + 21):
        for j in range(mid - 20, mid + 21):
            g[i][j] = "."
    order = list(DOORS)
    random.shuffle(order)
    for k in range(6):
        d = 4 + 3 * k
        ring = []
        for t in range(-d + 1, d):
            ring += [(mid - d, mid + t), (mid + d, mid + t), (mid + t, mid - d), (mid + t, mid + d)]
        for (i, j) in ring:
            g[i][j] = "#"
        for (i, j) in ((mid - d, mid - d), (mid - d, mid + d), (mid + d, mid - d), (mid + d, mid + d)):
            g[i][j] = "#"
        for _ in range(door_cnt):
            i, j = ring[ri(0, len(ring) - 1)]
            g[i][j] = order[k]
    g[mid][mid] = "T"
    out_cells = [(i, j) for (i, j) in opens(g) if max(abs(i - mid), abs(j - mid)) > 19]
    for letter in KEYS:
        for _ in range(copies):
            i, j = out_cells[ri(0, len(out_cells) - 1)]
            if g[i][j] == ".":
                g[i][j] = letter
    return g, out_cells


def keyed_maze(r, c, braid, extra):
    g = maze(r, c, braid)
    s, t = (0, 0), (r - 1 - (r - 1) % 2, c - 1 - (c - 1) % 2)
    par = {s: None}
    q = [s]
    for v in q:
        i, j = v
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            w = (i + di, j + dj)
            if 0 <= w[0] < r and 0 <= w[1] < c and g[w[0]][w[1]] == "." and w not in par:
                par[w] = v
                q.append(w)
    path = [t]
    while path[-1] != s:
        path.append(par[path[-1]])
    path.reverse()
    index = {v: k for k, v in enumerate(path)}
    attach = dict(index)
    for v in q:
        if v not in attach:
            attach[v] = attach[par[v]]
    letters = list(range(6))
    random.shuffle(letters)
    cuts = sorted(random.sample(range(len(path) // 8, len(path) - 2), 6))
    for k, cut in zip(letters, cuts):
        side = [v for v in q if attach[v] < cut and v not in index and g[v[0]][v[1]] == "."]
        if not side:
            side = [v for v in path[1:cut] if g[v[0]][v[1]] == "."]
        i, j = side[ri(0, len(side) - 1)]
        g[i][j] = KEYS[k]
        i, j = path[cut]
        g[i][j] = DOORS[k]
    reach = [v for v in q if g[v[0]][v[1]] == "."]
    random.shuffle(reach)
    for (i, j) in reach[:extra]:
        g[i][j] = random.choice(KEYS + DOORS)
    g[s[0]][s[1]] = "S"
    g[t[0]][t[1]] = "T"
    return g


add(["S.a#.",
     ".#.#.",
     "...AT"])
add(["a.S.Ab.B.T"])
add(["S.T"])
add(["S#T",
     "...",
     "bAa"])
add(["a.#T...",
     "..#.#B#",
     "S.A.#..",
     "##.##b.",
     "......."])
add(["T.Cc...",
     "####.#.",
     "S...Ab.",
     "####B#.",
     "a.....#"])

add(["ST"])
add(["S", "A", "T"])
add(["Sa", "AT"])
add(["SA", "aT"])
for _ in range(2):
    g = sprinkle(rnd(5, 6, 0.2), KEYS[:3] + DOORS[:3], 10)
    add(put(put(g, "S"), "T"))
g = sprinkle(rnd(8, 8, 0.25), KEYS + DOORS, 20)
add(put(put(g, "S"), "T"))
g = sprinkle(maze(9, 11, 0.1), KEYS[:4] + DOORS[:4], 14)
add(put(put(g, "S", (0, 0)), "T", (8, 10)))
g, out = vault(60, 0.15, 1, 2)
add(put(g, "S", (0, 0)))

R = C = MAXR
g, out = vault(R, 0.2, 2, 3)
add(put(g, "S", (0, 0)))
g, out = vault(R - 1, 0.05, 1, 1)
add(put(g, "S", out[ri(0, len(out) - 1)]))
g = blank(R, C)
for letter in KEYS:
    put(g, letter)
put(g, "S", (0, 0))
put(g, "T", (R // 2, C // 2))
for (i, j) in ((R // 2 - 1, C // 2), (R // 2 + 1, C // 2), (R // 2, C // 2 - 1), (R // 2, C // 2 + 1)):
    g[i][j] = "#"
add(g)
add(keyed_maze(R, C, 0.0, 0))
add(keyed_maze(R - 1, C, 0.03, 40))
add(keyed_maze(R, C - 1, 0.2, 300))
g = sprinkle(rnd(R, C, 0.25), KEYS + DOORS, 2000)
add(put(put(g, "S"), "T"))
g = sprinkle(rnd(R, C, 0.1), KEYS + DOORS, 9000)
add(put(put(g, "S"), "T"))
g = sprinkle(blank(R, C), DOORS, 20000)
add(put(put(g, "S", (0, 0)), "T", (R - 1, C - 1)))
g = blank(R, C)
for i in range(R - 1):
    g[i][C // 2] = "#"
g[0][C // 2] = "E"
g[0][1] = "e"
add(put(put(g, "S", (0, 0)), "T", (0, C - 1)))
g = blank(R, C)
for j in range(C):
    g[R // 2][j] = "D"
for letter in "abcef":
    put(g, letter)
g[R - 1][C - 1] = "d"
add(put(put(g, "S", (0, 0)), "T", (R - 2, C - 2)))
g = blank(R, C)
band = R // 7
for k in range(6):
    for j in range(C):
        g[band * (k + 1)][j] = "#"
    g[band * (k + 1)][(C - 1) if k % 2 == 0 else 0] = DOORS[k]
    g[band * k + band // 2][0 if k % 2 == 0 else C - 1] = KEYS[k]
add(put(put(g, "S", (0, C // 2)), "T", (R - 1, C // 2)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

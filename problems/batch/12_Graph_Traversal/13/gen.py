# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7013)
MAXR = MAXC = 1000
MAXK, MAXT = 100_000, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(rows, fires):
    r, c, k = len(rows), len(rows[0]), len(fires)
    assert 1 <= r <= MAXR and 1 <= c <= MAXC and 1 <= k <= MAXK
    assert all(len(x) == c and set(x) <= set(".#S") for x in rows)
    assert sum(x.count("S") for x in rows) == 1
    for a, b, t in fires:
        assert 1 <= a <= r and 1 <= b <= c and rows[a - 1][b - 1] != "#" and 1 <= t <= MAXT
    tests.append(f"{r} {c} {k}\n" + "".join(x + "\n" for x in rows)
                 + "".join(f"{a} {b} {t}\n" for a, b, t in fires))


def grid(r, c, dens):
    return [["#" if random.random() < dens else "." for _ in range(c)] for _ in range(r)]


def free_cell(g, inner=False):
    r, c = len(g), len(g[0])
    while True:
        i, j = ri(0, r - 1), ri(0, c - 1)
        if g[i][j] == "." and (not inner or 0 < i < r - 1 and 0 < j < c - 1):
            return i, j


def finish(g, s, fires):
    """g: list of lists, s = (i, j) 0-based, fires = [(i, j, t)] 0-based cells"""
    g[s[0]][s[1]] = "S"
    rows = ["".join(x) for x in g]
    add(rows, [(i + 1, j + 1, t) for i, j, t in fires])


def random_fires(g, k, tlo, thi):
    res = []
    for _ in range(k):
        i, j = free_cell(g)
        res.append((i, j, ri(tlo, thi)))
    return res


def serpentine(r, c):
    """border of walls, corridors on odd rows joined at alternating ends, the exit gap at the end;
    returns the grid, the start cell and the number of steps from the start to the exit gap"""
    g = [["#"] * c for _ in range(r)]
    rows = list(range(1, r - 1, 2))
    for k, i in enumerate(rows):
        for j in range(1, c - 1):
            g[i][j] = "."
        if k + 1 < len(rows):
            g[i + 1][c - 2 if k % 2 == 0 else 1] = "."
    last = rows[-1]
    end_j = c - 2 if (len(rows) - 1) % 2 == 0 else 1
    exit_j = end_j + 1 if end_j == c - 2 else 0
    g[last][exit_j] = "."
    steps = len(rows) * (c - 3) + 2 * (len(rows) - 1) + 1
    return g, (1, 1), (last, exit_j), steps


# samples
add(["#####",
     "#...#",
     "#.S..",
     "#...#",
     "##.##"], [(3, 4, 1)])
add(["######",
     "#S....",
     "######"], [(2, 5, 3)])
add(["######",
     "#S....",
     "######"], [(2, 5, 4)])
add(["..S..",
     "....."], [(1, 3, 1), (2, 1, 2)])
add(["#.####",
     "#....#",
     "#.##S#",
     "####.#"], [(4, 5, 1), (1, 2, 6)])
add(["#####",
     "#.S.#",
     "#####"], [(2, 2, 5)])
# hidden: small (checked by simulation)
add(["S"], [(1, 1, 1)])
add(["...", ".S.", "..."], [(2, 2, 1)])
add(["#.#", "#S#", "#.#"], [(1, 2, 1), (3, 2, 1)])
add(["#.#", "#S#", "#.#"], [(1, 2, 2), (3, 2, 1)])
for r, c, d, k, thi in ((6, 6, 0.2, 2, 5), (8, 9, 0.3, 3, 10), (10, 10, 0.25, 5, 8), (12, 15, 0.3, 4, 20),
                        (15, 15, 0.2, 10, 15), (20, 20, 0.35, 6, 30), (25, 30, 0.3, 30, 40), (40, 40, 0.25, 50, 60)):
    g = grid(r, c, d)
    s = free_cell(g, True)
    finish(g, s, random_fires(g, k, 1, thi))
g, s, ex, L = serpentine(21, 15)
finish(g, s, [(ex[0], ex[1], L + 1)])                            # just in time
g, s, ex, L = serpentine(21, 15)
finish(g, s, [(ex[0], ex[1], L)])                                # one minute late
g = grid(60, 60, 0.3)
s = free_cell(g, True)
finish(g, s, random_fires(g, 400, 1, 100))
# hidden: large
R, C = MAXR, MAXC
g = [["."] * C for _ in range(R)]                                 # open field, fires near the middle of each side
finish(g, (R // 2, C // 2), [(0, C // 2, 1), (R - 1, C // 2, 1), (R // 2, 0, 1), (R // 2, C - 1, 1)])
g = [["."] * C for _ in range(R)]                                 # fires at the corners a bit later
finish(g, (R // 2 - 3, C // 2 + 10), [(0, 0, 20), (R - 1, C - 1, 1), (0, C - 1, 5), (R - 1, 0, 12)])
g = grid(R, C, 0.3)
s = free_cell(g, True)
finish(g, s, random_fires(g, MAXK, 1, MAXT))                      # many fires, most of them too late to matter
g = grid(R, C, 0.25)
s = (R // 2, C // 2)
g[s[0]][s[1]] = "."
f = random_fires(g, MAXK, 600, 5000)                              # many fires at close times, listed latest first
f.sort(key=lambda x: -x[2])
finish(g, s, f)
g = grid(R, C, 0.2)
s = (R // 2, C // 2)
g[s[0]][s[1]] = "."
finish(g, s, random_fires(g, 2000, 400, 900))
g, s, ex, L = serpentine(R - 1, C)
finish(g, s, [(ex[0], ex[1], L + 1)] + [(ex[0], ex[1], MAXT)] * 10)   # just in time along the long corridor
g, s, ex, L = serpentine(R - 1, C)
finish(g, s, [(ex[0], ex[1], L)])                                 # one minute late
g, s, ex, L = serpentine(R - 1, C)
mid = (R // 2 | 1, C // 2)                                        # a fire in the middle of the way, late enough
finish(g, s, [(mid[0], mid[1], L - 3000)] + random_fires(g, 1000, L, MAXT))
g = grid(R, C, 0.3)                                               # the person is walled in: no way out, no fire
s = (R // 2, C // 2)
for i in range(s[0] - 2, s[0] + 3):
    for j in range(s[1] - 2, s[1] + 3):
        g[i][j] = "#" if max(abs(i - s[0]), abs(j - s[1])) == 2 else "."
fires = [(i, j, t) for i, j, t in random_fires(g, 100, 1, 10) if max(abs(i - s[0]), abs(j - s[1])) > 2]
finish(g, s, fires)
g = [["."] * C for _ in range(R)]                                 # the fire starts under the person's feet
finish(g, (R // 2, 3), [(R // 2, 3, 1)] + [(ri(0, R - 1), ri(10, C - 1), ri(1, 50)) for _ in range(500)])
g = grid(R, C, 0.15)
s = (R // 2, C // 2)
g[s[0]][s[1]] = "."
fires = []
for _ in range(MAXK):                                             # a ring of fires around the person
    i, j = free_cell(g)
    d = abs(i - s[0]) + abs(j - s[1])
    fires.append((i, j, max(1, d + ri(20, 300))))
finish(g, s, fires)
for dens, k, thi in ((0.2, 1000, 1500), (0.1, MAXK, 3000)):     # fires at very different times all over the map
    g = grid(R, C, dens)
    s = (R // 2, C // 2)
    g[s[0]][s[1]] = "."
    finish(g, s, random_fires(g, k, 1, thi))
g = [["#"] * C for _ in range(R)]                                # two corridors; a late fire sits where an early one arrives
for j in range(601):
    g[499][j] = g[520][j] = "."
for i in range(499, 521):
    g[i][600] = "."
for i in range(450, 499):
    g[i][300] = "."
cells = [(i, j) for i in range(R) for j in range(C) if g[i][j] == "." and (i, j) != (499, 600)]
fires = [(450, 300, 1), (499, 300, MAXT)] + [(*cells[ri(0, len(cells) - 1)], ri(900, MAXT)) for _ in range(1000)]
finish(g, (499, 600), fires)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

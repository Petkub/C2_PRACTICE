# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43006)
MAXHW, MAXN = 10**6, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g, s, e, d):
    h, w, n = len(g), len(g[0]), len(d)
    assert 1 <= h and 1 <= w and h * w <= MAXHW and 1 <= n <= MAXN
    assert all(len(r) == w and set(r) <= set(".#") for r in g) and set(d) <= set("UDLR")
    (sr, sc), (er, ec) = s, e
    assert 1 <= sr <= h and 1 <= sc <= w and 1 <= er <= h and 1 <= ec <= w
    assert g[sr - 1][sc - 1] == "." and g[er - 1][ec - 1] == "."
    tests.append(f"{h} {w} {n}\n{sr} {sc} {er} {ec}\n{d}\n" + "\n".join(g) + "\n")


def grid(h, w, p):
    return [["#" if random.random() < p else "." for _ in range(w)] for _ in range(h)]


def rows(g):
    return ["".join(r) for r in g]


def free(g, *cells):
    for r, c in cells:
        g[r - 1][c - 1] = "."


def dirs(n, alpha="UDLR", run=1):
    out, total = [], 0
    while total < n:
        k = ri(1, run)
        out.append(random.choice(alpha) * k)
        total += k
    return "".join(out)[:n]


def snake(h, w):
    g = [["#"] * w for _ in range(h)]
    for r in range(0, h, 2):
        for c in range(w):
            g[r][c] = "."
        if r + 1 < h:
            g[r + 1][w - 1 if (r // 2) % 2 == 0 else 0] = "."
    return g


def detour(h, w, p, fill_n, alpha1, alpha2, r, c):
    g = grid(h, w, p)
    for rr in range(r - 1, r + 3):
        for cc in range(c, c + 3):
            g[rr - 1][cc - 1] = "."
    g[r - 1][c] = "#"
    g[r][c] = "#"
    d = dirs(fill_n, alpha1, 3) + "DDRRUU"
    return g, (r, c), (r, c + 2), d


add(["..##", "....", ".#.."], (1, 1), (3, 4), "RRDLDLRURD")
add(["...", "..."], (1, 1), (2, 3), "RRRR")
add([".#", ".."], (2, 1), (2, 1), "URL")
add(["#.#..", "#....", "...##", "...#."], (4, 1), (1, 5), "DURLRURLRU")
add(["..#", "..#", "...", "#.#", "..."], (1, 1), (5, 3), "DRDLDLDRL")


add(["."], (1, 1), (1, 1), "U")
add(["..", ".."], (1, 1), (2, 2), "DDDDLLLLR")
add(["...", ".#.", "..."], (2, 1), (2, 3), "UURRRDD")
g, s, e, d = detour(4, 3, 0.0, 0, "U", "U", 2, 1)
add(rows(g), s, e, d + "UULL")
for h, w, n, p, a, run in [(5, 5, 40, 0.2, "UDLR", 1), (6, 8, 80, 0.3, "UDLR", 4), (8, 8, 150, 0.35, "DRRUL", 3),
                           (10, 12, 300, 0.25, "UDLR", 6), (12, 15, 400, 0.2, "ULR", 2)]:
    g = grid(h, w, p)
    sr, sc, er, ec = ri(1, h), ri(1, w), ri(1, h), ri(1, w)
    free(g, (sr, sc), (er, ec))
    add(rows(g), (sr, sc), (er, ec), dirs(n, a, run))
g, s, e, d = detour(10, 10, 0.1, 60, "UDL", "UL", 5, 5)
add(rows(g), s, e, d + dirs(40, "UL", 2))
g, s, e, d = detour(20, 20, 0.0, 200, "UDL", "LU", 9, 12)
add(rows(g), s, e, d + dirs(100, "LU", 3))


N = MAXN
g = grid(1000, 1000, 0.0)
for rr, cc in [(499, 500), (501, 500), (500, 499), (500, 501)]:
    g[rr - 1][cc - 1] = "#"
add(rows(g), (1, 1), (500, 500), dirs(N, "UDLR", 3))
add(rows(snake(999, 1001)), (1, 1), (999, 1), dirs(N, "UDLR", 4))
add(["." * MAXHW], (1, 1), (1, 200_000), dirs(N, "UDLR", 5))
add(["."] * MAXHW, (MAXHW, 1), (MAXHW - 150_000, 1), dirs(N, "UDLR", 2))
g = grid(1000, 1000, 0.3)
free(g, (1, 1), (1000, 1000))
add(rows(g), (1, 1), (1000, 1000), dirs(N, "UDLR", 6))
g = grid(500, 2000, 0.2)
free(g, (250, 1), (250, 2000))
add(rows(g), (250, 1), (250, 2000), dirs(N, "DLUULRUD", 3))
for p, r, c in [(0.0, 500, 998), (0.15, 300, 400), (0.1, 997, 900)]:
    g, s, e, d = detour(1000, 1000, p, N // 2, "UDL", "UL", r, c)
    add(rows(g), s, e, d + dirs(N - len(d), "UL", 4))
g, s, e, d = detour(1000, 1000, 0.05, N - 400_006, "UDL", "UL", 700, 300)
add(rows(g), s, e, d + dirs(400_000, "LU", 1))
g = snake(1000, 1000)
add(rows(g), (1, 1), (999, 1000 if (998 // 2) % 2 == 0 else 1), dirs(N, "UDLR", 1))
g = grid(1000, 1000, 0.32)
free(g, (500, 500), (1, 1000))
add(rows(g), (500, 500), (1, 1000), dirs(N, "UDDLRR", 2))
g = grid(1, MAXHW, 0.0)
add(rows(g), (1, MAXHW // 2), (1, MAXHW // 2 - 150_000), "R" * (N - 400_000) + dirs(400_000, "LR", 8))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

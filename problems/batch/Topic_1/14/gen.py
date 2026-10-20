# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(121407)
MAXRC, MAXV, MAXS = 500, 10 ** 9, 100
tests = []


def check_stamp(p):
    h, w = len(p), len(p[0])
    assert 1 <= h <= MAXS and 1 <= w <= MAXS and all(len(x) == w and set(x) <= set(".#") for x in p)
    cols = ["".join(p[r][c] for r in range(h)) for c in range(w)]
    for line in list(p) + cols:
        assert "#" in line
        assert "#" not in line[line.index("#"):].lstrip("#")      # one block of '#'


def add(grid_text, r, c, p):
    """grid_text: the grid lines already joined (big grids are reused by several tests)"""
    check_stamp(p)
    h, w = len(p), len(p[0])
    assert 1 <= r <= MAXRC and 1 <= c <= MAXRC
    assert (h <= r and w <= c) or (w <= r and h <= c)
    tests.append(f"{r} {c}\n" + grid_text + f"{h} {w}\n" + "".join(x + "\n" for x in p))


def text(g):
    for row in g:
        assert all(-MAXV <= v <= MAXV for v in row)
    return "".join(" ".join(map(str, row)) + "\n" for row in g)


def grid(r, c, lo=-MAXV, hi=MAXV):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def walk(n, lo, hi, up, delay=0):
    """a monotone random sequence of length n between lo and hi (an increasing one waits `delay` steps at lo,
    a decreasing one starts at hi)"""
    v = lo if up else hi
    out = []
    for i in range(n):
        out.append(v)
        if i >= delay and random.random() < 0.5:
            v = min(hi, v + random.randint(0, 3)) if up else max(lo, v - random.randint(0, 3))
    return out


def blob(h, w, cut):
    """a random stamp: every row and every column is one block (the four corners are cut off by monotone
    walls of different sizes)"""
    cut = min(cut, (w - 1) // 2)
    while True:
        c1, c2, c3, c4 = (random.randint(0, cut) for _ in range(4))
        tl = walk(h, 0, c1, False)                            # top-left corner: left edge goes left
        tr = [w - 1 - x for x in walk(h, 0, c2, False)]       # top-right corner: right edge goes right
        bl = walk(h, 0, c3, True, random.randint(h // 2, h))  # bottom-left corner: left edge goes right
        br = [w - 1 - x for x in walk(h, 0, c4, True, random.randint(h // 2, h))]
        rows = []
        for r in range(h):
            a = max(tl[r], bl[r])
            b = min(tr[r], br[r])
            if a > b:
                break
            rows.append("." * a + "#" * (b - a + 1) + "." * (w - 1 - b))
        else:
            # drop empty columns
            keep = [c for c in range(w) if any(row[c] == "#" for row in rows)]
            rows = ["".join(row[c] for c in keep) for row in rows]
            try:
                check_stamp(rows)
            except AssertionError:
                continue
            return rows


def orient(p, k, m):
    """k quarter turns clockwise after an optional mirror"""
    if m:
        p = [row[::-1] for row in p]
    for _ in range(k):
        p = ["".join(p[len(p) - 1 - r][c] for r in range(len(p))) for c in range(len(p[0]))]
    return p


def plant(g, p, val):
    """add val under the '#' cells of p at a random position"""
    r, c = len(g), len(g[0])
    i = random.randint(0, r - len(p))
    j = random.randint(0, c - len(p[0]))
    for x, row in enumerate(p):
        for y, ch in enumerate(row):
            if ch == "#":
                g[i + x][j + y] = max(-MAXV, min(MAXV, g[i + x][j + y] + val))


def small(r, c, h, w, cut, lo=-9, hi=9):
    g = grid(r, c, lo, hi)
    p = blob(h, w, cut)
    if not ((len(p) <= r and len(p[0]) <= c) or (len(p[0]) <= r and len(p) <= c)):
        p = blob(min(h, r, c), min(w, r, c), cut)
    add(text(g), r, c, p)


# samples
add(text([[3, -1, 2, 0, 5],
          [1, 4, -2, 6, 1],
          [0, 2, 7, 3, -4],
          [2, -3, 1, 1, 2]]), 4, 5, ["#.", "#.", "##"])
add(text([[4], [-1], [3]]), 3, 1, ["###"])
add(text([[-5, -2], [-7, -3]]), 2, 2, ["#.", "##"])
add(text([[1, -2], [-3, 4]]), 2, 2, ["#"])
add(text([[2, 9, 1, 0], [6, 1, 8, 2]]), 2, 4, ["##.", ".##"])
# hidden: small
add(text([[-MAXV]]), 1, 1, ["#"])
add(text([[MAXV, -MAXV, MAXV]]), 1, 3, ["#", "#"])
add(text([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), 3, 3, [".#.", "###", ".#."])
small(6, 7, 3, 4, 2)
small(10, 8, 5, 5, 2)
small(12, 15, 7, 4, 3)
small(20, 20, 8, 9, 4, -100, 100)
small(25, 30, 12, 6, 5, -MAXV, MAXV)
small(9, 40, 30, 5, 2)                         # only the turned stamp fits
g = grid(30, 30, -50, 50)
p = blob(10, 7, 4)
plant(g, orient(p, 3, 1), 1000)
add(text(g), 30, 30, p)
# hidden: large
R = C = MAXRC
G1 = text(grid(R, C))
G2 = text(grid(R, C, -MAXV, MAXV // 2))
add(G1, R, C, blob(100, 100, 30))
add(G1, R, C, blob(100, 97, 45))
add(G2, R, C, blob(99, 100, 20))
add(G2, R, C, blob(100, 70, 35))
add(G1, R, C, ["#" * 100] + ["#" * 99 + "."] * 99)   # nearly a square, still 8 different orientations
g = grid(R, C)
p = blob(100, 100, 40)
plant(g, orient(p, 1, 1), 3 * 10 ** 8)              # the best place needs mirror + one turn
add(text(g), R, C, p)
g = grid(R, C, -MAXV, -MAXV + 1000)                  # every value negative: the answer is negative
add(text(g), R, C, blob(100, 100, 35))
add(text([[MAXV] * C for _ in range(R)]), R, C, ["#" * 100] * 100)     # largest total 10^13
g = grid(R, C)
p = blob(100, 95, 30)
plant(g, orient(p, 2, 0), 4 * 10 ** 8)
add(text(g), R, C, p)
add(text(grid(MAXS, R)), MAXS, R, blob(MAXS, 40, 15))                  # stamp as tall as the paper
add(text(grid(R, 120)), R, 120, blob(60, 100, 25))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

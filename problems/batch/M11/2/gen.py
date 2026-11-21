# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511003)
MAXR = MAXC = 600
MAXH = 10 ** 6
tests = []


def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC and all(len(row) == c for row in g)
    assert all(1 <= x <= MAXH for row in g for x in row)
    tests.append(f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))


def parse(s):
    return [list(map(int, line.split())) for line in s.strip().split("\n")]


def rnd(r, c, lo, hi):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def frame(r, c, inner, step, base, rise=1):

    g = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            d = min(i, j, r - 1 - i, c - 1 - j)
            depth = max(0, inner - d)
            g[i][j] = base + ((depth + step - 1) // step) * rise
    return g


def snake(r, c, low, wall, leak):

    g = [[wall] * c for _ in range(r)]
    path = []
    rows = list(range(2, r - 2, 2))
    for k, i in enumerate(rows):
        cols = range(2, c - 2) if k % 2 == 0 else range(c - 3, 1, -1)
        for j in cols:
            path.append((i, j))
        if k + 1 < len(rows):
            j = c - 3 if k % 2 == 0 else 2
            path.append((i + 1, j))
    for i, j in path:
        g[i][j] = low
    if leak:
        i, j = path[-1]
        g[i][j] = low - 1
    return g


def patches(r, c, count, high, big=40):

    g = [[2] * c for _ in range(r)]
    for _ in range(count):
        h, w = random.randint(3, big), random.randint(3, big)
        i, j = random.randint(1, r - h - 2), random.randint(1, c - w - 2)
        for a in range(i, i + h):
            for b in range(j, j + w):
                g[a][b] = high if a in (i, i + h - 1) or b in (j, j + w - 1) else 1
    return g


def rings(r, c, width, top):

    g = [[0] * c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            d = min(i, j, r - 1 - i, c - 1 - j)
            g[i][j] = top - d // width
    return g


add(parse("5 5 5 5 5\n5 2 2 4 5\n5 5 5 1 5\n5 5 5 5 5"))
add(parse("2 2 2 2\n2 1 1 2\n2 1 2 2\n2 2 2 2"))
add(parse("5 5 5\n5 4 5\n5 5 5"))
add(parse("3 3 2 2 4 4\n4 4 1 1 4 4\n3 3 3 3 1 3\n4 1 1 1 1 4\n4 3 4 4 2 2"))
add(parse("3 4 3 4 2 2 4\n2 1 1 1 2 1 2\n2 2 5 1 4 3 3\n4 3 5 2 1 4 3\n4 5 2 2 2 5 5"))

add([[7]])
add([[3, 3, 3]])
add([[2] * 4 for _ in range(4)])
add(rnd(6, 8, 1, 3))
add(rnd(8, 6, 1, 2))
add(frame(9, 9, 2, 1, 1))
add(snake(9, 12, 2, 3, True))
add(rnd(12, 12, 1, 4))

add(rnd(60, 80, 1, 3))
add(patches(80, 80, 6, 3))
add(rings(70, 90, 5, 30))

add(frame(MAXR, MAXC, 220, 7, 1))
add(snake(MAXR, MAXC, 5, 9, False))
add(snake(MAXR, MAXC, 5, 9, True))
add(patches(MAXR, MAXC, 60, 3))
add(rings(MAXR, MAXC, 60, 50))
add(frame(MAXR, MAXC, 40, 3, MAXH - 200))
add([[2] * MAXC for _ in range(MAXR)])
add(patches(MAXR, MAXC, 5, 3, 250))
g = frame(MAXR, MAXC, 200, 5, 1)
for i in range(MAXR):
    for j in range(MAXC):
        if g[i][j] == 1 and random.random() < 0.0005:
            g[i][j] = 2
add(g)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

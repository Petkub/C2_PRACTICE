# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7004)
MAXR = MAXC = 1000
tests = []


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(x) == c and set(x) <= set(".#H") for x in rows)
    assert any("H" in x for x in rows)
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def grid(r, c, pwall, phosp):
    rows = []
    for _ in range(r):
        row = []
        for _ in range(c):
            x = random.random()
            row.append("#" if x < pwall else ("H" if x < pwall + phosp else "."))
        rows.append("".join(row))
    if not any("H" in x for x in rows):
        rows[0] = "H" + rows[0][1:]
    return rows


def put(g, cells, ch):
    g = [list(x) for x in g]
    for i, j in cells:
        g[i][j] = ch
    return ["".join(x) for x in g]


def snake(r, c):
    """corridors one cell wide joined at alternating ends"""
    g = []
    for i in range(r):
        if i % 2 == 0:
            g.append("." * c)
        elif i % 4 == 1:
            g.append("#" * (c - 1) + ".")
        else:
            g.append("." + "#" * (c - 1))
    return g


# samples
add(["H...#", ".##..", "....H"])
add(["H.#.", "..#.", "##.."])
add(["H"])
add(["H#.", "##."])
add(["..#...", "H.#..H", "..##..", "......"])
add(["H.#....", "..#.##.", "###.#H.", "...#..."])
# hidden: small
add(["H."])
add(["HHH", "HHH"])                                         # no ordinary cell
add(["H#H", "#.#", "H#H"])                                  # the only ordinary cell is enclosed
add(["." * 9 + "H"])
add(put(snake(7, 6), [(6, 5)], "H"))
add(grid(6, 8, 0.3, 0.05))
add(grid(10, 10, 0.4, 0.02))
add(grid(15, 20, 0.2, 0.01))
add(grid(30, 30, 0.35, 0.003))
add(put(snake(101, 99), [(0, 0)], "H"))
add(grid(200, 300, 0.25, 0.001))
add(grid(400, 500, 0.0, 0.00005))
# hidden: large
R = C = 1000
add(put(["." * C] * R, [(0, 0)], "H"))                      # one hospital in a corner, largest distance
add(["H" * C] + ["." * C] * (R - 1))                        # the whole top row
add(["." * (C - 1) + "H"] * R)                              # the whole right column
add(put(["." * C] * R, [(i, i) for i in range(R)], "H"))    # the diagonal
add(put(snake(R, C), [(R - 1, 0 if (R - 2) % 4 == 1 else C - 1)], "H"))   # the end of a long snake
add(put(snake(R, C), [(0, 0), (R - 1, C - 1)], "H"))
add(grid(R, C, 0.3, 0.01))
add(grid(R, C, 0.45, 0.0005))                               # many cells cannot reach a hospital
add(grid(R, C, 0.1, 0.3))
g = ["." * C] * R                                           # a walled square without hospital in the middle
g = put(g, [(i, j) for i in range(250, 751) for j in (250, 750)] +
        [(i, j) for i in (250, 750) for j in range(250, 751)], "#")
add(put(g, [(0, C - 1), (R - 1, 0)], "H"))
add(put(["#" * C] * R, [(i, j) for i in range(R) for j in range(C) if (i + j) % 2 == 0], "H"))  # no ordinary cell

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

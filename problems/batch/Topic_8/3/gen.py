# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7003)
MAXR = MAXC = 1000
tests = []


def add(rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(x) == c and set(x) <= set(".#ST") for x in rows)
    text = "".join(rows)
    assert text.count("S") == 1 and text.count("T") == 1
    tests.append(f"{r} {c}\n" + "".join(x + "\n" for x in rows))


def board(r, c, p, s, t, rng=random):
    """r x c board, each square damaged with probability p, S and T at the given (row, col)"""
    g = [["#" if rng.random() < p else "." for _ in range(c)] for _ in range(r)]
    g[s[0]][s[1]] = "S"
    g[t[0]][t[1]] = "T"
    return ["".join(x) for x in g]


def put(g, cells, ch):
    g = [list(x) for x in g]
    for i, j in cells:
        g[i][j] = ch
    return ["".join(x) for x in g]


def snake(r, c, s_top=True):
    """corridors of 2 open rows, walls of 3 damaged rows with a 4-wide shaft at alternating ends"""
    g = []
    k = 0
    while len(g) + 2 <= r:
        g += ["." * c] * 2
        if len(g) + 3 + 2 > r:
            break
        gap = "#" * (c - 4) + "...." if k % 2 == 0 else "...." + "#" * (c - 4)
        g += [gap] * 3
        k += 1
    while len(g) < r:
        g.append("#" * c)
    last = max(i for i in range(r) if "." in g[i])
    g = put(g, [(0, 0)], "S")
    tcol = c - 1 if k % 2 == 0 else 0
    return put(g, [(last, tcol)], "T")


# samples
add(["S...", "....", "...T"])
add(["S..", ".T.", "..."])
add(["S.#..", ".#...", "..#..", "....T"])
add(["S...T."])
add(["....", ".ST.", "....", "...."])
add(["S.....#.", "...#.#..", "###..#.#", ".##.##..", "#...#..T"])
# hidden: small
add(["ST"])
add(["S", "T"])
add(["S.", "..", ".T"])
add(["S..", "...", "..T"])
add(["S" + "." * 9, "." * 9 + "T"])                           # two rows
add(["S" + "." * 7 + "T.", "." * 10])
add(board(6, 6, 0.25, (0, 0), (5, 5)))
add(board(8, 9, 0.35, (2, 3), (7, 0)))
add(board(12, 15, 0.35, (0, 0), (11, 14)))
add(put(board(10, 10, 0.0, (0, 0), (9, 9)), [(7, 8), (8, 7)], "#"))   # T cannot be reached
add(snake(40, 30))
add(board(100, 100, 0.3, (2, 1), (99, 99)))
add(board(300, 400, 0.4, (150, 0), (0, 399)))
# hidden: large
R = C = 1000
add(board(R, C, 0.0, (0, 0), (R - 1, C - 1)))                  # open board, opposite corners
add(board(R, C, 0.0, (500, 500), (500, 501)))                  # neighbours, but not a knight move
add(board(R, C, 0.3, (0, 0), (R - 1, C - 1)))
add(board(R, C, 0.5, (R - 1, 0), (0, C - 1)))
add(board(R, C, 0.6, (0, 0), (R - 1, C - 1)))
add(put(board(R, C, 0.1, (0, 0), (R - 1, C - 1)),             # T is cut off: every knight move into it is damaged
        [(R - 2, C - 3), (R - 3, C - 2)], "#"))
add(snake(R, C))
add(snake(R, 997))
add(board(2, C, 0.0, (0, 0), (1, C - 2)))                     # a 2-row strip
add(board(R, 3, 0.05, (0, 1), (R - 1, 1)))
add(board(R, C, 0.0, (0, 0), (1, 1)))                          # 4 moves although the squares touch

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

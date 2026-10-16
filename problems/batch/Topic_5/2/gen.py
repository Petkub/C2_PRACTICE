# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(50202)
MAXR = MAXC = 1000
tests = []


def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(row) == c and all(ch in "0123456789#" for ch in row) for row in g)
    tests.append(f"{r} {c}\n" + "".join(row + "\n" for row in g))


def rnd(r, c, pblock, digits="0123456789"):
    g = []
    for _ in range(r):
        g.append("".join("#" if random.random() < pblock else random.choice(digits) for _ in range(c)))
    return g


def put(g, i, j, ch):
    g[i] = g[i][:j] + ch + g[i][j + 1:]


# samples
add(["3#21", "5196", "2#8#", "1403"])
add(["12#", "3#4", "#56"])
add(["7"])
add(["#5", "55"])
add(["9", "0", "9"])
add(["1#99", "1#99", "1111"])
# hidden: small (the brute force checks these)
add(["5", "#", "5"])
add(["123456789"])
g = rnd(6, 7, 0.2); put(g, 0, 0, "3"); put(g, 5, 6, "4"); add(g)
g = rnd(9, 9, 0.25); put(g, 0, 0, "1"); put(g, 8, 8, "1"); add(g)
g = rnd(11, 12, 0.15); put(g, 0, 0, "0"); put(g, 10, 11, "9"); add(g)
add(["0" * 6 + "#" + "9" * 5] * 11 + ["0" * 6 + "#" + "9" * 5])   # unreachable
add(["1" * 12] * 12)
g = ["0" * 5 + "#" + "9" * 6 for _ in range(11)] + ["0" * 12]  # the 9s cannot be reached
add(g)


def wall(r, c, col, gap):
    """column col is blocked except in row gap; the part right of it is full of 9s"""
    g = []
    for i in range(r):
        left = "".join(random.choice("01") for _ in range(col))
        mid = "0" if i == gap else "#"
        right = "9" * (c - col - 1)
        g.append(left + mid + right)
    return g


# hidden: large
add(rnd(MAXR, MAXC, 0.0))
add(["9" * MAXC] * MAXR)
g = rnd(MAXR, MAXC, 0.2); put(g, 0, 0, "5"); put(g, MAXR - 1, MAXC - 1, "5"); add(g)
g = rnd(MAXR, MAXC, 0.25); put(g, 0, 0, "5"); put(g, MAXR - 1, MAXC - 1, "5"); add(g)
g = rnd(MAXR, MAXC, 0.4); put(g, 0, 0, "5"); put(g, MAXR - 1, MAXC - 1, "5"); add(g)   # most likely -1
add(wall(MAXR, MAXC, 500, MAXR - 1))       # pass along the last row only
g = wall(MAXR, MAXC, 500, MAXR - 1); put(g, MAXR - 1, 500, "#"); add(g)   # no way at all
g = wall(MAXR, MAXC, 300, 0); add(g)       # the gap is on the first row
g = rnd(MAXR, MAXC, 0.05); put(g, MAXR - 1, MAXC - 1, "#"); add(g)
g = rnd(MAXR, MAXC, 0.05); put(g, 0, 0, "#"); add(g)
g = []                                     # a narrow open band along the diagonal
for i in range(MAXR):
    g.append("".join(random.choice("123456789") if abs(i - j) <= 2 else "#" for j in range(MAXC)))
add(g)
g = []                                     # wide band, everything outside is blocked
for i in range(MAXR):
    g.append("".join(random.choice("0123456789") if abs(i - j) <= 40 else "#" for j in range(MAXC)))
add(g)
add(rnd(1, MAXC, 0.0))
add([random.choice("0123456789") for _ in range(MAXR)])
add(rnd(MAXR, MAXC, 0.1, "09"))

for t in tests:
    assert t.endswith("\n")
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

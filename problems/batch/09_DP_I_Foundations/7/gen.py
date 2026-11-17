# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60001)
MAXR = MAXC = 1000
tests = []


def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXR and 1 <= c <= MAXC
    assert all(len(row) == c and set(row) <= set(".*#") for row in g)
    tests.append(f"{r} {c}\n" + "".join(row + "\n" for row in g))


def rnd(r, c, rock, star):
    g = []
    for _ in range(r):
        row = []
        for _ in range(c):
            x = random.random()
            row.append("#" if x < rock else "*" if x < rock + star else ".")
        g.append("".join(row))
    return g


def put(g, i, j, ch):
    g[i] = g[i][:j] + ch + g[i][j + 1:]


def clear_ends(g):
    put(g, 0, 0, ".")
    put(g, len(g) - 1, len(g[0]) - 1, ".")
    return g


add(["..*.", ".#..", "...."])
add([".#*", "..."])
add(["*..", "...", "..."])
add(["#"])
add(["...#....", ".*....#.", "..#.*...", "#.......", "...*..#."])
add(["."] * 3 + ["*"] + ["."] * 2)

add(["*"])
add(["."])
add(["...."])
add(["..*.", "....", "...#"])
add(clear_ends(rnd(8, 9, 0.2, 0.05)))
add(clear_ends(rnd(12, 12, 0.1, 0.02)))
add(clear_ends(rnd(13, 14, 0.05, 0.0)))
g = ["." * 14 for _ in range(14)]
put(g, 13, 13, "*")
add(g)
add(clear_ends(rnd(14, 13, 0.0, 0.3)))
add(rnd(10, 10, 0.0, 1.0))

R = C = 1000


def blank(r, c):
    return ["." * c for _ in range(r)]


g = blank(R, C)
put(g, 500, 500, "*")
add(g)
g = blank(R, C)
put(g, 0, 0, "*")
add(g)
add(rnd(R, C, 0.0, 1.0))
add(clear_ends(rnd(R, C, 0.1, 0.0001)))
add(clear_ends(rnd(R, C, 0.25, 0.001)))
add(clear_ends(rnd(R, C, 0.05, 0.05)))
add(clear_ends(rnd(R, C, 0.1, 0.0)))
g = clear_ends(rnd(R, C, 0.02, 0.0))
put(g, R - 1, C - 1, "*")
add(g)
g = blank(R, C)
for i in range(R):
    if i % 97 != 0:
        put(g, i, C - 1 - i, "#")
for k in range(30):
    put(g, random.randrange(R), random.randrange(C), "*")
add(clear_ends(g))
g = blank(R, C)
put(g, 0, 0, "#")
put(g, 3, 3, "*")
add(g)
add(["*" if i == 700 else "." for i in range(R)])
add([".." * 300 + "*" + "." * 399])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

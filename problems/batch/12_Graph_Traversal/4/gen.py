# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(12005)
MAXN = 1000
tests = []


def add(a, b, rows):
    r, c = len(rows), len(rows[0])
    assert 1 <= r <= MAXN and 1 <= c <= MAXN
    assert 0 <= a <= 1000 and 0 <= b <= 1000 and a + b >= 1
    assert all(len(x) == c and set(x) <= set(".#") for x in rows)
    assert rows[0][0] == "."
    tests.append(f"{r} {c} {a} {b}\n" + "".join(x + "\n" for x in rows))


def rand_grid(r, c, pwater):
    g = ["".join("#" if random.random() < pwater else "." for _ in range(c)) for _ in range(r)]
    return ["." + g[0][1:]] + g[1:]


def serpentine(r, c, a, b, pwater=0.0):
    t = max(a, b)
    w = a + b + 1
    h = a + b + 1
    g = [[("#" if random.random() < pwater else ".") for _ in range(c)] for _ in range(r)]
    x, k = w, 0
    while x < c:
        rows = range(0, r - h) if k % 2 == 0 else range(h, r)
        for i in rows:
            for j in range(x, min(c, x + t)):
                g[i][j] = "#"
        x += t + w
        k += 1
    g[0][0] = "."
    return ["".join(row) for row in g]


add(1, 2, ["...", "...", "..#"])
add(0, 1, ["...", ".#.", "..."])
add(1, 2, ["....", ".#..", "...."])
add(2, 1, ["..", ".."])
add(2, 3, ["..#..", ".....", "#..#.", ".....", "..#.."])
add(3, 1, ["......", ".##...", "......", "...#..", "......"])

add(1, 2, ["."])
add(0, 1, ["....."])
add(2, 2, ["....."] * 5)
add(5, 1, ["..."] * 3)
add(3, 0, rand_grid(7, 7, 0.15))
add(1, 1, rand_grid(8, 9, 0.2))
add(1, 2, rand_grid(10, 10, 0.2))
add(4, 4, rand_grid(12, 15, 0.1))
add(2, 3, rand_grid(30, 30, 0.25))
add(0, 2, rand_grid(50, 50, 0.2))
g = rand_grid(300, 300, 0.1)
g = [list(x) for x in g]
for i, j in ((1, 2), (2, 1)):
    g[i][j] = "#"
add(1, 2, ["".join(x) for x in g])
add(1, 2, rand_grid(200, 200, 0.3))

R = C = MAXN
add(1, 2, serpentine(R, C, 1, 2))
add(2, 1, serpentine(R, C, 2, 1, 0.05))
add(0, 1, serpentine(R, C, 0, 1))
add(1, 1, serpentine(R, C, 1, 1))
add(3, 0, serpentine(R, C, 3, 0))
add(2, 2, serpentine(R, C, 2, 2))
add(1, 3, serpentine(R, C, 1, 3))
add(5, 2, serpentine(R, C, 5, 2, 0.04))
add(1, 2, serpentine(R, C - 1, 1, 2, 0.1))
add(0, 2, serpentine(R, C, 0, 2))
add(4, 3, serpentine(R, C, 4, 3, 0.03))
add(2, 3, serpentine(R, C, 2, 3, 0.03))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

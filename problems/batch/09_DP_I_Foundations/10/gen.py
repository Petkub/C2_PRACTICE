# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90010)
MAXS = 300
MAXG = 10 ** 6
tests = []


def add(e, t, g):
    r, c = len(t), len(t[0])
    assert 1 <= r <= MAXS and 1 <= c <= MAXS and 1 <= e <= MAXS
    assert all(len(row) == c and set(row) <= set(".#A") for row in t) and t[0][0] == "."
    assert len(g) == r and all(len(row) == c and min(row) >= 0 and max(row) <= MAXG for row in g)
    tests.append(f"{r} {c} {e}\n" + "".join(row + "\n" for row in t)
                 + "".join(" ".join(map(str, row)) + "\n" for row in g))


def grid(r, c, p_stone, p_anvil):
    t = []
    for i in range(r):
        row = random.choices(".#A", [1 - p_stone - p_anvil, p_stone, p_anvil], k=c)
        t.append(row)
    t[0][0] = "."
    return ["".join(row) for row in t]


def ore(t, lo_dot, hi_dot, lo_st, hi_st):
    return [[random.randint(lo_st, hi_st) if ch == "#" else random.randint(lo_dot, hi_dot) for ch in row]
            for row in t]


def carve(t, e):
    t = [list(row) for row in t]
    r, c = len(t), len(t[0])
    moves = ["D"] * (r - 1) + ["R"] * (c - 1)
    random.shuffle(moves)
    i = j = 0
    d = e
    for m in moves:
        if m == "D":
            i += 1
        else:
            j += 1
        if t[i][j] == "#":
            if d == 0:
                t[i][j] = "."
            else:
                d -= 1
        elif t[i][j] == "A":
            d = e
    return ["".join(row) for row in t]


def ore_case(r, c, e, p_stone, p_anvil, paths=3):
    t = grid(r, c, p_stone, p_anvil)
    for _ in range(paths):
        t = carve(t, e)
    add(e, t, ore(t, 0, MAXG // 5, MAXG // 3, MAXG))


def banded(r, c, e, thick):
    t = [list(row) for row in grid(r, c, 0.3, 0.01)]
    k = r // 2
    for i in range(k, min(r, k + thick)):
        t[i] = ["#"] * c
    t = ["".join(row) for row in t]
    add(e, t, ore(t, 0, 1000, 0, MAXG))


add(1, ["..#A#", "#.#.#", ".##.#", "...AA"],
    [[2, 4, 18, 9, 27], [0, 2, 9, 6, 21], [0, 6, 24, 6, 3], [9, 6, 2, 5, 8]])
add(1, [".##", "##."], [[1, 5, 5], [5, 5, 1]])
add(5, [".#.#", "#.#.", ".#.#"], [[3, 9, 1, 8], [7, 2, 6, 1], [1, 9, 4, 5]])
add(3, ["."], [[42]])
add(2, ["..#A", "####", ".#.."], [[0, 4, 21, 4], [9, 27, 15, 21], [5, 15, 1, 3]])

add(1, [".A.##", ".##A.", ".#.##", "AA##A"],
    [[9, 3, 4, 12, 3], [8, 9, 18, 7, 1], [3, 15, 4, 15, 27], [3, 0, 6, 18, 9]])
for r, c, e, ps, pa in [(1, 6, 2, 0.5, 0.0), (6, 1, 1, 0.3, 0.2), (2, 2, 1, 0.9, 0.0), (5, 6, 1, 0.5, 0.1),
                        (7, 7, 2, 0.6, 0.08), (8, 9, 3, 0.7, 0.05), (10, 12, 1, 0.4, 0.05), (11, 11, 4, 0.8, 0.03)]:
    ore_case(r, c, e, ps, pa)
add(1, [".#", "#."], [[1, 2], [3, 4]])

ore_case(40, 60, 3, 0.5, 0.02)
banded(30, 30, 2, 3)

ore_case(300, 300, 1, 0.5, 0.01)
ore_case(300, 300, 2, 0.45, 0.005)
ore_case(300, 300, 5, 0.6, 0.004)
ore_case(300, 300, 12, 0.7, 0.002)
ore_case(300, 300, 300, 0.9, 0.0)
ore_case(300, 300, 40, 0.85, 0.001)
ore_case(300, 300, 3, 0.35, 0.02)
ore_case(300, 250, 8, 0.65, 0.003)
banded(300, 300, 4, 5)
banded(300, 300, 5, 5)
add(300, ["." * 300 for _ in range(300)], [[MAXG] * 300 for _ in range(300)])
t = ["." + "#" * 299] + ["#" * 300 for _ in range(299)]
add(300, t, [[MAXG] * 300 for _ in range(300)])
t = [list(row) for row in grid(300, 300, 0.75, 0.0)]
for i in range(0, 300, 30):
    t[i] = ["A"] * 300
t[0][0] = "."
t = carve(["".join(row) for row in t], 6)
add(6, t, ore(t, 0, 10, MAXG // 2, MAXG))
ore_case(150, 300, 2, 0.55, 0.01)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

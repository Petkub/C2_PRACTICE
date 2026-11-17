# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11018)
MAXS = 1500
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(grid):
    R, C = len(grid), len(grid[0])
    assert 1 <= R <= MAXS and 1 <= C <= MAXS
    assert all(len(row) == C and set(row) <= set(".#") for row in grid)
    tests.append(f"{R} {C}\n" + "\n".join(grid) + "\n")


def dense(R, C, p):
    cells = random.choices(".#", weights=[1 - p, p], k=R * C)
    return ["".join(cells[r * C:(r + 1) * C]) for r in range(R)]


def sparse(R, C, cells):
    g = [["."] * C for _ in range(R)]
    for r, c in cells:
        g[r][c] = "#"
    return ["".join(row) for row in g]


def perm(R, C, k):
    rows = sorted(random.sample(range(R), k))
    cols = random.sample(range(C), k)
    return list(zip(rows, cols))


def rcells(R, C, k):
    s = set()
    while len(s) < k:
        s.add((ri(0, R - 1), ri(0, C - 1)))
    return sorted(s)


add(["#..", "...", "..#"])
add(["##", "##"])
add(["#.#.#"])
add([".#..", "#...", "...#", "..#."])
add(["#"])
add(["#..#", "....", ".#.."])

add(["."])
add(["..", ".."])
add(sparse(6, 7, [(i, i) for i in range(6)]))
add(sparse(8, 8, perm(8, 8, 6)))
add(sparse(10, 9, perm(10, 9, 9)))
add(dense(12, 12, 0.05))
add(sparse(9, 9, [(8 - i, i) for i in range(9)]))

add(dense(150, 170, 0.002))
add(sparse(200, 200, [(i * 10 + 3, (i * 37) % 200) for i in range(20)]))

M = MAXS


core = [(M // 2, M - 1), (M - 1, M // 2), (M - 1, M - 1)]
add(sparse(M, M, [(0, 0), (M // 4, M // 4)] + core))
add(sparse(M, M, [(i * 70, i * 70 + 7) for i in range(10)] + core))
add(sparse(M, M, [(i, i) for i in range(M // 2)] + core))
add(sparse(M, M, [(299 - i, i) for i in range(0, 300, 3)] + core))
add(sparse(M, M, rcells(M // 2, M // 2, 25) + core))
add(sparse(M, M, perm(400, 400, 300) + core))
add(sparse(M, M, perm(300, 300, 300) + core))
add(sparse(M, M, perm(M // 2, M // 2, 8) + core))
add(sparse(M, M, [(ri(0, M // 2 - 1), ri(0, M // 2 - 1)) for _ in range(5)] + [(0, M // 2 - 1), (M // 2 - 1, 0)] + core))
add(sparse(M, 1000, [(i * 3, i) for i in range(500)]))
add(sparse(M, M, core + [(r, c) for r, c in perm(M // 6, M // 6, 30)]))
add(dense(M, 1000, 0.3))
add(sparse(M, M, [(i * 60, (i * 7919) % (M // 2)) for i in range(12)] + core))
add(sparse(M, M, core))
add(sparse(M, M, [(M // 3, M - 1), (M - 1, 2 * M // 3), (M - 1, M - 1), (M - 1, M - 3)]))

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

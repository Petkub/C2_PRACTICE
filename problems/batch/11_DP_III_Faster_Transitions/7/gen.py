# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11007)
MAXS = 1500
tests = []


def add(K, grid):
    R, C = len(grid), len(grid[0])
    assert 1 <= R <= MAXS and 1 <= C <= MAXS and 1 <= K <= MAXS
    assert all(len(row) == C and set(row) <= set(".#") for row in grid)
    assert grid[0][0] == "." and grid[-1][-1] == "."
    tests.append(f"{R} {C} {K}\n" + "\n".join(grid) + "\n")


def rgrid(R, C, p):
    """each cell is a rock with probability p (start and end kept free)"""
    cells = random.choices(".#", weights=[1 - p, p], k=R * C)
    cells[0] = cells[-1] = "."
    return ["".join(cells[r * C:(r + 1) * C]) for r in range(R)]


def free(R, C):
    return ["." * C] * R


# samples
add(2, ["....", ".#..", "....", "...."])
add(1, ["...", "...", "..."])
add(3, ["....", ".#..", "...."])
add(2, [".....", ".....", "..#..", ".....", "....."])
add(5, [".#.", "#.#", ".#."])
add(3, ["." * 6] * 5)
# hidden: small
add(1, ["."])
add(4, ["." * 7])
add(1, free(7, 7))
add(1, free(6, 7))
add(3, rgrid(8, 9, 0.2))
add(10, rgrid(10, 10, 0.1))
add(2, rgrid(12, 7, 0.3))
add(4, ["." + "#" * 9] + ["#" * 10] * 2 + ["#" * 9 + "."])
# hidden: medium
add(20, rgrid(80, 90, 0.15))
add(100, rgrid(100, 100, 0.05))
# hidden: maximum size
M = MAXS
add(M, free(M, M))
add(M // 2, free(M, M))
add(1, free(M, M))                                  # one path: the diagonal
add(2, free(M, M - 1))
add(700, rgrid(M, M, 0.1))
add(M, rgrid(M, M, 0.4))
add(1000, rgrid(M, M, 0.02))
add(M - 1, rgrid(M - 1, M, 0.2))
wall = [["."] * M for _ in range(M)]
for r in range(M):
    for c in range(M):
        if abs((r - c) - 3) <= 1 and 5 < r < M - 5:
            wall[r][c] = "#"
add(3, ["".join(row) for row in wall])              # rocks along a diagonal band
add(999, rgrid(M, 1000, 0.25))

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11007)
MAXS = 3000
MAXM = 200000
tests = []


def add(R, C, K, rocks):
    assert 1 <= R <= MAXS and 1 <= C <= MAXS and 1 <= K <= MAXS
    assert 0 <= len(rocks) <= MAXM and len(set(rocks)) == len(rocks)
    assert all(1 <= r <= R and 1 <= c <= C for r, c in rocks)
    assert (1, 1) not in rocks and (R, C) not in rocks
    lines = [f"{R} {C} {K} {len(rocks)}"] + [f"{r} {c}" for r, c in rocks]
    tests.append("\n".join(lines) + "\n")


def from_grid(K, grid):
    R, C = len(grid), len(grid[0])
    assert all(len(row) == C and set(row) <= set(".#") for row in grid)
    add(R, C, K, [(r + 1, c + 1) for r in range(R) for c in range(C) if grid[r][c] == "#"])


def rand_p(R, C, K, p):
    rocks = [(r, c) for r in range(1, R + 1) for c in range(1, C + 1)
             if random.random() < p and (r, c) != (1, 1) and (r, c) != (R, C)]
    random.shuffle(rocks)
    add(R, C, K, rocks)


def rand_m(R, C, K, M):
    cells = random.sample(range(1, R * C - 1), M)
    add(R, C, K, [(x // C + 1, x % C + 1) for x in cells])


from_grid(2, ["....", ".#..", "....", "...."])
from_grid(1, ["...", "...", "..."])
from_grid(3, ["....", ".#..", "...."])
from_grid(2, [".....", ".....", "..#..", ".....", "....."])
from_grid(5, [".#.", "#.#", ".#."])
from_grid(3, ["." * 6] * 5)

add(1, 1, 1, [])
add(1, 7, 4, [])
rand_p(50, 60, 8, 0.2)
rand_p(8, 9, 3, 0.2)
rand_p(10, 10, 10, 0.1)
rand_p(12, 7, 2, 0.3)
add(4, 10, 4, [(1, c) for c in range(2, 11)] + [(r, c) for r in (2, 3) for c in range(1, 11)]
    + [(4, c) for c in range(1, 10)])
add(300, 300, 1, [])
add(300, 299, 2, [])
add(300, 300, 3, [(r + 1, c + 1) for r in range(300) for c in range(300)
                  if abs((r - c) - 3) <= 1 and 5 < r < 295])

rand_p(80, 90, 20, 0.15)
rand_p(400, 400, 150, 0.35)
rand_p(500, 450, 60, 0.6)

M = MAXS
add(M, M, M, [])
add(M, M, M // 2, [])
add(M, M - 1, 2400, [])
rand_m(M, M, 2000, MAXM)
rand_m(M, M, 1500, 100000)
rand_m(M, M, M, MAXM)
rand_m(M - 1, M, M - 1, MAXM)
rand_m(M, M, 1800, 50000)
add(M, M, 2500, [(r, c) for r in range(1301, 1701) for c in range(1201, 1701)])
add(M, M, 1700, [(r, c) for r in range(2, M, 2) for c in range((50 - r % 50) % 50 or 50, M + 1, 50)])

rand_m(M, M, 1000, MAXM)

for t in tests:
    assert t.endswith("\n") and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

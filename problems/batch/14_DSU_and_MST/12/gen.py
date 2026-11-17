# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(91201)
MAXRC, MAXK = 1000, 300_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(R, C, cells):
    k = len(cells)
    assert 1 <= R <= MAXRC and 1 <= C <= MAXRC and 1 <= k <= min(R * C, MAXK)
    assert all(1 <= r <= R and 1 <= c <= C for (r, c) in cells)
    assert len(set(cells)) == k
    tests.append(f"{R} {C} {k}\n" + "".join(f"{r} {c}\n" for (r, c) in cells))


def all_cells(R, C):
    return [(r, c) for r in range(1, R + 1) for c in range(1, C + 1)]


def rnd(R, C, k):
    cells = all_cells(R, C)
    random.shuffle(cells)
    return cells[:k]


def snake(R, C):
    path = []
    for i, r in enumerate(range(1, R + 1, 2)):
        cols = range(1, C + 1) if i % 2 == 0 else range(C, 0, -1)
        path += [(r, c) for c in cols]
        if r + 1 <= R:
            path.append((r + 1, C if i % 2 == 0 else 1))
    return path


def without_row(R, C, k, row):
    cells = [(r, c) for (r, c) in all_cells(R, C) if r != row]
    random.shuffle(cells)
    return cells[:k]


add(3, 3, [(1, 2), (3, 3), (2, 1), (2, 2), (3, 2), (1, 1)])
add(2, 2, [(1, 1), (2, 2)])
add(1, 4, [(1, 3), (1, 1)])
add(4, 3, [(4, 1), (3, 1), (1, 3), (2, 2), (2, 3), (3, 2)])
add(3, 4, [(2, 4), (1, 1), (3, 4), (1, 4), (2, 2)])

add(1, 1, [(1, 1)])
add(5, 1, [(2, 1), (5, 1), (1, 1), (4, 1), (3, 1)])
add(4, 4, rnd(4, 4, 16))
add(6, 7, rnd(6, 7, 30))
add(20, 20, rnd(20, 20, 400))
p = snake(25, 9)
add(25, 9, p[1:] + p[:1])
add(50, 60, without_row(50, 60, 2500, 25))
add(300, 200, rnd(300, 200, 30000))
cells = [(r, c) for r in range(1, 1001) for c in (1, 2, 3)]
cells = [x for x in cells if x[0] != 500] + [(500, 2)]
add(1000, 3, cells)

add(500, 600, rnd(500, 600, MAXK))
cells = [(r, c) for r in range(1, 301) for c in range(1, 1001)]
random.shuffle(cells)
add(1000, 1000, cells)
p = snake(999, 598)
assert len(p) <= MAXK
add(999, 598, p)
p = snake(999, 598)
random.shuffle(p)
add(999, 598, p)
p = snake(999, 598)
add(999, 598, p[-1:] + p[:-1][::-1])
add(600, 500, without_row(600, 500, MAXK - 500, 599))
cells = [(r, c) for (r, c) in all_cells(600, 500) if (r + c) % 2 == 0]
random.shuffle(cells)
rest = [(r, c) for (r, c) in all_cells(600, 500) if (r + c) % 2 == 1 and r < 600]
random.shuffle(rest)
add(600, 500, cells + rest)
add(1000, 1, [(r, 1) for r in range(1000, 0, -1)])
add(1, 1000, rnd(1, 1000, 1000))
add(1000, 300, rnd(1000, 300, MAXK))
cells = [(r, c) for (r, c) in all_cells(1000, 300) if r != 500]
random.shuffle(cells)
row = [(500, c) for c in range(1, 301)]
random.shuffle(row)
add(1000, 300, cells + row)
add(700, 420, rnd(700, 420, 700 * 420))
cells = [(r, c) for r in range(1, 1001) for c in range(1, 151)]
random.shuffle(cells)
cells = cells[:MAXK - 1000] + [(r, 1000) for r in range(1, 1001)]
add(1000, 1000, cells)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

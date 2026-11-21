# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(490001)
MAXN = 1000
MAXU = 100000
tests = []


def add(g, ups):
    n = len(g)
    assert 1 <= n <= MAXN and 0 <= len(ups) <= MAXU
    assert all(len(row) == n and set(row) <= set("#.") for row in g)
    assert all(1 <= r <= n and 1 <= c <= n for r, c in ups)
    tests.append(f"{n} {len(ups)}\n" + "".join(row + "\n" for row in g) + "".join(f"{r} {c}\n" for r, c in ups))


def grid(n, p):
    return ["".join("#" if random.random() < p else "." for _ in range(n)) for _ in range(n)]


def symmetric(n, p):
    g = [["."] * n for _ in range(n)]
    for r in range((n + 1) // 2):
        for c in range(r, (n + 1) // 2):
            ch = "#" if random.random() < p else "."
            for a, b in ((r, c), (c, r)):
                for x, y in ((a, b), (a, n - 1 - b), (n - 1 - a, b), (n - 1 - a, n - 1 - b)):
                    g[x][y] = ch
    return ["".join(row) for row in g]


def ups_random(n, u):
    return [(random.randint(1, n), random.randint(1, n)) for _ in range(u)]


def ups_lines(n, u):
    out = []
    m = (n + 1) // 2
    for _ in range(u):
        i = random.randint(1, n)
        out.append(random.choice([(i, i), (i, n + 1 - i), (m, i), (i, m)]))
    return out


add([".#..", "#..#", "...#", ".##."], [(1, 3), (3, 1)])
add(["##..##", "###.#.", "..##..", "..###.", ".#..##", "##...#"], [(6, 5), (2, 3)])
add(["#"], [(1, 1), (1, 1)])
add([".#...", "#....", ".....", "....#", "...#."], [(1, 4)])
add(["###..#", "..#..#", "#####.", "..####", "..##..", "#..###"], [])

add(["."], [])
add(grid(2, 0.5), ups_random(2, 6))
add(grid(3, 0.5), ups_random(3, 12))
add(grid(5, 0.4), ups_lines(5, 15))
add(grid(7, 0.6), ups_random(7, 20))
add(grid(8, 0.5), ups_lines(8, 20))
add(symmetric(9, 0.5), ups_lines(9, 20))
add(grid(60, 0.5), ups_random(60, 2000))
add(grid(61, 0.3), ups_lines(61, 2000))

add(grid(1000, 0.5), ups_random(1000, MAXU))
add(grid(999, 0.5), ups_random(999, MAXU))
add(["#" * 1000] * 1000, ups_random(1000, MAXU))
add(["." * 999] * 999, ups_lines(999, MAXU))
add(symmetric(1000, 0.5), ups_lines(1000, MAXU))
add(symmetric(997, 0.3), ups_lines(997, MAXU))
add(grid(998, 0.1), ups_lines(998, MAXU))
add(grid(1000, 0.9), [(500, 501)] * MAXU)
add(grid(999, 0.5), ups_lines(999, MAXU))
add(symmetric(1000, 0.7), ups_random(1000, MAXU))
add(grid(1000, 0.5), [(1, 1)] * (MAXU // 2) + ups_lines(1000, MAXU // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

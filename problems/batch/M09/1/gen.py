# Test generator of this problem (the judge runs it to rebuild the big tests).
import math, os, random

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


def target(n, width, p):
    lit = [random.random() < p for _ in range(n + 2)]
    h = (n - 1) / 2
    return ["".join("#" if lit[int(math.sqrt((r - h) ** 2 + (c - h) ** 2) / width)] else "." for c in range(n))
            for r in range(n)]


def frames(n, p):
    lit = [random.random() < p for _ in range(n + 1)]
    return ["".join("#" if lit[max(abs(2 * r - n + 1), abs(2 * c - n + 1))] else "." for c in range(n))
            for r in range(n)]


def noise(g, p):
    flip = {"#": ".", ".": "#"}
    return ["".join(flip[ch] if random.random() < p else ch for ch in row) for row in g]


def ups_random(n, u):
    return [(random.randint(1, n), random.randint(1, n)) for _ in range(u)]


def ups_box(n, u, r0, c0, h):
    assert 1 <= r0 and r0 + h - 1 <= n and 1 <= c0 and c0 + h - 1 <= n
    return [(random.randint(r0, r0 + h - 1), random.randint(c0, c0 + h - 1)) for _ in range(u)]


def ups_walk(n, u):
    r, c, out = random.randint(1, n), random.randint(1, n), []
    for _ in range(u):
        r = min(n, max(1, r + random.randint(-1, 1)))
        c = min(n, max(1, c + random.randint(-1, 1)))
        out.append((r, c))
    return out


add([".#..", "#..#", "...#", ".##."], [(1, 3), (3, 1)])
add(["##..##", "###.#.", "..##..", "..###.", ".#..##", "##...#"], [(6, 5), (2, 3)])
add(["#"], [(1, 1), (1, 1)])
add([".#...", "#....", ".....", "....#", "...#."], [(1, 4)])
add(["###..#", "..#..#", "#####.", "..####", "..##..", "#..###"], [])

add(["."], [])
add(grid(2, 0.5), ups_random(2, 6))
add(grid(3, 0.5), ups_box(3, 12, 1, 1, 3))
add(grid(5, 0.4), ups_walk(5, 15))
add(grid(7, 0.6), ups_random(7, 20))
add(frames(8, 0.5), ups_walk(8, 20))
add(target(9, 1, 0.5), ups_box(9, 20, 3, 3, 3))
add(grid(60, 0.5), ups_random(60, 2000))
add(noise(target(61, 3, 0.5), 0.05), ups_box(61, 2000, 26, 26, 10))

add(grid(1000, 0.5), ups_random(1000, MAXU))
add(grid(999, 0.5), ups_random(999, MAXU))
add(["#" * 1000] * 1000, ups_random(1000, MAXU))
add(["." * 999] * 999, ups_box(999, MAXU, 490, 490, 21))
add(target(1000, 1, 0.5), ups_walk(1000, MAXU))
add(noise(frames(997, 0.3), 0.01), ups_box(997, MAXU, 480, 480, 39))
add(grid(998, 0.1), ups_walk(998, MAXU))
add(grid(1000, 0.9), [(500, 501)] * MAXU)
add(noise(target(999, 7, 0.5), 0.002), ups_box(999, MAXU, 1, 900, 100))
add(target(1000, 2, 0.7), ups_random(1000, MAXU))
add(grid(1000, 0.5), [(1, 1)] * (MAXU // 2) + ups_walk(1000, MAXU // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

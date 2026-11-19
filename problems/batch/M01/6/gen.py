# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4106)
MAXH, MAXW, MAXQ, MAXA, MAXP = 500, 500, 100000, 100000, 100000
tests = []


def add(grid, qs):
    h, w = len(grid), len(grid[0])
    assert 1 <= h <= MAXH and 1 <= w <= MAXW and 1 <= len(qs) <= MAXQ
    assert all(len(row) == w and all(0 <= x <= MAXA for x in row) for row in grid)
    assert all(1 <= r <= h and 1 <= c <= w and 1 <= p <= MAXP for r, c, p in qs)
    out = [f"{h} {w} {len(qs)}"]
    out += [" ".join(map(str, row)) for row in grid]
    out += [f"{r} {c} {p}" for r, c, p in qs]
    tests.append("\n".join(out) + "\n")


def rnd_grid(h, w, lo, hi):
    return [[random.randint(lo, hi) for _ in range(w)] for _ in range(h)]


def rnd_q(h, w, q, lo, hi):
    return [(random.randint(1, h), random.randint(1, w), random.randint(lo, hi)) for _ in range(q)]


def snake(h, w):
    g = [[random.randint(90000, MAXA) for _ in range(w)] for _ in range(h)]
    path = []
    for r in range(0, h, 2):
        for c in range(w):
            g[r][c] = random.randint(0, 999)
            path.append((r, c))
        if r + 1 < h:
            c = w - 1 if (r // 2) % 2 == 0 else 0
            g[r + 1][c] = random.randint(0, 999)
            path.append((r + 1, c))
    return g, path


def path_q(path, q, lo, hi):
    out = []
    for _ in range(q):
        r, c = random.choice(path)
        out.append((r + 1, c + 1, random.randint(lo, hi)))
    return out


add([[6, 12, 4, 16, 2],
     [10, 2, 8, 18, 4],
     [14, 6, 4, 12, 10],
     [18, 16, 18, 2, 8]], [(2, 2, 9), (1, 5, 5), (2, 3, 7)])
add([[7]], [(1, 1, 6), (1, 1, 8)])
add([[4, 4, 4], [4, 4, 4], [4, 4, 4]], [(2, 2, 9), (3, 1, 100000)])
add([[10, 20, 30, 40], [45, 35, 25, 15]], [(1, 1, 33), (2, 4, 33), (1, 4, 50), (2, 2, 12)])
add([[0, 5, 0, 5], [0, 5, 0, 5], [0, 0, 0, 5], [5, 5, 5, 0]], [(1, 3, 3), (4, 4, 6), (4, 4, 1), (1, 2, 2)])

add([[0]], [(1, 1, 1)])
add([[MAXA] * 3], [(1, 2, MAXP), (1, 1, MAXP - 1)])
add(rnd_grid(4, 4, 0, 5), rnd_q(4, 4, 30, 1, 6))
add(rnd_grid(1, 40, 0, 9), rnd_q(1, 40, 50, 1, 10))
add(rnd_grid(30, 1, 0, 9), rnd_q(30, 1, 50, 1, 10))
add(rnd_grid(20, 25, 0, 100), rnd_q(20, 25, 300, 1, 101))
g, path = snake(31, 30)
add(g, path_q(path, 400, 1, MAXP))
add(rnd_grid(60, 60, 0, MAXA), rnd_q(60, 60, 2000, 1, MAXP))

H, W, Q = MAXH, MAXW, MAXQ
add(rnd_grid(H, W, 0, MAXA - 1), rnd_q(H, W, Q, 60000, MAXP))
add(rnd_grid(H, W, 0, 20), rnd_q(H, W, Q, 1, 21))
g, path = snake(H, W)
add(g, path_q(path, Q, 1000, 89999))
g, path = snake(H, W)
add(g, path_q(path, Q, 1, MAXP))
add([[7] * W for _ in range(H)], rnd_q(H, W, Q, 7, 8))
add([[(r + c) * 100 for c in range(W)] for r in range(H)], rnd_q(H, W, Q, 1, MAXP))
add(rnd_grid(H, W, 0, MAXA), [(random.randint(1, H), random.randint(1, W), MAXP) for _ in range(Q)])
g = rnd_grid(H, W, 0, 50)
for r in range(0, H, 50):
    for c in range(W):
        if c % 100 != 7:
            g[r][c] = random.randint(50000, 60000)
add(g, rnd_q(H, W, Q, 40, 70000))
add(rnd_grid(H, W, 0, 3), rnd_q(H, W, Q, 1, 4))
g = [[random.choice([0, MAXA]) if random.random() < 0.45 else random.randint(0, 9) for _ in range(W)] for _ in range(H)]
add(g, rnd_q(H, W, Q, 1, 10))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

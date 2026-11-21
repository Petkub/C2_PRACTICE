# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(130018)
MAXRC = 500
MAXK = 20000
MAXH = 10 ** 6
tests = []


def add(g, pumps):
    R, C, K = len(g), len(g[0]), len(pumps)
    assert 1 <= R <= MAXRC and 1 <= C <= MAXRC and 1 <= K <= MAXK
    for row in g:
        assert len(row) == C and all(-MAXH <= x <= MAXH for x in row)
    for r, c, p in pumps:
        assert 1 <= r <= R and 1 <= c <= C and -MAXH <= p <= 0
    lines = [f"{R} {C} {K}"] + [" ".join(map(str, row)) for row in g] + [f"{r} {c} {p}" for r, c, p in pumps]
    tests.append("\n".join(lines) + "\n")


def grid(R, C, f):
    return [[f(i, j) for j in range(C)] for i in range(R)]


def noise(n, lo, hi):
    pool = [random.randint(lo, hi) for _ in range(4096)]
    return [pool[random.getrandbits(12)] for _ in range(n)]


def rgrid(R, C, lo, hi):
    vals = noise(R * C, lo, hi)
    return [vals[i * C:(i + 1) * C] for i in range(R)]


def rpumps(g, K, plo=-MAXH, phi=0, wet=True):
    R, C = len(g), len(g[0])
    out = []
    while len(out) < K:
        r, c = random.randrange(R), random.randrange(C)
        if wet and g[r][c] >= 0 and random.random() < 0.9:
            continue
        out.append((r + 1, c + 1, random.randint(plo, phi)))
    return out


def series(r, c, top, bottom, cnt):
    return [(r, c, top - (top - bottom) * t // (cnt - 1)) for t in range(cnt)]


def dig(g, r, c, v):
    for i in range(r - 2, r + 1):
        for j in range(c - 2, c + 1):
            if 0 <= i < len(g) and 0 <= j < len(g[0]):
                g[i][j] = v


def clamp(x):
    return max(-MAXH, min(MAXH, x))


add([[-4, -6, -1, -5], [-3, -2, 3, -7]], [(1, 1, -5)])
add([[-9, -9, 2, -9, -9]], [(1, 1, -3), (1, 5, -12), (1, 2, -6)])
add([[0, 5, 1], [2, 0, 3]], [(1, 2, -4)])
add([[-5, -5, -5], [-5, 4, -5], [-5, -5, -8]], [(2, 2, -10), (3, 3, -1)])
add([[-1, -5, -9, -8, 0], [3, -8, -3, -8, -5], [-3, -8, -9, 1, -9], [-6, -6, -9, -2, -3]],
    [(4, 4, -8), (2, 3, -4), (1, 3, -4)])

add([[-7]], [(1, 1, 0)])
add([[-7]], [(1, 1, -MAXH)])
add([[-3, 5], [5, -4]], [(1, 1, -9)])
add(rgrid(5, 6, -9, 3), rpumps(rgrid(5, 6, -9, 3), 3, -10, 0, False))
g = rgrid(6, 6, -12, 2)
add(g, rpumps(g, 4, -15, 0))
g = rgrid(8, 7, -20, 5)
add(g, rpumps(g, 6, -25, 0))
g = grid(7, 7, lambda i, j: 3 if (i + j) % 4 == 0 else -6 - (i * j) % 5)
add(g, [(2, 2, -4), (6, 7, -9)])
g = rgrid(30, 40, -MAXH, MAXH // 3)
add(g, rpumps(g, 50))
g = grid(40, 40, lambda i, j: -30 + abs(i - 20) + abs(j - 20) + (7 if i == j or i + j == 39 else 0))
add(g, rpumps(g, 30, -40, 0))

N = MAXRC
low = noise(N * N, -MAXH, -600000)
high = noise(N * N, -600000, MAXH)
g = grid(N, N, lambda i, j: low[i * N + j] if random.random() < 0.7 else high[i * N + j])
dig(g, 250, 250, -MAXH)
add(g, series(250, 250, -50000, -590000, 800) + rpumps(g, MAXK - 800))
g = rgrid(N, N, -MAXH, -1)
dig(g, 100, 400, -MAXH)
add(g, series(100, 400, -1000, -290000, 800) + rpumps(g, MAXK - 800, -MAXH, -MAXH // 2))
base = noise(N * N, -MAXH, -MAXH + 50)
g = [base[i * N:(i + 1) * N] for i in range(N)]
add(g, [(random.randint(1, N), random.randint(1, N), -k * 40) for k in range(1, MAXK + 1)])
dn = noise(N * N, 0, 200)
g = grid(N, N, lambda i, j: 9 if (i + j) % 25 == 0 and (i // 25) % 3 else -500000 + (i * 997 + j * 131) % 1000 - dn[i * N + j])
add(g, series(2, 2, 0, -495000, 600) + rpumps(g, 5000, -MAXH, -100000))
dn = noise(N * N, -1000, 1000)
g = grid(N, N, lambda i, j: clamp(-MAXH + 3000 * (abs(i - 250) // 10 + abs(j - 250) // 10) + dn[i * N + j]))
add(g, series(251, 251, 0, -845000, 600) + rpumps(g, 8000))
dn = noise(N * N, -20, 20)
g = grid(N, N, lambda i, j: clamp((i + j) * 4000 - 2 * MAXH + 8000 + dn[i * N + j]))
add(g, series(1, 1, 0, -300000, 800)
    + [(random.randint(1, 200), random.randint(1, 200), random.randint(-MAXH, 0)) for _ in range(MAXK - 800)])
g = grid(N, N, lambda i, j: (5 if j % 4 == 1 and i != (0 if j % 8 == 1 else N - 1) else -MAXH + j * 3000 + i))
add(g, series(1, 1, 0, -990000, 1500) + [(random.randint(1, N), random.randint(1, N), 0) for _ in range(3500)])
dn = noise(N * N, -MAXH, -MAXH // 4)
g = grid(N, N, lambda i, j: 1 if (i - j) % 7 == 0 or (i + j) % 11 == 0 else dn[i * N + j])
add(g, series(4, 2, 0, -240000, 800) + rpumps(g, MAXK - 800))
dn = noise(N * N, -MAXH, MAXH // 10)
g = [dn[i * N:(i + 1) * N] for i in range(N)]
g[N // 2 - 1][N // 2 - 1] = -MAXH
add(g, series(N // 2, N // 2, 0, -MAXH, MAXK))
dn = noise(N * N, -MAXH, -MAXH // 2)
g = grid(N, N, lambda i, j: -(abs((i % 100) - 50) + abs((j % 100) - 50)) * 3000 - 100 if (i // 100 + j // 100) % 2 else dn[i * N + j])
add(g, series(51, 51, 0, -490000, 800) + rpumps(g, 9200, -MAXH, 0))
dn = noise(N * N, -MAXH, -1)
g = [dn[i * N:(i + 1) * N] for i in range(N)]
add(g, sorted(rpumps(g, MAXK), key=lambda t: -t[2]))
dn = noise(N * N, -MAXH, 300000)
g = [dn[i * N:(i + 1) * N] for i in range(N)]
dig(g, 300, 300, -MAXH)
add(g, series(300, 300, -1, -2000, 2000) + rpumps(g, MAXK - 2000, -2000, 0))

base = noise(N * N, -MAXH, -MAXH + 50)
g = [base[i * N:(i + 1) * N] for i in range(N)]
cups = []
for k in range(2 * (N // 3)):
    r = 1 if k % 2 == 0 else N - 2
    c = 3 * (k // 2) + 1
    b = -1000 * (k + 1)
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            g[i][j] = b
    g[r][c] = -MAXH
    cups.append((r + 1, c + 1, -MAXH + k))
add(g, cups + [(random.randint(1, N), random.randint(1, N), random.randint(-1000, 0)) for _ in range(5000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

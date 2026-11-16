# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180007)
MAXRC, MAXV = 600, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(d, g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXRC and 1 <= c <= MAXRC and 0 <= d <= MAXV
    assert all(len(row) == c and all(1 <= v <= MAXV for v in row) for row in g)
    t = f"{r} {c} {d}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd(r, c, lo, hi):
    return [[ri(lo, hi) for _ in range(c)] for _ in range(r)]


def slope(r, c, a, b, noise, base=1):
    """h = base + a*i + b*j + noise: every plot of size s has spread about (a + b)(s - 1)"""
    return [[base + a * i + b * j + ri(0, noise) for j in range(c)] for i in range(r)]


def plant(g, s, lo, hi):
    """a flat s x s plot with heights in [lo, hi] at a random place"""
    r, c = len(g), len(g[0])
    i0, j0 = ri(0, r - s), ri(0, c - s)
    for i in range(i0, i0 + s):
        for j in range(j0, j0 + s):
            g[i][j] = ri(lo, hi)
    return g


# samples
add(2, [[3, 4, 4, 9, 1], [5, 3, 4, 8, 2], [4, 4, 5, 7, 7], [4, 3, 4, 8, 6]])
add(0, [[7, 7, 7], [7, 7, 7], [7, 7, 7]])
add(0, [[1, 2, 3]])
add(1, [[1, 2, 1, 2], [3, 2, 1, 2], [2, 2, 2, 1], [9, 1, 2, 2], [1, 1, 1, 1]])
add(10**9 - 1, [[1, MAXV], [MAXV, 1]])
# hidden: small (the brute checks these)
add(3, rnd(8, 8, 1, 10))
add(0, rnd(1, 30, 1, 3))
add(5, rnd(30, 1, 1, 9))
add(20, slope(40, 50, 1, 2, 3))
add(4, plant(rnd(50, 60, 1, 1000), 12, 500, 504))
add(MAXV, rnd(45, 45, 1, MAXV))
# hidden: maximum size (heights kept short so the input stays <= 3 MB)
M = MAXRC
add(600, slope(M, M, 1, 1, 0))                                      # level squares of size 301
add(900, slope(M, M, 2, 1, 20))
add(5000, rnd(M, M, 1, 99_999))                                     # random: small squares
add(99_998, rnd(M, M, 1, 99_999))                                   # almost everything level
add(0, [[77_777] * M for _ in range(M)])                            # all equal: the whole field
add(10, plant(rnd(M, M, 1, 99_999), 450, 50_000, 50_010))
add(3, plant(slope(M, M, 0, 0, 5, 40_000), 1, 1, 1))               # nearly flat field with one hole
g = slope(M, M, 0, 0, 3, 40_000)
for _ in range(30):
    g[ri(0, M - 1)][ri(0, M - 1)] = 99_999                           # spikes cut the field
add(3, g)
add(1000, slope(M, 500, 3, 0, 100))                                 # R != C
add(200, slope(250, M, 0, 1, 10))
add(0, rnd(M, M, 1, 2))
add(250, slope(M, M, 1, 0, 50))                                     # level squares of size about 200
add(40, plant(slope(M, M, 0, 1, 30, 1000), 320, 2000, 2040))

def lattice(m, step, d):
    """a nearly flat field (spread <= d) with a spike or a pit every step rows and every step columns:
    the largest level plots fit between the spikes, and a plot is seen not level only when a scan reaches a spike"""
    g = [[40_000 + ri(0, d) for _ in range(m)] for _ in range(m)]
    oi, oj = ri(0, step - 1), ri(0, step - 1)
    for i in range(oi, m, step):
        for j in range(oj, m, step):
            g[i][j] = 99_999 if random.random() < 0.5 else 1
    return g


add(3, lattice(M, 100, 3))
add(5, lattice(M, 160, 5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

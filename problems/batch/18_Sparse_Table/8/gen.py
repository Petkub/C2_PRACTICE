# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180007)
MAXRC, MAXV = 1000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(d, g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXRC and 1 <= c <= MAXRC and 0 <= d <= MAXV
    assert all(len(row) == c and 1 <= min(row) and max(row) <= MAXV for row in g)
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
add(99_998, rnd(70, 80, 1, 99_999))                                 # almost everything level
add(0, [[77_777] * 90 for _ in range(90)])                          # all equal: the whole field
# hidden: medium size
add(5000, rnd(500, 500, 1, 99_999))                                 # random: small squares
g = rnd(500, 500, 1, 99_999)                                        # the only flat plot (size 200) is
for i in range(300, 500):                                           # in the bottom right corner
    for j in range(300, 500):
        g[i][j] = ri(60_000, 60_100)
add(100, g)
g = [[7] * 700 for _ in range(700)]                                 # all equal but one pit in the middle
g[350 + ri(-3, 3)][350 + ri(-3, 3)] = 6
add(0, g)


# hidden: maximum size (heights kept short so the input stays <= 3 MB)
def tilt(r, c, a, b, p, noise=0):
    """h = 1 + (a i + b j + shift) // p (+ a random 0 or 1): heights rise steadily in one direction"""
    shift = max(0, -a * (r - 1)) + max(0, -b * (c - 1))
    if noise:
        return [[1 + (a * i + b * j + shift) // p + random.getrandbits(1) for j in range(c)] for i in range(r)]
    return [[1 + (a * i + b * j + shift) // p for j in range(c)] for i in range(r)]


def steps(r, c, pi, pj, flip):
    """h = 1 + i // pi + j' // pj with j' = j or c - 1 - j: terraces"""
    col = [(c - 1 - j if flip else j) // pj for j in range(c)]
    return [[1 + i // pi + x for x in col] for i in range(r)]


M = MAXRC
add(35, tilt(M, M, 1, 1, 21))
add(35, tilt(M, M, 1, -1, 21))
add(25, steps(M, M, 15, 40, False))
add(25, steps(M, M, 15, 40, True))
add(25, tilt(M, M, 1, 0, 11))
add(17, tilt(M, M, 1, 1, 42, 1))
add(30, tilt(M, M, 1, -1, 21, 1))
add(35, tilt(M, 900, 1, 1, 20))                                     # R != C
add(30, tilt(900, M, 1, -1, 20))
g = tilt(M, M, 1, 1, 21)
g[M // 2 + ri(-5, 5)][M // 2 + ri(-5, 5)] = 99                      # one spike
add(35, g)
add(30, tilt(M, M, 2, -1, 40, 1))
add(24, tilt(M, M, 1, 2, 40, 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

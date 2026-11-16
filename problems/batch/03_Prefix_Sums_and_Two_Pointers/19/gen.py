# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11905)
MAXSIDE = 10_000
MAXSHORT = 30
V = 10
MAXT = 10**6
tests = []


def add(t, g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= MAXSIDE and 1 <= c <= MAXSIDE and min(r, c) <= MAXSHORT
    assert -MAXT <= t <= MAXT
    assert all(len(row) == c and all(-V <= x <= V for x in row) for row in g)
    tests.append(f"{r} {c} {t}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))


def rnd(r, c, lo=-V, hi=V):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]


def const(r, c, x):
    return [[x] * c for _ in range(r)]


# samples
add(3, [[1, 2, 0], [-1, 1, 2]])
add(5, [[1, 1], [1, 1]])
add(0, const(2, 3, 0))
add(-2, [[3, -2, 1], [-4, 2, -3], [1, -1, 0]])
add(7, [[7]])
add(4, [[2, -1, 3, 0, -2, 4, 1, -3]])
# hidden (small)
add(-7, [[7]])
add(0, rnd(1, 1))
add(0, rnd(5, 5, -1, 1))
add(1, rnd(8, 3, -2, 2))
add(3, rnd(3, 12, -3, 3))
add(10, rnd(20, 20))
add(0, rnd(30, 25, -1, 1))
add(-5, rnd(15, 40, -4, 2))
add(40, const(10, 10, 10))
add(MAXT, const(12, 12, 10))
add(-4, rnd(300, 30, -3, 3))
# large (the 4-loop brute force needs about 2*10^10 steps on a full 30 x 10000 field)
W, H = MAXSIDE, MAXSHORT
add(0, const(H, W, 0))                            # every rectangle
add(10 * 36, const(W, H, 10))                     # area 36, many rows
add(-MAXT, const(H, W, -10))                      # area 100000 only
add(0, rnd(H, W, -1, 1))
add(7, rnd(H, W))
add(0, rnd(W, H, -1, 1))                          # many rows, few columns
add(-3, rnd(W, H, -3, 3))
add(3, rnd(H, W, -2, 2))
add(-12, rnd(28, W - 1, -2, 1))
add(1, rnd(W, 29, -1, 2))
g = [[(1 if (i + j) % 2 == 0 else -1) for j in range(H)] for i in range(W)]
add(0, g)                                         # checkerboard
add(MAXT - 1, const(H, W, 10))                    # unreachable
add(10, rnd(H, W, 0, 1))
add(-1, rnd(W, H))
add(2, [[random.choice([1, -1, 1, 0]) for _ in range(W)]])
add(1, [[random.choice([1, -1])] for _ in range(W)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

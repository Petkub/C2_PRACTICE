# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11018)
MAXN, MAXC = 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(rects):
    n = len(rects)
    assert 1 <= n <= MAXN
    assert all(0 <= x1 < x2 <= MAXC and 0 <= y1 < y2 <= MAXC for x1, y1, x2, y2 in rects)
    t = f"{n}\n" + "".join(f"{x1} {y1} {x2} {y2}\n" for x1, y1, x2, y2 in rects)
    assert len(t) <= 3_300_000
    tests.append(t)


def rnd_rect(c, maxside):
    x1, y1 = ri(0, c - 1), ri(0, c - 1)
    return (x1, y1, min(c, x1 + ri(1, maxside)), min(c, y1 + ri(1, maxside)))


def big_square(c, margin):
    """a rectangle that spans most of [0, c] in both directions"""
    return (ri(0, margin), ri(0, margin), ri(c - margin, c), ri(c - margin, c))


def tall(c, width, margin):
    x1 = ri(0, c - width)
    return (x1, ri(0, margin), x1 + ri(1, width), ri(c - margin, c))


def wide(c, height, margin):
    y1 = ri(0, c - height)
    return (ri(0, margin), y1, ri(c - margin, c), y1 + ri(1, height))


# samples
add([(1, 1, 5, 4), (3, 2, 7, 6)])
add([(0, 0, 4, 4), (1, 1, 3, 3), (4, 0, 6, 2)])
add([(0, 0, MAXC, MAXC)])
add([(0, 0, 2, 2), (0, 0, 2, 2), (0, 0, 2, 2)])
add([(0, 1, 6, 2), (2, 0, 3, 5), (1, 0, 4, 3), (5, 0, 6, 6)])
# hidden: small
add([(0, 0, 1, 1), (1, 0, 2, 1), (0, 1, 1, 2), (1, 1, 2, 2)])          # touching only
add([rnd_rect(10, 5) for _ in range(8)])
add([rnd_rect(30, 12) for _ in range(40)])
add([rnd_rect(MAXC, MAXC) for _ in range(300)])
add([rnd_rect(10**6, 10**5) for _ in range(1500)])
add([(i, i, 2000 - i, 2000 - i) for i in range(1000)])                  # nested
add([tall(10**5, 100, 10**4) if i % 2 else wide(10**5, 100, 10**4) for i in range(1500)])
# hidden: maximum size
N, C = MAXN, 999_999
add([big_square(C, 10**5) for _ in range(N)])
add([tall(C, 3000, 10**5) if i % 2 else wide(C, 3000, 10**5) for i in range(N)])
add([rnd_rect(C, 10**5) for _ in range(N)])
add([(i * 4 + ri(0, 3), i * 4 + ri(0, 3), C - i * 4 - ri(0, 3), C - i * 4 - ri(0, 3)) for i in range(N)])  # nested
add([(0, 0, MAXC, MAXC)] * 65_000)                                       # the largest areas
add([big_square(MAXC, 10**8) for _ in range(65_000)])
tiles = []                                                              # a grid of tiles touching at the edges
for i in range(316):
    for j in range(316):
        tiles.append((i * 3163, j * 3163, (i + 1) * 3163, (j + 1) * 3163))
random.shuffle(tiles)
add(tiles)
add([tall(C, 20, 4 * 10**5) for _ in range(N)])                         # thin strips, many overlap
xs = sorted(random.sample(range(C + 1), 40))
rects = []
for _ in range(N):                                                      # many posters start/end at the same x
    a, b = sorted(random.sample(xs, 2))
    y1 = ri(0, 2 * 10**5)
    rects.append((a, y1, b, ri(8 * 10**5, C)))
add(rects)
rects = []
for i in range(N):                                                      # a staircase: each overlaps the next
    s = i * 9
    rects.append((s, s // 2, s + 1 + ri(0, 2 * 10**5), min(C, s // 2 + 1 + ri(4 * 10**5, 6 * 10**5))))
add(rects)
add([big_square(C, 4 * 10**5) if i % 10 == 0 else rnd_rect(C, 2000) for i in range(N)])
rects = []
for i in range(N // 2):                                                 # crossing pairs: double cover only where they cross
    rects.append(tall(C, 5, 2 * 10**5))
    rects.append(wide(C, 5, 2 * 10**5))
add(rects)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(41900)
MAXN = 5000
MAXC = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(rs):
    n = len(rs)
    assert 1 <= n <= MAXN
    for x1, y1, x2, y2 in rs:
        assert 0 <= x1 < x2 <= MAXC and 0 <= y1 < y2 <= MAXC
    tests.append(f"{n}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in rs))


def shuffled(rs):
    rs = list(rs)
    random.shuffle(rs)
    return rs


def rnd_rect(cmax, maxside=None):
    if maxside is None:
        x1, x2 = sorted(random.sample(range(cmax + 1), 2))
        y1, y2 = sorted(random.sample(range(cmax + 1), 2))
    else:
        x1, y1 = ri(0, cmax - 1), ri(0, cmax - 1)
        x2, y2 = min(cmax, x1 + ri(1, maxside)), min(cmax, y1 + ri(1, maxside))
    return (x1, y1, x2, y2)


def cuts(k, lo, hi):
    """k + 1 strictly increasing cut positions from lo to hi"""
    return [lo] + sorted(random.sample(range(lo + 1, hi), k - 1)) + [hi]


def tiling(a, b, lo, hi):
    """a x b posters that exactly tile the square [lo, hi]^2 (neighbours share whole sides)"""
    xc, yc = cuts(a, lo, hi), cuts(b, lo, hi)
    return [(xc[i], yc[j], xc[i + 1], yc[j + 1]) for i in range(a) for j in range(b)]


def frames(k, size, gap):
    """k x k square frames (4 posters each) around holes; neighbouring frames touch"""
    rs = []
    t = size // 4                                   # frame thickness
    for i in range(k):
        for j in range(k):
            x, y = i * (size + gap), j * (size + gap)
            rs += [(x, y, x + size, y + t), (x, y + size - t, x + size, y + size),
                   (x, y + t, x + t, y + size - t), (x + size - t, y + t, x + size, y + size - t)]
    return rs


# samples
add([(0, 0, 4, 3), (2, 1, 6, 5)])
add([(0, 0, 2, 2), (2, 0, 5, 2)])
add([(0, 0, 3, 1), (0, 2, 3, 3), (0, 1, 1, 2), (2, 1, 3, 2)])
add([(0, 0, 10, 10), (2, 2, 5, 5)])
add([(0, 0, 1, 1), (1, 1, 2, 2)])
add([(1, 1, 4, 3), (3, 0, 5, 2), (4, 2, 6, 4), (0, 3, 2, 5)])
# hidden: small
add([(0, 0, MAXC, MAXC)])
add([(5, 5, 6, 6)] * 3)
add([rnd_rect(8) for _ in range(6)])
add([rnd_rect(30) for _ in range(40)])
add([rnd_rect(100, 10) for _ in range(300)])
add(shuffled(tiling(12, 15, 0, 1000)))
add(shuffled(frames(6, 40, 0)))                     # frames touching each other, every hole kept
add([rnd_rect(MAXC) for _ in range(200)])
# large (N = 5000)
N = MAXN
S = 45 * 10**7                                      # touching structures live in [0, S]^2 ...


def big_layer(k):
    """... and k big posters that all overlap each other live in [5.5e8, 1e9]^2 (painting cells is slow)"""
    return [(ri(55 * 10**7, 62 * 10**7), ri(55 * 10**7, 62 * 10**7), ri(93 * 10**7, MAXC), ri(93 * 10**7, MAXC))
            for _ in range(k)]


add([(ri(0, MAXC // 2 - 1), ri(0, MAXC // 2 - 1), ri(MAXC // 2, MAXC), ri(MAXC // 2, MAXC)) for _ in range(N)])
add([rnd_rect(MAXC) for _ in range(N)])
add([rnd_rect(MAXC, 10**7) for _ in range(N)])      # mostly separate small posters
add(shuffled([(0, 2 * i, MAXC, 2 * i + 1) for i in range(N)]))   # long thin strips: the answer needs 64 bits
add(shuffled(tiling(50, 60, 0, S) + big_layer(N - 3000)))   # a square cut into touching pieces
add(shuffled(tiling(50, 100, 10**8, 9 * 10**8)))
s = 10**5                                           # checkerboard: pieces touch only at corners
add(shuffled([(i * s, j * s, (i + 1) * s, (j + 1) * s) for i in range(70) for j in range(70) if (i + j) % 2 == 0]
             + big_layer(N - 2450)))
add(shuffled([(i * 10**5, i * 10**5, MAXC - i * 10**5, MAXC - i * 10**5) for i in range(N)]))   # nested
add(shuffled(frames(25, 16 * 10**6, 0) + big_layer(N - 2500)))
xs = cuts(N // 4, 0, S)
ys = cuts(N // 4, 0, S)
mesh = [(xs[i], 0, xs[i] + 1, S) for i in range(N // 4) if xs[i] + 1 < xs[i + 1]] + \
       [(0, ys[j], S, ys[j] + 1) for j in range(N // 4) if ys[j] + 1 < ys[j + 1]]
add(shuffled(mesh + big_layer(N - len(mesh))))                                 # thin bars both ways: a net with very many holes
rs = []                                             # brick wall: rows of bricks, each row shifted
h = S // 30
for j in range(30):
    xc = cuts(99, 0, S)
    rs += [(xc[i], j * h, xc[i + 1], (j + 1) * h) for i in range(99)]
add(shuffled(rs + big_layer(N - len(rs))))
rs = []                                             # a chain: each poster starts where the previous one ends
x = 0
for i in range(3000):
    w = ri(1, 10**5)
    y1 = ri(0, S - 10**6)
    rs.append((x, y1, x + w, y1 + ri(1, 10**6)))
    x += w
add(shuffled(rs + big_layer(N - 3000)))
add([(ri(0, 10**8), ri(0, 10**8), ri(9 * 10**8, MAXC), ri(9 * 10**8, MAXC)) for _ in range(N)])   # huge, all overlap
rs = []                                             # wide bars and tall bars, every one thick
for i in range(N // 2):
    a = ri(0, 7 * 10**8)
    rs.append((ri(0, 10**7), a, ri(MAXC - 10**7, MAXC), a + ri(10**8, 3 * 10**8)))
    a = ri(0, 7 * 10**8)
    rs.append((a, ri(0, 10**7), a + ri(10**8, 3 * 10**8), ri(MAXC - 10**7, MAXC)))
add(shuffled(rs))
rs = tiling(40, 50, 0, 4 * 10**8)                   # touching pieces in one corner, big overlapping posters elsewhere
rs += [(ri(5 * 10**8, 7 * 10**8), ri(5 * 10**8, 7 * 10**8), ri(8 * 10**8, MAXC), ri(8 * 10**8, MAXC))
       for _ in range(N - len(rs))]
add(shuffled(rs))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

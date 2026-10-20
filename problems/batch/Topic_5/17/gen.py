# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(41700)
MAXN = 200_000
MAXC = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(pts):
    n = len(pts)
    assert 2 <= n <= MAXN
    xs = [x for x, y in pts]
    ys = [y for x, y in pts]
    assert -MAXC <= min(xs) and max(xs) <= MAXC and -MAXC <= min(ys) and max(ys) <= MAXC
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def shuffled(p):
    p = list(p)
    random.shuffle(p)
    return p


def line(n, step, jitter, vertical, base=0, offset=0):
    """n points along a line through the middle, consecutive ones about step apart"""
    start = -(n * step) // 2 + offset
    pts = []
    for k in range(n):
        a = start + k * step + ri(0, jitter)
        b = base + ri(0, jitter)
        pts.append((b, a) if vertical else (a, b))
    return pts


# samples
add([(0, 0), (5, 5), (3, 4), (9, 1), (7, 7)])
add([(2, 3), (-1, 4), (2, 3)])
add([(1, 1), (4, 5)])
add([(0, 10), (0, 0), (0, 3), (0, 7)])
add([(-3, 2), (4, -1), (0, 0), (1, 5), (-2, -2), (3, 3)])
# hidden: small
add([(-MAXC, -MAXC), (MAXC, MAXC)])                           # the largest possible answer
add([(-MAXC, MAXC), (MAXC, -MAXC), (MAXC, MAXC)])
add([(ri(-5, 5), ri(-5, 5)) for _ in range(8)])
add([(ri(-100, 100), ri(-100, 100)) for _ in range(50)])
add([(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(500)])
add(shuffled(line(3000, 1000, 50, True) + line(3000, 1000, 50, False, base=10**6)))
add([(ri(-10**6, 10**6), ri(-10**6, 10**6)) for _ in range(5000)])
add([(7, 7)] * 4000)                                          # everybody at one place
# large: N = MAXN with coordinates below about 10^6 (input near 3 MB), or N = 130 000 with full coordinates
N = MAXN
add([(ri(-10**6, 10**6), ri(-10**6, 10**6)) for _ in range(N)])
add(shuffled(line(N, 9000, 100, True)))                       # one vertical line: sorting by x and stopping early fails
add(shuffled(line(N, 9000, 100, False)))                      # one horizontal line
N2 = 180_000
add(shuffled(line(N2 // 2, 400, 10, True, base=-1000) + line(N2 // 2, 400, 10, False, base=1000)))
p = line(N - 2, 10**4, 0, True)                               # the close pair is far apart in x order
p += [(-1, 123_456), (1, 123_456)]
add(shuffled(p))
p = [(ri(0, 100), 400 * k + ri(0, 10)) for k in range(-N2 // 4, N2 // 4)]       # narrow vertical band
p += [(400 * k + ri(0, 10), 10**8 + ri(0, 100)) for k in range(-N2 // 4, N2 // 4)]  # narrow horizontal band
add(shuffled(p))
s = 4400                                                      # square lattice, one pair a bit closer
p = [(s * i, s * j) for i in range(-223, 224) for j in range(-223, 224)][:N]
p[ri(0, len(p) - 1)] = (s * 10 + 3000, s * 10 + 1)
add(shuffled(p))
M = 130_000
s = 5 * 10**6                                                 # lattice with a huge gap: the answer needs 64 bits
p = [(s * i, s * j) for i in range(-180, 181) for j in range(-180, 181)][:M]
add(shuffled(p))
s = 100                                                       # a tall thin and a wide flat lattice
p = [(-10**6 + s * k, -25 * 10**5 + s * j) for k in range(2) for j in range(N // 4)]
p += [(-25 * 10**5 + s * j + s // 2, 10**6 + s * k + s // 2) for k in range(2) for j in range(N // 4)]
add(shuffled(p))
p = [(ri(-MAXC, -MAXC + 10**6), ri(-MAXC, -MAXC + 10**6)) for _ in range(M // 2)]
p += [(ri(MAXC - 10**6, MAXC), ri(MAXC - 10**6, MAXC)) for _ in range(M // 2)]
add(shuffled(p))
p = [(7 * k, 7 * k + ri(0, 3)) for k in range(-N // 2, N // 2)]   # along a diagonal
add(shuffled(p))
p = line(N - 1, 9000, 0, True)
p.append(p[ri(0, N - 2)])                                      # one repeated point
add(shuffled(p))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

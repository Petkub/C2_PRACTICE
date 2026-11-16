# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90117)
MAXN, MAXC = 100_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(pts):
    n = len(pts)
    assert 2 <= n <= MAXN
    assert all(1 <= c <= MAXC for p in pts for c in p)
    tests.append(f"{n}\n" + "".join(f"{x} {y} {z}\n" for x, y, z in pts))


def rnd(n, hx, hy=None, hz=None):
    r = random.random
    hy = hx if hy is None else hy
    hz = hx if hz is None else hz
    return [(1 + int(r() * hx), 1 + int(r() * hy), 1 + int(r() * hz)) for _ in range(n)]


def perm3(pts):
    """the same stars with the coordinates in a random order (each axis gets every role)"""
    o = [0, 1, 2]
    random.shuffle(o)
    return [(p[o[0]], p[o[1]], p[o[2]]) for p in pts]


def zmatters(n):
    """x and y are spread far apart, z is packed: the cheap tunnels come from the z order"""
    xs = random.sample(range(1, MAXC + 1), n)
    ys = random.sample(range(1, MAXC + 1), n)
    zs = [ri(1, max(1, n // 4)) * 3 for _ in range(n)]
    return [(xs[i], ys[i], zs[i]) for i in range(n)]


def layers(n, k):
    """k far apart groups along x, inside a group the stars are close along y or z"""
    pts = []
    for i in range(n):
        g = i % k
        base = 1 + g * (MAXC // k)
        pts.append((base + ri(0, 50), ri(1, MAXC), ri(1, MAXC)))
    return pts


def diagonal(n, gap):
    """x = y = z: every tunnel costs the full difference"""
    pts = []
    v = 1
    for i in range(n):
        pts.append((v, v, v))
        v += ri(1, gap)
    random.shuffle(pts)
    return pts


def twisted(n):
    """three interleaved rising sequences: each axis is good for a different pair"""
    pts = []
    for i in range(n):
        a = 1 + i * (MAXC // n)
        pts.append((a, MAXC - a + 1, ri(1, MAXC)) if i % 3 == 0 else
                   (ri(1, MAXC), a, MAXC - a + 1) if i % 3 == 1 else
                   (MAXC - a + 1, ri(1, MAXC), a))
    random.shuffle(pts)
    return pts


# samples
add([(1, 5, 10), (4, 9, 2), (7, 1, 6), (8, 8, 8)])
add([(1, 1, 1), (10, 20, 30)])
add([(10, 1, 7), (3, 8, 7), (6, 6, 1), (1, 2, 12), (12, 11, 5)])
add([(2, 2, 2), (2, 2, 2), (2, 2, 3)])
add([(1, 1, 1), (3, 3, 3), (6, 6, 6), (10, 10, 10), (1000000, 1000000, 1000000)])
# hidden: small
add([(1, 1, 1), (1000000, 1000000, 1000000)])
for n, h in ((5, 5), (6, 3), (8, 20), (10, 1000), (30, 50), (60, 10**6), (200, 300)):
    add(rnd(n, h))
add(perm3(zmatters(40)))
add(perm3(layers(50, 5)))
add(diagonal(100, 1000))
add(twisted(120))
add(rnd(3000, MAXC))
add(perm3(zmatters(3000)))
# hidden: maximum size
N = MAXN
add(rnd(N, MAXC))
add(rnd(N, 300))                                                # many equal coordinates
add(rnd(N, MAXC, MAXC, 1))                                      # one coordinate equal: answer 0
add(zmatters(N))
add(perm3(zmatters(N)))
add(perm3(zmatters(N)))
add(layers(N, 1000))
add(perm3(layers(N, 37)))
add(diagonal(N, 10))                                            # answer = the largest minus the smallest
add(twisted(N))
add(rnd(N, MAXC, 1000, MAXC))
add(perm3(rnd(N, 5000, MAXC, 2 * 10**5)))
add([(MAXC - ri(0, 1), MAXC - ri(0, 1), ri(1, MAXC)) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

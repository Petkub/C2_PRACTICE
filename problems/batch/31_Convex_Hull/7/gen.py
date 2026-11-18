# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from functools import cmp_to_key
from math import gcd

random.seed(31009)
MAXN = 200_000
MAXC = 10**6
tests = []


RB = random.getrandbits


def ri(lo, hi):
    return lo + ((RB(32) * (hi - lo + 1)) >> 32)


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = (RB(32) * (i + 1)) >> 32
        a[i], a[j] = a[j], a[i]


def half(v):
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def by_angle(a, b):
    ha, hb = half(a), half(b)
    if ha != hb:
        return ha - hb
    c = a[0] * b[1] - a[1] * b[0]
    return -1 if c > 0 else (1 if c < 0 else 0)


def lattice_polygon(k):
    r = 2
    while (r + 1) * (r + 1) <= k // 2:
        r += 1
    while True:
        vs = [(a, b) for a in range(-r, r + 1) for b in range(-r, r + 1)
              if (a or b) and a * a + b * b <= r * r and gcd(abs(a), abs(b)) == 1]
        if 100 * len(vs) >= 115 * k:
            break
        r += 1
    vs.sort(key=lambda v: (v[0] * v[0] + v[1] * v[1], v))
    keep = vs[:115 * k // 100]
    shuffle(keep)
    keep = keep[:k - 1]
    mult = {v: 1 for v in keep}
    sx = sum(v[0] for v in keep)
    sy = sum(v[1] for v in keep)
    if sx or sy:
        g = gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        mult[d] = mult.get(d, 0) + g
    edges = sorted(mult, key=cmp_to_key(by_angle))
    x = y = 0
    pts = []
    for e in edges:
        pts.append((x, y))
        x += e[0] * mult[e]
        y += e[1] * mult[e]
    assert (x, y) == (0, 0)
    mx = min(p[0] for p in pts)
    my = min(p[1] for p in pts)
    return [(p[0] - mx, p[1] - my) for p in pts]


def add(pts):
    n = len(pts)
    assert 1 <= n <= MAXN
    for x, y in pts:
        assert 0 <= x <= MAXC and 0 <= y <= MAXC
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def interior(poly, cnt, f=900):
    cx = sum(p[0] for p in poly) // len(poly)
    cy = sum(p[1] for p in poly) // len(poly)
    out = []
    m = len(poly)
    for _ in range(cnt):
        p = poly[(RB(32) * m) >> 32]
        t = (RB(32) * f) >> 32
        out.append((cx + (p[0] - cx) * t // 1000, cy + (p[1] - cy) * t // 1000))
    return out


def place(poly, scale, dx, dy):
    return [(dx + p[0] * scale, dy + p[1] * scale) for p in poly]


add([(2, 1), (6, 2), (4, 5), (3, 3), (1, 4), (7, 6)])
add([(3, 3), (1, 1), (5, 5), (5, 1), (3, 3)])
add([(4, 4)])
add([(0, 0), (6, 0), (6, 4), (0, 4), (3, 2), (2, 7)])
add([(5, 2), (5, 2), (2, 8), (8, 8), (1, 5), (9, 5), (5, 9)])

add([(MAXC, MAXC), (0, 0), (MAXC, 0), (0, MAXC), (MAXC // 2, MAXC // 2)])
add([(7, 3)] * 10 + [(7, 9)] * 5 + [(7, 1)])
add([(ri(0, 10), ri(0, 10)) for _ in range(12)])
add([(ri(0, 6), ri(0, 6)) for _ in range(40)])
add([(ri(0, 100), ri(0, 100)) for _ in range(300)])
p = lattice_polygon(60)
q = interior(p, 60) + p
shuffle(q)
add(q)
p = place(lattice_polygon(200), 50, 1000, 2000)
add(interior(p, 300) + p)
p = lattice_polygon(1500)
q = p + interior(p, 1500)
shuffle(q)
add(q)

big = lattice_polygon(30000)
assert max(max(x, y) for x, y in big) <= MAXC
q = big + interior(big, MAXN - len(big))
shuffle(q)
add(q)
q = list(big)
shuffle(q)
add(q + interior(big, MAXN - len(big)))
q = interior(big, MAXN - len(big), 990)
add(q[:MAXN // 2] + big[::2] + big[1::2] + q[MAXN // 2:])

rings = []
small = lattice_polygon(8000)
for s in (1, 2, 3, 4):
    w = max(max(x, y) for x, y in small) * s
    off = (MAXC - w) // 2
    r = place(small, s, off, off)
    shuffle(r)
    rings += r
w = max(max(x, y) for x, y in big)
off = (MAXC - w) // 2
r = place(big, 1, off, off)
shuffle(r)
rings += r
add(rings + interior(place(big, 1, off, off), MAXN - len(rings)))
q = big + big[:20000] + interior(big, MAXN - len(big) - 20000)
shuffle(q)
add(q)
q = [(x, y) for x, y in big] + [(x, ri(min(y, MAXC // 2), max(y, MAXC // 2))) for x, y in big[: len(big) // 2]]
q += interior(big, MAXN - len(q))
shuffle(q)
add(q)
mirror = [(MAXC - y, x) for x, y in big]
q = mirror + interior(mirror, MAXN - len(mirror))
shuffle(q)
add(q)
add(big + interior(big, MAXN - len(big)))
q = sorted(big)
add(q + interior(big, MAXN - len(big), 990))
small2 = lattice_polygon(15000)
w = max(max(x, y) for x, y in small2)
q = place(small2, 1, 0, 0) + place(small2, 1, MAXC - w, MAXC - w)
q += interior(place(small2, 1, 0, 0), (MAXN - len(q)) // 2)
q += interior(place(small2, 1, MAXC - w, MAXC - w), MAXN - len(q))
shuffle(q)
add(q)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_100_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

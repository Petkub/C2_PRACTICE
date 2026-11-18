# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from math import gcd

random.seed(310010)
RB = random.getrandbits
MAXN = 200_000
MAXC = 10**9
tests = []


def rnd(m):
    return (RB(32) * m) >> 32


def ri(lo, hi):
    return lo + rnd(hi - lo + 1)


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = rnd(i + 1)
        a[i], a[j] = a[j], a[i]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def angle_key(v, r, big):
    a, b = v
    if a > 0 and b >= 0:
        q, a2, b2 = 0, a, b
    elif a <= 0 and b > 0:
        q, a2, b2 = 1, b, -a
    elif a < 0 and b <= 0:
        q, a2, b2 = 2, -a, -b
    else:
        q, a2, b2 = 3, -b, a
    return q * (r + 1) * big + b2 * big // a2


def lattice_polygon(k):
    r = 2
    while (r + 1) * (r + 1) <= 6 * k // 10:
        r += 1
    while True:
        quarter = [(a, b) for a in range(1, r + 1) for b in range(0, r + 1)
                   if a * a + b * b <= r * r and gcd(a, b) == 1]
        vs = quarter + [(-b, a) for a, b in quarter] + [(-a, -b) for a, b in quarter] + [(b, -a) for a, b in quarter]
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
    big = 2 * r * r + 2
    edges = sorted(mult, key=lambda v: angle_key(v, r, big))
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


def fit(poly, lim=MAXC):
    mx = min(p[0] for p in poly)
    my = min(p[1] for p in poly)
    poly = [(x - mx, y - my) for x, y in poly]
    w = max(max(p) for p in poly)
    s = lim // w
    assert s >= 1
    return [(p[0] * s, p[1] * s) for p in poly], s


def cap_point(poly, s, i, a, b):
    h = len(poly)
    p, v, q = poly[i - 1], poly[i], poly[(i + 1) % h]
    return (v[0] + (a * (p[0] - v[0]) + b * (q[0] - v[0])) // s,
            v[1] + (a * (p[1] - v[1]) + b * (q[1] - v[1])) // s)


def cap_area(poly, i):
    h = len(poly)
    return cross(poly[i - 1], poly[i], poly[(i + 1) % h])


def interior(poly, cnt, f=900):
    cx = sum(p[0] for p in poly) // len(poly)
    cy = sum(p[1] for p in poly) // len(poly)
    out = []
    m = len(poly)
    for _ in range(cnt):
        p = poly[rnd(m)]
        t = rnd(f)
        out.append((cx + (p[0] - cx) * t // 1000, cy + (p[1] - cy) * t // 1000))
    return out


def blocked_caps(poly, s, top):
    areas = sorted(set(cap_area(poly, i) for i in range(len(poly))), reverse=True)[:top]
    lim = areas[-1]
    return [cap_point(poly, s, i, 1, 1) for i in range(len(poly)) if cap_area(poly, i) >= lim]


def random_caps(poly, s, cnt):
    out = []
    h = len(poly)
    for _ in range(cnt):
        i = rnd(h)
        if rnd(8) == 0:
            a = ri(1, s - 1)
            out.append(cap_point(poly, s, i, a, s - a))
        else:
            a = ri(1, s - 2)
            b = ri(1, s - 1 - a)
            out.append(cap_point(poly, s, i, a, b))
    return out


def edge_points(poly, s, cnt):
    out = []
    h = len(poly)
    for _ in range(cnt):
        i = rnd(h)
        p, q = poly[i], poly[(i + 1) % h]
        g = gcd(abs(q[0] - p[0]), abs(q[1] - p[1]))
        if g < 2:
            continue
        t = ri(1, g - 1)
        out.append((p[0] + (q[0] - p[0]) // g * t, p[1] + (q[1] - p[1]) // g * t))
    return out


def add(pts, limit=MAXN):
    seen = set()
    uniq = []
    for p in pts:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    pts = uniq[:limit]
    n = len(pts)
    assert 4 <= n <= MAXN
    for x, y in pts:
        assert 0 <= x <= MAXC and 0 <= y <= MAXC
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def mixed(pts):
    pts = list(pts)
    shuffle(pts)
    return pts


add([(0, 0), (6, 0), (6, 3), (3, 7), (0, 4), (5, 1), (3, 3)])
add([(1, 3), (0, 0), (2, 2), (3, 1)])
add([(0, 0), (4, 0), (4, 4), (0, 4), (2, 2)])
add([(6, 2), (1, 2), (9, 9), (0, 3), (2, 0), (4, 2), (7, 2), (3, 6)])
add([(1, 1), (3, 3), (2, 2), (5, 5), (4, 4)])
add([(0, 1), (8, 4), (3, 4), (0, 2), (6, 0), (9, 7), (7, 8)])


add([(0, 0), (MAXC, 0), (MAXC, MAXC), (0, MAXC)])
add([(0, 0), (MAXC, 0), (0, MAXC), (1, 1), (MAXC - 2, 1), (1, MAXC - 2)])
add([(7 * i, 3 * i + 5) for i in range(20)])
add([(5, 5), (1, 1), (9, 1), (5, 9), (1, 9), (9, 9), (5, 1), (1, 5), (9, 5)])
for n, c in ((8, 6), (12, 8), (300, 60), (1000, 1000)):
    add([(ri(0, c), ri(0, c)) for _ in range(3 * n)], n)
p, s = fit(lattice_polygon(40), 5000)
add(mixed(p + random_caps(p, s, 80) + blocked_caps(p, s, 2) + edge_points(p, s, 10)))
p, s = fit(lattice_polygon(200), 10**6)
add(mixed(p + random_caps(p, s, 300) + blocked_caps(p, s, 3) + interior(p, 100)))


master = lattice_polygon(120_000)
p, s = fit(master)
add(mixed(p + blocked_caps(p, s, 3) + random_caps(p, s, 20_000)))
q = master[::2]
p, s = fit(q)
add(mixed(p + blocked_caps(p, s, 5) + random_caps(p, s, 70_000)))
q = master[1::3]
p, s = fit(q)
extra = [cap_point(p, s, i, ri(1, 4), ri(1, 4)) for i in range(len(p)) if rnd(2)]
add(mixed(p + extra + interior(p, 30_000)))
q = [(y, x) for x, y in master[::3]][::-1]
p, s = fit(q)
add(mixed(p + blocked_caps(p, s, 1) + edge_points(p, s, 50_000)))
p, s = fit(master[::4])
add(mixed(p + interior(p, 110_000)))
p, s = fit(master[::4])
add(mixed(p + [cap_point(p, s, i, ri(1, s // 2), ri(1, s // 2 - 1)) for i in range(len(p))] + random_caps(p, s, 40_000)))
small = lattice_polygon(30_000)
p, s = fit(small, 10**6)
add(mixed(p + interior(p, MAXN - len(p))))
p, s = fit(small[::2], 10**6)
add(mixed(p + interior(p, MAXN - len(p), 990)))
q = master[::2]
p, s = fit([(x + 20 * y, y) for x, y in q])
assert all(cross(p[i - 2], p[i - 1], p[i]) > 0 for i in range(len(p)))
add(mixed(p + blocked_caps(p, s, 2) + random_caps(p, s, 40_000)))
p, s = fit(master[2::3])
extra = []
for i in range(len(p)):
    a = ri(1, s - 1)
    extra.append(cap_point(p, s, i, a, s - a))
add(mixed(p + extra[::2] + blocked_caps(p, s, 2) + interior(p, 20_000)))
p, s = fit(master)
add(mixed(p))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_200_000, len(t)
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

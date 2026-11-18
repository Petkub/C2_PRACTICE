# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310003)
MAXN, MAXQ = 50_000, 80_000
MAXC = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffled(p):
    p = list(p)
    for i in range(len(p) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        p[i], p[j] = p[j], p[i]
    return p


def half(v):
    return 0 if v[1] < 0 or (v[1] == 0 and v[0] > 0) else 1


def by_angle(u, v):
    hu, hv = half(u), half(v)
    if hu != hv:
        return hu - hv
    c = u[0] * v[1] - u[1] * v[0]
    if c:
        return -1 if c > 0 else 1
    return -1 if (u[0], u[1]) < (v[0], v[1]) else (1 if (u[0], u[1]) > (v[0], v[1]) else 0)


def add(shops, houses):
    n, q = len(shops), len(houses)
    assert 3 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXC <= x <= MAXC and -MAXC <= y <= MAXC for x, y in shops + houses)
    a = shops[0]
    b = next(s for s in shops if s != a)
    assert any((b[0] - a[0]) * (s[1] - a[1]) - (b[1] - a[1]) * (s[0] - a[0]) != 0 for s in shops)
    tests.append(f"{n} {q}\n" + "".join(f"{x} {y}\n" for x, y in shops) + "".join(f"{x} {y}\n" for x, y in houses))


def convex_polygon(h):
    r = int(math.sqrt(h / 2.2)) + 3
    prim = [(a, b) for a in range(-r, r + 1) for b in range(-r, r + 1) if (a, b) != (0, 0) and math.gcd(a, b) == 1]
    prim.sort(key=lambda v: (v[0] * v[0] + v[1] * v[1], v))
    prim = prim[:int(h * 1.25)]
    keep = {v: 1 for v in prim if random.random() < 0.8}
    sx = sum(a * m for (a, b), m in keep.items())
    sy = sum(b * m for (a, b), m in keep.items())
    if sx or sy:
        g = math.gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        keep[d] = keep.get(d, 0) + g
    return sorted(((a, b, m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))


def polygon(edges, size):
    x = y = 0
    raw = []
    for a, b, m in edges:
        raw.append((x, y))
        x += a * m
        y += b * m
    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    w = max(max(xs) - min(xs), max(ys) - min(ys))
    s = max(1, size // w)
    ox = -(max(xs) + min(xs)) * s // 2
    oy = -(max(ys) + min(ys)) * s // 2
    pts = [(px * s + ox, py * s + oy) for px, py in raw]
    sides = [(pts[i], edges[i][0], edges[i][1], edges[i][2] * s) for i in range(len(edges))]
    return pts, sides


def pivot_sides(pts, sides):
    i = min(range(len(pts)), key=lambda k: pts[k])
    return [sides[i], sides[i - 1]]


def on_side(side):
    (x, y), a, b, L = side
    t = ri(0, L - 1)
    return (x + a * t, y + b * t)


def near_side(side, out, far=1):
    (x, y), a, b, L = side
    t = ri(0, L)
    d = ri(1, far)
    if out:
        return (x + a * t + b * d, y + b * t - a * d)
    return (x + a * t - b * d, y + b * t + a * d)


def houses_for(pts, sides, q, mix):
    piv = pivot_sides(pts, sides)
    out = []
    w = [int(f * q) for f in mix]
    w[1] += q - sum(w)
    for _ in range(w[0]):
        out.append(on_side(sides[ri(0, len(sides) - 1)]))
    for _ in range(w[1]):
        out.append(near_side(sides[ri(0, len(sides) - 1)], False, 3))
    for _ in range(w[2]):
        out.append(near_side(sides[ri(0, len(sides) - 1)], True, 3))
    for _ in range(w[3]):
        out.append(on_side(piv[ri(0, 1)]))
    for _ in range(w[4]):
        out.append((ri(-MAXC, MAXC), ri(-MAXC, MAXC)))
    for _ in range(w[5]):
        out.append(pts[ri(0, len(pts) - 1)])
    return shuffled(out)


add([(0, 0), (6, 0), (6, 4), (2, 5), (0, 3)], [(3, 3), (6, 2), (4, 5), (1, 4)])
add([(1, 1), (7, 1), (4, 7)], [(6, 3), (4, 3), (7, 7)])
add([(-5, -5), (5, -5), (5, 5), (-5, 5)], [(10**9, 10**9), (5, 0)])
add([(0, 0), (2, 1), (8, 4), (4, 0)], [(5, 1), (5, 2)])
add([(2, 2), (9, 4), (9, 4), (4, 8)], [(6, 9), (4, 8)])

add([(0, 0), (4, 0), (0, 4)], [(x, y) for x in range(-1, 6) for y in range(-1, 6)])
add([(ri(-6, 6), ri(-6, 6)) for _ in range(15)] + [(-7, 0), (7, 1), (0, 7)], [(x, y) for x in range(-8, 9) for y in range(-8, 9)])
add([(-MAXC, -MAXC), (MAXC, -MAXC), (MAXC, MAXC), (-MAXC, MAXC)],
    [(-MAXC, 0), (0, -MAXC), (MAXC, MAXC), (0, 0), (-MAXC, -MAXC), (MAXC, MAXC - 1), (MAXC - 1, MAXC), (-MAXC - 0, 5)])
add([(-MAXC, -MAXC), (MAXC, MAXC - 1), (MAXC - 1, MAXC)], [(0, 0), (1, 1), (-1, -1), (MAXC, MAXC), (-MAXC, -MAXC)])
pts, sides = polygon(convex_polygon(60), 3_000)
add(shuffled(pts + [(ri(-100, 100), ri(-100, 100)) for _ in range(40)]), houses_for(pts, sides, 2_000, (0.2, 0.3, 0.3, 0.1, 0.05, 0.05)))
pts, sides = polygon(convex_polygon(400), 10**6)
add(shuffled(pts), houses_for(pts, sides, 3_000, (0.2, 0.3, 0.3, 0.1, 0.05, 0.05)))
add([(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(3_000)], [(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(3_000)])

for h, size, mix in ((50_000, 2 * MAXC, (0.25, 0.6, 0.1, 0.05, 0.0, 0.0)), (45_000, 2 * MAXC, (0.1, 0.8, 0.05, 0.03, 0.01, 0.01)),
                     (40_000, MAXC, (0.3, 0.5, 0.1, 0.1, 0.0, 0.0)), (50_000, 2 * MAXC, (0.05, 0.85, 0.05, 0.05, 0.0, 0.0)),
                     (35_000, 2 * MAXC, (0.2, 0.7, 0.05, 0.0, 0.0, 0.05)), (50_000, 2 * MAXC, (0.3, 0.6, 0.1, 0.0, 0.0, 0.0)),
                     (45_000, 6 * MAXC // 5, (0.15, 0.7, 0.1, 0.05, 0.0, 0.0)), (50_000, 2 * MAXC, (0.2, 0.7, 0.05, 0.05, 0.0, 0.0))):
    pts, sides = polygon(convex_polygon(h), size)
    shops = pts[:MAXN]
    if len(pts) > MAXN:
        continue
    extra = MAXN - len(shops)
    shops = shuffled(shops + [on_side(sides[ri(0, len(sides) - 1)]) for _ in range(extra // 2)]
                     + [near_side(sides[ri(0, len(sides) - 1)], False, 10) for _ in range(extra - extra // 2)])
    add(shops, houses_for(pts, sides, MAXQ, mix))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

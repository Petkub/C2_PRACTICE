# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310001)
MAXN = 100_000
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


def add(pts):
    n = len(pts)
    assert 1 <= n <= MAXN
    assert all(-MAXC <= x <= MAXC and -MAXC <= y <= MAXC for x, y in pts)
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


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
    edges = sorted(((a, b, m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))
    return edges


def corners(edges, scale, x0, y0):
    x, y = x0, y0
    out = []
    for a, b, m in edges:
        out.append((x, y))
        x += a * m * scale
        y += b * m * scale
    assert (x, y) == (x0, y0)
    return out


def fit(edges):
    pts = corners(edges, 1, 0, 0)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    w = max(max(xs) - min(xs), max(ys) - min(ys))
    s = (2 * MAXC) // w
    return s, -MAXC - min(xs) * s, -MAXC - min(ys) * s


def side_points(edges, scale, x0, y0, cnt):
    pts = corners(edges, scale, x0, y0)
    cand = [i for i, e in enumerate(edges) if e[2] * scale > 1]
    out = []
    for _ in range(cnt):
        i = cand[ri(0, len(cand) - 1)]
        a, b, m = edges[i]
        t = ri(1, m * scale - 1)
        out.append((pts[i][0] + a * t, pts[i][1] + b * t))
    return out


def inside_points(pts, cnt, shrink=0.97):
    cx = sum(p[0] for p in pts) // len(pts)
    cy = sum(p[1] for p in pts) // len(pts)
    out = []
    for _ in range(cnt):
        p = pts[ri(0, len(pts) - 1)]
        f = random.random() * shrink
        out.append((cx + int((p[0] - cx) * f), cy + int((p[1] - cy) * f)))
    return out


add([(0, 0), (2, 0), (5, 0), (5, 3), (3, 4), (0, 4), (0, 2), (2, 2), (3, 1)])
add([(1, 1), (3, 3), (2, 2), (-1, -1)])
add([(7, -3)])
add([(0, 0), (6, 0), (0, 6), (3, 3), (2, 0), (0, 5), (1, 1), (2, 2), (4, 1)])
add([(-2, 1), (1, -3), (4, 0), (2, 4), (-1, 3), (0, 0), (1, 1), (3, 2)])
add([(4, 0), (4, 7), (4, 2), (4, -5)])

add([(5, 5), (5, 5)])
add([(MAXC, MAXC), (-MAXC, -MAXC), (MAXC, -MAXC), (-MAXC, MAXC), (0, 0), (MAXC, MAXC), (0, MAXC)])
add([(ri(-3, 3), ri(-3, 3)) for _ in range(12)])
add([(ri(-6, 6), ri(-6, 6)) for _ in range(60)])
add([(3 * k, -2 * k) for k in range(-20, 21)] + [(9, -6)] * 5)
add(shuffled([(x, y) for x in range(15) for y in range(15)] + [(0, 7)] * 3 + [(14, 0)] * 2))
add([(ri(-10**4, 10**4), ri(-10**4, 10**4)) for _ in range(3000)])
e = convex_polygon(400)
p = corners(e, 3, -500, 200)
add(shuffled(p + side_points(e, 3, -500, 200, 300) + inside_points(p, 500) + [p[ri(0, len(p) - 1)] for _ in range(50)]))

for h, side, inner, rep in ((90_000, 0, 5_000, 5_000), (60_000, 25_000, 10_000, 5_000),
                            (40_000, 40_000, 10_000, 10_000), (70_000, 10_000, 0, 20_000)):
    e = convex_polygon(h)
    s, x0, y0 = fit(e)
    p = corners(e, s, x0, y0)
    sp = side_points(e, s, x0, y0, side)
    extra = [p[ri(0, len(p) - 1)] for _ in range(rep // 2)] + [sp[ri(0, len(sp) - 1)] if sp else p[0] for _ in range(rep - rep // 2)]
    allp = p + sp + inside_points(p, inner) + extra
    add(shuffled(allp[:MAXN]))
M = 5_000
add([(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(M)])
p = [(k * 20_000 - MAXC, (k * 7) % 1000) for k in range(M // 2)]
add(shuffled(p + p))
q = [(ri(-MAXC, MAXC), 0) for _ in range(M - 2)] + [(-MAXC, 0), (MAXC, 0)]
add(shuffled(q))
for h, side, inner, rep in ((80_000, 15_000, 0, 5_000), (50_000, 30_000, 15_000, 5_000), (30_000, 50_000, 5_000, 15_000)):
    e = convex_polygon(h)
    s, x0, y0 = fit(e)
    p = corners(e, s, x0, y0)
    sp = side_points(e, s, x0, y0, side)
    extra = [p[ri(0, len(p) - 1)] for _ in range(rep // 2)] + [sp[ri(0, len(sp) - 1)] for _ in range(rep - rep // 2)]
    add(shuffled((p + sp + inside_points(p, inner) + extra)[:MAXN]))
e = convex_polygon(95_000)
s, x0, y0 = fit(e)
p = corners(e, s, x0, y0)
add(shuffled(p + [p[ri(0, len(p) - 1)] for _ in range(MAXN - len(p))]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

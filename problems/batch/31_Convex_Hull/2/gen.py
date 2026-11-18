# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310002)
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
    assert 3 <= n <= MAXN
    assert all(0 <= x <= MAXC and 0 <= y <= MAXC for x, y in pts)
    a = pts[0]
    b = next(q for q in pts if q != a)
    assert any((b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]) != 0 for q in pts)
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
    return sorted(((a, b, m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))


def corners(edges, scale, x0, y0):
    x, y = x0, y0
    out = []
    for a, b, m in edges:
        out.append((x, y))
        x += a * m * scale
        y += b * m * scale
    assert (x, y) == (x0, y0)
    return out


def placed(edges, size):
    pts = corners(edges, 1, 0, 0)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    w = max(max(xs) - min(xs), max(ys) - min(ys))
    s = max(1, size // w)
    x0 = ri(0, MAXC - (max(xs) - min(xs)) * s) - min(xs) * s
    y0 = ri(0, MAXC - (max(ys) - min(ys)) * s) - min(ys) * s
    return corners(edges, s, x0, y0)


def inside_points(pts, cnt, shrink=0.97):
    cx = sum(p[0] for p in pts) // len(pts)
    cy = sum(p[1] for p in pts) // len(pts)
    out = []
    for _ in range(cnt):
        p = pts[ri(0, len(pts) - 1)]
        f = random.random() * shrink
        out.append((cx + int((p[0] - cx) * f), cy + int((p[1] - cy) * f)))
    return out


add([(0, 0), (4, 0), (4, 2), (1, 3), (2, 1)])
add([(0, 0), (3, 0), (0, 3), (3, 0)])
add([(0, 0), (1, 0), (0, 1)])
add([(2, 5), (7, 1), (9, 9), (5, 5), (3, 3), (6, 2)])
add([(0, 0), (10, 1), (20, 2), (5, 0), (12, 1)])

add([(0, 0), (1, 1), (1, 0), (0, 1)])
add([(5, 5), (6, 7), (5, 5), (6, 7), (7, 9), (5, 6)])
add([(ri(0, 30), ri(0, 30)) for _ in range(20)])
add([(ri(100, 400), ri(200, 300)) for _ in range(300)])
add([(0, 0), (999, 1), (998, 0), (500, 0)])
p = placed(convex_polygon(40), 900)
add(shuffled(p + [p[3]] * 3 + inside_points(p, 20)))
add([(ri(0, 1000), ri(0, 1000)) for _ in range(2000)])

add([(0, 0), (MAXC, 0), (0, MAXC), (MAXC, MAXC), (MAXC // 2, MAXC // 2)])
add([(0, 0), (MAXC, 1), (MAXC - 1, 0)])
add([(0, 0), (MAXC, MAXC - 1), (1, 1), (MAXC // 3, MAXC // 3)])
add([(0, MAXC), (MAXC, 0), (MAXC, MAXC)])

for h, inner, rep, size in ((90_000, 5_000, 5_000, MAXC), (60_000, 30_000, 10_000, MAXC),
                            (30_000, 60_000, 10_000, MAXC), (70_000, 20_000, 10_000, 6 * MAXC // 10),
                            (5_000, 90_000, 5_000, MAXC)):
    p = placed(convex_polygon(h), size)
    extra = [p[ri(0, len(p) - 1)] for _ in range(rep)]
    add(shuffled((p + inside_points(p, inner) + extra)[:MAXN]))
add([(ri(0, MAXC), ri(0, MAXC)) for _ in range(MAXN)])
p = [(0, 0), (MAXC, 0), (MAXC, MAXC), (0, MAXC)]
p += [(ri(0, MAXC), 0) for _ in range(MAXN // 4)] + [(MAXC, ri(0, MAXC)) for _ in range(MAXN // 4)]
p += [(ri(1, MAXC - 1), ri(1, MAXC - 1)) for _ in range(MAXN // 2 - 4)]
add(shuffled(p))
p = [(k * 9_000, k * 9_000 // 7) for k in range(MAXN - 1)] + [(MAXC, 0)]
add(shuffled(p))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

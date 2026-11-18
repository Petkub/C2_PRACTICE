# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310006)
MAXN = 5_000
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
    assert 4 <= n <= MAXN and len(set(pts)) == n
    assert all(0 <= x <= MAXC and 0 <= y <= MAXC for x, y in pts)
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def convex_polygon(h, stretch=(1, 1)):
    r = int(math.sqrt(h / 2.2)) + 3
    prim = [(a, b) for a in range(-r, r + 1) for b in range(-r, r + 1) if (a, b) != (0, 0) and math.gcd(a, b) == 1]
    prim.sort(key=lambda v: (v[0] * v[0] + v[1] * v[1], v))
    prim = prim[:int(h * 1.25)]
    keep = {v: ri(1, 4) for v in prim if random.random() < 0.8}
    sx = sum(a * m for (a, b), m in keep.items())
    sy = sum(b * m for (a, b), m in keep.items())
    if sx or sy:
        g = math.gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        keep[d] = keep.get(d, 0) + g
    return sorted(((a * stretch[0], b * stretch[1], m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))


def placed(edges, size):
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
    x0 = ri(0, MAXC - (max(xs) - min(xs)) * s) - min(xs) * s
    y0 = ri(0, MAXC - (max(ys) - min(ys)) * s) - min(ys) * s
    return [(px * s + x0, py * s + y0) for px, py in raw]


def inside_points(pts, cnt, shrink=0.95):
    cx = sum(p[0] for p in pts) // len(pts)
    cy = sum(p[1] for p in pts) // len(pts)
    out = set()
    while len(out) < cnt:
        p = pts[ri(0, len(pts) - 1)]
        f = random.random() * shrink
        out.add((cx + int((p[0] - cx) * f), cy + int((p[1] - cy) * f)))
    return sorted(out - set(pts))


add([(0, 0), (4, 0), (5, 3), (2, 5), (0, 3), (2, 2)])
add([(0, 0), (6, 0), (0, 6), (1, 1), (2, 3)])
add([(0, 0), (1, 1), (2, 2), (5, 5)])
add([(1, 0), (3, 0), (4, 2), (3, 4), (1, 4), (0, 2)])
add([(0, 0), (10, 1), (9, 3), (1, 2), (5, 1)])

add([(0, 0), (MAXC, 0), (MAXC, MAXC), (0, MAXC)])
add([(0, 0), (MAXC, 1), (MAXC - 1, 0), (5, 2)])
add(sorted(set((ri(0, 6), ri(0, 6)) for _ in range(20))))
add(sorted(set((ri(0, 100), ri(0, 100)) for _ in range(40))))
add(shuffled(placed(convex_polygon(40), 1000)))
p = placed(convex_polygon(30), MAXC)
add(shuffled(p + inside_points(p, 15)))
add(sorted(set((ri(0, MAXC), ri(0, MAXC)) for _ in range(60))))
add([(k, k * k) for k in range(45)])

add(sorted(set((ri(0, MAXC), ri(0, MAXC)) for _ in range(MAXN))))
add(shuffled(placed(convex_polygon(800), MAXC)))

for h, inner, stretch in ((5_000, 0, (1, 1)), (4_800, 200, (1, 1)), (5_000, 0, (7, 1)), (4_900, 100, (1, 3)),
                          (5_000, 0, (1, 1)), (4_500, 500, (2, 5)), (5_000, 0, (11, 2)), (4_950, 50, (1, 1)),
                          (5_000, 0, (1, 1)), (5_000, 0, (3, 1))):
    p = placed(convex_polygon(h, stretch), MAXC)
    p = sorted(set(p))[:MAXN - inner]
    p = sorted(set(p))
    while len(p) > MAXN - inner:
        p.pop(ri(0, len(p) - 1))
    q = inside_points(p, inner)
    add(shuffled(p + q[:MAXN - len(p)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

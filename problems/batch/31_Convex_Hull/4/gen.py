# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310004)
MAXN, MAXQ = 50_000, 150_000
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


def add(trees, dirs):
    n, q = len(trees), len(dirs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXC <= x <= MAXC and -MAXC <= y <= MAXC for x, y in trees)
    assert all(-MAXC <= a <= MAXC and -MAXC <= b <= MAXC and (a, b) != (0, 0) for a, b in dirs)
    tests.append(f"{n} {q}\n" + "".join(f"{x} {y}\n" for x, y in trees) + "".join(f"{a} {b}\n" for a, b in dirs))


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
    return [(px * s + ox, py * s + oy) for px, py in raw]


def inside_points(pts, cnt, shrink=0.97):
    cx = sum(p[0] for p in pts) // len(pts)
    cy = sum(p[1] for p in pts) // len(pts)
    out = []
    for _ in range(cnt):
        p = pts[ri(0, len(pts) - 1)]
        f = random.random() * shrink
        out.append((cx + int((p[0] - cx) * f), cy + int((p[1] - cy) * f)))
    return out


def directions(edges, q, big):
    out = []
    for _ in range(q):
        r = random.random()
        if r < 0.5:
            a, b, m = edges[ri(0, len(edges) - 1)]
            k = ri(1, max(1, big // max(abs(a), abs(b))))
            out.append((b * k, -a * k) if random.random() < 0.5 else (-b * k, a * k))
        elif r < 0.6:
            out.append(random.choice([(1, 0), (0, 1), (-1, 0), (0, -1), (MAXC, 0), (0, -MAXC), (MAXC, MAXC), (-MAXC, MAXC)]))
        else:
            out.append((ri(-big, big), ri(-big, big)) if random.random() < 0.9 else (ri(-9, 9), ri(-9, 9)))
            if out[-1] == (0, 0):
                out[-1] = (1, 1)
    return out


add([(0, 0), (4, 0), (4, 3), (1, 4), (2, 2)], [(1, 0), (0, 1), (1, 1), (1, -1), (-2, 3)])
add([(-3, 1), (5, -2), (5, -2)], [(2, 1), (0, -1), (3, 8)])
add([(7, 7)], [(1000000000, -1000000000), (1, 2)])
add([(0, 0), (2, 0), (4, 0), (6, 3), (2, 6), (0, 4), (3, 3)], [(1, 2), (-3, 1), (0, 5), (2, -1)])
add([(-1000000000, -1000000000), (1000000000, 1000000000), (1000000000, -1000000000), (0, 999999999)],
    [(1000000000, 1000000000), (-1000000000, 1000000000), (1, 0)])

add([(ri(-5, 5), ri(-5, 5)) for _ in range(10)], [(ri(1, 5), ri(-5, 5)) for _ in range(30)])
add([(3 * k, -2 * k) for k in range(-20, 21)], [(2, 3), (-2, -3), (1, 0), (3, -2), (0, 1)])
e = convex_polygon(30)
p = polygon(e, 2_000)
add(shuffled(p + inside_points(p, 50)), directions(e, 500, 1000))
e = convex_polygon(500)
p = polygon(e, 2 * MAXC)
add(shuffled(p + inside_points(p, 1000)), directions(e, 2000, MAXC))
add([(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(3000)], [(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(3000)])
add([(-MAXC, -MAXC), (MAXC, MAXC), (-MAXC, MAXC), (MAXC, -MAXC)], [(MAXC, MAXC), (MAXC, -MAXC), (-MAXC, -MAXC), (MAXC, 1)])

for h, inner, size in ((50_000, 0, 2 * MAXC), (48_000, 2_000, 2 * MAXC), (50_000, 0, MAXC), (40_000, 10_000, 2 * MAXC),
                       (50_000, 0, 2 * MAXC), (45_000, 5_000, 2 * MAXC // 3), (50_000, 0, 2 * MAXC), (46_000, 4_000, 2 * MAXC)):
    e = convex_polygon(h)
    p = polygon(e, size)
    if len(p) > MAXN:
        p = p[:MAXN]
    p = shuffled(p + inside_points(p, min(inner, MAXN - len(p))))
    d = directions(e, MAXQ - 3_000, 1_000) + directions(e, 3_000, MAXC)
    add(p, shuffled(d))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

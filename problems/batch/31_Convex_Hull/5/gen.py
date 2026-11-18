# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310005)
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
    assert 2 <= n <= MAXN
    assert all(-MAXC <= x <= MAXC and -MAXC <= y <= MAXC for x, y in pts)
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in pts))


def primitive(r):
    prim = [(a, b) for a in range(-r, r + 1) for b in range(-r, r + 1) if (a, b) != (0, 0) and math.gcd(a, b) == 1]
    prim.sort(key=lambda v: (v[0] * v[0] + v[1] * v[1], v))
    return prim


def convex_polygon(h):
    prim = primitive(int(math.sqrt(h / 2.2)) + 3)[:int(h * 1.25)]
    keep = {v: 1 for v in prim if random.random() < 0.8}
    sx = sum(a * m for (a, b), m in keep.items())
    sy = sum(b * m for (a, b), m in keep.items())
    if sx or sy:
        g = math.gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        keep[d] = keep.get(d, 0) + g
    return sorted(((a, b, m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))


def symmetric_polygon(h, fold):
    r = int(math.sqrt(h / 2.2)) + 3
    if fold == 2:
        base = [v for v in primitive(r) if v[1] > 0 or (v[1] == 0 and v[0] > 0)]
    elif fold == 4:
        base = [v for v in primitive(r) if v[0] > 0 and v[1] >= 0]
    else:
        base = [v for v in primitive(r) if v[0] > 0 and 0 <= v[1] <= v[0]]
    keep = {}
    for a, b in base:
        if len(keep) >= h:
            break
        m = ri(1, 3)
        imgs = [(a, b), (-a, -b)]
        if fold >= 4:
            imgs += [(-b, a), (b, -a)]
        if fold >= 8:
            imgs += [(b, a), (-b, -a), (-a, b), (a, -b)]
        for v in imgs:
            keep[v] = m
    return sorted(((a, b, m) for (a, b), m in keep.items()), key=functools.cmp_to_key(by_angle))


def corners(edges, size):
    x = y = 0
    raw = []
    for a, b, m in edges:
        raw.append((x, y))
        x += a * m
        y += b * m
    assert (x, y) == (0, 0)
    xs = [p[0] for p in raw]
    ys = [p[1] for p in raw]
    w = max(max(xs) - min(xs), max(ys) - min(ys))
    s = max(1, size // w)
    ox = -(max(xs) + min(xs)) * s // 2
    oy = -(max(ys) + min(ys)) * s // 2
    return [(px * s + ox, py * s + oy) for px, py in raw]


def circle(R, primes):
    gauss = {5: (2, 1), 13: (3, 2), 17: (4, 1), 29: (5, 2), 37: (6, 1), 41: (5, 4), 53: (7, 2)}
    zs = [(1, 0)]
    for p in primes:
        a, b = gauss[p]
        sq = (a * a - b * b, 2 * a * b)
        choices = [sq, (sq[0], -sq[1]), (p, 0)]
        zs = [(x * c - y * d, x * d + y * c) for x, y in zs for c, d in choices]
    out = set()
    for x, y in zs:
        for u, v in ((x, y), (-y, x), (-x, -y), (y, -x)):
            out.add((u, v))
    assert all(x * x + y * y == R * R for x, y in out)
    return sorted(out)


def inside_points(pts, cnt, shrink=0.9):
    out = []
    for _ in range(cnt):
        p = pts[ri(0, len(pts) - 1)]
        f = random.random() * shrink
        out.append((int(p[0] * f), int(p[1] * f)))
    return out


def farthest_corners(pts):
    return sorted(pts, key=lambda p: -(p[0] * p[0] + p[1] * p[1]))[:4]


add([(0, 0), (4, 1), (1, 3), (2, 2), (-1, 1)])
add([(1, 1), (5, 4), (2, 5), (4, 0)])
add([(3, 3), (3, 3), (3, 3)])
add([(5, 0), (0, 5), (-5, 0), (0, -5), (3, 4), (-3, -4), (1, 1)])
add([(-2, 7), (6, 7), (2, 7), (2, 9)])

add([(0, 0), (0, 0), (1, 1), (1, 1), (1, 0)])
add([(0, 0), (2, 0), (2, 1), (0, 1)])
add([(MAXC, MAXC), (-MAXC, -MAXC), (MAXC, -MAXC), (-MAXC, MAXC), (MAXC, MAXC)])
add(shuffled(circle(5 * 13 * 17, [5, 13, 17]) + [(0, 0)] * 3 + [(1, 2)]))
c = circle(5 * 13 * 17 * 29 * 37 * 41, [5, 13, 17, 29, 37, 41])
add(shuffled(c + inside_points(c, 1000) + [c[0]] * 2 + [c[len(c) // 2]] * 3))
add([(7, -7)] * 2500)
p = corners(symmetric_polygon(400, 8), MAXC)
add(shuffled(p + inside_points(p, 300) + farthest_corners(p) * 2))

for h, kind, inner, rep in ((99_000, 0, 0, 1_000), (98_000, 8, 500, 1_000), (98_000, 4, 1_000, 1_000),
                            (98_000, 2, 0, 2_000), (97_000, 0, 1_000, 2_000), (99_000, 8, 0, 0),
                            (98_000, 4, 0, 2_000), (98_000, 2, 1_000, 1_000)):
    e = convex_polygon(h) if kind == 0 else symmetric_polygon(h, kind)
    p = corners(e, 2 * MAXC)
    extra = farthest_corners(p)
    p = p[:MAXN - inner - rep]
    reps = [extra[ri(0, len(extra) - 1)] for _ in range(rep)]
    add(shuffled(p + reps + inside_points(p, inner)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

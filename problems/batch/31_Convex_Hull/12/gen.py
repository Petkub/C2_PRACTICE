# Test generator of this problem (the judge runs it to rebuild the big tests).
import math, os, random

random.seed(310012)
MAXN, MAXQ = 50_000, 80_000
MAXC = 10**9
tests = []


_bits = random.getrandbits


def ri(lo, hi):
    return lo + _bits(64) % (hi - lo + 1)


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = _bits(64) % (i + 1)
        a[i], a[j] = a[j], a[i]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def add(stakes, pegs):
    n, q = len(stakes), len(pegs)
    assert 3 <= n <= MAXN and 1 <= q <= MAXQ
    vals = [v for s in stakes + pegs for v in s]
    assert -MAXC <= min(vals) and max(vals) <= MAXC
    a = stakes[0]
    b = next(s for s in stakes if s != a)
    assert any(cross(a, b, s) != 0 for s in stakes)
    tests.append(f"{n} {q}\n" + "".join(["%d %d\n" % s for s in stakes]) + "".join(["%d %d\n" % s for s in pegs]))


def angle_key(v):
    x, y = v[0], v[1]
    k = 0
    while not (x > 0 and y >= 0):
        x, y = y, -x
        k += 1
    return (k, y * 10**15 // x)


R0 = 185
PRIM = [(a, b) for a in range(-R0, R0 + 1) for b in range(-R0, R0 + 1) if (a, b) != (0, 0) and math.gcd(a, b) == 1]
PRIM.sort(key=lambda v: (v[0] ** 2 + v[1] ** 2, v))
PRIM = [v for v in PRIM if v[0] ** 2 + v[1] ** 2 <= R0 * R0]


def convex_polygon(h, flat=1):
    prim = [(a * flat // math.gcd(flat, b), b // math.gcd(flat, b)) for a, b in PRIM[:h * 5 // 4]]
    keep = {}
    for v in prim:
        if ri(0, 9) < 8:
            keep[v] = 1
    sx = sum(a * m for (a, b), m in keep.items())
    sy = sum(b * m for (a, b), m in keep.items())
    if sx or sy:
        g = math.gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        keep[d] = keep.get(d, 0) + g
    return sorted(((a, b, m) for (a, b), m in keep.items()), key=angle_key)


def polygon(edges, size, cx=0, cy=0):
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
    ox = cx - (max(xs) + min(xs)) * s // 2
    oy = cy - (max(ys) + min(ys)) * s // 2
    pts = [(px * s + ox, py * s + oy) for px, py in raw]
    sides = [(pts[i], edges[i][0], edges[i][1], edges[i][2] * s) for i in range(len(edges))]
    return pts, sides


def inside(pts, cnt):
    cx = sum(p[0] for p in pts) // len(pts)
    cy = sum(p[1] for p in pts) // len(pts)
    out = []
    for _ in range(cnt):
        p = pts[ri(0, len(pts) - 1)]
        f = ri(0, 960)
        out.append((cx + (p[0] - cx) * f // 1000, cy + (p[1] - cy) * f // 1000))
    return out


def ok(p):
    return -MAXC <= p[0] <= MAXC and -MAXC <= p[1] <= MAXC


def peg(sides, kind, lim):
    while True:
        (x, y), a, b, L = sides[ri(0, len(sides) - 1)]
        if kind == "on":
            t = ri(0, L)
            p = (x + a * t, y + b * t)
        elif kind == "near":
            t, d = ri(0, L), ri(1, 3)
            p = (x + a * t + b * d, y + b * t - a * d)
        elif kind == "line":
            k = ri(1, max(1, lim // max(1, abs(a) + abs(b)) // ri(1, 50)))
            p = (x + a * (L + k), y + b * (L + k)) if ri(0, 1) else (x - a * k, y - b * k)
        if ok(p):
            return p


def far(cnt, lim):
    out = [(ri(-lim, lim), ri(-lim, lim)) for _ in range(cnt)]
    for i in range(0, cnt, 4):
        x, y = out[i]
        out[i] = (lim if x > 0 else -lim, y) if y & 1 else (x, lim if y > 0 else -lim)
    return out


def pegs(pts, sides, q, mix, lim=MAXC):
    out = inside(pts, q * mix[0] // 100)
    for kind, f in zip(("on", "near", "line"), mix[1:4]):
        out += [peg(sides, kind, lim) for _ in range(q * f // 100)]
    out += [pts[ri(0, len(pts) - 1)] for _ in range(q * mix[5] // 100)]
    out += far(q - len(out), lim)
    shuffle(out)
    return out


add([(0, 0), (4, 0), (5, 3), (2, 5), (0, 3), (2, 2)], [(2, 2), (1, 4), (5, 0), (4, 5)])
add([(0, 0), (6, 0), (0, 4), (3, 0)], [(3, 1), (9, 0), (6, -2), (-1, 0)])
add([(2, 1), (2, 1), (5, 1), (2, 4), (3, 2)], [(3, 2), (5, 4), (6, 0), (0, 3)])
add([(-1000000000, -1000000000), (1000000000, -1000000000), (1000000000, 1000000000), (0, 0)],
    [(-1000000000, 1000000000), (0, 1000000000), (999999999, -999999999)])
add([(1, 1), (3, 1), (3, 3), (1, 3)], [(2, 2), (5, 1), (1, 5)])

for R, n, q in ((3, 6, 60), (5, 10, 80), (20, 12, 100)):
    while True:
        p = [(ri(-R, R), ri(-R, R)) for _ in range(n)]
        if any(cross(p[0], p[1], s) != 0 for s in p):
            break
    add(p, [(ri(-R - 4, R + 4), ri(-R - 4, R + 4)) for _ in range(q)])
add([(-MAXC, -MAXC), (MAXC, -MAXC), (MAXC, MAXC), (-MAXC, MAXC - 1), (0, 0), (0, 0)],
    [(-MAXC, MAXC), (0, MAXC), (MAXC, 0), (-MAXC, -MAXC), (1, MAXC), (-MAXC + 1, MAXC)])
e = convex_polygon(40)
p, sd = polygon(e, 600)
add(p + inside(p, 20), pegs(p, sd, 400, (10, 15, 20, 20, 30, 5), 400))
e = convex_polygon(2_000)
p, sd = polygon(e, 2 * MAXC)
add(p + inside(p, 500), pegs(p, sd, 5_000, (10, 10, 20, 20, 35, 5)))
pts = [(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(5_000)]
add(pts, [(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(5_000)])
shapes = {}

for h, inner, size, c, flat, mix, lim in (
        (50_000, 0, 2 * MAXC, 0, 1, (5, 5, 10, 10, 65, 5), MAXC),
        (48_000, 2_000, 2 * MAXC, 0, 1, (10, 10, 20, 20, 35, 5), MAXC),
        (50_000, 0, 4 * 10**8, 0, 1, (5, 5, 10, 10, 70, 0), MAXC),
        (50_000, 0, 3 * 10**8, 6 * 10**8, 1, (0, 5, 5, 10, 80, 0), MAXC),
        (45_000, 5_000, MAXC, 0, 3, (10, 10, 15, 15, 50, 0), MAXC),
        (50_000, 0, 2 * MAXC, 0, 1, (0, 20, 30, 30, 20, 0), MAXC),
        (50_000, 0, 5 * 10**8, -4 * 10**8, 2, (5, 5, 10, 10, 70, 0), MAXC),
        (40_000, 10_000, 2 * MAXC, 0, 1, (20, 10, 10, 10, 50, 0), MAXC),
        (50_000, 0, 2 * 10**8, 0, 1, (0, 0, 5, 5, 90, 0), MAXC),
        (50_000, 0, 2 * MAXC, 0, 4, (5, 5, 10, 10, 70, 0), MAXC)):
    if (h, flat) not in shapes:
        shapes[(h, flat)] = convex_polygon(h, flat)
    p, sd = polygon(shapes[(h, flat)], size, c, -c)
    if len(p) > MAXN:
        k = len(p) - MAXN
        p = p[k:]
        sd = sd[k:-1]
    st = p + inside(p, min(inner, MAXN - len(p)))
    shuffle(st)
    add(st, pegs(p, sd, MAXQ, mix, lim))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

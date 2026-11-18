# Test generator of this problem (the judge runs it to rebuild the big tests).
import math, os, random

random.seed(310011)
MAXN, MAXQ = 100_000, 100_000
MAXC = 10**9
tests = []
_bits = random.getrandbits


def ri(lo, hi):
    return lo + _bits(64) % (hi - lo + 1)


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = _bits(64) % (i + 1)
        a[i], a[j] = a[j], a[i]


def add(pts, qs):
    n, q = len(pts), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    vals = [v for s in pts for v in s] + [v for t in qs for v in t[2:]]
    assert -MAXC <= min(vals) and max(vals) <= MAXC
    assert all(1 <= l <= r <= n and (a, b) != (0, 0) for l, r, a, b in qs)
    t = f"{n} {q}\n" + "".join(["%d %d\n" % s for s in pts]) + "".join(["%d %d %d %d\n" % s for s in qs])
    assert len(t) <= 3_000_000
    tests.append(t)


def angle_key(v):
    x, y = v[0], v[1]
    k = 0
    while not (x > 0 and y >= 0):
        x, y = y, -x
        k += 1
    return (k, y * 10**15 // x)


R0 = 215
PRIM = [(a, b) for a in range(-R0, R0 + 1) for b in range(-R0, R0 + 1) if (a, b) != (0, 0) and math.gcd(a, b) == 1]
PRIM.sort(key=lambda v: (v[0] ** 2 + v[1] ** 2, v))
PRIM = [v for v in PRIM if v[0] ** 2 + v[1] ** 2 <= R0 * R0]
RANK = {v: i for i, v in enumerate(sorted(PRIM, key=angle_key))}


def convex_polygon(h, flat=1):
    keep = [v for v in PRIM[:h * 5 // 4] if ri(0, 9) < 8]
    keep.sort(key=RANK.__getitem__)
    edges = [(a * flat // math.gcd(flat, b), b // math.gcd(flat, b), 1) for a, b in keep]
    sx = sum(e[0] for e in edges)
    sy = sum(e[1] for e in edges)
    if sx or sy:
        g = math.gcd(abs(sx), abs(sy))
        d = (-sx // g, -sy // g)
        k = next((i for i, e in enumerate(edges) if (e[0], e[1]) == d), -1)
        if k >= 0:
            edges[k] = (d[0], d[1], 1 + g)
        else:
            edges.append((d[0], d[1], g))
            edges.sort(key=angle_key)
    return edges


def polygon(edges, size, h):
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
    return [(px * s + ox, py * s + oy) for px, py in raw[:h]]


def dirs(cnt, big, edges=None, normal=0):
    out = []
    for _ in range(cnt):
        if edges and ri(0, 99) < normal:
            a, b, m = edges[ri(0, len(edges) - 1)]
            k = ri(1, max(1, big // max(abs(a), abs(b))))
            out.append((b * k, -a * k) if ri(0, 1) else (-b * k, a * k))
        else:
            v = (ri(-big, big), ri(-big, big))
            out.append(v if v != (0, 0) else (1, 0))
    return out


def ranges(n, cnt, kind):
    out = []
    for _ in range(cnt):
        if kind == "long":
            out.append((ri(1, max(1, n // 20)), ri(n - n // 20, n)))
        elif kind == "wide":
            out.append((ri(1, max(1, n // 8)), ri(n - n // 8, n)))
        elif kind == "full":
            out.append((1, n))
        else:
            l, r = ri(1, n), ri(1, n)
            out.append((min(l, r), max(l, r)))
    return out


def queries(n, cnt, kind, big, edges=None, normal=0):
    return [(l, r, a, b) for (l, r), (a, b) in zip(ranges(n, cnt, kind), dirs(cnt, big, edges, normal))]


add([(3, 1), (1, 4), (-2, 2), (5, -1), (0, 0)], [(1, 3, 1, 1), (2, 5, 2, -1), (3, 3, -1, 5), (1, 5, -1, 0)])
add([(0, 0), (4, 1), (1, 3)], [(1, 3, 0, 1), (1, 2, -3, -1), (2, 3, 2, 2)])
add([(-1000000000, 1000000000), (1000000000, 1000000000), (7, -3)], [(1, 2, 1000000000, 1000000000), (1, 3, -1000000000, 1000000000), (3, 3, 2, -1000000000)])
add([(2, 2), (2, 2), (-1, -1), (4, 4)], [(1, 2, -1, 1), (2, 3, 3, 1), (1, 4, -1, -1), (3, 4, 1, -1)])
add([(5, 0), (0, 5), (-5, 0), (0, -5), (1, 1)], [(1, 4, 1, 2), (2, 5, -2, -1), (2, 4, 0, -7), (5, 5, 4, 4)])

add([(7, -7)], [(1, 1, 1, 0), (1, 1, -3, 4), (1, 1, 0, -1)])
p = [(ri(-5, 5), ri(-5, 5)) for _ in range(8)]
add(p, [(l, r, a, b) for l in range(1, 9) for r in range(l, 9) for a, b in ((ri(-5, 5), ri(1, 5)), (ri(-5, 5), ri(-5, -1)))])
e = convex_polygon(30)
p = polygon(e, 1000, 30)
add(p, queries(len(p), 300, "any", 10, e, 40))
p = [(3 * k - 40, -2 * k + 7) for k in range(50)]
shuffle(p)
add(p, queries(50, 300, "any", 9, [(3, -2, 1)], 50))
add([(ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(5_000)], queries(5_000, 5_000, "any", MAXC))
e = convex_polygon(3_000)
p = polygon(e, 2 * MAXC, 3_000)
add(p, queries(len(p), 5_000, "any", MAXC, e, 50))
corners = [(-MAXC, -MAXC), (MAXC, -MAXC), (MAXC, MAXC), (-MAXC, MAXC)]
add([corners[ri(0, 3)] for _ in range(2_000)], queries(2_000, 3_000, "any", MAXC))

N, Q, SIZE, BIG = 70_000, 85_000, 2 * 10**7, 999
shapes = [convex_polygon(N), convex_polygon(N), convex_polygon(N, 3)]
for i, kind in enumerate(("order", "reverse", "shuffled", "rotated", "random", "rings", "parabola", "full", "flat", "mixed")):
    e = shapes[2] if kind == "flat" else shapes[i % 2]
    p = polygon(e, SIZE, N)
    qk = "full" if kind == "full" else ("wide" if kind == "rotated" else "long")
    if kind == "reverse":
        p.reverse()
    elif kind == "shuffled":
        shuffle(p)
    elif kind == "rotated":
        k = ri(0, N - 1)
        p = p[k:] + p[:k]
    elif kind == "random":
        p = [(ri(-SIZE // 2, SIZE // 2), ri(-SIZE // 2, SIZE // 2)) for _ in range(N)]
    elif kind == "rings":
        inner = [(x // 2, y // 2) for x, y in p[::2]]
        p = [v for pair in zip(p[1::2], inner) for v in pair]
    elif kind == "parabola":
        p = [(x, -x * x // 2) for x in range(-N // 2, N // 2)]
        shuffle(p)
    elif kind == "mixed":
        p = p[:N // 2] + [(x // 3, y // 3) for x, y in p[N // 2:]]
        shuffle(p)
    qs = queries(len(p), Q, qk, BIG, e, 40)
    add(p, qs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

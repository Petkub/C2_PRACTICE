# Test generator of this problem (the judge runs it to rebuild the big tests).
import functools, math, os, random

random.seed(310007)
MAXN, MAXQ = 20_000, 130_000
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


def add(seeds, qs):
    n, q = len(seeds), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(set(seeds)) == n
    assert all(-MAXC <= x <= MAXC and -MAXC <= y <= MAXC for x, y in seeds + qs)
    tests.append(f"{n} {q}\n" + "".join(f"{x} {y}\n" for x, y in seeds) + "".join(f"{x} {y}\n" for x, y in qs))


def base_shape(m):
    while True:
        r = 3 + m
        cand = [(a, b) for a in range(-r, r + 1) for b in range(-r, r + 1) if (a, b) != (0, 0)]
        pts = random.sample(cand, m)
        pts.sort(key=functools.cmp_to_key(by_angle))
        ok = True
        for i in range(m):
            a, b, c = pts[i - 2], pts[i - 1], pts[i]
            if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) <= 0:
                ok = False
            if a[0] * b[1] - a[1] * b[0] <= 0:
                ok = False
        if ok:
            return pts


def onion(shape, layers, s, side_every=0, side_cnt=1, first=1):
    seeds = []
    m = len(shape)
    for k in range(first, layers + 1):
        f = k * s
        cs = [(x * f, y * f) for x, y in shape]
        seeds += cs
        if side_every and k % side_every == 0:
            for _ in range(side_cnt):
                i = ri(0, m - 1)
                a, b = cs[i], cs[(i + 1) % m]
                g = math.gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
                t = ri(1, g - 1)
                seeds.append((a[0] + (b[0] - a[0]) // g * t, a[1] + (b[1] - a[1]) // g * t))
    return sorted(set(seeds))


def onion_queries(shape, layers, s, q, deep=0.8):
    out = []
    m = len(shape)
    for _ in range(q):
        r = random.random()
        k = ri(1, max(1, layers // 20)) if r < deep else ri(1, layers + 1)
        f = k * s
        i = ri(0, m - 1)
        a, b = shape[i], shape[(i + 1) % m]
        t = random.random()
        x = int((a[0] + (b[0] - a[0]) * t) * f)
        y = int((a[1] + (b[1] - a[1]) * t) * f)
        if random.random() < 0.3:
            x, y = a[0] * f, a[1] * f
        x += ri(-1, 1)
        y += ri(-1, 1)
        out.append((max(-MAXC, min(MAXC, x)), max(-MAXC, min(MAXC, y))))
    return out


add([(0, 0), (4, 0), (4, 4), (0, 4), (1, 1), (3, 1), (2, 3)], [(2, 2), (1, 2), (5, 5)])
add([(0, 0), (8, 0), (4, 6), (3, 2), (5, 2)], [(4, 2), (4, 1), (9, 9)])
add([(5, -5)], [(5, -5)])
add([(-3, 0), (0, -3), (3, 0), (0, 3), (-1, 0), (1, 1)], [(0, 0), (2, 1)])
add([(0, 0), (10, 2), (4, 8), (5, 3)], [(5, 3), (8, 6)])

add([(x, y) for x in range(5) for y in range(5)], [(x, y) for x in range(-1, 6) for y in range(-1, 6)])
add([(k, 2 * k) for k in range(-6, 7)], [(0, 0), (1, 2), (1, 1), (6, 12), (7, 14), (-6, -12)])
add(sorted(set((ri(-8, 8), ri(-8, 8)) for _ in range(60))), [(ri(-9, 9), ri(-9, 9)) for _ in range(300)])
sh = base_shape(4)
add(onion(sh, 30, 2, 3, 2) + [(0, 0)], onion_queries(sh, 30, 2, 500))
sh = base_shape(5)
add(onion(sh, 200, 50, 4, 3), onion_queries(sh, 200, 50, 2_000))
c = [(0, 0), (1, 0), (2, 0), (-1, 0), (-2, 0)]
sh = [(-3, -2), (4, -1), (1, 3)]
add(onion(sh, 100, 5) + c, onion_queries(sh, 100, 5, 1_000) + c + [(3, 0), (0, 1)])


for m, inner, outer, side_cnt, deep in ((3, 4_000, 10, 790, 0.9), (3, 4_000, 8, 990, 0.95), (4, 3_000, 10, 790, 0.9),
                                        (3, 4_300, 0, 0, 0.9), (3, 3_800, 20, 420, 0.85), (4, 3_000, 4, 1_990, 0.9),
                                        (3, 4_000, 10, 790, 0.97), (5, 2_500, 10, 740, 0.9)):
    sh = base_shape(m)
    layers = inner + outer
    s = MAXC // (layers * max(max(abs(x), abs(y)) for x, y in sh))
    seeds = onion(sh, inner, s) + onion(sh, layers, s, 1, side_cnt, inner + 1)
    seeds = sorted(set(seeds + [(0, 0), (1, 0), (-1, 0), (2, 0), (0, 1)]))
    assert len(seeds) <= MAXN
    add(shuffled(seeds), onion_queries(sh, inner, s, MAXQ, deep))
p = sorted(set((ri(-MAXC, MAXC), ri(-MAXC, MAXC)) for _ in range(MAXN)))
add(shuffled(p), [(ri(-MAXC // 50, MAXC // 50), ri(-MAXC // 50, MAXC // 50)) for _ in range(MAXQ // 2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

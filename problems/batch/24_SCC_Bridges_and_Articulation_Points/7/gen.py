# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(2407)
MAXN, MAXC, MAXR = 10_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(pts, shuffle=True):
    pts = list(pts)
    if shuffle:
        random.shuffle(pts)
    n = len(pts)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXC and 0 <= y <= MAXC and 0 <= r <= MAXR for x, y, r in pts)
    assert len(set((x, y) for x, y, r in pts)) == n
    tests.append(f"{n}\n" + "".join(f"{x} {y} {r}\n" for x, y, r in pts))


def one_way_chain(n, x0, y0, g0, step, horizontal=True):
    """points along a line with shrinking gaps; each one sets off only the next one"""
    pts, pos = [], 0
    for i in range(n):
        g = g0 - step * i
        assert g > step
        p = (x0 + pos, y0) if horizontal else (x0, y0 + pos)
        pts.append((p[0], p[1], g + step // 2))
        pos += g
    return pts


def clusters(k, per, spread, links):
    """k clusters on a jittered grid with spacing 40 * spread (everyone inside a cluster sets off everyone else in
    it); links one-way links between neighbouring grid clusters, from the cluster with the lower random rank:
    the firecracker of cluster a nearest to b gets the radius that just reaches the nearest firecracker of b"""
    side = 1
    while side * side < k:
        side += 1
    S = 40 * spread
    assert side * S + 2 * S <= MAXC
    cells = [(gx, gy) for gx in range(side) for gy in range(side)][:k]
    rank = list(range(k))
    random.shuffle(rank)
    cl, at = [], {}
    for idx, (gx, gy) in enumerate(cells):
        cx = S + gx * S + ri(-spread, spread)
        cy = S + gy * S + ri(-spread, spread)
        pts = set()
        while len(pts) < per:
            pts.add((cx + ri(-spread, spread), cy + ri(-spread, spread)))
        cl.append([[x, y, 3 * spread] for x, y in sorted(pts)])
        at[(gx, gy)] = idx
    def d2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    for _ in range(links):
        a = ri(0, k - 1)
        gx, gy = cells[a]
        dx, dy = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        if (gx + dx, gy + dy) not in at:
            continue
        b = at[(gx + dx, gy + dy)]
        if rank[a] > rank[b]:
            a, b = b, a
        cb = (sum(q[0] for q in cl[b]) / per, sum(q[1] for q in cl[b]) / per)
        p = min(cl[a], key=lambda q: d2(q, cb))
        q = min(cl[b], key=lambda t: d2(p, t))
        dd = d2(p, q)
        r = int(dd ** 0.5)
        while r * r < dd:
            r += 1
        p[2] = max(p[2], r)
    return [tuple(p) for c in cl for p in c]


def chain_ending_at(n, xend, y, g0, step):
    """one_way_chain shifted so that its last firecracker is at (xend, y)"""
    ch = one_way_chain(n, 0, y, g0, step)
    sh = xend - ch[-1][0]
    assert sh >= 0
    return [(x + sh, yy, r) for x, yy, r in ch]


def blob(n, x0, y0, cols, gap):
    """n firecrackers on a grid with the given number of columns and spacing gap, radius gap: each one sets off
    its grid neighbours, so all of them end up in one group"""
    return [(x0 + gap * (i % cols), y0 + gap * (i // cols), gap) for i in range(n)]


def reach_to(p, q):
    """p with its radius raised just enough to set off q"""
    dd = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    r = int(dd ** 0.5)
    while r * r < dd:
        r += 1
    while r > 0 and (r - 1) * (r - 1) >= dd:
        r -= 1
    assert r <= MAXR
    return (p[0], p[1], max(p[2], r))


def rand_pts(n, lo_r, hi_r, box=MAXC):
    s = set()
    while len(s) < n:
        s.add((ri(0, box), ri(0, box)))
    return [(x, y, ri(lo_r, hi_r)) for x, y in sorted(s)]


# samples
add([(0, 0, 3), (3, 0, 4), (6, 0, 1), (6, 5, 5)], False)
add([(1, 1, 2), (2, 2, 2), (10, 10, 2), (11, 11, 2), (20, 20, 0)], False)
add([(5, 5, 0)], False)
add([(0, 0, 10), (3, 4, 5), (6, 8, 5)], False)
add([(0, 0, 1), (2, 0, 1), (4, 0, 2), (6, 0, 2)], False)
add([(0, 0, 2), (2, 0, 2), (4, 0, 1), (0, 3, 3), (9, 9, 20), (30, 30, 0)], False)
# hidden: small
for n, hi in ((5, 6), (7, 10), (8, 8), (10, 12), (12, 15)):
    add(rand_pts(n, 0, hi, 12))
add(clusters(6, 2, 3, 4))
add(rand_pts(500, 0, 60_000_000))
add(clusters(150, 10, 1000, 200))
add([(x, y, 0) for x, y, r in rand_pts(3000, 0, 0)])                     # nobody sets off anybody
# hidden: maximum size (most of them have a large group that many firecrackers reach)
N = MAXN
bl = blob(N - 4000, 500_000_000, 500_000_000, 63, 10)       # a one-way chain that ends next to a big group: 1
ch = chain_ending_at(4000, 500_000_000 - 3000, 500_000_000, 100_000, 10)
ch[-1] = reach_to(ch[-1], min(bl, key=lambda q: (q[0] - ch[-1][0]) ** 2 + (q[1] - ch[-1][1]) ** 2))
add(ch + bl)
bl = blob(N - 6000, 700_000_000, 200_000_000, 2, 300)      # two chains into one big group: 2
pts = list(bl)
for y in (200_000_000, 200_000_000 + 300 * 999):
    ch = chain_ending_at(3000, 700_000_000 - 3000, y, 100_000, 10)
    ch[-1] = reach_to(ch[-1], min(bl, key=lambda q: (q[0] - ch[-1][0]) ** 2 + (q[1] - ch[-1][1]) ** 2))
    pts += ch
add(pts)
add(clusters(125, 80, 1000, 190))                           # many clusters, sources are whole clusters
add(clusters(25, 400, 5000, 38))
add(clusters(500, 20, 1000, 375))
add(clusters(2500, 4, 100, 3750))
add(rand_pts(N, 0, 30_000_000))
add(rand_pts(N, 20_000_000, 40_000_000))
add(rand_pts(N, 0, 120_000_000, 400_000_000))
add([(10 * (i // 100), 10 * (i % 100), 10) for i in range(N)])           # a grid: one group, deep search
add([(x, y, MAXR) for x, y, r in rand_pts(N, 0, 0, 700_000_000)])        # everyone sets off everyone: 1
# 40 one-way chains in separate lanes; 27 of them end next to a tall column of 5999 firecrackers
bl = blob(5999, 900_000_000, 100_000_000, 1, 2000)
pts = list(bl)
for c in range(40):
    y = 100_000_000 + 200_000 * c
    ch = chain_ending_at(100, 900_000_000 - 3000, y, 100_000, 900)
    if c % 3:
        ch[-1] = reach_to(ch[-1], min(bl, key=lambda q: (q[0] - ch[-1][0]) ** 2 + (q[1] - ch[-1][1]) ** 2))
    pts += ch
pts.append((10, 10, 0))
add(pts)
# a dense group of 9000 (everyone sets off everyone: 8.1 * 10^7 pairs) and, far from it, 30 one-way chains of 25,
# 20 of them ending next to a column of 249 firecrackers
pts = [(100_000_000 + i % 95, 100_000_000 + i // 95, 140) for i in range(9000)]
bl = blob(249, 600_000_000, 100_000_000, 1, 24_000)
pts += bl
for c in range(30):
    y = 100_000_000 + 200_000 * c
    ch = chain_ending_at(25, 600_000_000 - 3000, y, 100_000, 3000)
    if c % 3:
        ch[-1] = reach_to(ch[-1], min(bl, key=lambda q: (q[0] - ch[-1][0]) ** 2 + (q[1] - ch[-1][1]) ** 2))
    pts += ch
pts.append((10, 10, 0))
add(pts)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import functools
import os, random, math

random.seed(141601)
MAXN = MAXQ = 100_000
MAXC = 10 ** 8
tests = []
_rnd = random.random


def ri(lo, hi):
    # fast uniform integer in [lo, hi] (random.randint is slow for millions of values)
    return lo + int(_rnd() * (hi - lo + 1))


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def strictly_convex_ccw(P):
    n = len(P)
    for k in range(n):
        ax, ay = P[k]
        bx, by = P[(k + 1) % n]
        cx, cy = P[(k + 2) % n]
        if cross(bx - ax, by - ay, cx - bx, cy - by) <= 0:
            return False
    # turning exactly once: the edge direction crosses the positive x-axis direction once
    turns = 0
    for k in range(n):
        ax, ay = P[k]
        bx, by = P[(k + 1) % n]
        cx, cy = P[(k + 2) % n]
        e1 = (bx - ax, by - ay)
        e2 = (cx - bx, cy - by)
        if e1[1] < 0 and e2[1] >= 0 or (e1[1] == 0 and e1[0] < 0 and e2[1] > 0):
            turns += 1
    return turns == 1


def add(P, qs):
    n = len(P)
    assert 4 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    for x, y in P:
        assert abs(x) <= MAXC and abs(y) <= MAXC
    assert strictly_convex_ccw(P)
    for i, j in qs:
        assert 1 <= i <= n and 1 <= j <= n and i != j
        assert (j - i) % n not in (1, n - 1)
    tests.append(f"{n}\n" + "".join(f"{x} {y}\n" for x, y in P) + f"{len(qs)}\n" + "".join(f"{i} {j}\n" for i, j in qs))


def chains(vals):
    # Valtr: split the sorted values into two chains from min to max; differences sum to zero
    vals = sorted(vals)
    lo, hi = vals[0], vals[-1]
    d = []
    a = b = lo
    for v in vals[1:-1]:
        if _rnd() < 0.5:
            d.append(v - a); a = v
        else:
            d.append(b - v); b = v
    d.append(hi - a)
    d.append(b - hi)
    return d


def convex(n, C, extra=1.05):
    # random strictly convex lattice polygon with n vertices, coordinates in [-C, C]
    m = max(int(n * extra) + 8, n + 8)
    while True:
        dx = chains([ri(-C, C) for _ in range(m)])
        dy = chains([ri(-C, C) for _ in range(m)])
        random.shuffle(dy)
        vec = [(a, b) for a, b in zip(dx, dy) if (a, b) != (0, 0)]
        def half(v):  # 0: angle in [0, pi), 1: angle in [pi, 2 pi)
            return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1

        def by_angle(u, w):  # exact integer comparison of directions
            if half(u) != half(w):
                return half(u) - half(w)
            c = u[0] * w[1] - u[1] * w[0]
            return -1 if c > 0 else (1 if c < 0 else 0)
        vec.sort(key=functools.cmp_to_key(by_angle))
        # exact fix of neighbours that floating point may have swapped (rare)
        changed = True
        while changed:
            changed = False
            for k in range(len(vec) - 1):
                (ux, uy), (wx, wy) = vec[k], vec[k + 1]
                if ux * wy - uy * wx < 0 and (uy > 0 or (uy == 0 and ux > 0)) == (wy > 0 or (wy == 0 and wx > 0)):
                    vec[k], vec[k + 1] = vec[k + 1], vec[k]
                    changed = True
        # merge parallel neighbours (same direction)
        merged = []
        for v in vec:
            if merged and cross(merged[-1][0], merged[-1][1], v[0], v[1]) == 0 and \
                    merged[-1][0] * v[0] + merged[-1][1] * v[1] > 0:
                merged[-1] = (merged[-1][0] + v[0], merged[-1][1] + v[1])
            else:
                merged.append(v)
        if len(merged) >= 2 and cross(merged[-1][0], merged[-1][1], merged[0][0], merged[0][1]) == 0:
            merged[0] = (merged[0][0] + merged[-1][0], merged[0][1] + merged[-1][1])
            merged.pop()
        if len(merged) < n:
            m = int(m * 1.3) + 5
            continue
        P = []
        x = y = 0
        for a, b in merged:
            P.append((x, y))
            x += a; y += b
        assert x == 0 and y == 0
        # drop random vertices (still strictly convex) down to n
        keep = sorted(random.sample(range(len(P)), n))
        P = [P[k] for k in keep]
        minx = min(p[0] for p in P); maxx = max(p[0] for p in P)
        miny = min(p[1] for p in P); maxy = max(p[1] for p in P)
        if maxx - minx > 2 * C or maxy - miny > 2 * C:
            continue
        sx = -C - minx + random.randint(0, 2 * C - (maxx - minx))
        sy = -C - miny + random.randint(0, 2 * C - (maxy - miny))
        P = [(px + sx, py + sy) for px, py in P]
        r = random.randrange(n)
        return P[r:] + P[:r]


def rq(n, q, mode="rand"):
    out = []
    for _ in range(q):
        if mode == "long":            # piece with almost every vertex
            i = ri(1, n)
            j = (i - 3 - ri(0, 3)) % n + 1
        elif mode == "half":          # both pieces have about n / 2 vertices
            i = ri(1, n)
            j = (i - 1 + n // 2 + ri(-3, 3)) % n + 1
        elif mode == "short":
            i = ri(1, n)
            j = (i + 1 + ri(1, 3)) % n + 1
        else:
            i = ri(1, n)
            while True:
                j = ri(1, n)
                if j != i and (j - i) % n not in (1, n - 1):
                    break
        out.append((i, j))
    return out


def square(C):
    return [(-C, -C), (C, -C), (C, C), (-C, C)]


# samples
add([(1, 0), (5, 0), (6, 3), (3, 5), (0, 3)], [(1, 3), (3, 1)])
add([(-2, -1), (2, -3), (4, 1), (0, 2)], [(4, 2), (1, 3)])
add([(0, 0), (MAXC, 0), (MAXC, MAXC), (0, MAXC)], [(1, 3), (4, 2)])
add([(0, 0), (7, 1), (6, 5), (-1, 3)], [(3, 1), (4, 2)])
add([(2, -3), (5, 0), (3, 4), (-2, 2), (-3, -1)], [(4, 2)])
# hidden: small
P = convex(4, 5); add(P, [(1, 3), (3, 1), (2, 4), (4, 2)])
for n, C, q in [(6, 20, 30), (12, 100, 60), (40, 1000, 300), (300, 10 ** 6, 2000), (2000, MAXC, 2000)]:
    P = convex(n, C)
    add(P, rq(n, q))
P = convex(500, MAXC); add(P, rq(500, 3000, "long"))
P = convex(1000, 10 ** 5); add(P, [(i, (i - 3) % 1000 + 1) for i in range(1, 1001)] + rq(1000, 1000, "short"))
add(square(MAXC), [(1, 3), (3, 1), (2, 4), (4, 2)] * 25)
# hidden: large (four big polygons, each used with different starting vertices and queries)
BIG = [convex(MAXN, MAXC) for _ in range(3)] + [convex(MAXN, 3 * 10 ** 7)]


def rot(P):
    r = random.randrange(len(P))
    return P[r:] + P[:r]


for k, mode in enumerate(["rand", "half", "half", "long", "rand", "half", "rand", "half"]):
    add(rot(BIG[k % 3]), rq(MAXN, MAXQ, mode))
n = MAXN
add(rot(BIG[0]), [(1, n - 1)] * (MAXQ // 2) + [(n, n - 2)] * (MAXQ // 2))
add(rot(BIG[3]), rq(MAXN, MAXQ, "half"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

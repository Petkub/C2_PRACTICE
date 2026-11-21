# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random
from itertools import accumulate

random.seed(41203)
MAXG = 100_000
MAXN = 100_000
MAXC = 10 ** 6
MAXT = 10 ** 9
tests = []
rnd = random.random


def ri(lo, hi):
    return lo + int(rnd() * (hi - lo + 1))


def isqrt(v):
    r = int(v ** 0.5)
    while r * r > v:
        r -= 1
    while (r + 1) * (r + 1) <= v:
        r += 1
    return r


def add(path, crew, keep=False):
    g, n = len(path), len(crew)
    assert 1 <= g <= MAXG and 1 <= n <= MAXN
    xs, ys, ts = zip(*path)
    assert min(xs) >= 0 and min(ys) >= 0 and min(ts) >= 0
    assert max(xs) <= MAXC and max(ys) <= MAXC and max(ts) <= MAXT
    assert all(t1 <= t2 and (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (t2 - t1) ** 2
               for (x1, y1, t1), (x2, y2, t2) in zip(path, path[1:]))
    xs, ys, a_s, b_s = zip(*crew)
    assert min(xs) >= 0 and min(ys) >= 0 and min(a_s) >= 0
    assert max(xs) <= MAXC and max(ys) <= MAXC and max(b_s) <= MAXT
    assert all(a <= b for a, b in zip(a_s, b_s))
    recs = list(path)
    if keep:
        pass
    elif g < 60_000:
        random.shuffle(recs)
    else:
        step_k = 7919 if g % 7919 else 7907
        recs = [recs[k * step_k % g] for k in range(g)]
    tests.append(f"{g} {n}\n" + "".join(f"{x} {y} {t}\n" for x, y, t in recs)
                 + "".join(f"{x} {y} {a} {b}\n" for x, y, a, b in crew))


def clamp(v):
    return 0 if v < 0 else (MAXC if v > MAXC else v)


def step(x, y, d):
    if rnd() < 0.15 and d >= 5:
        k = d // 5
        dx, dy = 3 * k * random.choice((-1, 1)), 4 * k * random.choice((-1, 1))
        if rnd() < 0.5:
            dx, dy = dy, dx
        nx, ny = x + dx, y + dy
        if 0 <= nx <= MAXC and 0 <= ny <= MAXC:
            return nx, ny
    dx = ri(-d, d)
    b = isqrt(d * d - dx * dx)
    dy = ri(-b, b)
    return clamp(x + dx), clamp(y + dy)


def walk(g, dtmax, stay=0.3, t0=0, start=None, full=0.5):
    x, y = start if start else (ri(0, MAXC), ri(0, MAXC))
    t = t0
    path = [(x, y, t)]
    while len(path) < g:
        dt = ri(1, dtmax) if rnd() < 0.95 else 0
        if rnd() < 0.01:
            dt = ri(dtmax, 15 * dtmax)
        t += dt
        if dt and rnd() >= stay:
            d = dt if rnd() < full else ri(0, dt)
            x, y = step(x, y, d)
        path.append((x, y, t))
    return path


def route_b(g, dtmax, home=None, t0=0):
    hx, hy = home if home else (ri(0, MAXC), ri(0, MAXC))
    t = t0 + ri(0, dtmax)
    path = [(hx, hy, t)]
    while len(path) < g:
        for _ in range(ri(1, 4)):
            if len(path) < g:
                t += ri(0, dtmax)
                path.append((hx, hy, t))
        d = ri(1, dtmax)
        ox, oy = step(hx, hy, d)
        need = isqrt((ox - hx) ** 2 + (oy - hy) ** 2) + 1
        t += need + ri(0, 3)
        if len(path) < g:
            path.append((ox, oy, t))
        t += need + ri(0, 3)
        if len(path) < g:
            path.append((hx, hy, t))
    return path


def groups(path):
    cut = [k for k in range(1, len(path)) if path[k][0] != path[k - 1][0] or path[k][1] != path[k - 1][1]]
    starts = [0] + cut
    ends = [k - 1 for k in cut] + [len(path) - 1]
    return list(zip(starts, ends))


def crew_a(path, n, slack, spread):
    st = groups(path)
    T = path[-1][2]
    crew = []
    for _ in range(n):
        r = rnd()
        if r < 0.55:
            i, j = random.choice(st)
            x, y = path[i][0], path[i][1]
            a, b = path[i][2], path[j][2]
            if b > a:
                a, b = sorted((ri(a, b), ri(a, b)))
            a = max(0, a - ri(0, slack))
            b = min(MAXT, b + ri(0, slack))
        elif r < 0.8:
            i = ri(0, len(path) - 2)
            x1, y1, t1 = path[i]
            x2, y2, t2 = path[i + 1]
            a = ri(t1, t2)
            b = min(MAXT, a + ri(0, max(0, (t2 - a) // 2)))
            x, y = step(x1, y1, ri(0, max(0, a - t1)))
        else:
            x, y = clamp(path[ri(0, len(path) - 1)][0] + ri(-spread, spread)), clamp(path[ri(0, len(path) - 1)][1] + ri(-spread, spread))
            a = ri(0, min(MAXT, T + 10))
            b = min(MAXT, a + ri(0, spread))
        crew.append((x, y, a, b))
    return crew


def crew_b(path, n):
    st = groups(path)
    crew = []
    for _ in range(n):
        k = ri(0, len(st) - 1)
        i = st[k][0]
        x, y = path[i][0], path[i][1]
        later = [s for s in st[k + 1:k + 4] if path[s[0]][:2] == (x, y)]
        if later and rnd() < 0.8:
            b = path[later[-1][0]][2]
        else:
            b = path[st[k][1]][2]
        crew.append((x, y, path[i][2], b))
    return crew


def extend(path, at, r):
    x, y, t = path[at]
    times = list(accumulate([t] + [int(rnd() * 3) for _ in range(r)]))[1:]
    block = [(x, y, v) for v in times]
    t = times[-1]
    shift = t - path[at][2] + ri(1, 3)
    rest = [(px, py, pt + shift) for px, py, pt in path[at + 1:]]
    return path[:at + 1] + block + rest, at, at + r


def crew_c(path, i, j, m):
    x, y = path[i][0], path[i][1]
    lo, hi = path[i][2], path[j][2]
    before = lo - path[i - 1][2] if i > 0 else lo
    after = path[j + 1][2] - hi if j + 1 < len(path) else MAXT - hi
    sa = max(0, min(lo, before - 1)) + 1
    sb = max(0, min(MAXT - hi, after - 1)) + 1
    tenth = (hi - lo) // 10 + 1
    return [(x, y, lo - int(rnd() * sa), hi + int(rnd() * sb)) if rnd() < 0.85
            else (x, y, lo + int(rnd() * tenth), hi - int(rnd() * tenth)) for _ in range(m)]


add([(2, 0, 2), (2, 0, 6), (8, 8, 20)], [(2, 0, 1, 8), (5, 4, 7, 9), (8, 8, 0, 25)])
add([(0, 0, 10)], [(3, 4, 0, 5), (3, 4, 6, 6), (0, 0, 10, 10)])
add([(1, 1, 0), (4, 5, 5), (4, 5, 9), (0, 2, 14)], [(4, 5, 5, 9), (0, 2, 14, 30)])
add([(5, 5, 5), (9, 8, 10)], [(5, 5, 0, 10), (0, 0, 0, 0), (9, 8, 6, 8)])
add([(3, 3, 4), (6, 7, 13), (1, 1, 30)], [(3, 3, 0, 8), (6, 7, 8, 21), (2, 2, 25, 26)])


p = walk(6, 6)
add(p, crew_a(p, 8, 3, 5))
p = route_b(8, 5, (20, 20))
add(p, crew_b(p, 5) + crew_a(p, 4, 2, 3))
p = walk(10, 4, stay=0.5, start=(0, 0))
add(p, crew_a(p, 10, 2, 4))
add([(MAXC, MAXC, MAXT)], [(0, 0, 0, MAXT - 1_414_213), (0, 0, 0, MAXT - 1_414_214),
                           (0, 0, 0, 0), (MAXC, MAXC, MAXT, MAXT), (MAXC, 0, MAXT - MAXC, MAXT - MAXC)])
p = route_b(12, 30)
add(p, crew_b(p, 6) + crew_a(p, 6, 5, 20))
p = walk(15, 1000, stay=0.2)
add(p, crew_a(p, 15, 50, 500))


p = walk(3000, 2000)
add(p, crew_a(p, 3000, 100, 1000))
p = route_b(4000, 500)
add(p, crew_b(p, 2000) + crew_a(p, 2000, 50, 300))
p = walk(5000, 100_000, stay=0.4, full=0.9)
add(p, crew_a(p, 5000, 1000, 20_000))


G, N = MAXG, MAXN
R = 88_000
M = 72_000
W = G - R - 300
K = 3000


def build(make, rest):
    path, i, j = extend(walk(300, 6, start=(ri(0, 99), ri(0, 99))), 299, R)
    x, y, t = path[-1]
    d = ri(1, 50)
    path = path + make(step(x, y, d), t + d)
    return path, crew_c(path, i, j, M)


p, c = build(lambda s, t: walk(W, 20_000, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 2000, 50_000))
p, c = build(lambda s, t: walk(W, 20_000, stay=0.6, full=0.95, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 100, 5000))
p, c = build(lambda s, t: route_b(W, 10_000, s, t), 0)
add(p, c + crew_b(p, K // 2) + crew_a(p, K // 2, 500, 5000))
p, c = build(lambda s, t: route_b(W, 20_000, s, t), 0)
add(p, c + crew_b(p, K))
p, c = build(lambda s, t: walk(W, 20_000, stay=0.1, full=1.0, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 0, 1000))
p, c = build(lambda s, t: route_b(W, 20_000, s, t), 0)
add(p, c + crew_b(p, K // 2) + [(x, y, t, t) for x, y, t in random.sample(p, K // 2)])
p, c = build(lambda s, t: walk(W, 200, stay=0.5, full=0.3, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 20, 200))
p = [(5, 5, i * 7) for i in range(G)]
add(p, [(5, 5, ri(0, 1000), MAXT) if rnd() < 0.9 else (ri(0, 9), ri(0, 9), ri(0, 7 * G), MAXT) for _ in range(90_000)])
p, c = build(lambda s, t: walk(W, 20_000, stay=0.3, full=0.7, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 20_000, 10 ** 6))
p, c = build(lambda s, t: route_b(W, 20_000, s, t), 0)
add(p, c + crew_b(p, K // 3) + crew_a(p, K - K // 3, 0, 100))
p, c = build(lambda s, t: walk(W, 2, stay=0.3, t0=t, start=s), 0)
add(p, c + crew_a(p, K, 1, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

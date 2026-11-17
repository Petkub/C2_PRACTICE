# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(170109)
MAXN, MAXT, MAXX, MAXP = 200_000, 10**9, 10**9, 10**9
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def add(ev):
    n = len(ev)
    assert 1 <= n <= MAXN
    ts, xs, ps = zip(*ev)
    assert 0 <= min(ts) and max(ts) <= MAXT and -MAXX <= min(xs) and max(xs) <= MAXX
    assert 1 <= min(ps) and max(ps) <= MAXP
    tests.append(f"{n}\n" + "\n".join(f"{t} {x} {p}" for t, x, p in ev) + "\n")


def cone(n, tmax, pmax, out=0.0):
    """events inside the reachable cone |x| <= t, a share `out` outside it"""
    ev = []
    for _ in range(n):
        t = ri(0, tmax)
        if random.random() < out:
            x = random.choice((1, -1)) * ri(t + 1, min(MAXX, t + 1 + tmax // 10 + 5))
        else:
            x = ri(-t, t)
        ev.append((t, x, ri(1, pmax)))
    return ev


def diagonals(n, tmax, pmax, step):
    """events on lines of full speed: x = t - c or x = c - t (equal t - x or equal t + x)"""
    ev = []
    while len(ev) < n:
        c = ri(0, tmax // 2)
        sgn = random.choice((1, -1))
        t = c + ri(0, step)
        for _ in range(ri(2, 30)):
            if t > tmax:
                break
            x = sgn * (t - c)
            ev.append((t, x, ri(1, pmax)))
            t += ri(0, step)
    ev = ev[:n]
    random.shuffle(ev)
    return ev


def walk(n, pmax, dtmax, slack):
    """one long feasible route (a random walk at speed <= 1) plus noise events near it"""
    ev, t, x = [], 0, 0
    while len(ev) < n:
        dt = ri(0, dtmax)
        t += dt
        x += ri(-dt, dt)
        ev.append((t, x, ri(1, pmax)))
        if random.random() < 0.5:
            ev.append((t + ri(0, slack), x + ri(-slack, slack), ri(1, pmax)))
    ev = [(t, x, p) for t, x, p in ev[:n] if abs(x) <= MAXX and t <= MAXT]
    random.shuffle(ev)
    return ev


# samples
add([(2, 1, 5), (3, -1, 4), (4, 2, 3), (5, 0, 6), (1, 3, 100)])
add([(3, 2, 4), (3, 2, 1), (3, -2, 6), (5, 0, 2)])
add([(1, 5, 7)])
add([(MAXT, MAXX, 1000), (MAXT, -MAXX, 999), (0, 0, 1)])
add([(4, -2, 3), (1, 1, 2), (6, 1, 4), (2, 0, 5), (6, -1, 4), (3, 3, 9)])
# hidden: small (the brute force checks these)
add([(0, 0, 5)])
add([(0, 1, 5), (0, 0, 2), (0, 0, 3)])
for n, tmax, pmax, out in ((8, 5, 10, 0.2), (40, 10, 10, 0.1), (200, 30, 100, 0.1), (500, 1000, MAXP, 0.1),
                           (800, 50, MAXP, 0.05)):
    add(cone(n, tmax, pmax, out))
add(diagonals(600, 200, MAXP, 3))
add(walk(700, 50, 5, 3))
ev = [(ri(0, 10), 0, ri(1, 9)) for _ in range(300)]        # many events at the same places
ev += [(t, random.choice((-1, 1)) * t, ri(1, 9)) for t in range(0, 11) for _ in range(20)]
random.shuffle(ev)
add(ev)
# hidden: maximum size (inputs kept near 3 MB: small numbers when N is large)
add(cone(MAXN, 200_000, 9))
add(cone(MAXN, 100_000, 9, out=0.3))
add(diagonals(MAXN, 100_000, 9, 3))
add(diagonals(130_000, 10_000, MAXP, 1))
add(walk(MAXN, 9, 3, 2))
n = 120_000                                                 # large points: totals near 10^14
add(cone(n, 50_000, MAXP))
add([(t, x, MAXP) for t, x, _ in walk(120_000, 1, 2, 1)])
ev = []                                                     # many events at the same time, few places
for t in range(0, 4000, 2):
    for _ in range(90):
        ev.append((t, ri(-min(t, 20), min(t, 20)), ri(1, 9)))
add(ev[:MAXN])
add(cone(130_000, MAXT, 9, out=0.2))                         # wide coordinates: few pairs can follow each other
add(diagonals(MAXN, 60_000, 9, 2))
add(cone(190_000, 150_000, 99, out=0.05))
# hidden: a medium test
add(cone(20_000, 20_000, MAXP, out=0.1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

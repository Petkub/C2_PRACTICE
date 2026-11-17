# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(14003)
MAXQ = 50_000
M = 10 ** 9
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(cuts):
    assert 1 <= len(cuts) <= MAXQ
    for x1, y1, x2, y2 in cuts:
        assert all(-M <= v <= M for v in (x1, y1, x2, y2)) and (x1, y1) != (x2, y2)
    tests.append(f"{len(cuts)}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in cuts))


def rnd_cut(lim, base=0):
    while True:
        c = (ri(base - lim, base + lim), ri(base - lim, base + lim), ri(base - lim, base + lim), ri(base - lim, base + lim))
        if c[:2] != c[2:]:
            return c


def multiple_cut(lim, gmin):

    while True:
        g = ri(gmin, lim)
        a, b = ri(-(2 * lim) // g, (2 * lim) // g), ri(-(2 * lim) // g, (2 * lim) // g)
        if (a, b) == (0, 0):
            continue
        x1, y1 = ri(-lim, lim), ri(-lim, lim)
        x2, y2 = x1 + a * g, y1 + b * g
        if -lim <= x2 <= lim and -lim <= y2 <= lim:
            return (x1, y1, x2, y2)


def line_cut(lim):

    x, y, t = ri(-lim, lim), ri(-lim, lim), ri(-lim, lim)
    while t == x:
        t = ri(-lim, lim)
    return (x, y, t, y) if ri(0, 1) else (y, x, y, t)


add([(0, 0, 6, 4), (0, 3, 3, 3)])
add([(0, 0, 3, 3), (-2, 1, 3, 2)])
add([(5, 7, 5, -2), (4, 1, 0, 0)])
add([(-M, 0, M, 7), (0, -M, M - 1, M)])
add([(3, 2, -3, -2), (0, 0, 1, 1), (10, 0, 0, 4)])

add([(0, 0, 0, 1)])
add([rnd_cut(10) for _ in range(3000)])
add([rnd_cut(60) for _ in range(1000)])
add([multiple_cut(100, 2) for _ in range(1000)] + [line_cut(100) for _ in range(500)])
add([rnd_cut(200, ri(-M + 300, M - 300)) for _ in range(200)])
add([(x, y, x + d * ri(1, 30), y - d * ri(1, 30)) for x, y, d in [(ri(-M, M - 1000), ri(-M + 1000, M), ri(1, 12)) for _ in range(500)]])
add([(0, 0, 1, k) for k in range(1, 200)] + [(0, 0, k, k) for k in range(1, 200)] + [(k, 0, 0, 1) for k in range(1, 200)])

add([rnd_cut(M) for _ in range(MAXQ)])
add([(-M, -M, M, M)] * (MAXQ // 2) + [(-M, M, M, -M + 1)] * (MAXQ // 2))
add([multiple_cut(M, 10 ** 6) for _ in range(MAXQ)])
add([multiple_cut(M, 10 ** 8) for _ in range(MAXQ)])
add([line_cut(M) for _ in range(MAXQ // 2)] + [rnd_cut(M) for _ in range(MAXQ // 2)])
add([(-M, ri(-M, M), M, ri(-M, M)) for _ in range(MAXQ)])
add([(ri(-M, M), -M, ri(-M, M), M) for _ in range(MAXQ)])
add([(M, M, -M, M - ri(1, 10)) for _ in range(MAXQ)])
add([(x, x, -x, -x) for x in [ri(1, M) for _ in range(MAXQ)]])
add([(ri(-M, M), ri(-M, M), 0, 0) for _ in range(MAXQ)])
add([(a, b, a + d * u, b + d * v) for a, b, d, u, v in
     [(ri(-M // 2, 0), ri(-M // 2, 0), 2 ** ri(20, 28), ri(-1, 1) or 1, 1) for _ in range(MAXQ)]])
add([rnd_cut(M) if i % 3 else line_cut(M) for i in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

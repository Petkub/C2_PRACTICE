# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110014)
MAXN, MAXC = 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def check_disjoint(ws):
    """wires (pos, a, b) with the same pos must not share a point"""
    rows = {}
    for p, a, b in ws:
        assert 0 <= p <= MAXC and 0 <= a < b <= MAXC
        rows.setdefault(p, []).append((a, b))
    for segs in rows.values():
        if len(segs) > 1:
            segs.sort()
            assert all(b1 < a2 for (a1, b1), (a2, b2) in zip(segs, segs[1:]))


def add(hs, vs):
    n, m = len(hs), len(vs)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN
    check_disjoint(hs)
    check_disjoint(vs)
    t = f"{n} {m}\n" + "".join(f"{y} {l} {r}\n" for (y, l, r) in hs) + "".join(f"{x} {d} {u}\n" for (x, d, u) in vs)
    assert len(t) <= 3_100_000
    tests.append(t)


def wires(count, c, maxlen, per_row=1):
    """count wires inside [0, c]; per_row wires share each row (pos), pairwise disjoint"""
    rows = (count + per_row - 1) // per_row
    poss = random.sample(range(c + 1), rows)
    res = []
    for r, p in enumerate(poss):
        k = min(per_row, count - r * per_row)
        if k == 1:
            a = ri(0, c - 1)
            res.append((p, a, min(c, a + ri(1, maxlen))))
        else:
            pts = sorted(ri(0, c - 2 * k + 1) for _ in range(2 * k))
            pts = [v + i for i, v in enumerate(pts)]   # strictly increasing, inside [0, c]
            res.extend((p, pts[2 * i], pts[2 * i + 1]) for i in range(k))
    return res


# samples
add([(2, 1, 5), (4, 0, 3)], [(2, 0, 5), (5, 2, 6), (4, 3, 4)])
add([(1, 0, 2)], [(3, 0, 5), (1, 2, 4)])
add([(0, 0, 1)], [(0, 0, 1)])
add([(3, 0, 2), (3, 4, 6)], [(2, 0, 3), (3, 0, 9), (4, 3, 5)])
add([(1, 0, 10), (5, 2, 8), (5, 9, 12)], [(4, 0, 9), (9, 1, 5), (3, 6, 7)])
# hidden: small
add([(5, 0, MAXC)], [(MAXC, 0, 5), (0, 5, MAXC)])
add(wires(10, 10, 10, 2), wires(10, 10, 10, 2))
add(wires(100, 30, 30, 4), wires(100, 30, 30, 4))
add(wires(1000, 1000, 1000), wires(1000, 1000, 300, 4))
add(wires(3000, MAXC, MAXC), wires(3000, MAXC, MAXC))
add(wires(5000, 200, 200, 30), wires(5000, 200, 200, 30))            # many end points touching
add(wires(5000, 10**5, 10**5, 1), wires(2000, 10**5, 10**5, 2))
# hidden: maximum size
K, C = 82_000, 99_999
add(wires(K, C, C), wires(K, C, C))                                    # long random wires
F = MAXN                                                               # one wire per row/column: N * M = 10^10
add([(y, 0, C) for y in random.sample(range(C + 1), F)],
    [(x, 0, C) for x in random.sample(range(C + 1), F)])               # full grid: every pair meets
add(wires(K, C, C, 5), wires(K, C, C, 5))
add(wires(K, 500, 500, 200), wires(K, 500, 500, 200))                 # dense, touching end points
add(wires(K, C, 3000), wires(K, C, 3000))                              # short wires
add([(y, 0, C if i % 2 else 49_999) for i, y in enumerate(random.sample(range(C + 1), F))],
    [(x, 0, C) for x in random.sample(range(C + 1), F)])               # long wires, 3/4 of the pairs meet
hs = [(y, 0, 49_999) for y in random.sample(range(C + 1), K)]
vs = [(x, d, u) for x in random.sample(range(50_000, C + 1), K // 2) for (d, u) in ((0, 49_999), (50_000, C))]
add(hs, vs)                                                            # no point at all
hs = [(y, ri(0, 50_000), ri(50_001, C)) for y in random.sample(range(C + 1), K)]
vs = [(50_000 + (j % 2), 2 * (j // 2), 2 * (j // 2) + 1) for j in range(K)]   # all verticals on two columns
add(hs, vs)
add(wires(49_000, MAXC, MAXC), wires(49_000, MAXC, MAXC))             # big coordinates
add(wires(MAXN, C, C, 2), wires(60_000, C, C))
add([(y, ri(0, 99), C - ri(0, 99)) for y in random.sample(range(C + 1), F)],
    [(x, ri(0, 99), C - ri(0, 99)) for x in random.sample(range(C + 1), F)])   # almost a full grid, ends near the edges
add([(y, 0, C) for y in random.sample(range(C + 1), K)], wires(K, C, C, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

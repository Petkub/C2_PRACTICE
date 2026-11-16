# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(40110)
MAXN, MAXQ, MAXX, MAXP, MAXC = 80_000, 80_000, 10**9, 10**5, 10**10
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(groups, qs):
    n, q = len(groups), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= s < e <= MAXX and 1 <= p <= MAXP for (s, e, p) in groups)
    assert all(1 <= c <= MAXC for c in qs)
    tests.append(f"{n} {q}\n" + "".join(f"{s} {e} {p}\n" for (s, e, p) in groups)
                 + " ".join(map(str, qs)) + "\n")


def loads(groups):
    """the load right after boarding at every position where somebody boards"""
    ev = sorted([(s, p) for (s, e, p) in groups] + [(e, -p) for (s, e, p) in groups])
    res, cur, i = [], 0, 0
    while i < len(ev):
        j = i
        while j < len(ev) and ev[j][0] == ev[i][0]:
            cur += ev[j][1]
            j += 1
        res.append(cur)
        i = j
    return res


def near(groups, q, spread=0.15):
    """capacities close to the largest load (answers late in the trip, or OK)"""
    m = max(loads(groups))
    lo, hi = max(1, int(m * (1 - spread))), min(MAXC, int(m * (1 + spread / 3)) + 1)
    return [ri(lo, hi) for _ in range(q)]


def exact(groups, q):
    """capacities equal to a load or one less (the boundary of 'more than C')"""
    ls = loads(groups)
    return [max(1, random.choice(ls) - ri(0, 1)) for _ in range(q)]


def rnd_group(lo, hi, maxp):
    s = ri(lo, hi - 1)
    return (s, ri(s + 1, hi), ri(1, maxp))


# samples
add([(2, 5, 3), (4, 8, 2), (5, 9, 4)], [4, 5, 6, 2])
add([(1, 3, 5), (3, 6, 5)], [5, 4])
add([(10, 20, 7)], [7, 6, 1])
add([(1, 100, 1), (50, 60, 2), (60, 70, 2), (2, 3, 1), (60, 61, 1)], [2, 3, 1, 4])
add([(5, 6, 100000), (1, 10, 100000), (3, 6, 100000)], [100000, 200000, 299999, 300000, 10000000000])
# hidden: small
add([(1, 2, 1)], [1])
add([(i, i + 1, 9) for i in range(1, 30)], [9, 8, 10])          # people leave exactly where others board
g = [rnd_group(1, 20, 5) for _ in range(10)]
add(g, exact(g, 10))
g = [rnd_group(1, 100, 100) for _ in range(50)]
add(g, exact(g, 25) + near(g, 25))
g = [rnd_group(1, 1000, MAXP) for _ in range(500)]
add(g, exact(g, 300) + [ri(1, MAXC) for _ in range(200)])
g = [rnd_group(1, MAXX, MAXP) for _ in range(3000)]
add(g, exact(g, 1500) + near(g, 1500))
g = []
for i in range(5000):                                           # many shared stops
    s = ri(1, 300)
    g.append((s, s + ri(1, 5), ri(1, 1000)))
add(g, exact(g, 5000))
# hidden: maximum size
N, Q = MAXN, MAXQ
g = [(ri(1, MAXX - 1), MAXX, ri(1, MAXP)) for _ in range(N)]   # everybody rides to the end: load grows
add(g, near(g, Q))
g = [(ri(1, MAXX - 1), MAXX, MAXP) for _ in range(N)]          # load up to 10^10
add(g, near(g, Q, 0.05))
g = [rnd_group(1, MAXX, MAXP) for _ in range(N)]
add(g, near(g, Q // 2) + exact(g, Q // 2))
g = [rnd_group(1, MAXX, MAXP) for _ in range(N)]
m = max(loads(g))
add(g, [ri(1, m + 10) for _ in range(Q)])
g = [(1, MAXX, MAXP)] * N                                      # one stop, 10^10 people
add(g, [MAXC - ri(0, 1) for _ in range(Q)])
g = []
x = 1
for i in range(N):                                             # chain: leave where the next boards
    d = ri(1, 9000)
    g.append((x, x + d, MAXP - ri(0, 3)))
    x += d
add(g, [ri(MAXP - 4, MAXP + 1) for _ in range(Q)])
g = [(ri(1, MAXX - 1), MAXX, ri(1, MAXP)) for _ in range(N)]
add(g, [MAXC] * Q)                                             # nobody ever exceeds: all OK
g = []
for i in range(N):                                             # load grows slowly with many shared stops
    s = ri(1, 50_000)
    g.append((s, ri(s + 1, s + 3) if i % 3 == 0 else MAXX, ri(1, MAXP)))
add(g, near(g, Q, 0.1))
g = [(1, ri(2, MAXX), ri(1, MAXP)) for _ in range(N)]          # everybody boards at the start
add(g, exact(g, Q))
g = []
for i in range(N):                                             # a rising staircase of short trips
    s = ri(1, MAXX - 10**7)
    g.append((s, s + ri(1, 10**7), 1 + s // 10**4))
add(g, near(g, Q, 0.3))
g = [(ri(1, MAXX - 1), MAXX, ri(1, MAXP)) for _ in range(N)]
add(g, near(g, Q // 2, 0.02) + exact(g, Q // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(81313)
MAXN, MAXM, MAXQ, MAXW = 300, 50_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, qs, shuffle=True):
    edges = list(edges)
    if shuffle:
        random.shuffle(edges)
    m, q = len(edges), len(qs)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= a <= n and 1 <= b <= n and -MAXW <= w <= MAXW for a, b, w in edges)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)
    tests.append(f"{n} {m} {q}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
                 + "".join(f"{u} {v}\n" for u, v in qs))


def rq(n, q):
    return [(ri(1, n), ri(1, n)) if random.random() < 0.97 else (x, x) for x in [ri(1, n) for _ in range(q)]]


def potential(n, m, pmax, cmax, verts=None):
    """roads w = p(b) - p(a) + c with c >= 0: many negative roads but no negative cycle"""
    verts = verts or list(range(1, n + 1))
    p = {v: ri(0, pmax) for v in verts}
    res = []
    for _ in range(m):
        a, b = random.choice(verts), random.choice(verts)
        res.append((a, b, max(-MAXW, min(MAXW, p[b] - p[a] + ri(0, cmax)))))
    return res


def chain_potential(n, extra, pmax, cmax):
    """a long cheap route through all towns plus random roads, no negative cycle"""
    order = list(range(1, n + 1))
    random.shuffle(order)
    p = {v: ri(0, pmax) for v in order}
    res = [(order[i], order[i + 1], p[order[i + 1]] - p[order[i]] + ri(0, 3)) for i in range(n - 1)]
    for _ in range(extra):
        a, b = random.choice(order), random.choice(order)
        res.append((a, b, min(MAXW, p[b] - p[a] + ri(cmax // 2, cmax))))
    return res


def plant_cycles(n, k, length, wmin):
    """k small cycles of negative total length"""
    res = []
    for _ in range(k):
        cyc = random.sample(range(1, n + 1), length)
        ws = [ri(-MAXW // 2, MAXW // 2) for _ in range(length - 1)]
        last = -sum(ws) - ri(1, wmin)
        if not -MAXW <= last <= MAXW:
            continue
        ws.append(last)
        res += [(cyc[i], cyc[(i + 1) % length], ws[i]) for i in range(length)]
    return res


def groups(n, sizes):
    """split the towns into groups (random order)"""
    order = list(range(1, n + 1))
    random.shuffle(order)
    res, at = [], 0
    for s in sizes:
        res.append(order[at:at + s])
        at += s
    return res


def scc_dag(n, k, m, pbad, pmax, cmax, cyc=1):
    """k groups; inside a group roads both ways without negative cycles, between groups only forward;
    a fraction pbad of the groups get one negative cycle"""
    cuts = sorted(random.sample(range(1, n), k - 1))
    sizes = [b - a for a, b in zip([0] + cuts, cuts + [n])]
    gs = groups(n, sizes)
    inner = m * 3 // 4
    e = []
    for g in gs:
        e += potential(n, max(1, inner * len(g) // n), pmax, cmax, g)
        if random.random() < pbad:
            if len(g) == 1:
                e.append((g[0], g[0], -ri(1, cyc)))
            else:
                a, b = random.sample(g, 2)
                w = ri(-MAXW + cyc, MAXW - cyc)
                e += [(a, b, w), (b, a, -w - ri(1, cyc))]
    while len(e) < m:
        i, j = sorted(random.sample(range(k), 2)) if k > 1 else (0, 0)
        e.append((random.choice(gs[i]), random.choice(gs[j]), ri(-MAXW // 10, MAXW)))
    return e[:m]


# samples
add(4, [(1, 2, 4), (2, 3, -2), (1, 3, 3), (3, 4, 1), (4, 2, 5)], [(1, 3), (4, 1)], False)
add(4, [(1, 2, 1), (2, 3, -3), (3, 2, 1), (3, 4, 2)], [(1, 4), (1, 1)], False)
add(3, [(2, 2, -1), (1, 3, 7)], [(1, 3), (2, 2), (3, 1)], False)
add(4, [(1, 2, -MAXW), (2, 3, -MAXW), (3, 4, -MAXW)], [(1, 4), (4, 1)], False)
add(2, [(1, 2, -5), (2, 1, 5)], [(1, 2), (2, 2)], False)
# hidden: small
add(5, [(1, 2, 2), (2, 3, 2), (3, 1, -5), (4, 5, -1), (5, 4, 1), (3, 4, 10), (1, 1, 0)],
    [(1, 5), (4, 4), (5, 1), (4, 5), (5, 5), (2, 2)])
add(1, [(1, 1, -5)], [(1, 1)])
add(1, [(1, 1, 3)], [(1, 1)])
add(2, [(1, 2, -MAXW), (2, 1, MAXW)], [(1, 2), (2, 1), (1, 1), (2, 2)])
for n, m, wneg, wpos in ((5, 8, 3, 5), (6, 12, 2, 6), (8, 15, 1, 10), (10, 25, 5, 20), (15, 40, 3, 30)):
    add(n, [(ri(1, n), ri(1, n), ri(-wneg, wpos)) for _ in range(m)], rq(n, 100))
add(30, potential(30, 120, 1000, 50), rq(30, 300))
add(30, potential(30, 100, 1000, 50) + plant_cycles(30, 2, 3, 5), rq(30, 300))
add(60, chain_potential(60, 200, 10**6, 10**6) + plant_cycles(60, 1, 4, 1), rq(60, 500))
gs = groups(80, [30, 30, 20])
e = potential(80, 300, 10**4, 100, gs[0]) + potential(80, 300, 10**4, 100, gs[1]) + potential(80, 200, 10**4, 100, gs[2])
e += [(gs[1][0], gs[1][1], -10**5), (gs[1][1], gs[1][0], 0)] + [(gs[0][0], gs[1][2], 7), (gs[1][3], gs[2][0], 9)]
add(80, e, rq(80, 800))
add(100, [(ri(1, 100), ri(1, 100), ri(-10, 10**4)) for _ in range(1500)], rq(100, 1000))
# hidden: maximum size
N, M, Q = MAXN, MAXM, MAXQ
add(N, potential(N, M, 5 * 10**8, 10**8), rq(N, Q))
add(N, chain_potential(N, M - N, 5 * 10**8, MAXW // 2), rq(N, Q))
add(N, scc_dag(N, 12, M, 0.3, 10**6, 10**7), rq(N, Q))
gs = groups(N, [100, 100, 100])                       # three parts; only the middle one has a negative cycle
e = []
for g in gs:
    e += potential(N, M // 3 - 50, 4 * 10**8, 10**8, g)
x, y = gs[1][0], gs[1][1]
e += [(x, y, -MAXW), (y, x, MAXW - 1)]
for _ in range(20):
    e += [(random.choice(gs[0]), random.choice(gs[1]), ri(1, MAXW)), (random.choice(gs[1]), random.choice(gs[2]), ri(1, MAXW))]
add(N, e, rq(N, Q))
add(N, scc_dag(N, 6, M, 0.5, 10**8, 10**8, MAXW), rq(N, Q))                    # very negative cycles: watch overflow
add(N, [(ri(1, N), ri(1, N), ri(-MAXW, -MAXW + 10)) for _ in range(M)], rq(N, Q))  # everything is -INF
e = [(i, i + 1, -MAXW) for i in range(1, N)] + [(i, i, 0) for i in range(1, N + 1)]
e += [(i, j, ri(-MAXW, MAXW)) for i, j in (sorted(random.sample(range(1, N + 1), 2)) for _ in range(M - len(e)))]
add(N, e, rq(N, Q))                                   # long, very negative routes, no cycle
add(N, scc_dag(N, 20, M - 1, 0.0, 10**8, 10**6) + [(150, 150, -1)], rq(N, Q))   # one negative loop
gs = groups(N, [150, 150])                            # no road from the second half to the first
e = potential(N, M // 2, 10**8, 10**6, gs[0]) + potential(N, M // 2 - 50, 10**8, 10**6, gs[1])
e += [(random.choice(gs[0]), random.choice(gs[1]), ri(-MAXW, MAXW)) for _ in range(50)]
add(N, e, rq(N, Q))
order = list(range(1, N + 1))
random.shuffle(order)
e = [(order[i], order[j], ri(-MAXW, MAXW)) for i, j in (sorted(random.sample(range(N), 2)) for _ in range(M))]
add(N, e, rq(N, Q))                                   # no cycle at all, any signs
add(N, scc_dag(N, 40, M, 0.3, 4 * 10**8, MAXW // 2), rq(N, Q))
add(N, scc_dag(N, 3, M, 0.4, 10**4, 10), rq(N, Q))
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

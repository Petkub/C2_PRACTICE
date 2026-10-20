# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(132006)
MAXN = 80
MAXM = 10_000
MAXK = 10**9
MAXC = 10**9
MAXQ = 1000
tests = []


def add(n, edges, qs):
    assert 2 <= n <= MAXN and 1 <= len(edges) <= MAXM and 1 <= len(qs) <= MAXQ
    for a, b, c in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b and 1 <= c <= MAXC
    for s, t, k in qs:
        assert 1 <= s <= n and 1 <= t <= n and 1 <= k <= MAXK
    tests.append(f"{n} {len(edges)}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in edges)
                 + f"{len(qs)}\n" + "".join(f"{s} {t} {k}\n" for s, t, k in qs))


def ri(lo, hi):
    return random.randint(lo, hi)


# K = 2^30 - 1 - 2^j (j = 27, 28, 29) and 2^29 - 1 have 29 one bits: the most squarings to combine
HEAVY = [(1 << 30) - 1 - (1 << j) for j in (27, 28, 29)] + [(1 << 29) - 1]
assert all(k <= MAXK and bin(k).count("1") == 29 for k in HEAVY)


def rand_k(kind=None):
    """a number of flights of a random kind: uniform, many one bits, small, a power of two, the maximum"""
    k = ri(0, 9) if kind is None else kind
    if k <= 3:
        return ri(1, MAXK)
    if k <= 5:     # many one bits (all bits of a random length, with a few cleared)
        b = ri(20, 29)
        v = (1 << b) - 1
        for _ in range(ri(0, 2)):
            v &= ~(1 << ri(0, b - 1))
        return random.choice(HEAVY) if ri(0, 2) == 0 else max(1, v)
    if k == 6:
        return ri(1, 50)
    if k == 7:
        return 1 << ri(0, 29)
    if k == 8:
        return MAXK - ri(0, 3)
    return ri(MAXK // 2, MAXK)


def rand_edges(n, m, cmax, cmin=1):
    out = []
    for _ in range(m):
        a = ri(1, n)
        b = ri(1, n - 1)
        if b >= a:
            b += 1
        out.append((a, b, ri(cmin, cmax)))
    return out


def rand_q(n, q, kmax=MAXK, kind=None):
    return [(ri(1, n), ri(1, n), rand_k(kind) if kmax == MAXK else ri(1, kmax)) for _ in range(q)]


def all_pairs(n, kmax):
    return [(s, t, ri(1, kmax)) for s in range(1, n + 1) for t in range(1, n + 1)]


def bipartite(n, m, cmax):
    """flights only between odd and even cities: the parity of K decides which pairs are possible"""
    out = []
    while len(out) < m:
        a, b = ri(1, n), ri(1, n)
        if a % 2 != b % 2:
            out.append((a, b, ri(1, cmax)))
    return out


def cycle_layers(n, L, m, cmax):
    """city i belongs to layer i mod L; flights only go from layer j to layer j + 1 (mod L)"""
    out = []
    for i in range(1, n + 1):                       # make every layer reachable
        j = i % n + 1
        while (j % L) != ((i + 1) % L):
            j = j % n + 1
        out.append((i, j, ri(1, cmax)))
    while len(out) < m:
        a, b = ri(1, n), ri(1, n)
        if b % L == (a + 1) % L and a != b:
            out.append((a, b, ri(1, cmax)))
    return out


def dag(n, m, cmax):
    out = []
    while len(out) < m:
        a, b = ri(1, n), ri(1, n)
        if a < b:
            out.append((a, b, ri(1, cmax)))
    return out


# samples
add(3, [(1, 2, 5), (2, 3, 3), (3, 1, 4), (2, 1, 1)], [(1, 3, 4), (2, 2, 2)])
add(2, [(1, 2, 7), (2, 1, 3)], [(1, 2, 3), (1, 1, 3), (1, 1, 2)])
add(2, [(1, 2, MAXC), (2, 1, MAXC)], [(1, 1, MAXK), (2, 1, MAXK - 1)])
add(3, [(1, 2, 3), (1, 2, 1)], [(1, 2, 1), (2, 1, 1)])
add(4, [(4, 3, 12), (3, 2, 18), (3, 1, 1), (2, 4, 14), (4, 2, 18)], [(4, 4, 7), (3, 3, 6)])
# hidden: small K (the brute force adds one flight at a time)
add(2, [(1, 2, 4)], [(s, t, k) for s in (1, 2) for t in (1, 2) for k in (1, 2, 3)])
add(3, rand_edges(3, 6, 10), all_pairs(3, 20) + all_pairs(3, 7))
add(5, rand_edges(5, 12, 100), all_pairs(5, 60))
add(6, bipartite(6, 15, 1000), all_pairs(6, 40) + all_pairs(6, 41))
add(8, cycle_layers(8, 3, 20, 50), all_pairs(8, 100))
add(10, rand_edges(10, 40, MAXC), all_pairs(10, 1000))
add(10, dag(10, 30, 100), [(s, t, ri(1, 10)) for s in range(1, 11) for t in range(1, 11)])
add(12, rand_edges(12, 30, 10), rand_q(12, 300, 999))
add(20, rand_edges(20, 200, MAXC, MAXC - 10), rand_q(20, 300, 2000))
add(30, cycle_layers(30, 7, 150, 1000), rand_q(30, 500, 300))
add(MAXN, rand_edges(MAXN, 500, MAXC), rand_q(MAXN, 300, 400))
# hidden: large (every query has its own K up to 10^9)
add(MAXN, rand_edges(MAXN, MAXM, MAXC), rand_q(MAXN, MAXQ))
add(MAXN, rand_edges(MAXN, MAXM, MAXC, MAXC - 1000), rand_q(MAXN, MAXQ, kind=4))
add(MAXN, rand_edges(MAXN, 250, 1000), rand_q(MAXN, MAXQ))
add(MAXN, bipartite(MAXN, MAXM, MAXC), rand_q(MAXN, MAXQ))
add(MAXN, bipartite(MAXN, 1500, 10**6), rand_q(MAXN, MAXQ, kind=0))
add(MAXN, cycle_layers(MAXN, 7, MAXM, MAXC), rand_q(MAXN, MAXQ))
add(MAXN, cycle_layers(MAXN, MAXN, MAXN, MAXC), rand_q(MAXN, MAXQ))                 # one big ring
add(MAXN, cycle_layers(MAXN, 10, 400, 100), rand_q(MAXN, MAXQ, kind=4))
add(MAXN, dag(MAXN, MAXM, MAXC), [(ri(1, MAXN), ri(1, MAXN), rand_k(6) if i % 2 else rand_k()) for i in range(MAXQ)])
add(MAXN, [(i, i % MAXN + 1, MAXC) for i in range(1, MAXN + 1)] + [(i % MAXN + 1, i, MAXC) for i in range(1, MAXN + 1)],
    [(ri(1, MAXN), ri(1, MAXN), random.choice(HEAVY + [MAXK, MAXK - 1]) if i % 4 == 0 else rand_k(ri(8, 9)))
     for i in range(MAXQ)])                                                        # answers up to 10^18
add(MAXN, rand_edges(MAXN, MAXM, MAXC), [(ri(1, MAXN), ri(1, MAXN), rand_k(ri(6, 7))) for _ in range(MAXQ)])
add(MAXN, rand_edges(MAXN, MAXM, 100), [(ri(1, MAXN), ri(1, MAXN), random.choice(HEAVY) if i % 4 == 0 else rand_k(4))
                                         for i in range(MAXQ)])
add(MAXN, rand_edges(MAXN, 120, MAXC) + [(1, 2, 1), (2, 1, 1)], rand_q(MAXN, MAXQ))
add(MAXN, rand_edges(MAXN, MAXM, MAXC), [(s, s, rand_k()) for s in (ri(1, MAXN) for _ in range(MAXQ))])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2411)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXN, MAXM = 200_000, 200_000
tests = []


def shuffled(a):
    """a random permutation of the list a (faster than random.shuffle for long lists)"""
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    assert 1 <= n <= MAXN and 0 <= len(edges) <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {len(edges)}\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, edges, one):
    """random city numbers; the shape's vertex `one` becomes city 1; random road order"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    j = lab.index(1)
    lab[one - 1], lab[j] = lab[j], lab[one - 1]
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return n, e


def blocks(n, m, size_fn, links, cut=None):
    """consecutive blocks, each a cycle; links random forward roads between blocks (with cut = a block number,
    no link jumps over that block or leaves it); the rest of the m roads stay inside blocks.
    Returns the roads and the blocks."""
    e, bl, start = [], [], 1
    where = [0] * (n + 1)
    while start <= n:
        s = min(size_fn(), n - start + 1)
        for x in range(start, start + s):
            where[x] = len(bl)
        bl.append((start, start + s - 1))
        if s >= 2:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        start += s
    for (a, b), (c, d) in zip(bl, bl[1:]):          # a chain through all blocks
        e.append((ri(a, b), ri(c, d)))
    if cut is not None:                             # a few roads from far left blocks into the cut block
        for _ in range(5):
            x, y = bl[ri(0, cut // 2)]
            c, d = bl[cut]
            e.append((ri(x, y), ri(c, d)))
            links -= 1
    while links > 0:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if where[u] < where[v] and (cut is None or where[v] <= cut or where[u] > cut):
            e.append((u, v))
            links -= 1
    assert len(e) <= max(m, len(e)) and (len(e) >= m or any(b > a for a, b in bl))
    while len(e) < m:
        u = ri(1, n)
        a, b = bl[where[u]]
        v = ri(a, b)
        if u != v:
            e.append((u, v))
    return e, bl


def gadget(k):
    """1 -> v, u -> 1, u -> x_1 -> ... -> x_k -> v, u -> v: riding u -> v backwards once gives 3 cities,
    riding it backwards twice would give all k + 3"""
    one, v, u = 1, 2, 3
    xs = list(range(4, 4 + k))
    e = [(one, v), (u, one), (u, v), (u, xs[0]), (xs[-1], v)] + [(xs[i], xs[i + 1]) for i in range(k - 1)]
    return k + 3, e


def rand_edges(n, m):
    e = []
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
    return e


# samples
add(6, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (1, 5), (6, 4)])
add(4, [(2, 1), (1, 4), (2, 3), (3, 4), (2, 4)])
add(1, [])
add(3, [(1, 2), (2, 3)])
add(5, [(1, 2), (2, 1), (3, 4), (4, 3), (4, 1), (2, 5)])
add(6, [(2, 1), (3, 2), (1, 4), (4, 5), (5, 4), (6, 3), (5, 6), (4, 2)])
# hidden: small (searched exhaustively by brute)
add(2, [(1, 2)])
add(2, [(2, 1), (2, 1)])
for n, m in ((5, 6), (7, 9), (8, 10), (10, 14), (13, 20)):
    add(n, rand_edges(n, m))
add(*relabel(*gadget(8), 1))
# hidden: medium
e, bl = blocks(2000, 4000, lambda: ri(1, 3), 1500)
add(*relabel(2000, e, ri(*bl[len(bl) // 2])))
add(*relabel(20_000, [(i, i + 1) for i in range(1, 20_000)] + [(20_000, 1)], ri(1, 20_000)))   # one big cycle
# hidden: maximum size
N = MAXN
add(*relabel(*gadget(N - 4), 1))                                        # reversing a road twice would visit all
e, bl = blocks(N, MAXM, lambda: 1, MAXM - N + 1)                          # a long chain plus forward jumps
add(*relabel(N, e, N // 2))
add(*relabel(N, [(i, i + 1) for i in range(1, N)], N // 3))                 # one chain: only 2
e, bl = blocks(120_000, MAXM, lambda: ri(1, 4), 20_000)
add(*relabel(120_000, e, ri(*bl[len(bl) // 2])))
# no forward jump passes city 1's block: the longest ride away from 1 cannot come back
e, bl = blocks(120_000, MAXM, lambda: ri(1, 4), 20_000, 16_000)
add(*relabel(120_000, e, ri(*bl[16_000])))
e, bl = blocks(190_000, MAXM, lambda: ri(20, 200) if rnd() < 0.002 else 1, 3000, 30_000)
add(*relabel(190_000, e, ri(*bl[30_000])))
e, bl = blocks(120_000, MAXM, lambda: ri(1, 2), 30_000, 20_000)
add(*relabel(120_000, e, ri(*bl[20_000])))
e, bl = blocks(170_000, MAXM, lambda: 1, 30_001, 40_000)
add(*relabel(170_000, e, 40_001))
n1 = 100_000                                                            # a gadget glued to city 1 of a DAG
e, bl = blocks(n1, 0, lambda: ri(1, 2), 20_000)
one = ri(*bl[len(bl) // 2])
n2, g2 = gadget(40_000)
ren = {1: one}                                                          # the gadget's city 1 is `one`
for x in range(2, n2 + 1):
    ren[x] = n1 + x - 1
e += [(ren[a], ren[b]) for a, b in g2]
add(*relabel(n1 + n2 - 1, e, one))
add(N // 2, rand_edges(N // 2, MAXM))                                    # a giant group around city 1
add(N, rand_edges(N, N))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2405)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXN, MAXM, MAXG = 200_000, 200_000, 10**9
tests = []


def shuffled(a):
    """a random permutation of the list a (faster than random.shuffle for long lists)"""
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, g, edges):
    assert 1 <= n <= MAXN and 0 <= len(edges) <= MAXM and len(g) == n
    assert all(0 <= x <= MAXG for x in g)
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {len(edges)}\n" + " ".join(map(str, g)) + "\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, g, edges):
    """random room numbers (gold moves with the rooms) and a random tunnel order"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    g2 = [0] * n
    for i in range(n):
        g2[lab[i] - 1] = g[i]
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return n, g2, e


def blocks(n, m, size_fn, chain=True):
    """consecutive blocks, each a cycle; tunnels between blocks only go forward (a DAG of blocks)"""
    e, bl, start = [], [], 1
    while start <= n:
        s = min(size_fn(), n - start + 1)
        bl.append((start, start + s - 1))
        if s >= 2:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        start += s
    if chain:
        for (a, b), (c, d) in zip(bl, bl[1:]):
            e.append((ri(a, b), ri(c, d)))
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u < v:
            e.append((u, v))
    return e[:m]


def rand_edges(n, m):
    e = []
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
    return e


def rg(n, lo=0, hi=MAXG):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(5, [3, 1, 4, 1, 5], [(1, 2), (2, 1), (2, 3), (1, 4), (4, 5)])
add(4, [5, 0, 5, 3], [(1, 2), (2, 3), (3, 1), (4, 1)])
add(1, [0], [])
add(3, [4, 9, 2], [])
add(4, [MAXG] * 4, [(1, 2), (2, 3), (3, 4)])
add(6, [2, 7, 1, 8, 2, 8], [(1, 2), (2, 3), (3, 1), (3, 4), (5, 4), (5, 6), (6, 5), (2, 6)])
# hidden: small
add(2, [5, 6], [(1, 2), (2, 1)])
for n, m in ((6, 7), (8, 10), (10, 12), (12, 14), (12, 20)):
    add(n, rg(n, 0, 20), rand_edges(n, m))
add(*relabel(2000, rg(2000), blocks(2000, 5000, lambda: ri(1, 4), False)))
add(*relabel(2500, rg(2500, 0, 100), blocks(2500, 6000, lambda: ri(1, 2), True)))
add(3000, rg(3000), rand_edges(3000, 3000))
# hidden: maximum size
N = MAXN
add(*relabel(N, [MAXG] * N, [(i, i + 1) for i in range(1, N)]))                   # one long chain: 2 * 10^14
add(*relabel(N, rg(N), [(i, i + 1) for i in range(1, N)] + [(N, 1)]))            # one long cycle
add(*relabel(N, rg(N, 0, 999), blocks(N, MAXM, lambda: 1, False)))                 # a random DAG
add(*relabel(N, rg(N), blocks(N, MAXM, lambda: ri(1, 3), True)))
add(*relabel(N, rg(N, 0, 10), blocks(N, MAXM, lambda: ri(1, 3), False)))
add(*relabel(N, rg(N), blocks(N, MAXM, lambda: ri(100, 2000), True)))
add(*relabel(N, rg(N, 0, 9999), blocks(N, MAXM, lambda: 2, False)))
add(N, rg(N), rand_edges(N, MAXM))
add(N, rg(N, 0, 99), rand_edges(N, N // 2))
add(*relabel(N, [0] * (N - 1) + [MAXG], [(i, i + 1) for i in range(1, N // 2)] + [(i + 1, i) for i in range(N // 2, N)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

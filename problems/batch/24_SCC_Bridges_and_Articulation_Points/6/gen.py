# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2406)
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


def relabel(n, edges):
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return e


def blocks(n, m, size_fn, links):
    """consecutive blocks, each a cycle; links random forward roads between blocks (a DAG of blocks), then
    random roads inside blocks up to m"""
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
    while links > 0:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if where[u] < where[v]:
            e.append((u, v))
            links -= 1
    while len(e) < m:
        u = ri(1, n)
        a, b = bl[where[u]]
        v = ri(a, b)
        if u != v:
            e.append((u, v))
    return e


def rand_edges(n, m):
    e = []
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
    return e


# samples
add(5, [(1, 2), (2, 3), (3, 1), (3, 4), (5, 4)])
add(3, [])
add(1, [])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
add(2, [(1, 2)])
add(6, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])
# hidden: small
add(2, [(1, 2), (2, 1)])
add(4, [(1, 2), (2, 1), (3, 4), (4, 3)])
add(5, [(1, 2), (3, 2), (4, 2), (2, 5)])
add(5, [(2, 1), (3, 1), (1, 4), (1, 5), (4, 5)])
for n, m in ((5, 3), (5, 5), (5, 6), (4, 3)):
    add(n, rand_edges(n, m))
add(2000, relabel(2000, blocks(2000, 3000, lambda: ri(1, 3), 1200)))
add(3000, rand_edges(3000, 3000))
# hidden: maximum size
N = MAXN
add(N, relabel(N, blocks(N, MAXM, lambda: 1, MAXM)))                         # a random DAG
add(N, relabel(N, [(i, i + 1) for i in range(1, N)]))                       # one chain: 1
add(N, relabel(N, [(i, i + 1) for i in range(1, N)] + [(N, 1)]))            # one long cycle: 0
add(N, relabel(N, blocks(N, N, lambda: 2, 0)))                              # separate pairs, nobody without a road in
add(170_000, relabel(170_000, blocks(170_000, MAXM, lambda: ri(2, 6), 20_000)))           # sources and sinks are cycles
add(N, relabel(N, [(1, i) for i in range(2, N + 1)]))                       # a star going out
add(N, relabel(N, [(i, 1) for i in range(2, N // 3)] + [(1, i) for i in range(N // 3, N + 1)]))
add(N, rand_edges(N, MAXM))
add(N, rand_edges(N, N // 2))
add(N, [])
add(150_000, relabel(150_000, blocks(150_000, 0, lambda: ri(2, 3), 8000)))      # cycles joined by a few roads
add(N - 1000, relabel(N - 1000, blocks(N - 1000, MAXM, lambda: ri(500, 1500), 150)))
add(N - 10, relabel(N - 10, blocks(N - 10, MAXM, lambda: 50_000, 3)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

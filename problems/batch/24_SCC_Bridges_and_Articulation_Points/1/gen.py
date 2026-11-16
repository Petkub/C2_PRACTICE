# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2401)
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
    """random user numbers and a random edge order"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return e


def blocks(n, m, sizes_fn):
    """cut 1..n into consecutive blocks; each block is a cycle (or a single user), the blocks form a chain,
    and the rest of the m edges go forward (from a smaller to a larger number) or inside a block"""
    edges, start, blk = [], 1, []
    while start <= n:
        s = min(sizes_fn(), n - start + 1)
        blk.append((start, start + s - 1))
        if s >= 2:
            edges += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        start += s
    for (a, b), (c, d) in zip(blk, blk[1:]):
        edges.append((ri(a, b), ri(c, d)))
    while len(edges) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u < v:
            edges.append((u, v))
    return edges[:m]


def rand_graph(n, m):
    edges = []
    while len(edges) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            edges.append((u, v))
    return edges


# samples
add(6, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 4), (6, 5)])
add(4, [(1, 2), (2, 1), (1, 2), (3, 4)])
add(1, [])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
add(5, [])
add(7, [(1, 2), (2, 3), (3, 2), (4, 5), (5, 6), (6, 4), (6, 7), (7, 1)])
# hidden: small
add(2, [(1, 2), (2, 1)])
add(3, [(1, 2), (2, 3), (1, 3)])
for n, m in ((6, 8), (8, 12), (10, 9), (12, 25)):
    add(n, rand_graph(n, m))
add(2000, relabel(2000, blocks(2000, 5000, lambda: ri(1, 4))))
add(3000, rand_graph(3000, 3300))
add(1500, relabel(1500, [(i, i + 1) for i in range(1, 1500)] + [(1500, 1)]))
# hidden: maximum size
N = MAXN
add(N, relabel(N, blocks(N, MAXM, lambda: 1)))                              # a DAG: every user alone
add(N, relabel(N, [(i, i + 1) for i in range(1, N)]))                       # one long chain
add(N, relabel(N, [(i, i + 1) for i in range(1, N)] + [(N, 1)]))            # one long cycle: N(N-1)/2 pairs
add(N, relabel(N, blocks(N, MAXM, lambda: 2)))                              # pairs chained one after another
add(N, relabel(N, blocks(N, MAXM, lambda: ri(1, 5))))
add(N, relabel(N, blocks(N, MAXM, lambda: ri(1, 1000))))
add(N, relabel(N, blocks(N, MAXM, lambda: 50_000)))
add(N, rand_graph(N, MAXM))                                                  # random: one big group + singles
add(N, relabel(N, [(1, i) for i in range(2, N + 1)]))                       # a star, all alone
add(N - 1, relabel(N - 1, [(i, i + 1) for i in range(1, N - 1)] + [(i + 1, i) for i in range(1, 2)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

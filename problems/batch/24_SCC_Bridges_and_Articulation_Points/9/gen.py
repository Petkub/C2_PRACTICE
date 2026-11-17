# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2409)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXN, MAXM, MAXQ = 100_000, 100_000, 100_000
tests = []


def shuffled(a):
    """a random permutation of the list a (faster than random.shuffle for long lists)"""
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def connected(n, edges):
    """union-find with path halving, written inline (fast enough for 2 * 10^5 edges)"""
    root = list(range(n + 1))
    comps = n
    for u, v in edges:
        while root[u] != u:
            root[u] = root[root[u]]
            u = root[u]
        while root[v] != v:
            root[v] = root[root[v]]
            v = root[v]
        if u != v:
            root[u] = v
            comps -= 1
    return comps == 1


def add(n, edges, qs):
    assert 1 <= n <= MAXN and n - 1 <= len(edges) <= MAXM and 1 <= len(qs) <= MAXQ
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in qs)
    assert connected(n, edges)
    tests.append(f"{n} {len(edges)} {len(qs)}\n" + "".join(["%d %d\n" % p for p in edges])
                 + "".join(["%d %d\n" % p for p in qs]))


def relabel(n, edges, qs, one=0):
    """random junction numbers for the edges and the queries, random road order and ends
    (one > 0: vertex `one` of the shape gets number 1)"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    if one:
        j = lab.index(1)
        lab[one - 1], lab[j] = lab[j], lab[one - 1]
    l0 = [0] + lab
    e = [(l0[a], l0[b]) if rnd() < 0.5 else (l0[b], l0[a]) for a, b in edges]
    e = shuffled(e)
    return n, e, [(l0[a], l0[b]) for a, b in qs]


def tree(n, kind):
    e = []
    half = n // 2
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "broom":
            p = i - 1 if i <= half else half
        else:
            p = 1
        e.append((p, i))
    return e


def bead_chain(n, lo, hi, parallel=False):
    """a chain of small cycles (or pairs of parallel roads) joined by single roads: a long bridge tree"""
    e, start, prev = [], 1, None
    while start <= n:
        s = min(ri(lo, hi), n - start + 1)
        if s >= 3:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        elif s == 2:
            e += [(start, start + 1)] * (2 if parallel or random.random() < 0.5 else 1)
        if prev is not None:
            e.append((ri(prev[0], prev[1]), ri(start, start + s - 1)))
        prev = (start, start + s - 1)
        start += s
    return e


def extra(n, e, k, near=0):
    e = list(e)
    while k > 0:
        u = ri(1, n)
        v = ri(1, n) if near == 0 else ri(max(1, u - near), min(n, u + near))
        if u != v:
            e.append((u, v))
            k -= 1
    return e


def rq(n, q):
    return [(ri(1, n), ri(1, n)) for _ in range(q)]


def far(n, q, w=100):
    """queries between the two ends of the shape (long tree paths)"""
    return [(ri(1, w), ri(n - w + 1, n)) if random.random() < 0.5 else (ri(n - w + 1, n), ri(1, w))
            for _ in range(q)]


# samples
add(6, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (5, 6)], [(1, 6), (2, 3), (4, 1), (6, 6), (5, 4)])
add(4, [(1, 2), (2, 3), (3, 4)], [(1, 4), (2, 4), (4, 1)])
add(1, [], [(1, 1)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1)], [(1, 3), (2, 4)])
add(5, [(1, 2), (2, 1), (2, 3), (3, 4), (3, 5)], [(1, 4), (4, 5), (1, 2), (5, 2)])
add(7, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4), (6, 7)], [(1, 7), (2, 5), (7, 4), (1, 3)])
# hidden: small
add(2, [(1, 2)], [(1, 2), (2, 1), (1, 1)])
add(2, [(1, 2), (2, 1)], [(1, 2)])
for n, k in ((6, 2), (8, 3), (10, 4), (12, 3)):
    add(*relabel(n, extra(n, tree(n, "random"), k), rq(n, 20)))
add(*relabel(20, bead_chain(20, 1, 4), rq(20, 30)))
add(*relabel(150, extra(150, tree(150, "random"), 30), rq(150, 150)))
add(*relabel(3000, tree(3000, "path") + [(3000, 1)], rq(3000, 3000)))           # one cycle: all 0
add(*relabel(3000, tree(3000, "binary"), rq(3000, 3000)))
# hidden: maximum size
N, M, Q = MAXN, MAXM, MAXQ
add(*relabel(N, tree(N, "path"), far(N, Q)))                                  # every road a bridge, long paths
e = bead_chain(70_000, 2, 4)
add(*relabel(70_000, e, far(70_000, Q)))
e = bead_chain(N // 2, 2, 2, True)                                            # pairs of parallel roads in a chain
add(*relabel(N // 2, e, far(N // 2, Q)))
c = 20_000                                                                    # a cycle with a long tail
add(*relabel(N, tree(N, "path") + [(c, 1)], far(N, Q), 22_000))
add(*relabel(N, tree(N, "broom"), far(N, Q, 5)))
add(*relabel(95_000, extra(95_000, tree(95_000, "path"), 5000, 2), far(95_000, Q), 5_000))  # a path, small cycles
e = tree(90_000, "path")                                                       # a path, some roads doubled
add(*relabel(90_000, e + random.sample(e, 9_999), far(90_000, Q), 5_000))
h = 70_000                                                                    # a comb: a path with leaves
add(*relabel(N, tree(h, "path") + [(ri(1, h), i) for i in range(h + 1, N + 1)], rq(N, Q), 1))
add(*relabel(N - 1000, extra(N - 1000, tree(N - 1000, "deep"), 1000, 30), far(N - 1000, Q)))
add(*relabel(60_000, bead_chain(60_000, 1, 3), far(60_000, Q)))
add(*relabel(N - 1, extra(N - 1, tree(N - 1, "path"), 1, 2), far(N - 1, Q, 1000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(200009)
MAXN, MAXK, MAXA = 100_000, 300, 10**9
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] (1 <= i < n) is a node in 0..i-1; node 0 is the root"""
    par = [-1] * n
    h = max(1, n // 2)
    s = max(1, int(n ** 0.5))
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # long and thin, short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "spider":                  # about sqrt(n) legs of length about sqrt(n) at the root
            par[i] = 0 if (i - 1) % s == 0 else i - 1
        elif kind == "twopaths":                # two long chains below the root
            par[i] = 0 if i <= 2 else i - 2
        elif kind == "midstar":                 # a path whose middle node has many leaves
            par[i] = i - 1 if i < h else h // 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    """a random numbering 1..n of the nodes 0..n-1 (node 0 gets root if given)"""
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def edge_list(par, lab):
    """edges (lab[u], lab[v]) of the tree in random order and orientation"""
    r = _rnd
    es = [(lab[par[i]], lab[i]) if r() < 0.5 else (lab[i], lab[par[i]]) for i in range(1, len(par))]
    shuf(es)
    return es


def shape_ok(par, lab):
    """par[i] < i for every node and lab is a numbering 1..n: the edges form a tree"""
    n = len(par)
    return (par[0] == -1 and all(0 <= par[i] < i for i in range(1, n))
            and len(set(lab)) == n and min(lab) == 1 and max(lab) == n)


def is_tree(n, es):
    if len(es) != n - 1:
        return False
    d = list(range(n + 1))

    def find(x):
        while d[x] != x:
            d[x] = d[d[x]]
            x = d[x]
        return x
    for u, v in es:
        if not (1 <= u <= n and 1 <= v <= n and u != v):
            return False
        a, b = find(u), find(v)
        if a == b:
            return False
        d[a] = b
    return True


def mis_size(n, es):
    """largest number of pairwise non-adjacent villages (greedy: take a leaf, drop its neighbour)"""
    adj = [[] for _ in range(n + 1)]
    for u, v in es:
        adj[u].append(v)
        adj[v].append(u)
    order, par = [1], [0] * (n + 1)
    par[1] = -1
    for v in order:
        for x in adj[v]:
            if x != par[v]:
                par[x] = v
                order.append(x)
    taken, blocked, cnt = [False] * (n + 1), [False] * (n + 1), 0
    for v in reversed(order):
        if not blocked[v]:
            taken[v] = True
            cnt += 1
            if par[v] > 0:
                blocked[par[v]] = True
    return cnt


def mis_par(par):
    """the same greedy on a shape with par[i] < i (children have larger indices)"""
    n = len(par)
    blocked, cnt = [False] * n, 0
    for v in range(n - 1, -1, -1):
        if not blocked[v]:
            cnt += 1
            if v:
                blocked[par[v]] = True
    return cnt


def add(K, a, es, checked=False):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= K <= min(n, MAXK)
    assert -MAXA <= min(a) and max(a) <= MAXA
    assert checked or is_tree(n, es)
    assert checked or K <= mis_size(n, es)
    tests.append(f"{n} {K}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in es))


def blocks_shape(n, k):
    """the root has many children, each heading a block of k nodes (worst case for the merging)"""
    par = [-1]
    for i in range(1, n):
        j = (i - 1) % k
        par.append(0 if j == 0 else i - ri(1, min(j, 3)))
    return par


def hubs_shape(n, k):
    """a random tree on n // k hubs, every other node a leaf of a random hub (many merges into a full table)"""
    m = max(1, n // k)
    par = [-1] + [int(_rnd() * i) for i in range(1, m)]
    while len(par) < n:
        par.append(ri(0, m - 1))
    return par


def build(n, K, kind, val, k=0):
    if kind == "blocks":
        par = blocks_shape(n, k)
    elif kind == "hubs":
        par = hubs_shape(n, k)
    else:
        par = shape(n, kind)
    dep = [0] * n
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
    lab = labels(n)
    a = [0] * n
    for i in range(n):
        a[lab[i] - 1] = val(i, dep[i])
    assert shape_ok(par, lab) and K <= mis_par(par)
    add(K, a, edge_list(par, lab), checked=True)


def uni(lo, hi):
    return lambda i, d: ri(lo, hi)


def bait(i, d):
    """odd levels are big, even levels negative: the forced choices hurt"""
    return ri(MAXA // 2, MAXA) if d % 2 == 1 else -ri(0, MAXA)


def mostly_neg(i, d):
    return ri(1, MAXA) if _rnd() < 0.05 else -ri(1, MAXA)


# samples
add(2, [5, 8, 6, 7, 3], [(1, 2), (1, 3), (3, 4), (3, 5)])
add(3, [-1, 4, -2, -3, 5], [(1, 2), (2, 3), (3, 4), (4, 5)])
add(1, [-7], [])
add(3, [10, 1, 1, 1, 1], [(1, 2), (1, 3), (1, 4), (1, 5)])
add(3, [4, -5, 9, 2, -1, 6, 3, -2], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)])
# hidden: small
add(1, [MAXA, -MAXA], [(1, 2)])
build(8, 3, "random", uni(-10, 10))
build(12, 5, "deep", bait)
build(16, 4, "random", mostly_neg)
build(18, 6, "cater", uni(-20, 20))
build(300, 100, "random", bait)
build(1000, 300, "blocks", uni(-MAXA, MAXA), 50)
build(2000, 150, "path", mostly_neg)
build(3000, 250, "spider", uni(-MAXA, MAXA))
# hidden: maximum size
N, K = MAXN, MAXK
build(N, K, "path", uni(-MAXA, MAXA))
build(N, K, "path", uni(MAXA, MAXA))           # the largest answer
build(N, K, "blocks", uni(-MAXA, MAXA), 300)  # worst case for the merging work
build(N, K, "blocks", bait, 200)
build(N, K, "hubs", mostly_neg, 400)          # skipping only the impossible rows is still O(N K^2) here
build(N, K, "random", uni(-MAXA, MAXA))
build(N, K, "hubs", bait, 1500)
build(N, K, "broom", uni(-MAXA, MAXA))
build(N, K, "star", uni(-MAXA, MAXA))
build(N, K, "binary", mostly_neg)
build(N, K, "deep", bait)
build(N, K, "cater", uni(-MAXA, MAXA))
build(N, K, "spider", bait)
build(N, K, "random", uni(-MAXA, -1))         # every value negative

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

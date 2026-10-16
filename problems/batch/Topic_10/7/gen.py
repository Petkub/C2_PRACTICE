# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(100707)
MAXN = 200_000
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    rnd = _rnd
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))                                 # = ri(0, i)
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] for i = 1..n-1 is a node in 0..i-1; node 0 is the root"""
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)                            # = ri(0, i - 1)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # depth about n / 2, a few short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging anywhere on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":                # two long chains below the root
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    """a random numbering 1..n of the nodes 0..n-1; node 0 gets the number root if given"""
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def add(n, edges, is_tree=False):
    """is_tree: from_par() already checked that the edges form a tree"""
    assert 1 <= n <= MAXN and len(edges) == n - 1
    if not is_tree:
        assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
        adj = [[] for _ in range(n + 1)]                        # n - 1 edges connecting everything: a tree
        for e in edges:
            adj[e[0]].append(e[1])
            adj[e[1]].append(e[0])
        seen, order = [False] * (n + 1), [1]
        seen[1] = True
        for v in order:
            for u in adj[v]:
                if not seen[u]:
                    seen[u] = True
                    order.append(u)
        assert len(order) == n
    t = f"{n}\n" + "".join(f"{a} {b}\n" for a, b in edges)
    assert len(t) <= 3_000_000
    tests.append(t)


def from_par(par, lab=None):
    n = len(par)
    if lab is None:
        lab = labels(n)
    # every node i >= 1 hangs below an earlier node and lab is a numbering 1..n: the edges form a tree
    assert all(0 <= par[i] < i for i in range(1, n)) and sorted(lab) == list(range(1, n + 1))
    rnd = _rnd
    edges = [(lab[par[i]], lab[i]) if rnd() >= 0.5 else (lab[i], lab[par[i]]) for i in range(1, n)]
    shuf(edges)
    add(n, edges, True)


def tree(n, kind):
    from_par(shape(n, kind))


def broom(n, handle):
    """a path of handle + 1 nodes, the other nodes are leaves at its end"""
    par = [-1] + [i - 1 if i <= handle else handle for i in range(1, n)]
    from_par(par)


def spider(n, legs, length_fun):
    """a centre with legs of the given lengths (the remaining nodes go to the first leg)"""
    lens = [length_fun() for _ in range(legs)]
    lens[0] += n - 1 - sum(lens)
    assert lens[0] >= 1
    par, cur = [-1], 0
    for L in lens:
        prev = 0
        for _ in range(L):
            cur += 1
            par.append(prev)
            prev = cur
    from_par(par)


def two_centres(n, small_first):
    """a path of even node count (two centres) with leaves near the middle; the centre with the smaller
    number is the first or the second middle node"""
    L = max(2, n // 4 * 2)                                      # number of path nodes (even)
    par = [-1] + [i - 1 for i in range(1, L)]
    for i in range(L, n):                                       # hang leaves on the middle part only
        par.append(ri(L // 4, 3 * L // 4))
    lab = labels(n)
    a, b = L // 2 - 1, L // 2                                   # the two centres
    if (lab[a] < lab[b]) != small_first:
        lab[a], lab[b] = lab[b], lab[a]
    from_par(par, lab)


# samples
add(6, [(4, 2), (2, 6), (6, 1), (1, 5), (6, 3)])
add(4, [(3, 1), (1, 4), (4, 2)])
add(1, [])
add(5, [(5, 1), (2, 5), (5, 3), (4, 5)])
add(2, [(2, 1)])
add(8, [(7, 3), (3, 6), (6, 2), (2, 8), (3, 1), (6, 5), (8, 4)])
# hidden: small
add(3, [(1, 3), (3, 2)])
add(4, [(4, 3), (3, 2), (2, 1)])
for n, kind in ((7, "random"), (10, "path"), (11, "path"), (12, "binary"), (30, "cater"), (100, "deep"),
                (1000, "random"), (3000, "twopaths")):
    tree(n, kind)
broom(500, 300)
two_centres(2000, False)
spider(5000, 20, lambda: ri(1, 100))
# hidden: maximum size
N = MAXN
tree(N, "path")
tree(N - 1, "path")
tree(N, "star")
tree(N, "random")
tree(N, "deep")
tree(N, "binary")
broom(N, 2 * N // 3)                                            # centre is in the handle, not at the busy end
two_centres(N, False)
two_centres(N - 1, True)
spider(N, 100, lambda: ri(1000, 2000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

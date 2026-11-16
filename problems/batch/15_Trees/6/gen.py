# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100606)
MAXN, MAXQ = 100_000, 100_000
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


def add(edges, qs, is_tree=False):
    """is_tree: tree() already checked that the edges form a tree"""
    n, q = len(edges) + 1, len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in qs)
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
    t = f"{n} {q}\n" + "".join(f"{a} {b}\n" for a, b in edges) + "".join(f"{u} {v}\n" for u, v in qs)
    assert len(t) <= 3_000_000
    tests.append(t)


def tree(n, kind, q, related=0.6):
    """random numbering with the mouth as point 1; about related * q queries ask a point and one of its
    ancestors (in random order), mostly deep points; the rest are random pairs"""
    par, lab = shape(n, kind), labels(n, 1)
    # every node hangs below an earlier node and lab is a numbering 1..n: the edges below form a tree
    assert all(0 <= par[i] < i for i in range(1, n)) and sorted(lab) == list(range(1, n + 1)) and lab[0] == 1
    ch = [[] for _ in range(n)]
    depth = [0] * n
    for i in range(1, n):
        ch[par[i]].append(i)
        depth[i] = depth[par[i]] + 1
    rnd, choice = _rnd, random.choice                           # rnd() inlined: ri(lo, hi) = lo + int(rnd() * (hi - lo + 1))
    anc, path, st = [-1] * n, [], [0]                           # preorder DFS; path = the nodes above the current one
    while st:
        v = st.pop()
        dv = depth[v]
        del path[dv:]
        if v:
            anc[v] = path[int(rnd() * dv)]                      # a random proper ancestor of v
        path.append(v)
        st.extend(reversed(ch[v]))
    order = sorted(range(1, n), key=depth.__getitem__, reverse=True)     # deepest first (stable)
    deep = order[:max(1, len(order) * 3 // 10)]
    qs = []
    for _ in range(q):
        if rnd() < related:
            v = choice(deep)
            a, b = lab[v], lab[anc[v]]
        else:
            a, b = 1 + int(rnd() * n), 1 + int(rnd() * (n - 1))
            if b >= a:
                b += 1
        qs.append((a, b) if int(rnd() * 2) else (b, a))
    edges = []
    for i in range(1, n):
        e = (lab[par[i]], lab[i])
        edges.append(e if int(rnd() * 2) else e[::-1])
    shuf(edges)
    add(edges, qs, True)


# samples
add([(1, 2), (2, 3), (4, 2), (4, 5)], [(5, 2), (2, 5), (3, 4), (5, 1)])
add([(2, 1), (1, 3), (3, 4)], [(4, 1), (2, 4), (3, 4)])
add([(3, 1), (2, 3), (5, 1), (4, 5)], [(2, 3), (4, 3), (1, 4), (3, 2)])
add([(1, 4), (4, 2), (3, 4)], [(2, 3), (1, 3), (3, 4)])
add([(2, 1)], [(1, 2), (2, 1)])
# hidden: small
for n, kind, q in ((6, "random", 15), (10, "path", 20), (12, "binary", 30), (15, "star", 30), (40, "cater", 50),
                   (200, "deep", 300), (1000, "twopaths", 1000), (3000, "random", 3000), (5000, "broom", 5000)):
    tree(n, kind, q)
# hidden: maximum size
N, Q = MAXN, MAXQ
tree(N, "path", Q, 0.2)
tree(N, "path", Q, 0.9)
tree(N, "deep", Q)
tree(N, "twopaths", Q, 0.5)
tree(N, "broom", Q)
tree(N, "cater", Q)
tree(N, "random", Q)
tree(N, "star", Q, 0.3)
tree(N, "binary", Q, 0.5)
tree(N, "twopaths", Q, 0.1)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

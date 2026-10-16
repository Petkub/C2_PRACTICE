# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100303)
MAXN, MAXW = 100_000, 10**9
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))                                # = ri(0, i)
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


def add(edges):
    n = len(edges) + 1
    assert 2 <= n <= MAXN
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= w <= MAXW for a, b, w in edges)
    adj = [[] for _ in range(n + 1)]                            # n - 1 edges connecting everything: a tree
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
    t = f"{n}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
    assert len(t) <= 3_000_000
    tests.append(t)


def tree(n, kind, wfun):
    """wfun(i, par) gives the weight of the edge from node i to its parent"""
    par, lab = shape(n, kind), labels(n)
    edges = []
    for i in range(1, n):
        a, b = lab[par[i]], lab[i]
        if ri(0, 1):
            a, b = b, a
        edges.append((a, b, wfun(i, par)))
    shuf(edges)
    add(edges)


rnd = lambda lo, hi: (lambda i, par: ri(lo, hi))

# samples
add([(1, 2, 3), (2, 3, 4), (2, 4, 2), (4, 5, 6)])
add([(1, 2, 1), (2, 3, 1), (3, 4, 1), (5, 2, 9)])
add([(2, 1, MAXW)])
add([(1, 2, MAXW), (3, 2, MAXW), (3, 4, MAXW)])
add([(4, 7, 5), (1, 4, 2), (7, 3, 8), (6, 1, 3), (2, 4, 7), (8, 1, 4), (5, 6, 6)])
# hidden: small
add([(1, 2, 1)])
add([(1, 2, 5), (1, 3, 5), (1, 4, 5)])
for n, kind, f in ((6, "random", rnd(1, 10)), (9, "binary", rnd(1, 10)), (12, "random", rnd(1, 100)),
                   (20, "cater", rnd(1, 5)), (60, "deep", rnd(1, MAXW)), (300, "random", rnd(1, 1000)),
                   (2000, "broom", rnd(1, MAXW)), (5000, "random", rnd(1, MAXW))):
    tree(n, kind, f)
# hidden: maximum size
N = MAXN
tree(N, "path", lambda i, par: MAXW)                             # answer (N - 1) * 10^9
tree(N, "path", rnd(1, MAXW))
tree(N, "star", rnd(1, MAXW))
tree(N, "random", rnd(1, MAXW))
tree(N, "deep", rnd(1, MAXW))
# a long light spine and heavy leaves: the longest trail joins two leaves, not the spine ends
tree(N, "cater", lambda i, par: 1 if i < N // 2 else ri(MAXW // 2, MAXW))
# a broom: the handle is light, the bristles heavy
tree(N, "broom", lambda i, par: ri(1, 100) if i <= N // 2 else ri(1, MAXW))
tree(N, "twopaths", rnd(MAXW - 10, MAXW))
tree(N, "binary", rnd(1, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

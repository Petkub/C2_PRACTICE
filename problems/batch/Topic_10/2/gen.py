# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100202)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10**9
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


def add(r, w, edges, qs):
    n, q = len(w), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and 1 <= r <= n
    assert all(0 <= x <= MAXW for x in w) and all(1 <= v <= n for v in qs)
    assert len(edges) == n - 1 and all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
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
    t = (f"{n} {q} {r}\n" + " ".join(map(str, w)) + "\n" + "".join(f"{a} {b}\n" for a, b in edges)
         + " ".join(map(str, qs)) + "\n")
    assert len(t) <= 3_200_000
    tests.append(t)


def tree(n, kind, q, wfun, heavy=0.5):
    """random numbering, root is node 0; about heavy * q queries ask the nodes nearest to the root"""
    par, lab = shape(n, kind), labels(n)
    edges = []
    for i in range(1, n):
        e = (lab[par[i]], lab[i])
        edges.append(e if ri(0, 1) else e[::-1])
    shuf(edges)
    w = [wfun() for _ in range(n)]
    top = min(n, 20)
    qs = [lab[ri(0, top - 1)] if random.random() < heavy else ri(1, n) for _ in range(q)]
    add(lab[0], w, edges, qs)


# samples
add(2, [3, 5, 1, 4, 2], [(2, 1), (2, 3), (3, 4), (5, 3)], [2, 3, 1, 4])
add(4, [10, 20, 30, 40], [(1, 2), (3, 2), (3, 4)], [1, 3, 4])
add(5, [7, 0, 2, 9, 4], [(5, 2), (1, 5), (4, 1), (3, 4)], [5, 2, 1, 3])
add(1, [0], [], [1])
add(2, [MAXW] * 2, [(1, 2)], [2, 1])
# hidden: small
add(2, [1, 2], [(1, 2)], [1, 2, 2, 1])
for n, kind in ((7, "random"), (10, "path"), (12, "binary"), (15, "star"), (40, "cater"), (200, "deep"),
                (1000, "random"), (3000, "twopaths")):
    tree(n, kind, n, lambda: ri(0, 100), 0.3)
tree(5000, "path", 5000, lambda: MAXW)
# hidden: maximum size
N, Q = MAXN, MAXQ
big = lambda: ri(MAXW - 1000, MAXW)
tree(N, "path", Q, big, 0.0)
tree(N, "path", Q, lambda: MAXW, 0.9)
tree(N, "deep", Q, big)
tree(N, "star", Q, big)
tree(N, "random", Q, lambda: ri(0, MAXW))
tree(N, "broom", Q, big)
tree(N, "twopaths", Q, lambda: ri(0, 10))
tree(N, "binary", Q, big, 0.8)
tree(N, "cater", Q, lambda: MAXW)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
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
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def add(edges, qs, is_tree=False):
    n, q = len(edges) + 1, len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in qs)
    if not is_tree:
        assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
        adj = [[] for _ in range(n + 1)]
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
    par, lab = shape(n, kind), labels(n, 1)

    assert all(0 <= par[i] < i for i in range(1, n)) and sorted(lab) == list(range(1, n + 1)) and lab[0] == 1
    ch = [[] for _ in range(n)]
    depth = [0] * n
    for i in range(1, n):
        ch[par[i]].append(i)
        depth[i] = depth[par[i]] + 1
    rnd, choice = _rnd, random.choice
    anc, path, st = [-1] * n, [], [0]
    while st:
        v = st.pop()
        dv = depth[v]
        del path[dv:]
        if v:
            anc[v] = path[int(rnd() * dv)]
        path.append(v)
        st.extend(reversed(ch[v]))
    order = sorted(range(1, n), key=depth.__getitem__, reverse=True)
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


add([(1, 2), (2, 3), (4, 2), (4, 5)], [(5, 2), (2, 5), (3, 4), (5, 1)])
add([(2, 1), (1, 3), (3, 4)], [(4, 1), (2, 4), (3, 4)])
add([(3, 1), (2, 3), (5, 1), (4, 5)], [(2, 3), (4, 3), (1, 4), (3, 2)])
add([(1, 4), (4, 2), (3, 4)], [(2, 3), (1, 3), (3, 4)])
add([(2, 1)], [(1, 2), (2, 1)])

for n, kind, q in ((6, "random", 15), (10, "path", 20), (12, "binary", 30), (15, "star", 30), (40, "cater", 50),
                   (200, "deep", 300), (1000, "twopaths", 1000), (3000, "random", 3000), (5000, "broom", 5000)):
    tree(n, kind, q)

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

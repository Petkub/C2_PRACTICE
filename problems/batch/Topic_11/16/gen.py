# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90116)
MAXN, MAXM, MAXW = 50_000, 150_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True):
    m = len(edges)
    assert 2 <= n <= MAXN and n - 1 <= m <= MAXM
    par = list(range(n + 1))                     # all cables together connect every city
    comps = n
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        while par[v] != v:
            par[v] = par[par[v]]
            v = par[v]
        if u != v:
            par[u] = v
            comps -= 1
    assert comps == 1
    if shuffle:
        edges = edges[:]
        random.shuffle(edges)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def tree(n, kind):
    """(parent, depth) arrays of a tree on 1..n before relabelling"""
    p, d = [0, 0], [0, 0]
    for i in range(2, n + 1):
        if kind == "path":
            p.append(i - 1)
        elif kind == "deep":
            p.append(ri(max(1, i - 4), i - 1))
        elif kind == "star":
            p.append(1)
        else:
            p.append(ri(1, i - 1))
        d.append(d[p[i]] + 1)
    return p, d


def layered(n, m, kind, step, lo, extra, needles=0):
    """the cable from a city to its parent costs g(depth), g never decreasing; any other cable
    between x and y costs g(max depth) + delta: delta >= 1 keeps the cheapest network unique,
    delta = 0 (a needle) gives a second one. The first needle runs from the deepest city to the
    root; it and the network cable of the deepest city are the last two lines"""
    p, d = tree(n, kind)
    g = [lo + dd // step for dd in range(n + 1)]
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    deepest = max(range(1, n + 1), key=lambda v: d[v])
    edges, last = [], []
    for i in range(2, n + 1):
        e = (lab[i], lab[p[i]], g[d[i]])
        (last if needles and i == deepest else edges).append(e)
    r = random.random
    for k in range(m - (n - 1)):
        x = 1 + int(r() * n)
        y = 1 + int(r() * (n - 1))
        y += y >= x
        if k == 0 and needles:
            x, y = deepest, 1
        e = (lab[x], lab[y], g[max(d[x], d[y])] + (0 if k < needles else ri(1, extra)))
        (last if k == 0 and needles else edges).append(e)
    if n < 1000:
        random.shuffle(edges)
    random.shuffle(last)
    return edges + last


def rnd_graph(n, m, wlo, whi):
    p, d = tree(n, "rnd")
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    edges = [(lab[i], lab[p[i]], ri(wlo, whi)) for i in range(2, n + 1)]
    while len(edges) < m:
        x = ri(1, n)
        y = ri(1, n - 1)
        edges.append((x, y + (y >= x), ri(wlo, whi)))
    return edges


# samples
add(4, [(1, 2, 1), (2, 3, 2), (3, 4, 2), (1, 4, 3), (2, 4, 2)], False)
add(3, [(1, 2, 5), (2, 3, 5), (1, 3, 6)], False)
add(2, [(1, 2, 4), (2, 1, 4)], False)
add(2, [(1, 2, 1000000)], False)
add(5, [(1, 2, 3), (2, 3, 3), (3, 1, 4), (3, 4, 1), (4, 5, 3), (4, 3, 3), (1, 5, 5)], False)
# hidden: small
add(2, [(1, 2, 1)])
add(3, [(1, 2, 2), (2, 3, 2), (1, 3, 2)])                        # a triangle of equal cables
add(4, [(1, 2, 1), (1, 2, 1), (2, 3, 5), (3, 4, 2)])             # equal parallel cables
add(4, [(1, 2, 1), (1, 2, 2), (2, 3, 5), (3, 4, 5), (2, 4, 6)])  # different parallel cables
for n, m, wmax in ((5, 8, 3), (6, 10, 2), (7, 12, 4), (8, 14, 3), (9, 16, 5), (10, 18, 3)):
    add(n, rnd_graph(n, m, 1, wmax))
add(9, layered(9, 18, "rnd", 2, 1, 2), False)
add(10, layered(10, 18, "deep", 1, 5, 1), False)
add(10, layered(10, 18, "rnd", 3, 1, 3, 1), False)
add(300, rnd_graph(300, 900, 1, 1000))
add(500, layered(500, 1500, "deep", 3, 1, 2), False)
add(500, layered(500, 1500, "rnd", 1, 1, 2, 1), False)
add(1000, layered(1000, 3000, "deep", 1, 1, 2, 20), False)  # a few needles
# hidden: maximum size
N, M = MAXN, MAXM
add(N, layered(N, M, "path", 7, 1, 3), False)                   # unique, many equal costs
add(N, layered(N, M, "deep", 1, 1, 2), False)
add(N, layered(N, M, "deep", 50, 1, 1), False)
add(N, layered(N, M, "path", 1, 1, 2, 1), False)                # exactly one needle
add(N, layered(N, M, "deep", 1, 1, 5, 1), False)
add(N, layered(N, M, "deep", 5, 1, 3), False)
add(N, layered(N, M, "star", 1, MAXW - 2, 1), False)            # all network cables cost the same
add(N, rnd_graph(N, M, 1, MAXW), False)                         # random costs
add(N, rnd_graph(N, M, 1, 20), False)                           # many equal costs
add(N, rnd_graph(N, N - 1, MAXW, MAXW), False)                  # only a tree: unique, largest total
add(N, rnd_graph(N, N, MAXW, MAXW), False)                      # one more cable of the same cost
add(N, layered(N, M, "path", 1, MAXW - N, 1), False)
add(N, layered(N, M, "deep", 3, 1, 1), False)
add(N, layered(N, M, "path", 20, MAXW - N, 1), False)
add(N, layered(N, M, "path", 2, 1, 1), False)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

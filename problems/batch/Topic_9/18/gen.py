# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90118)
MAXN, MAXM, MAXW = 5000, 150_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True):
    m = len(edges)
    assert 2 <= n <= MAXN and n - 1 <= m <= MAXM
    par = list(range(n + 1))                     # all roads together connect every city
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
    """(parent, depth) of a tree on 1..n before relabelling"""
    p, d = [0, 0], [0, 0]
    for i in range(2, n + 1):
        if kind == "path":
            p.append(i - 1)
        elif kind == "deep":
            p.append(ri(max(1, i - 3), i - 1))
        elif kind == "broom":                    # a long handle, then a star
            p.append(i - 1 if i <= n // 2 else n // 2)
        elif kind == "star":
            p.append(1)
        else:
            p.append(ri(1, i - 1))
        d.append(d[p[i]] + 1)
    return p, d


def layered(n, m, kind, g, dlo, dhi, far, ties=0):
    """the road from a city to its parent costs g[depth] (g never decreasing), any other road between
    x and y costs g[max depth] + delta with dlo <= delta <= dhi, so the tree is a cheapest network.
    far: one end among the shallowest tenth of the cities, the other among the deepest tenth.
    ties: extra short roads (2 to 5 levels up) that cost exactly as much as the dearest road they bypass"""
    p, d = tree(n, kind)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    edges = [(lab[i], lab[p[i]], g[d[i]]) for i in range(2, n + 1)]
    order = sorted(range(1, n + 1), key=lambda v: d[v])
    k = max(1, n // 10)
    r = random.random
    for _ in range(m - (n - 1) - ties):
        if far:
            x, y = order[int(r() * k)], order[n - 1 - int(r() * k)]
            if x == y:
                y = order[-1] if x != order[-1] else order[0]
        else:
            x = 1 + int(r() * n)
            y = 1 + int(r() * (n - 1))
            y += y >= x
        edges.append((lab[x], lab[y], g[max(d[x], d[y])] + dlo + int(r() * (dhi - dlo + 1))))
    deep = [v for v in range(1, n + 1) if d[v] >= 2]
    for _ in range(ties):
        y = random.choice(deep)
        x = p[p[y]]
        for _ in range(ri(0, 3)):
            if p[x]:
                x = p[x]
        edges.append((lab[x], lab[y], g[d[y]]))
    if n < 1000:
        random.shuffle(edges)
    return edges


def steps(n, lo, every):
    """never decreasing costs by depth: +1 after every 'every' levels"""
    return [lo + dd // every for dd in range(n + 1)]


def rnd_graph(n, m, wlo, whi):
    p, d = tree(n, "rnd")
    edges = [(i, p[i], ri(wlo, whi)) for i in range(2, n + 1)]
    while len(edges) < m:
        x = ri(1, n)
        y = ri(1, n - 1)
        edges.append((x, y + (y >= x), ri(wlo, whi)))
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    return [(lab[u - 1], lab[v - 1], w) for u, v, w in edges]


# samples
add(4, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 3, 2), (2, 4, 5)], False)
add(3, [(1, 2, 4), (2, 3, 4), (1, 3, 4)], False)
add(4, [(1, 2, 7), (1, 3, 1), (1, 4, 1000000)], False)
add(3, [(1, 2, 2), (1, 2, 3), (2, 3, 2), (3, 1, 3)], False)
add(5, [(1, 2, 3), (2, 3, 3), (3, 4, 5), (4, 5, 5), (5, 1, 5), (2, 4, 6), (1, 3, 3)], False)
# hidden: small (every set of roads is tried)
add(2, [(1, 2, 1)])
add(2, [(1, 2, 5), (2, 1, 5), (1, 2, 6)])
for n, m, wmax in ((4, 8, 2), (5, 10, 3), (6, 12, 1), (6, 14, 3), (7, 16, 4), (8, 18, 10)):
    add(n, rnd_graph(n, m, 1, wmax))
add(8, layered(8, 18, "path", [5] * 4 + [6] * 5, 0, 0, False))
add(9, layered(9, 18, "rnd", steps(9, 1, 1), 0, 1, False))
add(9, layered(9, 18, "path", steps(9, 1, 1), 2, 3, True, 3))
# hidden: medium
add(200, rnd_graph(200, 2000, 1, 3))
add(500, layered(500, 5000, "deep", steps(500, 1, 40), 0, 1, True))
add(600, layered(600, 6000, "path", steps(600, 1, 1), 2, 4, True, 20))
add(1000, rnd_graph(1000, 20000, 1, MAXW))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, layered(N, M, "path", steps(N, 1, 1), 2, 5, True, 10), False)          # long cycles everywhere
add(N, layered(N, M, "path", steps(N, MAXW - 3000, 2), 1, 3, True, 10), False)
add(N, layered(N, M, "deep", steps(N, 1, 1), 2, 2, True, 10), False)
add(N, layered(N, M, "broom", steps(N, 1000, 1), 3, 9, True, 5), False)
add(N, layered(N, M, "path", steps(N, 1, 3), 1, 1, True, 3), False)
add(N, layered(N, M, "path", steps(N, 1, 1), 2, 2, True, 0), False)          # equal swaps are not there
add(N, layered(N, M, "path", [MAXW] * (N + 1), 0, 0, True), False)          # every network costs the same
add(N, layered(N, M, "path", [7] * (N // 2) + [8] * (N - N // 2 + 1), 0, 0, True), False)
add(N, layered(N, M, "deep", steps(N, 1, 100), 0, 0, True), False)
add(N, layered(N, M, "rnd", steps(N, 1, 1), 0, 1, False), False)
add(N, layered(N, M, "broom", steps(N, 1, 2), 1, 4, True, 10), False)
add(N, layered(N, M, "deep", steps(N, MAXW - N, 1), 2, 3, True, 10), False)
add(N, layered(N, M, "star", [MAXW - 1] * (N + 1), 0, 1, False), False)
add(N, rnd_graph(N, M, 1, MAXW), False)
add(N, rnd_graph(N, M, 1, 2), False)
add(N, rnd_graph(N, N - 1, 1, MAXW), False)                                  # only one network
add(N, layered(N, M, "path", steps(N, MAXW - N - 5, 1), 2, 5, True, 10), False)  # largest costs

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

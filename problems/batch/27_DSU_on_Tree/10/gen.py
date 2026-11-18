# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


random.seed(271010)
MAXN = MAXM = MAXQ = 100_000


def add(n, p, edges, qs):
    assert 2 <= n <= MAXN and 1 <= len(edges) <= MAXM and 1 <= len(qs) <= MAXQ
    assert sorted(p) == list(range(1, n + 1))
    seen = set()
    for u, v in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        key = (min(u, v), max(u, v))
        assert key not in seen
        seen.add(key)
    for u, v in qs:
        assert 1 <= u <= n and 1 <= v <= n and u != v
    tests.append(f"{n} {len(edges)}\n" + " ".join(map(str, p)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges)
                 + f"{len(qs)}\n" + "".join(f"{u} {v}\n" for u, v in qs))


def graph(n, m, kind, comps=1):
    edges = set()
    lab = list(range(1, n + 1))
    shuffle(lab)
    size = max(2, n // comps)
    blocks = [lab[i:i + size] for i in range(0, n, size)]
    if len(blocks[-1]) < 2 and len(blocks) > 1:
        blocks[-2] += blocks.pop()

    def put(u, v):
        if u != v:
            edges.add((min(u, v), max(u, v)))
    for bl in blocks:
        if kind == "tree":
            for i in range(1, len(bl)):
                put(bl[i], bl[ri(0, i - 1)])
        elif kind == "path":
            for i in range(1, len(bl)):
                put(bl[i], bl[i - 1])
    tries = 0
    while len(edges) < m and tries < 20 * m:
        tries += 1
        bl = blocks[ri(0, len(blocks) - 1)]
        put(bl[ri(0, len(bl) - 1)], bl[ri(0, len(bl) - 1)])
    out = sorted(edges)
    shuffle(out)
    return [(u, v) if random.random() < 0.5 else (v, u) for u, v in out][:m]


def make(n, m, q, kind, comps=1, order="rand"):
    edges = graph(n, m, kind, comps)
    p = list(range(1, n + 1))
    shuffle(p)
    if order == "deg":
        deg = [0] * (n + 1)
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
        p.sort(key=lambda x: deg[x])
    qs = []
    adjq = [[] for _ in range(n + 1)]
    for u, v in edges:
        adjq[u].append(v)
        adjq[v].append(u)
    for _ in range(q):
        u = ri(1, n)
        if random.random() < 0.3:
            if adjq[u]:
                w = adjq[u][ri(0, len(adjq[u]) - 1)]
                v = adjq[w][ri(0, len(adjq[w]) - 1)]
            else:
                v = ri(1, n)
        else:
            v = ri(1, n)
        if v == u:
            v = u % n + 1
        qs.append((u, v))
    add(n, p, edges, qs)


def hubs(n, m, q, h, s):
    lab = list(range(1, n + 1))
    shuffle(lab)
    hub = lab[:h]
    edges = set()
    for x in hub:
        others = lab[h:]
        shuffle(others)
        for y in others[:s]:
            edges.add((min(x, y), max(x, y)))
    while len(edges) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            edges.add((min(u, v), max(u, v)))
    out = sorted(edges)
    shuffle(out)
    out = out[:m]
    rest = lab[h:]
    shuffle(rest)
    p = hub + rest
    qs = []
    for _ in range(q):
        u, v = ri(1, n), ri(1, n)
        if v == u:
            v = u % n + 1
        qs.append((u, v))
    add(n, p, out, qs)


add(6, [3, 1, 5, 2, 6, 4], [(3, 1), (3, 5), (3, 6), (1, 2), (5, 4)], [(1, 6), (3, 4), (6, 5), (1, 4)])
add(5, [3, 1, 4, 5, 2], [(1, 2), (2, 3), (3, 4), (4, 5)], [(1, 4), (2, 4), (1, 5)])
add(2, [2, 1], [(1, 2)], [(2, 1)])
add(4, [1, 2, 3, 4], [(1, 2), (1, 3), (1, 4)], [(2, 4), (3, 1)])
add(3, [1, 3, 2], [(1, 2), (2, 3)], [(1, 3)])

make(8, 9, 20, "rand")
make(20, 25, 40, "tree", 2)
make(50, 80, 100, "path")
make(100, 150, 200, "rand", 3)
make(300, 400, 400, "tree", 1, "deg")
make(1000, 1500, 1000, "rand", 5)
make(2000, 3000, 2000, "path", 2)

make(MAXN, MAXM, MAXQ, "rand")
make(MAXN, MAXM, MAXQ, "tree")
hubs(MAXN, MAXM, MAXQ, 1, 99_000)
make(MAXN, MAXM, MAXQ, "rand", 2)
hubs(MAXN, MAXM, MAXQ, 4, 25_000)
hubs(MAXN, MAXM, MAXQ, 5, 18_000)
make(MAXN, MAXM, MAXQ, "path", 3)
hubs(MAXN, MAXM, MAXQ, 2, 52_000)
hubs(MAXN, MAXM, MAXQ, 1, 70_000)
make(MAXN, 99_999, MAXQ, "tree")
hubs(MAXN, MAXM, MAXQ, 3, 30_000)

write_all()

import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    """Fisher-Yates with random.random (faster than random.shuffle, same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind, legs=4):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape (node 1 is the root), before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    leg = max(1, (n - 1) // legs)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "deep":                        # depth about n / 2, a few short branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "caterpillar":                 # a spine of n / 2 nodes with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "spider":                      # legs long chains hanging from the root
            p = 1 if (i - 2) % leg == 0 or i - 1 > leg * legs else i - 1
        elif kind == "lopsided":                    # the root joins a chain of 90% and a chain of 10%
            p = 1 if i == 2 or i == 2 + (n - 1) * 9 // 10 else i - 1
        elif kind == "forkdeep":                    # a chain of n / 4, then two long chains
            q = n // 4
            if i <= q:
                p = i - 1
            elif i == q + 1 or i == q + 2:
                p = q
            else:
                p = i - 2
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def depths(par):
    d = [0] * len(par)
    for i in range(2, len(par)):
        d[i] = d[par[i]] + 1
    return d


def colours(par, mode, k=2, keep=0.8):
    """col[i] = company of the road i - par[i] (shape labels)"""
    n = len(par) - 1
    col = [0] * (n + 1)
    pal = list(range(1, k + 1)) if mode in ("few", "runs") else []
    if mode == "pal":                               # k big company numbers
        pal = [ri(1, 10 ** 9) for _ in range(k)]
    d = depths(par) if mode == "alt" else None
    for i in range(2, n + 1):
        if mode == "few":
            col[i] = pal[ri(0, k - 1)]
        elif mode in ("runs", "pal"):               # a company tends to serve a long stretch of roads
            if par[i] != 1 and random.random() < keep:
                col[i] = col[par[i]]
            else:
                col[i] = pal[ri(0, k - 1)]
        elif mode == "big":
            col[i] = ri(1, 10 ** 9)
        elif mode == "same":
            col[i] = k
        elif mode == "alt":                         # companies alternate road by road
            col[i] = 1 + d[i] % 2
        else:
            raise ValueError(mode)
    return col


MAXN, MAXQ = 100_000, 100_000


def check_tree(n, edges):
    adj = [[] for _ in range(n + 1)]
    for a, b, c in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b and 1 <= c <= 10 ** 9
        adj[a].append(b)
        adj[b].append(a)
    seen, order = [False] * (n + 1), [1]
    seen[1] = True
    for v in order:
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                order.append(w)
    assert len(order) == n


def add(n, edges, qs):
    assert 2 <= n <= MAXN and len(edges) == n - 1 and 1 <= len(qs) <= MAXQ
    check_tree(n, edges)
    for u, v in qs:
        assert 1 <= u <= n and 1 <= v <= n
    t = f"{n} {len(qs)}\n" + "".join(["%d %d %d\n" % e for e in edges]) \
        + "".join(["%d %d\n" % x for x in qs])
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    tests.append(t)


def make(n, kind, q, cmode, k=2, keep=0.8, qmode="rand", legs=4, top=10, deep=0.05, ptop=0.3, same=0.01):
    """qmode rand: both ends anywhere; far: one end among the deepest fraction `deep` of the shape, the other
    with probability ptop among the `top` shallowest towns, else also among the deepest ones"""
    par = shape(n, kind, legs)
    col = colours(par, cmode, k, keep)
    lab = list(range(1, n + 1))                     # random labels, the root keeps label 1
    shuffle(lab)
    j = lab.index(1)
    lab[0], lab[j] = lab[j], lab[0]
    edges = []
    for i in range(2, n + 1):
        a, b = lab[i - 1], lab[par[i] - 1]
        if random.random() < 0.5:
            a, b = b, a
        edges.append((a, b, col[i]))
    shuffle(edges)
    d = depths(par)
    byd = sorted(range(1, n + 1), key=d.__getitem__)      # stable: ties by label
    bottom = byd[-max(2, int(n * deep)):]
    tops = byd[:max(1, top)]
    rnd = random.random
    qs = []
    for _ in range(q):
        if qmode == "far":
            u = bottom[int(rnd() * len(bottom))]
            v = tops[int(rnd() * len(tops))] if rnd() < ptop else bottom[int(rnd() * len(bottom))]
        else:
            u, v = ri(1, n), ri(1, n)
        if rnd() < same:
            v = u
        if rnd() < 0.5:
            u, v = v, u
        qs.append((lab[u - 1], lab[v - 1]))
    add(n, edges, qs)


random.seed(230202)
# samples
add(6, [(1, 2, 1), (4, 2, 1), (5, 2, 3), (1, 3, 2), (6, 3, 3)], [(4, 6), (5, 6), (6, 1)])
add(5, [(4, 2, 5), (2, 1, 8), (1, 3, 8), (3, 5, 5)], [(4, 5), (2, 3), (5, 5)])
add(2, [(2, 1, 7)], [(1, 2), (2, 2)])
add(4, [(1, 2, 1), (3, 1, 2), (1, 4, 1)], [(2, 4), (2, 3), (4, 1)])
add(6, [(5, 1, 10 ** 9), (5, 2, 10 ** 9), (2, 6, 3), (3, 5, 10 ** 9), (1, 4, 3)], [(6, 3), (6, 4), (2, 3)])
# hidden: small and medium (any shape)
add(3, [(2, 3, 4), (1, 3, 9)], [(u, v) for u in range(1, 4) for v in range(1, 4)])
make(10, "random", 30, "few", k=2)
make(60, "deep", 100, "runs", k=3, keep=0.6, qmode="far", top=3, deep=0.2)
make(100, "caterpillar", 100, "few", k=2, same=0.05)
make(300, "binary", 300, "runs", k=2, keep=0.5)
make(3000, "star", 3000, "few", k=3)
make(4000, "random", 3000, "runs", k=4, keep=0.7)
make(5000, "spider", 3000, "pal", k=3, keep=0.8, qmode="far", legs=6, deep=0.1)
# hidden: maximum size, deep shapes, ends far apart
make(MAXN, "path", MAXQ, "few", k=2, qmode="far", top=50, ptop=0.5)
make(MAXN, "path", MAXQ, "runs", k=3, keep=0.9)
make(MAXN, "spider", MAXQ, "few", k=2, qmode="far", legs=2, deep=0.02, ptop=0.4)
make(MAXN, "spider", MAXQ, "pal", k=5, keep=0.85, qmode="far", legs=7, deep=0.02, ptop=0.2)
make(MAXN, "deep", MAXQ, "runs", k=4, keep=0.7, qmode="far", top=1000, ptop=0.5)
make(MAXN, "caterpillar", MAXQ, "few", k=2, qmode="far", deep=0.05)
make(MAXN, "broom", MAXQ, "runs", k=2, keep=0.8, qmode="far", top=200)
make(MAXN, "forkdeep", MAXQ, "few", k=3, qmode="far", top=20, deep=0.3)
make(MAXN, "lopsided", 80_000, "big", qmode="far", top=100, deep=0.4)
make(MAXN, "path", MAXQ, "same", k=7, qmode="far", top=20)
make(MAXN, "deep", MAXQ, "alt", qmode="far", top=500, deep=0.1)
make(MAXN, "spider", MAXQ, "runs", k=3, keep=0.95, qmode="far", legs=3, deep=0.1, ptop=0.5)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

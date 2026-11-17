import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    h = max(1, 7 * n // 10)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":                        # depth about n / 2, a few short branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a spine of n / 2 nodes with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "twopaths":                    # two long chains meeting at node 1
            p = 1 if i <= 3 else i - 2
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        elif kind == "longrandom":                  # a chain of 7n / 10 nodes, the rest hung at random
            p = i - 1 if i <= h else ri(1, i - 1)
        elif kind == "longbinary":                  # a chain of 7n / 10 nodes ending in a binary tree
            p = i - 1 if i <= h else h - 1 + (i - h + 1) // 2
        elif kind == "longstar":                    # a chain of 7n / 10 nodes plus a star around node 1
            p = i - 1 if i <= h else 1
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    """Fisher-Yates with random.random (faster than random.shuffle, same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def relabel(par, root_first=False):
    """random labels (node 1 of the shape keeps label 1 if root_first), shuffled edges and ends;
    lab[i - 1] is the label of shape node i"""
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))       # so the edges below always form a tree
    lab = list(range(1, n + 1))
    shuffle(lab)
    if root_first:
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
    rnd = random.random
    edges = [(lab[i - 1], lab[par[i] - 1]) if rnd() < 0.5 else (lab[par[i] - 1], lab[i - 1]) for i in range(2, n + 1)]
    shuffle(edges)
    return edges, lab


def random_ancestors(par, stay):
    """for every shape node i a random proper ancestor (i itself for the root): with probability stay the
    choice of the parent is inherited, so the jump is about 1 / (1 - stay) levels on average (O(n) total)"""
    n = len(par) - 1
    far = list(range(n + 1))
    rnd = random.random
    for i in range(2, n + 1):
        far[i] = far[par[i]] if par[i] != 1 and rnd() < stay else par[i]
    return far


def check_tree(n, edges):
    """the N - 1 edges connect all N nodes (union-find)"""
    assert len(edges) == n - 1
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for e in edges:
        u, v = e[0], e[1]
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b
        root[a] = b


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(230112)
MAXN, MAXQ, MAXC = 100_000, 50_000, 10**6


def add(c, edges, qs, tree_ok=False):
    n = len(c)
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(1 <= x <= MAXC for x in c)
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= x <= MAXC for u, v, x in qs)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, c)) + "\n" + "".join(f"{a} {b}\n" for a, b in edges)
                 + "".join(f"{u} {v} {x}\n" for u, v, x in qs))


def make(n, kind, q, cheap=0.001, far=False, xmode="rare", root_first=False):
    """prices: a fraction `cheap` of the towns cost 1..1000, the others 1001..10^6;
    xmode rare: x below 1001 (only cheap towns count, long scans), any: x anything, none: x below every price"""
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    rnd = random.random
    c = [1 + int(rnd() * 1000) if rnd() < cheap else 1001 + int(rnd() * (MAXC - 1000)) for _ in range(n)]
    if xmode == "none":
        for i in range(n):
            c[i] = max(c[i], 2)
    m = min(n, 100)
    qs = []
    for _ in range(q):
        if far:
            u = lab[int(rnd() * m)] if rnd() < 0.3 else lab[n - 1 - int(rnd() * m)]
            v = lab[n - 1 - int(rnd() * 2 * m) % n] if rnd() < 0.5 else lab[n // 2 + int(rnd() * m) - m // 2]
        else:
            u, v = 1 + int(rnd() * n), 1 + int(rnd() * n)
        if xmode == "rare":
            x = 1 + int(rnd() * 1000)
        elif xmode == "none":
            x = 1
        else:
            x = 1 + int(rnd() * MAXC)
        qs.append((u, v, x) if rnd() < 0.5 else (v, u, x))
    add(c, edges, qs, True)


# samples
add([30, 50, 20, 40, 10, 25, 15], [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
    [(4, 6, 30), (4, 7, 20), (6, 5, 12), (7, 7, 10)])
add([5, 1, 5, 1, 5], [(1, 2), (2, 3), (3, 4), (4, 5)], [(1, 5, 1), (5, 1, 1), (3, 3, 4)])
add([7], [], [(1, 1, 7)])
add([9, 3, 8, 2], [(3, 1), (1, 2), (2, 4)], [(3, 4, 3), (4, 3, 8), (1, 1, 1)])
add([12, 7, 9, 15, 3], [(2, 1), (1, 3), (3, 4), (4, 5)], [(5, 2, 8), (2, 5, 8), (4, 1, 2)])
# hidden: small and medium
make(10, "random", 60, 0.3, xmode="any")
make(30, "binary", 100, 0.1)
make(60, "caterpillar", 200, 0.05)
make(100, "deep", 300, 0.03, True)
make(3000, "path", 3000, 0.002, True)
make(4000, "twopaths", 3000, 0.001, True)
make(5000, "random", 5000, 0.01)
make(5000, "chains", 5000, 0.001)
make(5000, "star", 5000, 0.01)
# hidden: maximum size
make(MAXN, "path", MAXQ, 0.0001, True, root_first=True)
make(MAXN, "path", MAXQ, 0.0, True, "none", True)
make(MAXN, "twopaths", MAXQ, 0.0002, True)
make(MAXN, "deep", MAXQ, 0.0002, True)
make(MAXN, "caterpillar", MAXQ, 0.0005, True)
make(MAXN, "broom", MAXQ, 0.0002, True)
make(MAXN, "twopaths", MAXQ, 0.01, True, "any")
make(MAXN, "longrandom", MAXQ, 0.001, True, root_first=True)
make(MAXN, "path", MAXQ, 0.00003, True, "any", True)
make(MAXN, "longstar", MAXQ, 0.001, True, root_first=True)

write_all()

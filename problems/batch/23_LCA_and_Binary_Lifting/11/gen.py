import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    h = max(1, 3 * n // 5)
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
        elif kind == "longrandom":                  # a chain of 3n / 5 nodes, the rest hung at random
            p = i - 1 if i <= h else ri(1, i - 1)
        elif kind == "longbinary":                  # a chain of 3n / 5 nodes ending in a binary tree
            p = i - 1 if i <= h else h - 1 + (i - h + 1) // 2
        elif kind == "longstar":                    # a chain of 3n / 5 nodes plus a star around node 1
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

random.seed(230110)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10**6


def add(n, wedges, qs, tree_ok=False):
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(wedges) == n - 1
    else:
        check_tree(n, wedges)
    assert all(1 <= w <= MAXW for u, v, w in wedges)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges)
                 + "".join(f"{a} {b}\n" for a, b in qs))


def make(n, kind, q, lo=1, hi=MAXW, far=False, root_first=False, scale=1):
    """weights scale * (lo..hi): a big scale keeps the ties of small weights with long distances"""
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    rnd = random.random
    span = hi - lo + 1
    wedges = [(u, v, scale * (lo + int(rnd() * span))) for u, v in edges]
    near = random_ancestors(par, 0.9)
    m = min(n, 100)
    qs = []
    for _ in range(q):
        r = rnd()
        if far:
            a = lab[int(rnd() * m)] if rnd() < 0.5 else lab[n // 2 - int(rnd() * m)]
            b = lab[n - 1 - int(rnd() * m)]
        elif r < 0.3:                        # one shop above the other
            x = 1 + int(rnd() * n)
            a, b = lab[x - 1], lab[near[x] - 1]
        else:
            a, b = 1 + int(rnd() * n), 1 + int(rnd() * n)
        if rnd() < 0.02:
            b = a
        qs.append((a, b) if rnd() < 0.5 else (b, a))
    add(n, wedges, qs, True)


# samples
add(7, [(1, 2, 2), (1, 3, 4), (2, 4, 3), (2, 5, 1), (3, 6, 2), (3, 7, 5)], [(4, 6), (5, 1), (7, 7)])
add(5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1)], [(1, 5), (4, 1), (2, 2)])
add(1, [], [(1, 1)])
add(6, [(3, 1, 4), (1, 5, 4), (5, 2, 1), (5, 6, 3), (3, 4, 2)], [(4, 2), (6, 3), (3, 5), (2, 6)])
add(8, [(1, 2, 2), (2, 3, 2), (3, 4, 2), (2, 5, 1), (5, 6, 1), (3, 7, 3), (7, 8, 3)], [(1, 3), (6, 8), (5, 7), (8, 1)])
# hidden: small and medium
add(2, [(1, 2, 7)], [(1, 2), (2, 1), (1, 1)])
make(10, "random", 60, 1, 3)
make(30, "binary", 100, 1, 2)
make(60, "caterpillar", 200, 1, 10)
make(100, "deep", 300, 1, 1000)
make(3000, "path", 3000, 1, 2, far=True)
make(4000, "chains", 4000, 1, 5)
make(5000, "random", 5000, 1, 2)
make(5000, "star", 5000, 1, 3)
# hidden: maximum size
make(MAXN, "path", MAXQ, 1, 2, far=True, scale=500_000)
make(MAXN, "path", MAXQ, MAXW, MAXW, far=True, root_first=True)
make(MAXN, "twopaths", MAXQ, 1, 3, far=True, root_first=True, scale=333_333)
make(MAXN, "deep", MAXQ, 1, 2, far=True, scale=500_000)
make(MAXN, "caterpillar", MAXQ, 1, 4, far=True)
make(MAXN, "broom", MAXQ, 1, MAXW, far=True)
make(MAXN, "longrandom", MAXQ, 1, 2, scale=500_000)
make(MAXN, "twopaths", MAXQ, 1, 10, scale=100_000)
make(MAXN, "longbinary", MAXQ, 1, MAXW, far=True)
make(MAXN, "longstar", MAXQ, 1, 3, far=True)

write_all()

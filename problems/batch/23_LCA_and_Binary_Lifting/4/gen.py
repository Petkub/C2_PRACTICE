import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
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

random.seed(230104)
MAXN, MAXQ = 100_000, 100_000


def add(n, edges, qs, tree_ok=False):
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
                 + "".join(f"{u} {v}\n" for u, v in qs))


def make(n, kind, q, far=False):
    par = shape(n, kind)
    edges, lab = relabel(par)
    rnd = random.random
    m = min(n, 100)
    qs = []
    for _ in range(q):
        if far:
            u = lab[int(rnd() * m)] if rnd() < 0.5 else lab[n // 2 - int(rnd() * m)]
            v = lab[n - 1 - int(rnd() * m)]
        else:
            u, v = 1 + int(rnd() * n), 1 + int(rnd() * n)
            if rnd() < 0.05:
                v = u
        qs.append((u, v) if rnd() < 0.5 else (v, u))
    add(n, edges, qs, True)


def spiky(n, q):
    """a spine of about n / 3 houses, every spine house with two leaves: long paths with many neighbours"""
    s = n // 3
    par = [0, 0] + [i - 1 for i in range(2, s + 1)] + [1 + (i - s - 1) % s for i in range(s + 1, n + 1)]
    edges, lab = relabel(par)
    rnd = random.random
    qs = [(lab[int(rnd() * 50)], lab[s - 1 - int(rnd() * 50)]) for _ in range(q)]
    add(n, edges, qs, True)


# samples
add(8, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7), (6, 8)], [(4, 6), (7, 7), (8, 3), (5, 4)])
add(6, [(1, 2), (3, 1), (1, 4), (5, 1), (1, 6)], [(2, 3), (4, 4)])
add(1, [], [(1, 1)])
add(6, [(5, 2), (2, 6), (6, 1), (1, 4), (4, 3)], [(5, 3), (2, 4), (3, 3), (1, 6)])
add(9, [(3, 9), (9, 1), (9, 4), (4, 7), (4, 2), (2, 5), (1, 8), (8, 6)], [(5, 6), (7, 3), (9, 9), (2, 4), (6, 8)])
# hidden: small and medium
add(2, [(1, 2)], [(1, 2), (2, 2), (1, 1)])
make(10, "random", 50)
make(40, "binary", 100)
make(60, "caterpillar", 200)
spiky(300, 300)
make(3000, "path", 3000, far=True)
make(4000, "chains", 4000)
# hidden: maximum size
make(MAXN, "path", MAXQ, far=True)
make(MAXN, "caterpillar", MAXQ, far=True)
spiky(MAXN, MAXQ)
make(MAXN, "deep", MAXQ, far=True)
make(MAXN, "twopaths", MAXQ, far=True)
make(MAXN, "broom", MAXQ, far=True)
make(MAXN, "random", MAXQ)
make(MAXN, "star", MAXQ)
make(MAXN, "chains", MAXQ)

write_all()

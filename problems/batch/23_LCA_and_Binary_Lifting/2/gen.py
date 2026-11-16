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

random.seed(230102)
MAXN, MAXK, MAXQ, MAXW = 100_000, 50_000, 50_000, 1000


def add(n, wedges, s, eds, tree_ok=False):
    k, q = len(s), len(eds)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK and 1 <= q <= MAXQ
    if tree_ok:
        assert len(wedges) == n - 1
    else:
        check_tree(n, wedges)
    assert all(1 <= w <= MAXW for u, v, w in wedges)
    assert all(1 <= x <= n for x in s)
    assert all(1 <= i <= k and 1 <= x <= n for i, x in eds)
    tests.append(f"{n} {k} {q}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges)
                 + " ".join(map(str, s)) + "\n" + "".join(f"{i} {x}\n" for i, x in eds))


def make(n, kind, k, q, lo=1, hi=MAXW, ends=False, root_first=False):
    """ends: stops and edits at the two ends of the shape (long legs); edits often hit i = 1 and i = K"""
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    rnd = random.random
    span = hi - lo + 1
    wedges = [(u, v, lo + int(rnd() * span)) for u, v in edges]
    m = min(n, 50)

    def pick(j):
        if ends:
            return lab[int(rnd() * m)] if j % 2 == 0 else lab[n - 1 - int(rnd() * m)]
        return 1 + int(rnd() * n)
    s = [pick(j) for j in range(k)]
    eds = []
    for _ in range(q):
        r = rnd()
        i = 1 if r < 0.05 else k if r < 0.1 else 1 + int(rnd() * k)
        x = s[i - 2] if rnd() < 0.05 and i > 1 else pick(i - 1 + (rnd() < 0.2))
        eds.append((i, x))
    add(n, wedges, s, eds, True)


# samples
add(6, [(1, 2, 3), (1, 3, 5), (2, 4, 2), (2, 5, 4), (3, 6, 1)], [4, 5, 6, 1], [(2, 2), (4, 6), (1, 3)])
add(4, [(1, 2, 1000), (2, 3, 1000), (3, 4, 1000)], [1, 4, 1], [(2, 1), (3, 4), (1, 4)])
add(1, [], [1, 1, 1], [(2, 1)])
add(4, [(2, 4, 7), (4, 1, 2), (3, 4, 9)], [2, 3], [(1, 3), (2, 1)])
add(5, [(1, 5, 10), (5, 2, 6), (5, 3, 1), (1, 4, 3)], [4, 2, 3, 4], [(3, 1), (1, 3), (4, 2)])
# hidden: small and medium
add(2, [(2, 1, 1000)], [2], [(1, 1), (1, 2)])
make(10, "random", 8, 30, 1, 20)
make(30, "deep", 1, 20)
make(50, "caterpillar", 40, 100)
make(80, "binary", 60, 200, 1000, 1000)
make(3000, "path", 3000, 3000, ends=True)
make(4000, "chains", 2000, 4000)
# hidden: maximum size
make(MAXN, "path", MAXK, MAXQ, MAXW, MAXW, ends=True)
make(MAXN, "path", MAXK, MAXQ, ends=True, root_first=True)
make(MAXN, "twopaths", MAXK, MAXQ, ends=True, root_first=True)
make(MAXN, "deep", MAXK, MAXQ, ends=True)
make(MAXN, "caterpillar", MAXK, MAXQ)
make(MAXN, "broom", MAXK, MAXQ, ends=True)
make(MAXN, "random", MAXK, MAXQ)
make(MAXN, "chains", MAXK, MAXQ, 1, 10)
make(MAXN, "star", MAXK, MAXQ)

write_all()

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

random.seed(230108)
MAXN, MAXM = 100_000, 100_000


def add(n, edges, extra, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(extra) <= MAXM
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(1 <= c <= n and 1 <= d <= n and c != d for c, d in extra)
    tests.append(f"{n} {len(extra)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
                 + "".join(f"{c} {d}\n" for c, d in extra))


def make(n, kind, m, mode="rand"):
    """mode rand: random extra roads; far: between the two end regions of the shape (long covers); mix: 30% far,
    the rest local;
    local: next to a shape node (short covers, many uncovered roads); same: all on one main road"""
    par = shape(n, kind)
    edges, lab = relabel(par)
    rnd = random.random
    near = random_ancestors(par, 0.7)
    extra = []
    for _ in range(m):
        if mode == "rand":
            c, d = 1 + int(rnd() * n), 1 + int(rnd() * n)
            if c == d:
                d = c % n + 1
            extra.append((c, d))
            continue
        if mode == "far" or (mode == "mix" and rnd() < 0.3):
            x = 1 + int(rnd() * min(n, 30))
            y = n - int(rnd() * min(n, 30)) if mode == "far" else n // 2 + int(rnd() * (n - n // 2))
        elif mode in ("local", "mix"):
            y = 2 + int(rnd() * (n - 1))
            x = near[y]
        else:
            y = 2
            x = par[2]
        if x == y:
            y = x % n + 1
        extra.append((lab[x - 1], lab[y - 1]) if rnd() < 0.5 else (lab[y - 1], lab[x - 1]))
    add(n, edges, extra, True)


# samples
add(6, [(1, 2), (2, 3), (2, 4), (1, 5), (5, 6)], [(3, 4), (6, 3)])
add(4, [(1, 2), (2, 3), (3, 4)], [(1, 3)])
add(2, [(1, 2)], [(1, 2), (2, 1)])
add(5, [(4, 2), (2, 5), (5, 1), (1, 3)], [(4, 5), (3, 2), (1, 3)])
add(7, [(1, 2), (1, 3), (3, 4), (3, 5), (5, 6), (6, 7)], [(2, 4), (7, 4), (6, 5), (2, 3)])
# hidden: small and medium
make(3, "path", 1, "far")
make(8, "random", 4)
make(12, "binary", 6, "local")
make(20, "caterpillar", 10, "far")
make(60, "random", 30, "local")
make(3000, "path", 3000, "far")
make(4000, "chains", 2000, "local")
# hidden: maximum size
make(MAXN, "path", MAXM, "far")
make(MAXN, "path", MAXM, "mix")
make(MAXN, "path", MAXM, "same")
make(MAXN, "twopaths", MAXM, "far")
make(MAXN, "deep", MAXM, "far")
make(MAXN, "caterpillar", MAXM, "mix")
make(MAXN, "broom", MAXM, "far")
make(MAXN, "random", MAXM)
make(MAXN, "deep", MAXM, "mix")
make(MAXN, "star", MAXM, "local")
make(MAXN, "deep", 1, "far")

write_all()

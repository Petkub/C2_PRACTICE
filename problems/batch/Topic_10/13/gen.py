# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100113)
MAXN, MAXK, MAXW = 50_000, 500, 1000
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


def relabel(par, root_first=False):
    """random labels (node 1 of the shape keeps label 1 if root_first), shuffled edges and ends"""
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))       # so the edges below always form a tree
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    if root_first:
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
    rnd = random.random
    edges = [(lab[i - 1], lab[par[i] - 1]) if rnd() < 0.5 else (lab[par[i] - 1], lab[i - 1]) for i in range(2, n + 1)]
    random.shuffle(edges)
    return edges, lab


def check_tree(n, edges):
    """the N - 1 edges connect all N nodes (union-find)"""
    assert len(edges) == n - 1
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b
        root[a] = b


def weigh(edges, lo=1, hi=MAXW):
    rnd, k = random.random, hi - lo + 1
    return [(u, v, lo + int(rnd() * k)) for u, v in edges]


def add(n, k, wedges, from_shape=False):
    """from_shape: the edges come from relabel(), which already guarantees a tree"""
    assert 1 <= n <= MAXN and 1 <= k <= MAXK and len(wedges) == n - 1
    if not from_shape:
        check_tree(n, [(u, v) for u, v, w in wedges])
    assert all(1 <= w <= MAXW for u, v, w in wedges)
    tests.append(f"{n} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges))


def make(n, kind, k, lo=1, hi=MAXW, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, k, weigh(edges, lo, hi), True)


def two_level(a, b):
    """a root with a children, each with b leaves"""
    par = [0, 0] + [1] * a
    for i in range(a):
        par += [2 + i] * b
    return par


# samples
add(5, 3, [(1, 2, 1), (1, 3, 2), (3, 4, 1), (3, 5, 3)])
add(4, 5, [(1, 2, 5), (2, 3, 2), (3, 4, 3)])
add(1, 1, [])
add(6, 2, [(2, 1, 1), (3, 2, 1), (2, 4, 1), (5, 2, 1), (2, 6, 1)])
add(8, 4, [(1, 2, 1), (2, 3, 2), (2, 4, 3), (4, 5, 1), (1, 6, 2), (6, 7, 2), (6, 8, 1)])
# hidden: small and medium
add(2, 7, [(1, 2, 7)])
add(2, 3, [(2, 1, 4)])
make(10, "random", 3, 1, 3)
make(30, "deep", 6, 1, 2)
make(50, "star", 2, 1, 1)
make(200, "random", 10, 1, 5)
make(2000, "chains", 50, 1, 3)
make(5000, "caterpillar", 100, 1, 4)
make(10_000, "random", 15, 1, 2)
# hidden: maximum size
N = MAXN
make(N, "random", 10, 1, 1)
make(N, "random", 25, 1, 3)
make(N, "chains", 300, 1, 2)
make(N, "chains", MAXK, 1, 5)
make(N, "caterpillar", MAXK, 1, 1)
make(N, "path", MAXK, 1, 1, True)
make(N, "star", 2, 1, 1)                                        # about 1.25 * 10^9 pairs
make(N, "deep", MAXK, 1, 1)
make(N, "binary", 40, 1, 3, True)
make(N, "broom", MAXK, 1, MAXW)
make(N, "random", MAXK, 1, MAXW)
edges, lab = relabel(two_level(220, 220))
add(len(lab), 4, [(u, v, 1) for u, v in edges], True)
edges, lab = relabel(two_level(100, 498))
add(len(lab), 2, [(u, v, 1) for u, v in edges], True)
make(N, "chains", 200, 1, 1)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

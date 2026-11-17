# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
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
        elif kind == "spider":                      # about sqrt(n) legs of equal length from node 1
            p = 1 if i <= b + 1 else i - b
        elif kind == "bushy":                       # star of stars: about sqrt(n) hubs, each with many leaves
            p = 1 if i <= b + 1 else ri(2, b + 1)
        elif kind == "longspider":                  # 2000 legs of length about n / 2000 from node 1
            p = 1 if i <= 2001 else i - 2000
        elif kind == "fatcaterpillar":              # a spine of 100 nodes, every other node a leg of the spine
            p = i - 1 if i <= 100 else ri(1, 100)
        elif kind == "hubpath":                     # a path of 40 hubs, each with about n / 40 leaves
            p = i - 1 if i <= 40 else ri(1, 40)
        elif kind == "hubrand":                     # random tree in which node 1 gets about half of the nodes
            p = 1 if random.random() < 0.5 else ri(1, i - 1)
        elif kind == "doublestar":                  # nodes 1 and 2 joined, each with half of the leaves
            p = 1 if i == 2 or i % 2 else 2
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    """Fisher-Yates driven by random.random() only (fast, and the same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def relabel(par, root_first=False):
    """random labels (node 1 of the shape keeps label 1 if root_first), shuffled edges and ends"""
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


def write_tests():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(2109)
MAXN, MAXK = 100_000, 50


def add(n, k, edges, from_shape=False):
    assert 1 <= n <= MAXN and 0 <= k <= MAXK and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    tests.append(f"{n} {k}\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, k, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, k, edges, True)


# samples
add(6, 2, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6)])
add(5, 1, [(1, 2), (2, 3), (3, 4), (4, 5)])
add(1, 5, [])
add(3, 0, [(1, 2), (1, 3)])
add(7, 50, [(1, 2), (1, 3), (3, 4), (4, 5), (4, 6), (6, 7)])
# hidden: small and medium (thin trees, where every ball is small, stay below the maximum size)
add(2, 1, [(1, 2)])
make(10, "random", 2)
make(30, "deep", 7)
make(60, "star", 1)
make(300, "caterpillar", 3)
make(1000, "bushy", 2)
make(3000, "path", 50, True)
make(8000, "chains", 10)
make(60000, "deep", MAXK)
# hidden: maximum size (bushy shapes: the balls hold a large part of the tree)
N = MAXN
make(N, "random", MAXK)
make(N, "bushy", 4)              # every ball holds the whole tree (leaf, hub, centre, hub, leaf)
make(N, "broom", 30)
make(N, "fatcaterpillar", MAXK)
make(N, "random", 20)
make(N, "longspider", MAXK, True)
make(N, "doublestar", 3)
make(N, "binary", 30, True)
make(N, "hubpath", MAXK)
make(N, "bushy", MAXK)
make(N, "hubrand", 5)
make(N, "star", 2)
write_tests()

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

random.seed(2104)
MAXN, MAXC = 100_000, 10**9


def add(n, roads, from_shape=False):
    """roads: (u, v, c) = a one-way road u -> v, turning it around costs c"""
    assert 1 <= n <= MAXN and len(roads) == n - 1
    if not from_shape:
        check_tree(n, roads)
    assert all(1 <= c <= MAXC for u, v, c in roads)
    tests.append(f"{n}\n" + "".join(f"{u} {v} {c}\n" for u, v, c in roads))


def make(n, kind, lo=1, hi=MAXC, mode="random", root_first=False):
    """mode: random directions; "out" = all roads point away from the shape's node 1 (one cheap capital);
    "in" = all roads point towards node 1; "alt" = directions alternate with the depth (many ties with equal costs)"""
    par = shape(n, kind)
    lab = list(range(1, n + 1))
    shuffle(lab)
    if root_first:
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
    depth = [0] * (n + 1)
    roads = []
    span = hi - lo + 1
    for i in range(2, n + 1):
        depth[i] = depth[par[i]] + 1
        a, b = lab[par[i] - 1], lab[i - 1]      # a is the shape parent of b
        if mode == "random":
            down = random.random() < 0.5
        elif mode == "out":
            down = random.random() < 0.97
        elif mode == "in":
            down = random.random() < 0.03
        else:
            down = depth[i] % 2 == 0
        roads.append((a, b, lo + int(random.random() * span)) if down else (b, a, lo + int(random.random() * span)))
    shuffle(roads)
    add(n, roads, True)


# samples
add(4, [(2, 1, 5), (2, 3, 2), (4, 3, 1)])
add(3, [(1, 2, 4), (3, 2, 4)])
add(1, [])
add(6, [(1, 2, 3), (3, 1, 2), (1, 4, 6), (4, 5, 1), (6, 4, 1)])
add(7, [(2, 1, 1), (3, 1, 1), (1, 4, 1), (5, 4, 1), (4, 6, 1), (7, 6, 1)])
# hidden: small and medium
add(2, [(1, 2, MAXC)])
make(10, "random", 1, 3)
make(30, "path", 1, 1, "alt")
make(60, "star", 1, 2)
make(300, "caterpillar", 1, 5)
make(2000, "binary", 1, 1, "alt", True)
make(5000, "chains", 1, 10**9, "in")
make(8000, "spider", 1, 1, "alt")
# hidden: maximum size
N = MAXN
make(N, "path", MAXC, MAXC, "in", True)          # the largest costs
make(N, "path", 1, 1, "alt")                     # about half of the cities are the best
make(N, "deep", 1, 3)
make(N, "caterpillar", 1, 2, "alt")
make(N, "broom", mode="out")
make(N, "twopaths", 1, 1, "alt", True)
make(N, "chains")
make(N, "random", 1, 10)
make(N, "binary", 1, 1, "alt", True)
make(N, "star", 1, 1)
make(N, "spider", 1, 1, "alt")
make(N, "bushy", mode="in")
write_tests()

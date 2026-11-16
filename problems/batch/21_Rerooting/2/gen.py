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

random.seed(2102)
MAXN, MAXW = 100_000, 10**9


def add(n, cust, roads, from_shape=False):
    """cust: string of 0/1 (1 = a customer lives there), roads: (u, v, w)"""
    assert 1 <= n <= MAXN and len(roads) == n - 1
    assert len(cust) == n and set(cust) <= {"0", "1"} and "1" in cust
    if not from_shape:
        check_tree(n, roads)
    assert all(1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n}\n{cust}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def marks(n, k, where=None):
    """k customers; where = list of candidate nodes (default all)"""
    pool = list(where) if where else list(range(1, n + 1))
    chosen = set(random.sample(pool, min(k, len(pool))))
    return "".join("1" if i in chosen else "0" for i in range(1, n + 1))


def make(n, kind, k, lo=1, hi=MAXW, where=None, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    rnd, span = random.random, hi - lo + 1
    roads = [(u, v, lo + int(rnd() * span)) for u, v in edges]
    pool = None
    if where == "near":                     # customers only among the first nodes of the shape (one region)
        pool = lab[: max(1, n // 50)]
    add(n, marks(n, k, pool), roads, True)


# samples
add(5, "01001", [(1, 2, 4), (1, 3, 2), (3, 4, 6), (3, 5, 1)])
add(4, "0010", [(1, 2, 3), (2, 3, 5), (3, 4, 2)])
add(1, "1", [])
add(6, "111111", [(1, 2, 2), (2, 3, 2), (2, 4, 7), (1, 5, 1), (5, 6, 3)])
add(7, "1000010", [(4, 1, 5), (1, 7, 2), (7, 2, 8), (2, 3, 1), (6, 2, 4), (5, 4, 3)])
# hidden: small and medium
add(2, "01", [(1, 2, MAXW)])
make(10, "random", 3, 1, 10)
make(30, "deep", 1, 1, 5)
make(50, "star", 2, 1, 100)
make(300, "caterpillar", 5)
make(2000, "path", 1, 1, 10**9, root_first=True)
make(4000, "chains", 2000, 1, 100)
make(6000, "spider", 10, 1, 20)
make(8000, "random", 30, 1, 1000, where="near")
# hidden: maximum size
N = MAXN
make(N, "path", 1, MAXW, MAXW)                       # one customer, the largest distances
make(N, "path", 2)
make(N, "deep", N // 2)                              # many customers: BFS from each customer is too slow
make(N, "caterpillar", 3, where="near")
make(N, "broom", 500)
make(N, "twopaths", 1, root_first=True)
make(N, "chains", N)                                 # everyone is a customer
make(N, "random", 1000, where="near")
make(N, "binary", 7, 1, 10, root_first=True)
make(N, "star", N // 3)
make(N, "spider", 5, 1, 1000)
make(N, "bushy", 1500, where="near")
write_tests()

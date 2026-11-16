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

random.seed(2101)
MAXN, MAXT = 100_000, 10**6


def add(n, roads, from_shape=False):
    """roads: (u, v, a, b) = a minutes from u to v, b minutes from v to u"""
    assert 1 <= n <= MAXN and len(roads) == n - 1
    if not from_shape:
        check_tree(n, roads)
    assert all(1 <= a <= MAXT and 1 <= b <= MAXT for u, v, a, b in roads)
    tests.append(f"{n}\n" + "".join(f"{u} {v} {a} {b}\n" for u, v, a, b in roads))


def make(n, kind, lo=1, hi=MAXT, mode="random", root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    k = hi - lo + 1
    rnd = random.random
    roads = []
    for u, v in edges:
        a, b = lo + int(rnd() * k), lo + int(rnd() * k)
        if mode == "steep":                    # one direction cheap, the other expensive
            a, b = (lo, hi) if rnd() < 0.5 else (hi, lo)
        elif mode == "max":
            a = b = hi
        roads.append((u, v, a, b))
    add(n, roads, True)


# samples
add(4, [(1, 2, 3, 5), (2, 3, 1, 2), (2, 4, 4, 1)])
add(3, [(1, 2, 1, 10), (3, 2, 2, 2)])
add(1, [])
add(5, [(2, 1, 7, 7), (3, 2, 1, 9), (4, 3, 5, 2), (5, 4, 3, 3)])
add(6, [(1, 2, 2, 6), (1, 3, 4, 1), (4, 1, 3, 3), (5, 2, 8, 1), (2, 6, 1, 5)])
# hidden: small and medium
add(2, [(2, 1, MAXT, 1)])
make(10, "random", 1, 10)
make(40, "star", 1, 5, "steep")
make(200, "caterpillar")
make(1000, "binary", 1, 100)
make(3000, "path", 1, 10**6, "steep", True)
make(5000, "chains")
make(8000, "spider", 1, 20)
# hidden: maximum size
N = MAXN
make(N, "path", mode="max", root_first=True)            # the largest totals
make(N, "path", mode="steep")
make(N, "deep")
make(N, "caterpillar")
make(N, "broom", mode="steep")
make(N, "twopaths", root_first=True)
make(N, "chains")
make(N, "random")
make(N, "binary", 1, 10, root_first=True)
make(N, "star", mode="steep")
make(N, "spider")
make(N, "bushy")
write_tests()

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100109)
MAXN, MAXW = 100_000, 10**6
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


def add(n, wedges, from_shape=False):
    """from_shape: the edges come from relabel(), which already guarantees a tree"""
    assert 1 <= n <= MAXN and len(wedges) == n - 1
    if not from_shape:
        check_tree(n, [(u, v) for u, v, w in wedges])
    assert all(1 <= w <= MAXW for u, v, w in wedges)
    tests.append(f"{n}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges))


def make(n, kind, root_first=False, lo=1, hi=MAXW):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, weigh(edges, lo, hi), True)


# samples
add(5, [(1, 2, 3), (1, 3, 5), (3, 4, 2), (3, 5, 7)])
add(4, [(4, 3, 2), (3, 1, 9), (1, 2, 4)])
add(1, [])
add(5, [(2, 1, 4), (2, 3, 1), (4, 2, 6), (2, 5, 6)])
add(7, [(5, 7, 8), (1, 5, 3), (2, 7, 4), (6, 1, 1), (3, 2, 2), (4, 6, 5)])
# hidden: small and medium
add(2, [(2, 1, MAXW)])
add(3, [(1, 2, 5), (3, 1, 5)])
make(10, "random", lo=1, hi=10)
make(30, "deep", lo=1, hi=5)
make(40, "star", lo=1, hi=3)
make(200, "caterpillar")
make(3000, "path", True)
make(5000, "chains", lo=1, hi=100)
e, lab = relabel(shape(4000, "random"))
add(4000, [(u, v, 1) for u, v in e])                          # all lengths equal
e, lab = relabel(shape(6000, "broom"))
add(6000, [(u, v, MAXW if random.random() < 0.01 else 1) for u, v in e])   # a few very long roads
# hidden: maximum size
N = MAXN
make(N, "path", True)
make(N, "path", False, MAXW, MAXW)                              # the largest distances
make(N, "deep")
make(N, "caterpillar")
make(N, "broom")
make(N, "twopaths", True)
make(N, "chains")
make(N, "random")
make(N, "binary", True, 1, 10)
make(N, "star")
e, lab = relabel(shape(N, "caterpillar"))
add(N, [(u, v, MAXW if random.random() < 0.001 else ri(1, 3)) for u, v in e], True)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

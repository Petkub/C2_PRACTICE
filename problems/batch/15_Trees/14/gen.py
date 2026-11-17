# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(100110)
MAXN = 100_000
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


def add(n, edges, from_shape=False):
    """from_shape: the edges come from relabel(), which already guarantees a tree"""
    assert 1 <= n <= MAXN and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, edges, True)


# samples
add(5, [(1, 2), (1, 3), (3, 4), (3, 5)])
add(2, [(2, 1)])
add(1, [])
add(6, [(3, 5), (1, 6), (5, 2), (4, 1), (2, 4)])
add(6, [(2, 1), (3, 2), (2, 4), (5, 2), (2, 6)])
add(8, [(1, 2), (2, 3), (2, 4), (4, 5), (1, 6), (6, 7), (6, 8)])
# hidden: small (every set is tried) and medium
make(10, "random")
make(18, "caterpillar")
make(20, "random")
make(20, "path")
make(15, "star")
make(2000, "random")
make(10_000, "path")
make(20_000, "caterpillar")
# hidden: maximum size
N = MAXN
make(N, "path", True)
make(N, "star")
make(N, "random")
make(N, "deep")
make(N, "caterpillar")
make(N, "broom")
make(N, "binary", True)
make(N, "chains")
make(N, "path")
make(N, "twopaths", True)
half = N // 2
par = [0, 0] + [i - 1 for i in range(2, half + 1)] + [i - half for i in range(half + 1, N + 1)]
edges, lab = relabel(par)                                      # a comb: one leaf on every path node
add(N, edges, True)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

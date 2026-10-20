# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100114)
MAXN, MAXM = 100_000, 100_000
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


def add(n, edges, rs, from_shape=False):
    """from_shape: the edges come from relabel(), which already guarantees a tree"""
    assert 1 <= n <= MAXN and 1 <= len(rs) <= MAXM and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in rs)
    tests.append(f"{n} {len(rs)}\n" + "".join(f"{u} {v}\n" for u, v in edges)
                 + "".join(f"{a} {b}\n" for a, b in rs))


def rr(n, m):
    rnd = random.random
    return [(1 + int(rnd() * n), 1 + int(rnd() * n)) for _ in range(m)]


def far_r(lab, m, spread=100):
    """routes between the two far ends of the shape (long routes)"""
    n = len(lab)
    return [(lab[ri(0, spread - 1)], lab[n - 1 - ri(0, spread - 1)]) for _ in range(m)]


def big(kind, root_first=False, far=0):
    n, m = MAXN, MAXM
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, edges, far_r(lab, m, far) if far else rr(n, m), True)


# samples
add(5, [(1, 2), (1, 3), (3, 4), (3, 5)], [(2, 4), (5, 4)])
add(4, [(4, 3), (3, 1), (1, 2)], [(4, 2), (3, 3), (3, 1)])
add(1, [], [(1, 1), (1, 1)])
add(4, [(2, 1), (2, 3), (4, 2)], [(1, 3), (4, 1)])
add(5, [(5, 3), (1, 5), (2, 3), (4, 1)], [(4, 2)])
# hidden: small and medium
add(2, [(2, 1)], [(1, 2), (2, 2), (1, 1)])
for n, kind, m in ((10, "random", 5), (30, "deep", 20), (40, "star", 30), (60, "caterpillar", 60)):
    e, lab = relabel(shape(n, kind))
    add(n, e, rr(n, m))
e, lab = relabel(shape(3000, "path"), True)
add(3000, e, rr(3000, 3000))
e, lab = relabel(shape(5000, "chains"))
add(5000, e, rr(5000, 5000))
e, lab = relabel(shape(6000, "twopaths"), True)
add(6000, e, far_r(lab, 6000, 50))
e, lab = relabel(shape(8000, "path"))
add(8000, e, [(lab[0], lab[-1])] * 8000)                        # every route covers everything
# hidden: maximum size
big("path", True)
big("path", False, far=1000)
big("path", True, far=1)                                        # all junctions tie
big("deep")
big("caterpillar", True)
big("broom", True, far=100)
big("twopaths", True, far=3000)
big("chains")
big("random")
big("star")
big("deep", True, far=500)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

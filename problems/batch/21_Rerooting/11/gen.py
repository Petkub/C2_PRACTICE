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

random.seed(2111)
MAXN = 100_000


def add(n, edges, from_shape=False):
    assert 2 <= n <= MAXN and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, edges, True)


def make_par(par, root_first=False):
    edges, lab = relabel(par, root_first)
    add(len(par) - 1, edges, True)


def legs_par(n, legs):
    cuts = set(random.sample(range(3, n + 1), legs - 1))
    return [0, 0] + [1 if (i == 2 or i in cuts) else i - 1 for i in range(2, n + 1)]


def comb(n):
    """a spine whose nodes carry paths of decreasing length (many different diameters)"""
    par = [0, 0]
    spine = [1]
    i = 2
    while i <= n:
        par.append(spine[-1])
        spine.append(i)
        i += 1
        leg = int(max(0, n - i) ** 0.5)
        last = spine[-1]
        for _ in range(min(leg, n - i + 1)):
            par.append(last)
            last = i
            i += 1
    return par[: n + 1]


# samples
add(6, [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6)])
add(4, [(1, 2), (2, 3), (3, 4)])
add(2, [(2, 1)])
add(5, [(1, 2), (1, 3), (1, 4), (1, 5)])
add(9, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 7), (3, 8), (8, 9)])
# hidden: small and medium
make(10, "random")
make_par(legs_par(30, 4))
make(60, "star")
make(300, "caterpillar")
make_par(comb(1000))
make(3000, "path", True)
make_par(legs_par(5000, 3))
make(8000, "random")
# hidden: maximum size
N = MAXN
make(N, "path")
make(N, "deep")
make(N, "caterpillar")
make(N, "broom")
make(N, "twopaths", True)
make(N, "chains")
make(N, "random")
make(N, "binary", True)
make_par(comb(N))
make_par(legs_par(N, 3))
make(N, "spider")
make(N, "bushy")
# more small trees: the brute checks the best joining villages by BFS from every village (N <= 300)
make(100, "random")
make(200, "deep")
make(250, "chains")
make_par(legs_par(280, 5))
write_tests()

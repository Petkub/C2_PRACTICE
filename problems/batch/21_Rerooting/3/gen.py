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

random.seed(2103)
MAXN, MAXH = 100_000, 10**9


def add(n, h, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(h) == n and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, mode, lo=1, hi=MAXH, root_first=False):
    """heights per node of the shape (index i), then relabelled the same way as the edges"""
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    h = [0] * (n + 1)
    for i in range(1, n + 1):
        if mode == "random":
            x = ri(lo, hi)
        elif mode == "flat":                    # one big plateau
            x = hi
        elif mode == "few":                     # many equal heights
            x = ri(lo, lo + 2)
        elif mode == "mountain":                # the shape's node 1 is the top, never higher than the parent
            x = hi if i == 1 else max(lo, h[lab[par[i] - 1]] - ri(0, 1))
        elif mode == "valley":                  # node 1 is the bottom, never lower than the parent
            x = lo if i == 1 else min(hi, h[lab[par[i] - 1]] + ri(0, 2))
        elif mode == "hublow":                  # the hubs (nodes 1, 2 of the shape) lowest, the rest close above
            x = lo if i <= 2 else ri(lo, lo + 2)
        elif mode == "mostlylow":               # big plateaus at the lowest height
            x = lo if random.random() < 0.9 else lo + 1
        else:
            raise ValueError(mode)
        h[lab[i - 1]] = x
    add(n, h[1:], edges, True)


# samples
add(5, [5, 3, 3, 1, 4], [(1, 2), (2, 3), (3, 4), (1, 5)])
add(4, [2, 2, 1, 2], [(1, 2), (2, 3), (3, 4)])
add(1, [7], [])
add(6, [4, 4, 4, 4, 4, 4], [(1, 2), (1, 3), (3, 4), (3, 5), (5, 6)])
add(7, [6, 2, 6, 3, 8, 1, 6], [(1, 2), (1, 3), (3, 4), (5, 3), (4, 6), (7, 3)])
# hidden: small and medium
add(2, [MAXH, 1], [(2, 1)])
make(10, "random", "few", 1, 10)
make(30, "deep", "random", 1, 20)
make(60, "star", "few", 5, 10)
make(300, "caterpillar", "mountain", 1, 100)
make(2000, "twopaths", "few", root_first=True)
make(5000, "chains", "valley")
make(8000, "spider", "few", 1, 10**9)
# hidden: maximum size (every one has huge plateaus or a hub that most pours reach)
N = MAXN
make(N, "path", "flat")                          # one plateau: water reaches everything from everywhere
make(N, "path", "mountain", root_first=True)
make(N, "deep", "mountain")
make(N, "hubrand", "valley")                     # every pour runs down to the hub
make(N, "broom", "mountain")
make(N, "broom", "valley", root_first=True)
make(N, "hubrand", "mountain")
make(N, "random", "mostlylow")
make(N, "binary", "mostlylow", root_first=True)
make(N, "star", "hublow")
make(N, "bushy", "mostlylow")
make(N, "doublestar", "hublow")
write_tests()

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
MAXN, MAXA = 100_000, 10**9


def add(n, a, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(a) == n and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def values(n, mode):
    if mode == "big":                           # any profit or loss
        return [ri(-MAXA, MAXA) for _ in range(n)]
    if mode == "small":                         # many groups with total exactly 0
        return [ri(-3, 3) for _ in range(n)]
    if mode == "pos":                           # every group is profitable
        return [MAXA] * n
    if mode == "neg":                           # no group is profitable
        return [-MAXA] * n
    if mode == "mostpos":                       # big profits, a few huge losses
        return [ri(MAXA // 2, MAXA) if random.random() < 0.8 else -MAXA for _ in range(n)]
    if mode == "edge":                          # only +10^9 and -10^9
        return [MAXA if random.random() < 0.5 else -MAXA for _ in range(n)]
    if mode == "balanced":                      # big values whose total is exactly 0
        a = [ri(-MAXA, MAXA) for _ in range(n)]
        s = sum(a)
        i = 0
        while s != 0:                           # move the total to 0 one value at a time
            d = max(-MAXA - a[i], min(MAXA - a[i], -s))
            a[i] += d
            s += d
            i += 1
        return a
    raise ValueError(mode)


def make(n, kind, mode, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    v = values(n, mode)
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[lab[i - 1]] = v[i - 1]
    add(n, a[1:], edges, True)


# samples
add(5, [2, -4, 3, 1, -1], [(1, 2), (2, 3), (2, 4), (4, 5)])
add(3, [2, -2, 0], [(1, 2), (2, 3)])
add(1, [-7], [])
add(6, [-5, 2, 3, -1, 4, -2], [(1, 2), (1, 3), (4, 1), (1, 5), (6, 1)])
add(8, [-30, 25, -10, -40, 12, 50, -60, 8], [(1, 2), (1, 3), (2, 4), (5, 2), (3, 6), (6, 7), (8, 6)])
# hidden: small and medium
add(2, [5, -5], [(2, 1)])
make(10, "random", "small")
make(30, "deep", "small")
make(60, "star", "small")
make(300, "caterpillar", "big")
make(2000, "path", "small", root_first=True)
make(5000, "chains", "balanced")
make(8000, "spider", "edge")
# hidden: maximum size
N = MAXN
make(N, "path", "big", root_first=True)
make(N, "random", "big")
make(N, "star", "pos")
make(N, "binary", "neg", root_first=True)
make(N, "caterpillar", "small")
make(N, "broom", "balanced")
make(N, "deep", "big")
make(N, "twopaths", "small", root_first=True)
make(N, "chains", "mostpos")
make(N, "spider", "small")
make(N, "bushy", "edge")
make(N, "random", "balanced")
write_tests()

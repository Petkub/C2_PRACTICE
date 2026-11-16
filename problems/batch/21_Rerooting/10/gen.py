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

random.seed(2110)
MAXN, MAXA = 100_000, 10**8


def add(n, a, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(a) == n and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, mode="signed", lo=-MAXA, hi=MAXA, root_first=False):
    """"signed": random in [lo, hi]; "positive": 1..hi (a weighted centroid problem); "pairs": each surplus
    sits next to a matching demand (sums stay small, many near ties); "sided": one half of the shape
    supplies, the other half demands"""
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        if mode == "signed":
            x = ri(lo, hi)
        elif mode == "positive":
            x = ri(1, hi)
        elif mode == "pairs":
            x = ri(1, hi) if i % 2 else -ri(1, hi)
        elif mode == "sided":
            x = ri(0, hi) if i <= n // 2 else -ri(0, hi)
        else:
            raise ValueError(mode)
        a[lab[i - 1]] = x
    add(n, a[1:], edges, True)


def make_plant(n, kind, lim, tgt, pairs):
    """small values in [-lim, lim] with total tgt (or in [1, lim] if tgt is None), plus `pairs` roads p-c (c's side about a sixth to a
    third of the tree) with +B at c and -B at p: such a road decides M, every depot on c's side ties on
    M and S decides there, while the smallest S overall usually lies elsewhere (kills "minimise S only")"""
    par = shape(n, kind)
    sz = [1] * (n + 1)
    for i in range(n, 1, -1):
        sz[par[i]] += sz[i]
    a = [0] + [ri(1, lim) if tgt is None else ri(-lim, lim) for _ in range(n)]
    cand = [i for i in range(2, n + 1) if n // 6 <= sz[i] <= n // 3] or list(range(2, n + 1))
    B = MAXA - 3 * lim
    used = []
    for k in range(pairs):
        c = cand[ri(0, len(cand) - 1)]
        while c in used or par[c] in used:
            c = ri(2, n)
        used += [c, par[c]]
        a[c] += B >> k
        a[par[c]] -= B >> k
    need = 0 if tgt is None else tgt - sum(a)
    while need:
        j = ri(1, n)
        d = max(-lim, min(lim, need))
        if abs(a[j] + d) <= MAXA:
            a[j] += d
            need -= d
    edges, lab = relabel(par)
    b = [0] * (n + 1)
    for i in range(1, n + 1):
        b[lab[i - 1]] = a[i]
    assert tgt is None or sum(b) == tgt
    add(n, b[1:], edges, True)


# samples
add(6, [1, -1, -4, 3, -5, 1], [(1, 2), (2, 3), (3, 4), (3, 5), (1, 6)])
add(4, [5, -1, -1, -5], [(1, 2), (2, 3), (3, 4)])
add(1, [-7], [])
add(4, [3, -1, -1, 3], [(1, 2), (2, 3), (3, 4)])
add(7, [-2, 6, -3, 4, -6, 1, 2], [(1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (6, 7)])
# hidden: small and medium
add(2, [MAXA, -MAXA], [(1, 2)])
make(10, "random", "signed", -10, 10)
make(30, "deep", "pairs", hi=5)
make(60, "star", "signed", -100, 100)
make(300, "caterpillar", "sided")
make(2000, "path", "positive", root_first=True)
make_plant(5000, "chains", 3, 2, 1)
make(8000, "spider", "pairs")
# hidden: maximum size
N = MAXN
make(N, "path", "sided", hi=MAXA)                 # the largest loads
make(N, "path", "signed", -2, 2)
make(N, "deep", "signed")
make(N, "caterpillar", "pairs")
make(N, "broom", "positive")
make(N, "twopaths", "sided", root_first=True)
make(N, "chains", "signed", -1000, 1000)
make(N, "random", "signed")
make(N, "binary", "pairs", root_first=True)
make(N, "star", "signed")
make(N, "spider", "sided")
make(N, "bushy", "signed", -5, 5)
make_plant(N, "path", 1000, None, 1)
# hidden: one heavy road decides M, S decides among many depots (added in review)
make_plant(300, "caterpillar", 1000, None, 1)
make_plant(N, "caterpillar", 1000, None, 1)
make_plant(N, "chains", 1000, None, 1)
make_plant(N, "deep", 5, -1, 2)
write_tests()

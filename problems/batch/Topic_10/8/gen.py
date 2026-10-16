# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100108)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10**6
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


def add(n, wedges, qs, from_shape=False):
    """from_shape: the edges come from relabel(), which already guarantees a tree"""
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert len(wedges) == n - 1
    if not from_shape:
        check_tree(n, [(u, v) for u, v, w in wedges])
    assert all(1 <= w <= MAXW for u, v, w in wedges)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges)
                 + "".join(f"{a} {b}\n" for a, b in qs))


def weigh(edges, lo=1, hi=MAXW):
    rnd, k = random.random, hi - lo + 1
    return [(u, v, lo + int(rnd() * k)) for u, v in edges]


def rq(n, q):
    rnd = random.random
    return [(1 + int(rnd() * n), 1 + int(rnd() * n)) for _ in range(q)]


def big(kind, root_first=False, lo=1, hi=MAXW, far=False):
    n, q = MAXN, MAXQ
    edges, lab = relabel(shape(n, kind), root_first)
    if far:     # both ends near the two ends of the shape (long paths)
        qs = [(lab[ri(0, 99)], lab[n - 1 - ri(0, 99)]) for _ in range(q)]
    else:
        qs = rq(n, q)
    add(n, weigh(edges, lo, hi), qs, True)


# samples
add(5, [(1, 2, 3), (1, 3, 5), (3, 4, 2), (3, 5, 7)], [(2, 4), (4, 5), (1, 1), (5, 2)])
add(4, [(4, 3, 10**6), (3, 1, 10**6), (1, 2, 10**6)], [(4, 2), (2, 3), (3, 4)])
add(4, [(2, 1, 4), (2, 3, 1), (4, 2, 6)], [(1, 4), (3, 3)])
add(5, [(5, 3, 8), (1, 5, 3), (2, 3, 4), (4, 1, 1)], [(2, 4), (5, 2)])
add(1, [], [(1, 1)])
# hidden: small and medium
add(2, [(2, 1, 1)], [(1, 2), (2, 1), (2, 2)])
for n, kind in ((10, "random"), (30, "deep"), (40, "star"), (60, "caterpillar")):
    e, lab = relabel(shape(n, kind))
    add(n, weigh(e, 1, 20), rq(n, 50))
e, lab = relabel(shape(3000, "path"), True)
add(3000, weigh(e), rq(3000, 3000))
e, lab = relabel(shape(5000, "chains"))
add(5000, weigh(e), rq(5000, 5000))
e, lab = relabel(shape(6000, "twopaths"), True)
add(6000, weigh(e, MAXW, MAXW), [(lab[ri(0, 50)], lab[5999 - ri(0, 50)]) for _ in range(6000)])
# hidden: maximum size
big("path", True)
big("path", False, far=True)
big("path", True, MAXW, MAXW, far=True)            # the largest distances
big("deep")
big("caterpillar", True)
big("broom", True, far=True)
big("twopaths", True, far=True)
big("chains")
big("random")
big("star")
big("deep", True, 1, 10, far=True)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(150701)
MAXN = 200_000
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, edges, mix=False):
    """edges on towns 1..n; mix: random numbering, rotated list of roads, ends of some roads swapped"""
    assert 2 <= n <= MAXN and len(edges) == n - 1
    if n <= 1000:                               # DSU: n - 1 roads joining everything = a tree
        root = list(range(n + 1))

        def find(x):
            while root[x] != x:
                root[x] = root[root[x]]
                x = root[x]
            return x
        for u, v in edges:
            assert 1 <= u <= n and 1 <= v <= n and u != v
            ru, rv = find(u), find(v)
            assert ru != rv
            root[ru] = rv
    else:                                       # built trees: every town but 1 hangs on a smaller town
        assert all(1 <= u < v <= n for u, v in edges)
        assert sorted(v for _, v in edges) == list(range(2, n + 1))
    if mix:
        lab = list(range(n + 1))
        tail = lab[1:]
        shuf(tail)
        lab[1:] = tail
        edges = [(lab[u], lab[v]) if (u + v) % 3 else (lab[v], lab[u]) for u, v in edges]
        k = ri(0, n - 2)                        # start the list of roads somewhere in the middle
        edges = edges[k:] + edges[:k]
    tests.append(f"{n}\n" + "".join("%d %d\n" % e for e in edges))


def from_par(par):
    """par[i] (0-based, par[i] < i) -> edges on 1..n"""
    return [(par[i] + 1, i + 1) for i in range(1, len(par))]


def shape(n, kind):
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "cater":
            par[i] = i - 1 if i < h else ri(0, h - 1)
        else:
            raise ValueError(kind)
    return par


class Builder:
    def __init__(self):
        self.n, self.edges = 1, []

    def node(self, parent):
        self.n += 1
        if parent:
            self.edges.append((parent, self.n))
        return self.n

    def chain(self, start, length):
        x = start
        for _ in range(length):
            x = self.node(x)
        return x

    def star(self, centre, leaves):
        for _ in range(leaves):
            self.node(centre)


def double_broom(a, length, b):
    """a leaves on town 1, a path of `length` roads from town 1 to town c, b leaves on c"""
    t = Builder()
    t.star(1, a)
    c = t.chain(1, length)
    t.star(c, b)
    return t.n, t.edges


def spider(legs, length, fork_every=0):
    """legs of `length` roads from town 1; every fork_every-th leg ends in two towns instead of one"""
    t = Builder()
    for j in range(legs):
        x = t.chain(1, length - 1)
        t.node(x)
        if fork_every and j % fork_every == 0:
            t.node(x)
    return t.n, t.edges


def brooms(k, length, leaves):
    """k chains of `length` roads from town 1, each ending in a star of `leaves` leaves"""
    t = Builder()
    for _ in range(k):
        x = t.chain(1, length)
        t.star(x, leaves)
    return t.n, t.edges


def twin_binary(m):
    """two heap-shaped trees of m towns each, their roots joined by a road"""
    edges = [((i - 1) // 2 + 1, i + 1) for i in range(1, m)]
    edges += [((i - 1) // 2 + 1 + m, i + 1 + m) for i in range(1, m)]
    edges.append((1, m + 1))
    return 2 * m, edges


# samples
add(8, [(1, 2), (2, 3), (1, 4), (4, 5), (1, 6), (6, 7), (1, 8)])
add(7, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7)])
add(2, [(1, 2)])
add(5, [(3, 1), (3, 2), (3, 4), (3, 5)])
add(9, [(5, 1), (1, 4), (5, 2), (2, 7), (5, 9), (9, 3), (5, 6), (6, 8)])
add(10, [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7), (7, 8), (2, 9), (9, 10)])
# hidden: small (the brute does a BFS from every town)
add(3, [(1, 2), (2, 3)], True)
add(8, from_par(shape(8, "random")), True)
add(*double_broom(3, 4, 2), True)                    # odd longest distance, several ends on each side
add(100, from_par(shape(100, "random")), True)
add(511, from_par(shape(511, "binary")), True)
add(1000, from_par(shape(1000, "random")), True)
add(*spider(150, 20, 7), True)
add(5000, from_par(shape(5000, "cater")), True)
add(*double_broom(4000, 1001, 4998), True)
add(*twin_binary(1500), True)                        # odd, two halves
add(20_000, from_par(shape(20_000, "deep")), True)
# hidden: maximum size
N = MAXN
add(N, from_par(shape(N, "star")), True)
add(N, from_par(shape(N, "path")), True)
add(*double_broom(99_000, 1999, N - 99_000 - 2000), True)        # odd: 99 000 x 99 000 pairs
add(*spider(99_999, 2), True)
add(N, from_par(shape(N, "binary")), True)
add(N, from_par(shape(N, "random")), True)
add(N, from_par(shape(N, "deep")), True)
add(N, from_par(shape(N, "cater")), True)
add(*brooms(3, 22, 66_643), True)
add(*brooms(4, 5, 49_994), True)
add(*spider(66_666, 3), True)
add(*double_broom(80_000, 40_000, N - 120_001), True)            # even

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

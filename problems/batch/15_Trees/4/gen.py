# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100404)
MAXN, MAXQ = 200_000, 100_000
tests = []


_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    rnd = _rnd
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))                                 # = ri(0, i)
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] for i = 1..n-1 is a node in 0..i-1; node 0 is the root"""
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)                            # = ri(0, i - 1)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # depth about n / 2, a few short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "binary":
            par[i] = (i - 1) // 2
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging anywhere on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":                # two long chains below the root
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def labels(n, root=None):
    """a random numbering 1..n of the nodes 0..n-1; node 0 gets the number root if given"""
    lab = list(range(1, n + 1))
    shuf(lab)
    if root is not None:
        j = lab.index(root)
        lab[0], lab[j] = lab[j], lab[0]
    return lab


def depths(t):
    """t[i] = teacher of i (t[1] = 0); depth of every person, checking that everybody reaches person 1"""
    n = len(t) - 1
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        ch[t[i]].append(i)
    d = [-1] * (n + 1)
    d[1], order = 0, [1]
    for v in order:                                             # BFS: the list grows while we walk it
        dv = d[v] + 1
        for c in ch[v]:
            d[c] = dv
        order.extend(ch[v])
    assert min(d[1:]) >= 0
    return d


def add(t, qs, checked=False):
    """t = [t_2, ..., t_N]; checked = depths() already ran on it"""
    n, q = len(t) + 1, len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n and x != i + 2 for i, x in enumerate(t))
    assert all(1 <= v <= n and 1 <= k <= n for v, k in qs)
    if not checked:
        depths([0, 0] + t)
    t = f"{n} {q}\n" + " ".join(map(str, t)) + "\n" + "".join(f"{v} {k}\n" for v, k in qs)
    assert len(t) <= 3_000_000
    tests.append(t)


def queries(t, q, mode, d=None):
    """t = [t_2, ..., t_N]; deep people with k close to their depth (and some -1 answers);
    d = the depths if tree() already computed them"""
    n = len(t) + 1
    if d is None:
        d = depths([0, 0] + t)
    people = sorted(range(1, n + 1), key=d.__getitem__, reverse=True)
    deep = people[:max(1, n // 10)]
    L, rnd = len(deep), _rnd                                    # rnd() inlined: x = lo + int(rnd() * (hi - lo + 1))
    qs = []
    for _ in range(q):
        if mode == "deep":
            v = deep[int(rnd() * L)]
            k = d[v] // 2
            k += int(rnd() * (d[v] + 3 - k))                    # k in [d[v] / 2, d[v] + 2]
        elif mode == "edge":                                    # exactly the last ancestor, or one too far
            v = deep[int(rnd() * L)]
            k = d[v] + int(rnd() * 2)
        else:
            v = 1 + int(rnd() * n)
            k = 1 + int(rnd() * (d[v] + 1)) if int(rnd() * 4) else 1 + int(rnd() * n)
        qs.append((v, max(1, min(n, k))))
    return qs


def tree(n, kind):
    """returns (t_2..t_N, depth of every person); every node hangs below an earlier one, so it is a tree"""
    par, lab = shape(n, kind), labels(n, 1)
    assert all(0 <= par[i] < i for i in range(1, n)) and sorted(lab) == list(range(1, n + 1)) and lab[0] == 1
    t, d, dep = [0] * (n + 1), [-1] * (n + 1), [0] * n
    d[1] = 0
    for i in range(1, n):
        dep[i] = dep[par[i]] + 1
        t[lab[i]] = lab[par[i]]
        d[lab[i]] = dep[i]
    return t[2:], d


# samples
add([3, 1, 2, 2, 5, 1], [(6, 1), (6, 3), (6, 4), (6, 5), (7, 1)])
add([3, 4, 1], [(2, 2), (2, 3), (2, 4), (1, 1)])
add([1], [(2, 1), (2, 2), (1, 2)])
add([1, 1, 1, 1, 1], [(4, 1), (4, 2), (1, 6), (6, 1)])
add([5, 1, 6, 1, 3], [(4, 3), (4, 2), (2, 2), (6, 3)])
# hidden: small
for n, kind, q, mode in ((6, "random", 10, "any"), (10, "path", 15, "any"), (15, "binary", 20, "any"),
                         (40, "deep", 50, "edge"), (300, "cater", 300, "any"), (2000, "twopaths", 2000, "deep"),
                         (5000, "random", 5000, "any")):
    t, d = tree(n, kind)
    add(t, queries(t, q, mode, d), True)
t = [i - 1 for i in range(2, 5001)]                             # path 1 - 2 - ... - N
add(t, queries(t, 5000, "deep"), True)
# hidden: maximum size
N, Q = MAXN, MAXQ
t = [i - 1 for i in range(2, N + 1)]
add(t, queries(t, Q, "deep"), True)
for kind, mode in (("path", "deep"), ("path", "edge"), ("deep", "deep"), ("broom", "deep"),
                   ("twopaths", "deep"), ("cater", "any"), ("random", "any"), ("star", "any")):
    t, d = tree(N, kind)
    add(t, queries(t, Q, mode, d), True)
t = [i + 1 for i in range(2, N)] + [1]                          # path 1 - N - (N-1) - ... - 2: teachers have larger numbers
add(t, queries(t, Q, "deep"), True)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

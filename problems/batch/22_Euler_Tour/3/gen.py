# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220003)
MAXN, MAXQ, MAXV = 100_000, 200_000, 10**9
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
        elif kind == "deep":                        # depth about n / 2, short side branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a spine of n / 2 nodes with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def tree(n, kind):
    """parent array p[0..n] (p[1] = 0) of a tree of the given shape with random labels (shape node 1 = branch 1);
    also lab: lab[i - 1] = label of shape node i (small i = close to the root)"""
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


_seen = {}                                  # id(p) -> (p, depths): rops and add check the same tree once


def depths(n, p):
    """depth of every person (person 1 has depth 0); asserts that everybody reaches person 1"""
    if id(p) in _seen and _seen[id(p)][0] is p:
        return _seen[id(p)][1]
    assert p[0] == 0 and p[1] == 0 and 1 <= min(p[2:]) and max(p[2:]) <= n
    assert all(p[i] != i for i in range(2, n + 1))
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        ch[p[i]].append(i)
    dep = [0] * (n + 1)
    order = [1]
    for u in order:
        cu = ch[u]
        if cu:
            du = dep[u] + 1
            for c in cu:
                dep[c] = du
            order.extend(cu)
    assert len(order) == n
    _seen[id(p)] = (p, dep)
    return dep


def add(n, w, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(w) == n and len(p) == n + 1
    assert all(0 <= x <= MAXV for x in w)
    depths(n, p)
    assert all(len(op) == 3 for op in ops)
    assert all(1 <= v <= n and (0 <= x <= MAXV if t == 1 else t == 2 and 0 <= x <= n) for t, v, x in ops)
    assert any(op[0] == 2 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, w)) + "\n"
         + "".join("%d %d %d\n" % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, p, lab, p1=0.3, vhi=MAXV, top=None, upd=None, far=0.05):
    """random operations. Questions: v among the top nodes closest to the root (or any), and k aimed at the depth
    of a random person (so big generations are asked often); a few k beyond every generation.
    Changes: among the upd deepest nodes of the shape (or any)."""
    dep = depths(n, p)
    maxd = max(dep)
    res = []
    rnd = random.random
    for _ in range(q):
        if rnd() < p1:
            u = lab[n - 1 - int(rnd() * upd)] if upd else 1 + int(rnd() * n)
            res.append((1, u, int(rnd() * (vhi + 1))))
        else:
            v = lab[int(rnd() * top)] if top else 1 + int(rnd() * n)
            if rnd() < far:
                k = ri(maxd - dep[v], n)
            else:
                d = dep[1 + int(rnd() * n)]
                k = d - dep[v] if d >= dep[v] else int(rnd() * 4)
            res.append((2, v, k))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1, 1))
    return res


def big(kind, q, p1, vhi, top, upd, n=MAXN):
    p, lab = tree(n, kind)
    w = [ri(0, vhi) for _ in range(n)]
    add(n, w, p, rops(n, q, p, lab, p1, vhi, top, upd))


def heavy(p1, n=MAXN, q=MAXQ):
    """a handle 1 - 2 - ... - 20 ending in a star: questions from a handle person down to the huge last generation,
    changes inside that generation"""
    p = [0, 0] + [i - 1 if i <= 20 else 20 for i in range(2, n + 1)]
    ops = []
    for _ in range(q):
        if random.random() < p1:
            ops.append((1, ri(21, n), ri(0, 99)))
        else:
            v = ri(1, 20)
            ops.append((2, v, 21 - v))
    add(n, [ri(0, 99) for _ in range(n)], p, ops)


# samples
add(7, [3, 1, 5, 4, 2, 6, 7], [0, 0, 1, 1, 2, 2, 3, 3], [(2, 1, 2), (2, 2, 1), (1, 6, 10), (2, 1, 2), (2, 3, 0)])
add(4, [5, 6, 7, 8], [0, 0, 1, 2, 3], [(2, 1, 3), (2, 2, 3), (1, 4, 0), (2, 1, 3)])
add(2, [MAXV, MAXV], [0, 0, 1], [(2, 1, 0), (2, 1, 1), (2, 2, 1)])
add(6, [1, 2, 3, 4, 5, 6], [0, 0, 6, 6, 1, 3, 1], [(2, 1, 3), (2, 6, 1), (1, 2, 20), (2, 6, 1)])
add(5, [MAXV] * 5, [0, 0, 1, 1, 1, 1], [(2, 1, 1), (2, 1, 5), (2, 4, 0)])
# hidden: small and medium
for n, kind, q in ((3, "path", 6), (10, "random", 15), (30, "deep", 40), (50, "star", 60), (80, "caterpillar", 100),
                   (200, "binary", 300)):
    p, lab = tree(n, kind)
    add(n, [ri(0, 100) for _ in range(n)], p, rops(n, q, p, lab, 0.3, 100))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains")):
    p, lab = tree(n, kind)
    add(n, [ri(0, MAXV) for _ in range(n)], p, rops(n, 8000, p, lab, 0.3, MAXV, top=50, upd=n // 2))
# hidden: maximum size
big("path", 100_000, 0.2, 9999, 2_000, None)
big("broom", 100_000, 0.5, 9999, 30_000, 50_000)          # one generation of 50 000 people
big("broom", 60_000, 0.3, MAXV, 100, 50_000)              # the largest totals
big("caterpillar", 100_000, 0.3, 9999, 5_000, 50_000)
big("star", 200_000, 0.05, 99, 1, 99_999)                 # questions over the whole generation 1
big("star", 200_000, 0.95, 99, 1, 99_999)                 # changes inside generation 1
heavy(0.05)                                               # questions over the huge generation
heavy(0.95)                                               # changes inside the huge generation
big("binary", 100_000, 0.4, 9999, 30, 50_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

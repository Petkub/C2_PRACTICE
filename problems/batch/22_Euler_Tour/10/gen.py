# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220010)
MAXN, MAXQ, MAXA, MAXX = 100_000, 100_000, 10**9, 10**6
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


def add(n, a, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(a) == n and len(p) == n + 1
    assert all(0 <= x <= MAXA for x in a)
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # n - 1 roads i - p_i reaching every city from 1: a tree
    for op in ops:
        assert 1 <= op[1] <= n
        if op[0] == 2:
            assert len(op) == 3 and 1 <= op[2] <= MAXX
        else:
            assert op[0] in (1, 3) and len(op) == 2
    assert any(op[0] == 3 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, p[2:])) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, pr, pu, xhi=MAXX, deep=None, top=None, same=0.0):
    """random operations: `1 r` with probability pr (r among the `deep` deepest shape nodes if given),
    `2 v x` with probability pu, else `3 v`; v among the `top` shape nodes closest to city 1 if given
    (ancestors of a deep capital on paths), and v = the capital with probability same"""
    res, root = [], 1
    for _ in range(q):
        u = random.random()
        if u < pr:
            root = lab[n - 1 - int(random.random() * deep)] if deep else ri(1, n)
            res.append((1, root))
            continue
        if random.random() < same:
            v = root
        else:
            v = lab[int(random.random() * top)] if top else ri(1, n)
        if u < pr + pu:
            res.append((2, v, ri(1, xhi)))
        else:
            res.append((3, v))
    if not any(op[0] == 3 for op in res):
        res.append((3, 1))
    return res


def big(kind, q, pr, pu, ahi, xhi, deep, top, same=0.05, n=MAXN):
    p, lab = tree(n, kind)
    a = [ri(0, ahi) for _ in range(n)]
    add(n, a, p, rops(n, q, lab, pr, pu, xhi, deep, top, same))


# samples
add(6, [3, 1, 4, 1, 5, 9], [0, 0, 1, 1, 2, 2, 3], [(3, 2), (1, 4), (3, 2), (2, 1, 10), (3, 3)])
add(4, [1, 2, 3, 4], [0, 0, 1, 2, 3], [(1, 3), (3, 2), (2, 3, 5), (3, 4)])
add(2, [5, 7], [0, 0, 1], [(3, 1), (1, 2), (2, 2, 100), (3, 1)])
add(5, [1, 10, 100, 1000, 10000], [0, 0, 1, 1, 1, 1], [(1, 3), (2, 1, 1), (3, 1), (3, 3)])
add(4, [MAXA] * 4, [0, 0, 3, 4, 1], [(2, 2, MAXX), (1, 2), (3, 4), (3, 2)])
# hidden: small and medium
for n, kind, q in ((3, "path", 6), (8, "random", 12), (20, "star", 30), (40, "deep", 60), (60, "caterpillar", 80),
                   (100, "binary", 150), (300, "random", 400)):
    p, lab = tree(n, kind)
    add(n, [ri(0, 100) for _ in range(n)], p, rops(n, q, lab, 0.3, 0.3, 100, same=0.1))
for n, kind in ((4000, "path"), (6000, "broom"), (6000, "chains")):
    p, lab = tree(n, kind)
    add(n, [ri(0, MAXA) for _ in range(n)], p, rops(n, 6000, lab, 0.3, 0.3, MAXX, 500, 100))
# hidden: maximum size (deep capitals, regions of their ancestors)
big("path", 100_000, 0.3, 0.3, 9999, MAXX, 30_000, 30_000)
big("path", 100_000, 0.5, 0.2, 9999, 9999, 1_000, 1_000)
big("deep", 100_000, 0.3, 0.3, 9999, MAXX, 10_000, 10_000)
big("caterpillar", 100_000, 0.3, 0.3, 9999, 9999, 20_000, 20_000)
big("broom", 100_000, 0.3, 0.3, 9999, MAXX, 40_000, 40_000)
big("chains", 100_000, 0.3, 0.3, 9999, 9999, 10_000, 3_000)
big("random", 100_000, 0.3, 0.3, 9999, MAXX, None, None, 0.2)
big("star", 100_000, 0.3, 0.3, 9999, 9999, None, 1)
big("path", 60_000, 0.2, 0.4, MAXA, MAXX, 50_000, 50_000)          # the largest totals
big("deep", 100_000, 0.45, 0.1, 9999, MAXX, 500, 50, 0.0)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220004)
MAXN, MAXQ, MAXV = 200_000, 100_000, 10**9
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
def add(n, a, p, ops, lab=None):
    """lab (from tree()): every node listed after its parent, so reaching person 1 is checked along lab"""
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(a) == n and len(p) == n + 1
    assert all(-MAXV <= x <= MAXV for x in a)
    assert p[0] == p[1] == 0 and 1 <= min(p[2:]) and max(p[2:]) <= n and all(map(int.__ne__, p[2:], range(2, n + 1)))
    if lab is not None:
        assert lab[0] == 1 and sorted(lab) == list(range(1, n + 1))
        seen = [False] * (n + 1)
        seen[1] = True
        for v in lab[1:]:
            assert seen[p[v]]                  # the boss was already shown to reach person 1
            seen[v] = True
    else:
        ch = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            ch[p[i]].append(i)
        order = [1]
        for u in order:
            order.extend(ch[u])
        assert len(order) == n                 # everybody reaches person 1
    assert all(1 <= op[1] <= n and (len(op) == 3 and -MAXV <= op[2] <= MAXV if op[0] == 1 else op[0] == 2 and len(op) == 2)
               for op in ops)
    assert any(op[0] == 2 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, a)) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, p1=0.5, xlo=-MAXV, xhi=MAXV, top=None):
    """random operations; with top = s both kinds pick among the s people closest to the root (big teams)"""
    res = []
    rnd, span = random.random, xhi - xlo + 1
    for _ in range(q):
        v = lab[int(rnd() * top)] if top else 1 + int(rnd() * n)
        if rnd() < p1:
            res.append((1, v, xlo + int(rnd() * span)))
        else:
            res.append((2, v))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1))
    return res


def big(kind, q, p1, av, xv, top, n=MAXN):
    """scores in [av[0], av[1]], changes in [xv[0], xv[1]]"""
    p, lab = tree(n, kind)
    rnd, span = random.random, av[1] - av[0] + 1
    a = [av[0] + int(rnd() * span) for _ in range(n)]
    add(n, a, p, rops(n, q, lab, p1, xv[0], xv[1], top), lab)


# samples
add(6, [5, -2, 3, 1, 4, -6], [0, 0, 1, 1, 2, 2, 3], [(2, 2), (1, 2, 3), (2, 1), (2, 6)])
add(3, [-5, -8, -3], [0, 0, 1, 2], [(2, 2), (1, 2, -4), (2, 1)])
add(2, [MAXV, MAXV], [0, 0, 1], [(1, 1, MAXV), (1, 2, MAXV), (2, 1), (2, 2)])
add(5, [0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1], [(1, 1, -7), (1, 3, 2), (2, 1), (2, 4), (1, 1, 9)])
add(6, [-1, 4, 2, -3, 0, 6], [0, 0, 4, 1, 3, 3, 1], [(2, 3), (1, 4, -10), (2, 1), (1, 6, -10), (2, 1)])
# hidden: small and medium
for n, kind, q in ((3, "path", 6), (10, "random", 15), (30, "deep", 40), (50, "star", 60), (80, "caterpillar", 100),
                   (200, "binary", 300)):
    p, lab = tree(n, kind)
    add(n, [ri(-100, 100) for _ in range(n)], p, rops(n, q, lab, 0.5, -100, 100))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains")):
    p, lab = tree(n, kind)
    add(n, [ri(-MAXV, MAXV) for _ in range(n)], p, rops(n, 8000, lab, 0.5, -MAXV, MAXV, top=50))
# hidden: maximum size (both kinds on big teams)
big("path", 90_000, 0.5, (-99, 99), (-99, 99), 2_000)
big("path", 40_000, 0.6, (MAXV, MAXV), (MAXV, MAXV), 30, n=100_000)     # the largest scores (about 2 * 10^13)
big("path", 40_000, 0.6, (-MAXV, -MAXV), (-MAXV, -MAXV), 30, n=100_000)   # the smallest scores
big("deep", 90_000, 0.5, (-99, 99), (-99, 99), 1_000)
big("caterpillar", 90_000, 0.5, (-99, 99), (-99, 99), 1_000)
big("broom", 90_000, 0.5, (-99, 99), (-99, 99), 30_000)
big("chains", 90_000, 0.5, (-99, 99), (-99, 99), 200)
big("star", 90_000, 0.3, (-99, 99), (-99, 99), 1)
# hidden: maximum size, changes mostly negative so whole teams sink far below -10^9
big("deep", 55_000, 0.5, (-99, 99), (-MAXV, MAXV // 5), 500)
big("caterpillar", 55_000, 0.5, (-99, 99), (-MAXV, MAXV // 5), 300)
big("broom", 55_000, 0.5, (-99, 99), (-MAXV, MAXV // 5), 2_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

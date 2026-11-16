# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220002)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10**9
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
def add(n, p, w, ops):
    """w[0..n], w[i] = length of the road from city i to p[i] (i >= 2)"""
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(p) == n + 1 and len(w) == n + 1
    assert all(1 <= w[i] <= MAXW for i in range(2, n + 1))
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # every city reaches city 1
    for op in ops:
        if op[0] == 1:
            assert len(op) == 3 and 2 <= op[1] <= n and 1 <= op[2] <= MAXW
        else:
            assert op[0] == 2 and len(op) == 2 and 1 <= op[1] <= n
    assert any(op[0] == 2 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, w[2:])) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, p1=0.5, wlo=1, whi=MAXW, top=None, low=None):
    """random operations; with low = s queries pick among the s deepest cities (long walks up),
    with top = s changes pick among the s cities closest to the root (big subtrees)"""
    res = []
    for _ in range(q):
        if random.random() < p1:
            v = lab[1 + int(random.random() * min(top, n - 1))] if top else ri(2, n)
            res.append((1, v, ri(wlo, whi)))
        else:
            v = lab[n - 1 - int(random.random() * low)] if low else ri(1, n)
            res.append((2, v))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1))
    return res


def big(kind, q, p1, whi, top, low, n=MAXN):
    p, lab = tree(n, kind)
    w = [0, 0] + [ri(1, whi) for _ in range(n - 1)]
    add(n, p, w, rops(n, q, lab, p1, 1, whi, top, low))


# samples
add(5, [0, 0, 1, 1, 2, 2], [0, 0, 4, 7, 3, 5], [(2, 4), (1, 2, 10), (2, 4), (2, 1)])
add(4, [0, 0, 3, 4, 1], [0, 0, 1, 2, 3], [(2, 2), (1, 4, 100), (2, 3)])
add(2, [0, 0, 1], [0, 0, MAXW], [(2, 2), (2, 1), (1, 2, 1), (2, 2)])
add(6, [0, 0, 1, 2, 3, 4, 5], [0, 0, MAXW, MAXW, MAXW, MAXW, MAXW], [(2, 6), (1, 3, 5), (2, 6)])
add(6, [0, 0, 5, 1, 1, 4, 4], [0, 0, 2, 9, 1, 6, 3], [(2, 2), (1, 5, 1), (2, 6), (2, 2)])
# hidden: small and medium
for n, kind, q in ((3, "path", 4), (10, "random", 15), (30, "deep", 40), (50, "star", 60), (80, "caterpillar", 100),
                   (200, "binary", 300)):
    p, lab = tree(n, kind)
    w = [0, 0] + [ri(1, 100) for _ in range(n - 1)]
    add(n, p, w, rops(n, q, lab, 0.5, 1, 100))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains")):
    p, lab = tree(n, kind)
    w = [0, 0] + [ri(1, MAXW) for _ in range(n - 1)]
    add(n, p, w, rops(n, 8000, lab, 0.5, 1, MAXW, top=50, low=200))
# hidden: maximum size (changes near the root, questions deep down)
big("path", 100_000, 0.5, 9999, 2_000, 2_000)
big("path", 70_000, 0.3, MAXW, 100, 100)                # the largest distances (about 10^14)
big("deep", 100_000, 0.5, 9999, 1_000, 1_000)
big("caterpillar", 100_000, 0.5, 9999, 5_000, 1_000)
big("broom", 100_000, 0.5, 9999, 20_000, 30_000)
big("path", 100_000, 0.2, 9999, 50_000, 50_000)
big("random", 100_000, 0.5, 9999, None, None)
big("star", 100_000, 0.5, 9999, None, None)
big("deep", 100_000, 0.1, 9999, 50_000, 30_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

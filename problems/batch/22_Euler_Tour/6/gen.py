# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220006)
MAXN, MAXQ = 100_000, 100_000
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
    """parent array p[0..n] (p[1] = 0) of a tree of the given shape with random labels (shape node 1 = shop 1);
    lab[i - 1] = label of shape node i (small i = close to the root); size[i - 1] = subtree size of shape node i"""
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    size = [1] * (n + 1)
    for i in range(n, 1, -1):
        size[par[i]] += size[i]
    return p, lab, size[1:]


def add(n, s, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(s) == n and set(s) <= {"0", "1"} and len(p) == n + 1
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # every shop reaches shop 1
    ts = [op[0] for op in ops]
    vs = [op[1] for op in ops]
    ks = [op[2] for op in ops if len(op) == 3]
    assert set(ts) <= {1, 2} and 2 in ts and 1 <= min(vs) and max(vs) <= n and 1 <= min(ks) and max(ks) <= n
    assert all(len(op) == (2 if op[0] == 1 else 3) for op in ops)
    t = (f"{n} {q}\n" + s + "\n" + " ".join(map(str, p[2:])) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, size, dens, p1=0.2, top=None, pool=None, late=0.5):
    """random operations. Queries pick among the `top` nodes closest to the root (all nodes if None) and ask for a
    k near the expected number of open shops of the subtree (deep in the order; sometimes beyond it: -1).
    Toggles pick from a pool of `pool` nodes so that the density of open shops stays about `dens`."""
    pl = [ri(1, n) for _ in range(pool)] if pool else None
    res = []
    for _ in range(q):
        if random.random() < p1:
            res.append((1, pl[int(random.random() * pool)] if pool else ri(1, n)))
        else:
            i = int(random.random() * (top or n))
            exp = dens * size[i]
            lo = max(1, int(exp * late))
            hi = max(lo, min(n, int(exp * 1.05) + 1))
            res.append((2, lab[i], ri(lo, hi)))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1, 1))
    return res


def opens(n, dens):
    return "".join("1" if random.random() < dens else "0" for _ in range(n))


def big(kind, dens, q, p1, top, pool, late=0.5, n=MAXN):
    p, lab, size = tree(n, kind)
    add(n, opens(n, dens), p, rops(n, q, lab, size, dens, p1, top, pool, late))


# samples
add(7, "1011011", [0, 0, 3, 1, 5, 1, 3, 6], [(2, 1, 4), (2, 3, 2), (1, 3), (2, 3, 2)])
add(4, "0101", [0, 0, 1, 2, 3], [(2, 1, 2), (2, 2, 3), (1, 1), (2, 1, 1)])
add(2, "00", [0, 0, 1], [(2, 1, 1), (1, 2), (2, 1, 1)])
add(5, "11111", [0, 0, 1, 1, 1, 1], [(2, 1, 5), (1, 1), (2, 1, 1)])
add(6, "011111", [0, 0, 6, 1, 1, 3, 1], [(2, 1, 3), (2, 6, 2), (2, 1, 6)])
# hidden: small and medium
for n, kind, q in ((3, "path", 6), (10, "random", 20), (30, "deep", 40), (40, "star", 60), (80, "caterpillar", 100),
                   (300, "binary", 300)):
    p, lab, size = tree(n, kind)
    add(n, opens(n, 0.5), p, rops(n, q, lab, size, 0.5, 0.3))
for n, kind, dens in ((5000, "path", 0.05), (8000, "broom", 0.3), (8000, "chains", 0.5)):
    p, lab, size = tree(n, kind)
    add(n, opens(n, dens), p, rops(n, 8000, lab, size, dens, 0.2, 100, 500))
# hidden: maximum size (queries near the root, the k-th open shop far inside the order)
big("path", 0.02, MAXQ, 0.2, 1_000, 2_000)
big("path", 0.5, MAXQ, 0.1, 5_000, 2_000, late=0.8)
big("deep", 0.1, MAXQ, 0.2, 2_000, 2_000)
big("caterpillar", 0.05, MAXQ, 0.3, 1_000, 5_000)
big("broom", 0.2, MAXQ, 0.2, 500, 3_000)
big("star", 0.01, MAXQ, 0.4, 1, 1_000, late=0.9)
big("chains", 0.1, MAXQ, 0.2, 300, 2_000)
big("random", 0.5, MAXQ, 0.3, None, None)
big("path", 0.0, MAXQ, 0.05, 10_000, 1_000)                     # almost all closed: mostly -1
big("deep", 0.9, MAXQ, 0.2, 3_000, 5_000, late=0.9)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

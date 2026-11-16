# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220008)
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
    """parent array p[0..n] (p[1] = 0) of a tree of the given shape with random labels (shape node 1 = person 1);
    lab[i - 1] = label of shape node i (small i = close to the root)"""
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(p) == n + 1
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # every person reaches person 1
    ts, vs = zip(*ops)
    assert set(ts) <= {1, 2} and 2 in ts and 1 <= min(vs) and max(vs) <= n
    t = f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + "".join("%d %d\n" % e for e in ops)
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, p1, signers=None, asked=None):
    """random operations; new signers among the `signers` nodes closest to the root (any node if None),
    questions among the `asked` deepest nodes (any node if None)"""
    res = []
    for _ in range(q):
        if random.random() < p1:
            res.append((1, lab[int(random.random() * signers)] if signers else ri(1, n)))
        else:
            res.append((2, lab[n - 1 - int(random.random() * asked)] if asked else ri(1, n)))
    if not any(t == 2 for t, v in res):
        res.append((2, n))
    return res


def big(kind, q, p1, signers, asked, n=MAXN):
    p, lab = tree(n, kind)
    add(n, p, rops(n, q, lab, p1, signers, asked))


# samples
add(7, [0, 0, 1, 1, 2, 2, 3, 5], [(1, 2), (2, 7), (2, 6), (1, 5), (2, 7)])
add(5, [0, 0, 1, 2, 3, 4], [(1, 3), (2, 5), (2, 3), (2, 2)])
add(2, [0, 0, 1], [(2, 2), (1, 2), (2, 2), (2, 1)])
add(5, [0, 0, 1, 1, 1, 1], [(1, 1), (1, 4), (2, 4), (2, 5)])
add(6, [0, 0, 6, 1, 2, 3, 1], [(1, 6), (2, 4), (1, 3), (2, 5), (2, 2)])
# hidden: small and medium
for n, kind, q in ((3, "path", 6), (10, "random", 20), (30, "deep", 40), (40, "star", 60), (80, "caterpillar", 100),
                   (300, "binary", 300), (500, "random", 1000)):
    p, lab = tree(n, kind)
    add(n, p, rops(n, q, lab, 0.3))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains"), (10000, "caterpillar")):
    p, lab = tree(n, kind)
    add(n, p, rops(n, 10000, lab, 0.2, 100, 1000))
# hidden: maximum size (signers near the root, questions deep down)
Q = MAXQ
big("path", Q, 0.1, 1_000, 5_000)
big("path", Q, 0.3, 30_000, 30_000)
big("deep", Q, 0.1, 2_000, 20_000)
big("caterpillar", Q, 0.2, 10_000, 50_000)          # many signers off the question's path (on legs)
big("broom", Q, 0.05, 1_000, 45_000)
big("chains", Q, 0.2, 5_000, 50_000)
big("random", Q, 0.5, None, None)
big("binary", Q, 0.3, 20_000, 50_000)
big("path", Q, 0.0, 1, 50_000)                      # nobody but person 1 ever signs
big("path", Q, 0.5, 50_000, 50_000)                  # many signers, each over a huge subtree

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

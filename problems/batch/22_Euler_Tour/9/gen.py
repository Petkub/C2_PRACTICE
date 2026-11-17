# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220009)
MAXN, MAXQ, MAXV = 100_000, 100_000, 10**9
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
        elif kind == "longchains":                  # 20 chains of length n / 20 glued at random
            p = i - 1 if (i - 1) % max(2, n // 20) else ri(1, i - 1)
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def tree(n, kind):
    """parent array p[0..n] (p[1] = 0) of a tree of the given shape with random labels (shape node 1 = town 1);
    lab[i - 1] = label of shape node i (small i = close to the root)"""
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, a, p, qs):
    q = len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(a) == n and len(p) == n + 1
    assert 1 <= min(a) and max(a) <= MAXV
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # every town reaches town 1
    vs, xs = zip(*qs)
    assert 1 <= min(vs) and max(vs) <= n and 1 <= min(xs) and max(xs) <= MAXV
    t = (f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, p[2:])) + "\n"
         + "".join("%d %d\n" % e for e in qs))
    assert len(t) <= 3_100_000
    tests.append(t)


def rqs(n, q, a, lab, deep=None, vhi=MAXV):
    """questions from the `deep` deepest towns (any town if None); x is mostly a toll that occurs (ties),
    sometimes a random value, below every toll or above every toll"""
    res = []
    amin = min(a)
    for _ in range(q):
        v = lab[n - 1 - int(random.random() * deep)] if deep else ri(1, n)
        r = random.random()
        if r < 0.6:
            x = a[int(random.random() * n)]
        elif r < 0.9:
            x = ri(1, vhi)
        elif r < 0.95:
            x = max(1, amin - ri(0, 1))
        else:
            x = vhi
        res.append((v, x))
    return res


def big(kind, q, vhi, deep, n=MAXN, few=None):
    p, lab = tree(n, kind)
    a = [ri(1, few) * (vhi // few) for _ in range(n)] if few else [ri(1, vhi) for _ in range(n)]
    add(n, a, p, rqs(n, q, a, lab, deep, vhi))


# samples
add(7, [5, 3, 8, 6, 2, 4, 7], [0, 0, 1, 1, 2, 2, 3, 5], [(7, 5), (6, 4), (4, 10), (1, 4)])
add(4, [2, 2, 9, 1], [0, 0, 1, 2, 3], [(4, 2), (3, 1), (4, 9)])
add(2, [MAXV, MAXV], [0, 0, 1], [(2, MAXV), (1, MAXV)])
add(5, [1, 2, 3, 4, 5], [0, 0, 1, 1, 1, 1], [(5, 5), (3, 2), (1, 1)])
add(6, [4, 4, 4, 4, 4, 3], [0, 0, 6, 1, 2, 3, 1], [(4, 4), (5, 3), (5, 4)])
# hidden: small and medium
add(2, [MAXV, MAXV], [0, 0, 1], [(2, MAXV), (2, MAXV - 1), (1, 1)])
add(6, [4, 4, 4, 4, 4, 4], [0, 0, 6, 1, 2, 3, 1], [(4, 4), (5, 3), (5, 4), (6, 5)])
for n, kind, q in ((3, "path", 6), (10, "random", 20), (30, "deep", 40), (40, "star", 60), (80, "caterpillar", 100),
                   (300, "binary", 300), (500, "chains", 1000)):
    p, lab = tree(n, kind)
    a = [ri(1, 20) for _ in range(n)]
    add(n, a, p, rqs(n, q, a, lab, None, 20))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "deep")):
    p, lab = tree(n, kind)
    a = [ri(1, MAXV) for _ in range(n)]
    add(n, a, p, rqs(n, 8000, a, lab, 1000))
# hidden: a shallow tree (short ways home)
big("random", 50_000, 10**6, None, n=20_000)
# hidden: maximum size (questions from the deepest towns)
big("path", MAXQ, 10**6, 5_000)
big("path", 60_000, MAXV, 1_000)
big("path", MAXQ, 10**6, 20_000, few=10)                  # only 10 different tolls: many ties
big("deep", MAXQ, 10**6, 10_000)
big("caterpillar", MAXQ, 10**6, 30_000)
big("broom", MAXQ, 10**6, 40_000)
big("longchains", MAXQ, 10**6, 20_000)
big("deep", MAXQ, 1_000, 30_000)
big("deep", MAXQ, 10**6, 2_000)
big("caterpillar", MAXQ, 10**6, 5_000, few=1000)
big("broom", MAXQ, 10**6, 1_000)
big("longchains", 80_000, MAXV, 1_000)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

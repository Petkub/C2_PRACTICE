# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import gc, os, random

random.seed(220008)
gc.disable()                                    # many small tuples: the collector only slows this down
MAXN, MAXQ = 200_000, 200_000
tests = []
checked = {}


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the nodes 2..n of a tree of the given shape, before relabelling"""
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    rnd = random.random
    if kind == "path":
        par = list(range(-1, n))
    elif kind == "star":
        par = [1] * (n + 1)
    elif kind == "random":
        par = [1 + int(rnd() * (i - 1)) for i in range(n + 1)]
    elif kind == "deep":                            # depth about n / 2, short side branches
        par = [i - 1 - int(rnd() * min(3, i - 1)) for i in range(n + 1)]
    elif kind == "binary":
        par = [i // 2 for i in range(n + 1)]
    elif kind == "caterpillar":                     # a spine of n / 2 nodes with legs
        par = [i - 1 if i <= half else 1 + int(rnd() * half) for i in range(n + 1)]
    elif kind == "broom":                           # a long handle ending in a star
        par = [i - 1 if i <= half else half for i in range(n + 1)]
    elif kind == "longchains":                      # 20 chains of length n / 20 glued at random
        par = [i - 1 if (i - 1) % max(2, n // 20) else 1 + int(rnd() * (i - 1)) for i in range(n + 1)]
    elif kind == "chains":                          # chains of length about sqrt(n) glued at random
        par = [i - 1 if (i - 1) % b else 1 + int(rnd() * (i - 1)) for i in range(n + 1)]
    else:
        raise ValueError(kind)
    par[0] = par[1] = 0
    return par


def rperm(xs):
    """the items of xs in random order"""
    key = {x: random.random() for x in xs}
    return sorted(key, key=key.__getitem__)


def tree(n, kind):
    """parent array p[0..n] (p[1] = 0) of a tree of the given shape with random labels (shape node 1 = person 1);
    lab[i - 1] = label of shape node i (small i = close to the root)"""
    par = shape(n, kind)
    lab = [1] + rperm(range(2, n + 1))
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, p, ops, order=None):
    """order (optional): all people, person 1 first, each one after their direct boss"""
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(p) == n + 1
    assert 1 <= min(p[2:]) and max(p[2:]) <= n
    if order is None:
        ch = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            ch[p[i]].append(i)
        order = [1]
        for u in order:
            order.extend(ch[u])
    if id(p) not in checked:                    # a tree shared by two tests is checked once
        pos = [-1] * (n + 1)
        for i, v in enumerate(order):
            pos[v] = i
        assert order[0] == 1 and len(order) == n and min(pos[1:]) >= 0
        assert all(pos[p[v]] < pos[v] for v in order[1:])    # so every person reaches person 1
        checked[id(p)] = p
    ts, vs = zip(*ops)
    assert set(ts) <= {1, 2} and 2 in ts and 1 <= min(vs) and max(vs) <= n
    t = f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + ("%d %d\n" * q) % tuple(e for op in ops for e in op)
    assert len(t) <= 3_200_000
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
for n, kind in ((5000, "path"), (8000, "broom"), (10000, "caterpillar")):
    p, lab = tree(n, kind)
    add(n, p, rops(n, 10000, lab, 0.2, 100, 1000))
# hidden: shallow trees (questions walk only a few steps up)
big("random", 50_000, 0.5, None, None, n=20_000)
big("binary", 50_000, 0.3, 4_000, 10_000, n=20_000)
big("chains", 50_000, 0.2, 1_000, 10_000, n=20_000)
# hidden: maximum size
def heavy(kind, *runs, n=MAXN):
    """one tree, one test per run (p1, top, asked, q): p1 of the events give the right to distinct people among
    the `top` nodes closest to the root (in random order), the other events are questions from the `asked`
    deepest nodes"""
    p, lab = tree(n, kind)
    for p1, top, asked, q in runs:
        rnd = random.random
        kinds = [1 if rnd() < p1 else 2 for _ in range(q)]
        k = kinds.count(1)
        new = [lab[i] for i in rperm(range(min(top, n)))][:k]
        new += [lab[int(rnd() * top)] for _ in range(k - len(new))]          # repeats once all have it
        new.reverse()
        deep = lab[n - asked:]
        ops = [(1, new.pop()) if t == 1 else (2, deep[int(rnd() * asked)]) for t in kinds]
        add(n, p, ops, lab)


N, Q = MAXN, MAXQ
heavy("path", (0.5, N // 2, 50_000, Q), (0.3, 70_000, 20_000, Q))
heavy("path", (0.7, 140_000, 30_000, 180_000), (0.4, 40_000, 100_000, Q))
heavy("deep", (0.5, N // 2, 40_000, Q), (0.3, 60_000, 10_000, Q))
heavy("broom", (0.5, 60_000, 90_000, Q), (0.3, 50_000, 50_000, Q))
heavy("caterpillar", (0.4, 70_000, 60_000, Q), (0.4, 40_000, 20_000, Q))
heavy("path", (0.5, N // 2, 50_000, 180_000), (0.6, 30_000, 100_000, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

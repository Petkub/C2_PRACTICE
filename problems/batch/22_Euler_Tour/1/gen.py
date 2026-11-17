# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220101)
MAXN, MAXQ, MAXS = 100_000, 200_000, 10**9
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
    also lab: lab[i - 1] = label of shape node i (small i = close to the root)"""
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, p, s, cmds):
    q = len(cmds)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(s) == n and len(p) == n + 1
    assert all(0 <= x <= MAXS for x in s)
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n                     # every person reaches person 1
    assert all(1 <= v <= n for v in cmds)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, s)) + "\n"
         + " ".join(map(str, cmds)) + "\n")
    assert len(t) <= 3_100_000
    tests.append(t)


def rcmds(n, q, lab, top=None):
    """random commands; with top = k they pick among the k people closest to the root (big teams)"""
    if top:
        return [lab[int(random.random() * top)] for _ in range(q)]
    return [ri(1, n) for _ in range(q)]


def case(n, kind, q, shi, top=None):
    p, lab = tree(n, kind)
    add(n, p, [ri(0, shi) for _ in range(n)], rcmds(n, q, lab, top))


# samples
add(6, [0, 0, 1, 1, 2, 2, 3], [5, 4, 3, 2, 6, 2], [1, 1, 3, 2, 6, 1])
add(4, [0, 0, 1, 2, 3], [6, 2, 8, 2], [2, 2, 2, 2, 1])
add(2, [0, 0, 1], [MAXS, MAXS], [2, 2, 1, 1])
add(5, [0, 0, 3, 1, 3, 2], [3, 1, 9, 4, 1], [3, 3, 3, 3, 3])
add(5, [0, 0, 1, 1, 1, 1], [0, 7, 0, 7, 7], [1, 4, 1, 1, 4, 1])
# hidden: small and medium (many equal scores)
for n, kind, q, shi in ((3, "path", 4, 1), (10, "random", 15, 2), (30, "deep", 40, 3), (50, "star", 60, 2),
                        (80, "caterpillar", 100, 5), (200, "binary", 300, 10)):
    case(n, kind, q, shi)
case(5000, "random", 6000, 20)
case(5000, "broom", 6000, 3, top=100)
case(5000, "chains", 6000, MAXS, top=300)
# hidden: maximum size, every command on a big team
case(MAXN, "path", MAXQ, 50, top=1000)
case(MAXN, "path", MAXQ, MAXS, top=50)
case(MAXN, "deep", MAXQ, 5, top=1000)
case(MAXN, "caterpillar", MAXQ, 100, top=3000)
case(MAXN, "broom", MAXQ, 2, top=20_000)
case(MAXN, "chains", MAXQ, 1000, top=200)
case(MAXN, "star", MAXQ, 10, top=1)
case(MAXN, "binary", MAXQ, 3, top=3)
case(MAXN, "deep", MAXQ, MAXS, top=100)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

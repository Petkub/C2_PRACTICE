# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100112)
MAXN, MAXM, MAXX = 100_000, 100_000, 10**9
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
        elif kind == "deep":                        # depth about n / 2, a few short branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a spine of n / 2 nodes with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "twopaths":                    # two long chains meeting at node 1
            p = 1 if i <= 3 else i - 2
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def bosses(n, kind):
    """boss array p[2..n] of a tree of the given shape, random labels, the root is always person 1;
    also returns lab: lab[i - 1] is the label of node i of the shape (small i = close to the root)"""
    par = shape(n, kind)
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, p, ops):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXM and len(p) == n + 1
    under = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        under[p[i]].append(i)
    seen, k = [1], 0                      # everybody is reached from person 1 going down
    while k < len(seen):
        seen.extend(under[seen[k]])
        k += 1
    assert len(seen) == n
    assert all(t in (1, 2) and 1 <= v <= n and 1 <= x <= MAXX for t, v, x in ops)
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{t} {v} {x}\n" for t, v, x in ops))


def rops(n, m, lab=None, xlo=1, xhi=MAXX, p1=0.5, shallow=None):
    """random operations; with shallow = s, type 1 picks among the s nodes closest to the root of the shape
    and type 2 among the s deepest ones (the most work for a walk)"""
    rnd, res = random.random, []
    for _ in range(m):
        t = 1 if rnd() < p1 else 2
        if shallow is None:
            v = 1 + int(rnd() * n)
        elif t == 1:
            v = lab[int(rnd() * shallow)]
        else:
            v = lab[n - 1 - int(rnd() * shallow)]
        res.append((t, v, xlo + int(rnd() * (xhi - xlo + 1))))
    return res


def big(kind, shallow=None, p1=0.5, xlo=1, xhi=MAXX):
    n, m = MAXN, MAXM
    p, lab = bosses(n, kind)
    add(n, p, rops(n, m, lab, xlo, xhi, p1, shallow))


# samples
add(5, [0, 0, 1, 1, 3, 3], [(1, 3, 10), (2, 4, 5), (1, 1, 1)])
add(4, [0, 0, 4, 1, 3], [(2, 2, 100), (1, 4, 20), (2, 3, 7)])
add(2, [0, 0, 1], [(2, 1, 5), (1, 2, 3)])
add(6, [0, 0, 1, 1, 1, 1, 1], [(1, 1, 2), (2, 4, 3), (1, 6, 5), (2, 1, 4)])
add(7, [0, 0, 5, 2, 6, 1, 1, 2], [(1, 2, 3), (2, 4, 1), (1, 6, 4), (2, 3, 2)])
# hidden: small and medium
for n, kind, m in ((3, "path", 4), (10, "random", 10), (30, "deep", 40), (40, "star", 30), (60, "caterpillar", 80)):
    p, lab = bosses(n, kind)
    add(n, p, rops(n, m, lab, 1, 100))
p, lab = bosses(3000, "path")
add(3000, p, rops(3000, 3000, lab, shallow=300))
p, lab = bosses(5000, "chains")
add(5000, p, rops(5000, 5000))
p, lab = bosses(8000, "broom")
add(8000, p, rops(8000, 8000, lab, p1=0.2, shallow=100))
# hidden: maximum size
big("path", shallow=10_000)
big("path", shallow=100, xlo=MAXX, xhi=MAXX)                   # the largest totals
big("deep", shallow=5_000)
big("caterpillar", shallow=5_000)
big("broom", shallow=1_000, p1=0.3)
big("twopaths", shallow=5_000)
big("chains", shallow=2_000)
big("random")
big("star", shallow=1, p1=0.7)
big("path", shallow=1_000, p1=0.0)                              # only type 2
big("deep", shallow=50, p1=1.0)                                 # only type 1

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

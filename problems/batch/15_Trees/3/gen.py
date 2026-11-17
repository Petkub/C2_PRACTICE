# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(150301)
MAXN = 100_000
MAXC = 10**9
tests = []

_rnd = random.random


def ri(lo, hi):
    return lo + int(_rnd() * (hi - lo + 1))


def shuf(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(_rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    """par[i] for i = 1..n-1 is a node in 0..i-1; node 0 is house 1 (the top)"""
    par = [-1] * n
    h = max(1, n // 2)
    for i in range(1, n):
        if kind == "random":
            par[i] = int(_rnd() * i)
        elif kind == "path":
            par[i] = i - 1
        elif kind == "star":
            par[i] = 0
        elif kind == "deep":                    # depth about n / 2, short side branches
            par[i] = ri(max(0, i - 3), i - 1)
        elif kind == "broom":                   # a path of n / 2 nodes, then a star at its end
            par[i] = i - 1 if i <= h else h
        elif kind == "cater":                   # a path of n / 2 nodes with leaves hanging anywhere on it
            par[i] = i - 1 if i < h else ri(0, h - 1)
        elif kind == "twopaths":                # two long chains below the top
            par[i] = 0 if i <= 2 else i - 2
        else:
            raise ValueError(kind)
    return par


def add(n, rows, parcels):
    """rows[i] = (p, d, u) for house i = 2..n (index i - 2)"""
    assert 2 <= n <= MAXN and len(rows) == n - 1
    k = len(parcels)
    assert 1 <= k <= n and len(set(parcels)) == k and 1 <= min(parcels) and max(parcels) <= n
    p = [0, 0] + [r[0] for r in rows]
    assert 1 <= min(p[2:]) and max(p[2:]) <= n and all(p[i] != i for i in range(2, n + 1))
    assert 1 <= min(min(r[1], r[2]) for r in rows) and max(max(r[1], r[2]) for r in rows) <= MAXC
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        ch[p[i]].append(i)
    order = [1]                                 # every house reaches house 1 going up
    for v in order:
        order.extend(ch[v])
    assert len(order) == n
    lines = [f"{n} {k}"] + ["%d %d %d" % r for r in rows] + [" ".join(map(str, parcels))]
    tests.append("\n".join(lines) + "\n")


def tree(n, kind, cost, pick, par=None):
    """random labels (the top keeps number 1); cost(i) -> (d, u) for shape node i;
    pick(par) -> list of shape nodes that get a parcel"""
    if par is None:
        par = shape(n, kind)
    lab = list(range(2, n + 1))
    shuf(lab)
    lab = [1] + lab
    rows = [None] * (n - 1)
    for i in range(1, n):
        d, u = cost(i)
        rows[lab[i] - 2] = (lab[par[i]], d, u)
    nodes = pick(par)
    parcels = [lab[i] for i in nodes]
    shuf(parcels)
    add(n, rows, parcels)


def rnd_cost(hi):
    return lambda i: (ri(1, hi), ri(1, hi))


def sample(pool, cnt):
    """cnt different elements of pool (own Fisher-Yates, same result on every Python version)"""
    a = list(pool)
    for i in range(cnt):
        j = ri(i, len(a) - 1)
        a[i], a[j] = a[j], a[i]
    return a[:cnt]


def some(cnt):
    return lambda par: sample(range(len(par)), cnt)


def leaves(par):
    has = [False] * len(par)
    for i in range(1, len(par)):
        has[par[i]] = True
    return [i for i in range(len(par)) if not has[i]]


def everybody(par):
    return list(range(len(par)))


# samples
add(6, [(1, 2, 5), (1, 1, 3), (2, 1, 2), (3, 4, 6), (3, 1, 1)], [4, 6])
add(3, [(3, 2, 1), (1, 3, 4)], [3, 2])
add(2, [(1, 5, 5)], [1])
add(5, [(1, 3, 4), (1, 1, 2), (1, 2, 2), (1, 5, 1)], [2, 3, 4, 5])
add(5, [(1, 2, 3), (1, 4, 4), (2, 1, 1), (4, 2, 2)], [4, 1, 2])
# hidden: small (the brute handles K <= 12)
add(8, [(1, 2, 2), (1, 1, 1), (2, 3, 1), (2, 1, 2), (3, 2, 3), (6, 1, 4), (6, 5, 1)], [5, 7, 8])
add(2, [(1, MAXC, MAXC)], [2])
tree(10, "random", rnd_cost(10), some(3))
tree(12, "path", rnd_cost(100), some(2))
tree(30, "random", rnd_cost(MAXC), some(5))
# two chains: the long one is cheap to climb, the short one is expensive
par = shape(200, "twopaths")
tree(200, None, lambda i: (ri(1, 10), ri(1, 10)) if i % 2 == 1 else (ri(1, 10), ri(10**6, MAXC)),
     lambda par: [199, 198, 100, 101, 7, 8], par)
tree(1000, "random", rnd_cost(MAXC), some(10))
tree(2000, "broom", rnd_cost(MAXC), lambda par: leaves(par)[:8])
tree(3000, "cater", rnd_cost(MAXC), some(10))
tree(500, "star", rnd_cost(MAXC), some(10))
tree(1000, "deep", rnd_cost(MAXC), lambda par: [0])                 # only the post office itself
# hidden: medium
tree(20_000, "random", rnd_cost(MAXC), everybody)
tree(50_000, "deep", rnd_cost(MAXC), some(1000))
# hidden: maximum size
N = MAXN
tree(N, "path", rnd_cost(MAXC), everybody)
tree(N, "path", rnd_cost(MAXC), lambda par: sample(range(N // 2, N), N // 2))
tree(N, "deep", rnd_cost(MAXC), everybody)
tree(N, "broom", rnd_cost(MAXC), leaves)
tree(N, "twopaths", lambda i: (ri(1, 1000), ri(1, 1000)) if i % 2 == 1 else (ri(1, 1000), ri(10**8, MAXC)),
     lambda par: sample(range(N // 2, N - 2), 30_000) + [N - 1, N - 2])
tree(N, "cater", rnd_cost(MAXC), everybody)
tree(N, "path", lambda i: (MAXC, MAXC), everybody)
tree(N, "broom", rnd_cost(MAXC), lambda par: list(range(N // 4, N)))
tree(N, "twopaths", rnd_cost(MAXC), everybody)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

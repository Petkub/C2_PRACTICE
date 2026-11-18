# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    h = max(1, 3 * n // 5)
    legs = max(1, int(n ** 0.5) // 2)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "twopaths":
            p = 1 if i <= 3 else i - 2
        elif kind == "spider":
            p = 1 if i <= legs + 1 else i - legs
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        elif kind == "longrandom":
            p = i - 1 if i <= h else ri(1, i - 1)
        elif kind == "sqrtstar":
            p = i - 1 if i <= b else ri(1, b)
        else:
            raise ValueError(kind)
        assert 1 <= p < i
        par.append(p)
    return par


def tree_edges(n, kind):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    return [(lab[i], lab[par[i]]) if rnd() < 0.5 else (lab[par[i]], lab[i]) for i in range(2, n + 1)]


def check_tree(n, edges):
    assert len(edges) == n - 1
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for e in edges:
        u, v = e[0], e[1]
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b
        root[a] = b


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(290502)
MAXN, MAXW, MAXH = 100_000, 10_000, 10 ** 9


def add(n, E, W, h, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 0 <= E <= n - 1 and 1 <= W <= 10 ** 9
    assert len(h) == n and all(1 <= x <= MAXH for x in h)
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {E} {W}\n" + " ".join(map(str, h)) + "\n" + "".join(["%d %d %d\n" % e for e in edges]))


def make(n, kind, E, W, hmode, lo=1, hi=MAXW):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    hs = [0] * (n + 1)
    depth = [0] * (n + 1)
    for i in range(1, n + 1):
        if i > 1:
            depth[i] = depth[par[i]] + 1
        if hmode == "random":
            hs[i] = ri(1, MAXH)
        elif hmode == "few":
            hs[i] = ri(1, 3)
        else:
            hs[i] = min(MAXH, 1 + depth[i] * 1000 + ri(0, 1500))
    h = [0] * n
    for i in range(1, n + 1):
        h[lab[i] - 1] = hs[i]
    edges = [(lab[i], lab[par[i]], lo + int(rnd() * (hi - lo + 1))) for i in range(2, n + 1)]
    add(n, E, W, h, edges, True)


add(5, 1, 10, [5, 3, 8, 6, 1], [(1, 2, 2), (2, 3, 4), (3, 4, 3), (2, 5, 5)])
add(4, 0, 100, [1, 2, 3, 4], [(1, 2, 10), (2, 3, 10), (3, 4, 10)])
add(2, 0, 1, [7, 9], [(1, 2, 2)])
add(6, 2, 12, [4, 9, 2, 7, 5, 1], [(1, 2, 3), (1, 3, 4), (3, 4, 5), (4, 5, 2), (2, 6, 6)])
add(7, 1, 7, [10, 20, 30, 15, 25, 5, 35], [(1, 2, 1), (2, 3, 2), (1, 4, 3), (4, 5, 1), (4, 6, 2), (3, 7, 3)])

add(2, 1, 1, [3, 3], [(1, 2, 1)])
add(3, 0, 5, [2, 2, 2], [(1, 2, 1), (2, 3, 1)])
make(10, "random", 2, 30, "random", 1, 10)
make(60, "caterpillar", 5, 40_000, "few")
make(300, "binary", 3, 15_000, "slope")
make(2000, "chains", 20, 150_000, "random")
make(5000, "path", 1500, 6_000_000, "few", 1, 5000)
make(20_000, "random", 4, 25_000, "slope")

make(MAXN, "path", MAXN - 1, 10 ** 9, "random")
make(MAXN, "path", 30_000, 200_000_000, "few")
make(MAXN, "deep", 40_000, 150_000_000, "slope")
make(MAXN, "twopaths", 15_000, 10 ** 9, "few", 1, 100)
make(MAXN, "spider", 300, 1_500_000, "random")
make(MAXN, "caterpillar", 20_000, 120_000_000, "slope")
make(MAXN, "broom", 5_000, 10 ** 9, "few", 1, 20)
make(MAXN, "longrandom", 30_000, 160_000_000, "random")
make(MAXN, "random", 12, 70_000, "few")
make(MAXN, "star", 1, 12_000, "random")
make(MAXN, "sqrtstar", 200, 1_000_000, "slope")
make(MAXN, "binary", 15, 120_000, "few")
make(MAXN, "chains", 400, 1_500_000, "random")

write_all()

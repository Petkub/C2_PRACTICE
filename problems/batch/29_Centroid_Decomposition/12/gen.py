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

random.seed(291201)
MAXN, MAXW, MAXK = 100_000, 10_000, 10 ** 9


def add(n, K, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 0 <= K <= MAXK
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {K}\n" + "".join(["%d %d %d\n" % e for e in edges]))


def make(n, kind, wlo, whi, frac=None, K=None):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    w = [0, 0] + [ri(wlo, whi) for _ in range(2, n + 1)]
    if K is None:
        depth = [0] * (n + 1)
        for i in range(2, n + 1):
            depth[i] = depth[par[i]] + w[i]
        K = min(MAXK, int(frac * max(depth)))
    edges = [(lab[i], lab[par[i]], w[i]) if rnd() < 0.5 else (lab[par[i]], lab[i], w[i]) for i in range(2, n + 1)]
    add(n, K, edges, True)


add(5, 5, [(1, 2, 2), (2, 3, 3), (3, 4, 4), (2, 5, 1)])
add(4, 100, [(1, 2, 7), (1, 3, 7), (1, 4, 7)])
add(3, 0, [(1, 2, 1), (2, 3, 1)])
add(7, 5, [(1, 2, 3), (2, 3, 1), (2, 4, 1), (3, 5, 5), (2, 6, 2), (5, 7, 9)])
add(7, 6, [(1, 2, 3), (1, 3, 1), (1, 4, 2), (2, 5, 7), (2, 6, 4), (1, 7, 5)])

add(2, 1, [(2, 1, 1)])
make(10, "random", 1, 10, 0.6)
make(40, "caterpillar", 1, 100, 0.5)
make(200, "binary", 1, MAXW, 0.8)
make(500, "path", 1, 20, 0.3)
make(1500, "random", 1, MAXW, 0.9)
make(1500, "star", 1, 100, K=150)

make(MAXN, "path", 1, MAXW, K=MAXK)
make(MAXN, "path", 1, MAXW, 0.4)
make(MAXN, "deep", 1, MAXW, 0.6)
make(MAXN, "twopaths", 1, 100, 0.7)
make(MAXN, "spider", 1, MAXW, 0.8)
make(MAXN, "caterpillar", 1, MAXW, 0.5)
make(MAXN, "broom", 1, 10, 0.9)
make(MAXN, "longrandom", 1, MAXW, 0.5)
make(MAXN, "random", 1, MAXW, 0.7)
make(MAXN, "star", 1, MAXW, K=2 * MAXW)
make(MAXN, "binary", 1, MAXW, 0.9)
make(MAXN, "sqrtstar", 1, MAXW, 0.6)
make(MAXN, "chains", 1, MAXW, 0.4)

write_all()

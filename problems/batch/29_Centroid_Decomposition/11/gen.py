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

random.seed(291001)
MAXN, MAXW, MAXK = 100_000, 10 ** 9, 10 ** 14


def add(n, K, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 0 <= K <= MAXK
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {K}\n" + "".join(["%d %d %d\n" % e for e in edges]))


def make(n, kind, wmode, frac=None, K=None):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    if wmode == "heavy":
        w = [0, 0] + [ri(10 ** 8, MAXW) if rnd() < 0.05 else ri(1, 1000) for _ in range(2, n + 1)]
    else:
        w = [0, 0] + [ri(wmode[0], wmode[1]) for _ in range(2, n + 1)]
    if K is None:
        sm, mx = [0] * (n + 1), [0] * (n + 1)
        for i in range(2, n + 1):
            sm[i] = sm[par[i]] + w[i]
            mx[i] = max(mx[par[i]], w[i])
        cost = sorted(sm[i] - mx[i] for i in range(2, n + 1))
        K = min(MAXK, cost[min(len(cost) - 1, int(frac * len(cost)))])
    edges = [(lab[i], lab[par[i]], w[i]) if rnd() < 0.5 else (lab[par[i]], lab[i], w[i]) for i in range(2, n + 1)]
    add(n, K, edges, True)


add(5, 4, [(1, 2, 4), (2, 3, 8), (3, 4, 5), (2, 5, 1)])
add(5, 6, [(1, 2, 7), (1, 3, 7), (2, 4, 5), (2, 5, 3)])
add(3, 1_000_000_000, [(1, 2, 1_000_000_000), (2, 3, 1_000_000_000)])
add(6, 6, [(1, 2, 9), (2, 3, 3), (2, 4, 2), (4, 5, 3), (1, 6, 7)])
add(6, 9, [(1, 2, 7), (2, 3, 7), (1, 4, 2), (1, 5, 2), (3, 6, 5)])

add(2, 0, [(1, 2, 7)])
make(10, "random", (1, 10), 0.5)
make(50, "caterpillar", (1, 100), 0.3)
make(300, "binary", "heavy", 0.6)
make(2000, "path", (1, 10 ** 6), 0.4)
make(3000, "random", (1, MAXW), 0.7)
make(3000, "star", (1, 1000), K=0)

make(MAXN, "path", (MAXW - 1000, MAXW), K=MAXK)
make(MAXN, "path", (1, MAXW), 0.6)
make(MAXN, "deep", "heavy", 0.7)
make(MAXN, "twopaths", (1, 1000), 0.8)
make(MAXN, "spider", (1, MAXW), 0.9)
make(MAXN, "caterpillar", "heavy", 0.6)
make(MAXN, "broom", (1, 10 ** 6), 0.7)
make(MAXN, "longrandom", (1, MAXW), 0.75)
make(MAXN, "random", (1, MAXW), 0.95)
make(MAXN, "star", (1, MAXW), K=MAXW)
make(MAXN, "binary", "heavy", 0.9)
make(MAXN, "sqrtstar", (1, 1000), 0.9)
make(MAXN, "chains", (1, MAXW), 0.8)

write_all()

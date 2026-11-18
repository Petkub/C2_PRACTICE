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

random.seed(290201)
MAXN, MAXW, MAXK = 100_000, 1_000_000, 1_000_000


def add(n, K, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= K <= MAXK
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {K}\n" + "".join(["%d %d %d\n" % e for e in edges]))


def make(n, kind, wlo, whi, K=None, depth_frac=None):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    w = [0, 0] + [ri(wlo, whi) for _ in range(2, n + 1)]
    if K is None:
        dist = [0] * (n + 1)
        for i in range(2, n + 1):
            dist[i] = dist[par[i]] + w[i]
        cand = sorted(d for d in dist[2:] if d <= MAXK)
        K = cand[min(len(cand) - 1, int(depth_frac * len(cand)))]
    rnd = random.random
    edges = [(lab[i], lab[par[i]], w[i]) if rnd() < 0.5 else (lab[par[i]], lab[i], w[i]) for i in range(2, n + 1)]
    add(n, K, edges, True)


add(7, 10, [(1, 2, 4), (2, 3, 6), (2, 4, 3), (4, 5, 3), (1, 6, 10), (6, 7, 2)])
add(5, 6, [(1, 2, 3), (1, 3, 3), (1, 4, 3), (1, 5, 3)])
add(4, 100, [(1, 2, 30), (2, 3, 30), (3, 4, 30)])
add(6, 5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1)])
add(8, 7, [(1, 2, 7), (2, 3, 3), (3, 4, 4), (2, 5, 2), (5, 6, 2), (6, 7, 3), (1, 8, 3)])

add(2, 5, [(1, 2, 5)])
add(2, 1_000_000, [(2, 1, 999_999)])
make(10, "random", 1, 5, depth_frac=0.5)
make(50, "caterpillar", 1, 3, depth_frac=0.7)
make(300, "binary", 1, 10, depth_frac=0.9)
make(2000, "chains", 1, 100, depth_frac=0.6)
make(5000, "star", 7, 7, K=14)
make(20_000, "random", 1, 1000, depth_frac=0.3)
make(20_000, "path", 1, 2, depth_frac=0.8)

def starlike(n, kind):
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    e = []
    if kind == "two":
        for i in range(2, n + 1):
            e.append((1, i, 1 if random.random() < 0.5 else 3))
        K = 4
    elif kind == "mixed":
        for i in range(2, n + 1):
            x = random.random()
            e.append((1, i, 1 if x < 0.15 else 3 if x < 0.3 else 2))
        K = 4
    elif kind == "double":
        e.append((1, 2, 10))
        for i in range(3, n + 1):
            e.append((1 + (i & 1), i, 5))
        K = 20
    elif kind == "fan":
        for i in range(2, n + 1):
            e.append((1 if i <= 2 or random.random() < 0.72 else ri(2, i - 1), i, 1))
        K = 2
    else:
        h = n // 4
        for i in range(2, n + 1):
            e.append((i - 1 if 2 < i <= h else 1, i, 7 if 2 < i <= h else 100))
        K = 200
    edges = [(lab[a], lab[b], w) if random.random() < 0.5 else (lab[b], lab[a], w) for a, b, w in e]
    shuffle(edges)
    add(n, K, edges, True)


make(MAXN, "star", 500_000, 500_000, K=1_000_000)
starlike(MAXN, "two")
starlike(MAXN, "mixed")
starlike(MAXN, "double")
starlike(MAXN, "tail")
starlike(MAXN, "fan")
make(MAXN, "spider", 2, 2, K=400)
make(MAXN, "path", 1, 10, depth_frac=0.99)
make(MAXN, "path", 1, 1, K=50_000)
make(MAXN, "deep", 1, 8, depth_frac=0.95)
make(MAXN, "twopaths", 1, 6, depth_frac=0.9)
make(MAXN, "broom", 1, 3, depth_frac=0.99)
make(MAXN, "caterpillar", 1, 5, depth_frac=0.9)
make(MAXN, "longrandom", 1, 10, depth_frac=0.9)
make(MAXN, "sqrtstar", 1, 3, depth_frac=0.9)
make(MAXN, "random", 1, 20, depth_frac=0.9)

write_all()

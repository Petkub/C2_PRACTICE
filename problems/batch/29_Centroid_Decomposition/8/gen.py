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

random.seed(290801)
MAXN, MAXQ, MAXW, MAXA, MAXD = 100_000, 50_000, 10_000, 10_000, 10 ** 9


def add(n, a, edges, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(a) == n
    assert all(0 <= x <= MAXA for x in a)
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    for t, v, x in ops:
        assert t in (1, 2) and 1 <= v <= n
        assert 0 <= x <= (MAXA if t == 1 else MAXD)
    assert any(o[0] == 2 for o in ops)
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, a)) + "\n" + "".join(["%d %d %d\n" % e for e in edges])
                 + "".join(["%d %d %d\n" % o for o in ops]))


def make(n, kind, wlo, whi, q, pq=0.5, dfrac=(0.3, 1.0), full=0.1):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    w = [0, 0] + [ri(wlo, whi) for _ in range(2, n + 1)]
    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[par[i]] + w[i]
    D = max(depth)
    a = [0 if rnd() < 0.2 else ri(0, MAXA) for _ in range(n)]
    ops = []
    for _ in range(q):
        if rnd() < pq or not ops:
            d = MAXD if rnd() < full else int(D * (dfrac[0] + rnd() * (dfrac[1] - dfrac[0])))
            ops.append((2, ri(1, n), d))
        else:
            ops.append((1, ri(1, n), ri(0, MAXA)))
    edges = [(lab[i], lab[par[i]], w[i]) if rnd() < 0.5 else (lab[par[i]], lab[i], w[i]) for i in range(2, n + 1)]
    add(n, a, edges, ops, True)


add(5, [4, 0, 2, 7, 1], [(1, 2, 3), (2, 3, 2), (2, 4, 5), (4, 5, 1)],
    [(2, 2, 3), (2, 5, 6), (1, 2, 9), (2, 3, 4)])
add(4, [5, 5, 5, 5], [(1, 2, 10), (1, 3, 20), (1, 4, 30)], [(2, 1, 0), (2, 2, 30), (2, 4, 1000000000)])
add(2, [0, 0], [(1, 2, 10_000)], [(2, 1, 9_999), (1, 2, 10_000), (2, 1, 10_000)])
add(6, [1, 2, 3, 4, 5, 6], [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1)],
    [(2, 3, 1), (2, 6, 2), (2, 1, 5)])
add(6, [3, 0, 1, 0, 2, 0], [(1, 2, 4), (1, 3, 2), (3, 4, 7), (3, 5, 1), (5, 6, 3)],
    [(1, 6, 8), (2, 2, 7), (1, 4, 1), (2, 4, 9)])

make(2, "path", 1, 10, 10)
make(10, "random", 1, 10, 30)
make(50, "caterpillar", 1, 100, 200)
make(300, "binary", 1, MAXW, 500)
make(2000, "deep", 1, MAXW, 2000)
make(5000, "path", MAXW - 10, MAXW, 5000)
make(8000, "random", 1, 100, 8000)

make(MAXN, "path", 1, MAXW, MAXQ, 0.7)
make(MAXN, "path", MAXW, MAXW, MAXQ, 0.6, (0.5, 1.0))
make(MAXN, "deep", 1, MAXW, MAXQ, 0.6)
make(MAXN, "twopaths", 1, MAXW, MAXQ, 0.6)
make(MAXN, "spider", 1, MAXW, MAXQ, 0.5)
make(MAXN, "caterpillar", 1, MAXW, MAXQ, 0.5)
make(MAXN, "broom", 1, MAXW, MAXQ, 0.6)
make(MAXN, "longrandom", 1, MAXW, MAXQ, 0.5)
make(MAXN, "random", 1, MAXW, MAXQ, 0.5, (0.5, 1.0))
make(MAXN, "star", 1, MAXW, MAXQ, 0.5, (0.5, 1.0))
make(MAXN, "binary", 1, MAXW, MAXQ, 0.5, (0.5, 1.0))
make(MAXN, "sqrtstar", 1, MAXW, MAXQ, 0.6)
make(MAXN, "chains", 1, MAXW, MAXQ, 0.5, (0.5, 1.0))

write_all()

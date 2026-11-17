# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
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
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def relabel(par, root_first=False):
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(1, n + 1))
    shuffle(lab)
    if root_first:
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
    rnd = random.random
    edges = [(lab[i - 1], lab[par[i] - 1]) if rnd() < 0.5 else (lab[par[i] - 1], lab[i - 1]) for i in range(2, n + 1)]
    shuffle(edges)
    return edges, lab


def random_ancestors(par, stay):
    n = len(par) - 1
    far = list(range(n + 1))
    rnd = random.random
    for i in range(2, n + 1):
        far[i] = far[par[i]] if par[i] != 1 and rnd() < stay else par[i]
    return far


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

random.seed(230106)
MAXN, MAXQ, MAXW = 100_000, 50_000, 10**6


def add(n, wedges, qs, built=False):
    assert 3 <= n <= MAXN and 1 <= len(qs) <= MAXQ and len(wedges) == n
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in wedges)
    assert len(set((min(u, v), max(u, v)) for u, v, w in wedges)) == n
    if not built:
        root = list(range(n + 1))

        def find(x):
            while root[x] != x:
                root[x] = root[root[x]]
                x = root[x]
            return x
        for u, v, w in wedges:
            root[find(u)] = find(v)
        assert len(set(find(v) for v in range(1, n + 1))) == 1
    assert all(1 <= x <= n and 1 <= y <= n for x, y in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in wedges)
                 + "".join(f"{x} {y}\n" for x, y in qs))


def make(n, kind, q, lo=1, hi=10**4, extra="far", ew=None, qmode="rand"):
    par = shape(n, kind)
    edges, lab = relabel(par)
    rnd = random.random
    span = hi - lo + 1
    wedges = [(u, v, lo + int(rnd() * span)) for u, v in edges]
    have = set((min(u, v), max(u, v)) for u, v in edges)
    while True:
        if extra == "far":
            a, b = lab[int(rnd() * 3)], lab[n - 1 - int(rnd() * 3)]
        else:
            a, b = 1 + int(rnd() * n), 1 + int(rnd() * n)
        if a != b and (min(a, b), max(a, b)) not in have:
            break
    w = ew if ew is not None else lo + int(rnd() * span)
    wedges.insert(int(rnd() * n), (a, b, w))
    m = min(n, 200)
    qs = []
    for _ in range(q):
        if qmode == "far":
            x = lab[int(rnd() * m)] if rnd() < 0.5 else lab[n // 2 + int(rnd() * m) - m // 2]
            y = lab[n - 1 - int(rnd() * m)] if rnd() < 0.7 else lab[n // 2 + int(rnd() * m) - m // 2]
        else:
            x, y = 1 + int(rnd() * n), 1 + int(rnd() * n)
        qs.append((x, y) if rnd() < 0.5 else (y, x))
    add(n, wedges, qs, True)


add(6, [(1, 2, 4), (2, 3, 3), (3, 4, 5), (4, 1, 2), (3, 5, 1), (1, 6, 7)], [(2, 4), (5, 6), (2, 5), (6, 6)])
add(3, [(1, 2, 10), (2, 3, 10), (1, 3, 25)], [(1, 2), (1, 3)])
add(4, [(4, 2, 1000000), (2, 1, 1000000), (1, 3, 1000000), (3, 4, 1000000)], [(4, 1), (2, 3), (1, 1)])
add(7, [(1, 2, 5), (2, 3, 2), (3, 4, 9), (4, 5, 1), (5, 6, 3), (6, 7, 4), (7, 3, 6)],
    [(1, 5), (4, 7), (2, 6), (5, 1)])
add(6, [(3, 6, 2), (6, 1, 8), (1, 5, 1), (5, 2, 3), (2, 6, 4), (4, 1, 7)], [(3, 4), (2, 3), (4, 5), (6, 5)])

make(3, "path", 9, 1, 5)
make(10, "random", 50, 1, 10, "rand")
make(30, "path", 100, 1, 20)
make(50, "caterpillar", 100, 1, 100, "rand", 1)
make(80, "binary", 200, 1, 1000, "rand")
make(2000, "path", 2000, 1, 10**4, "far", 1, "far")
make(3000, "chains", 3000)

make(MAXN, "path", MAXQ, 1, 10**4, "far", 1, "far")
make(MAXN, "path", MAXQ, 1, MAXW, "far", 10**6, "far")
make(MAXN, "path", MAXQ, MAXW, MAXW, "far", None, "far")
make(MAXN, "deep", MAXQ, 1, MAXW, "far", 5, "far")
make(MAXN, "twopaths", MAXQ, 1, MAXW, "far", None, "far")
make(MAXN, "caterpillar", MAXQ, 1, MAXW, "far", 1, "far")
make(MAXN, "broom", MAXQ, 1, MAXW, "rand")
make(MAXN, "path", MAXQ, 1, MAXW, "rand")
make(MAXN, "chains", MAXQ, 1, 10**4, "rand", 1)
make(MAXN, "twopaths", MAXQ, MAXW // 2, MAXW, "rand")

make(20_000, "random", 20_000, 1, MAXW, "rand")
make(20_000, "star", 20_000, 1, 10**4, "rand")

write_all()

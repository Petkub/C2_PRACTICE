# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    global LONG, SPINE
    LONG, SPINE = n * 85 // 100, n * 3 // 4
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
        elif kind == "lopsided":
            p = 1 if i == LONG + 2 else i - 1
        elif kind == "comb":
            p = i - 1 if i <= SPINE or (i - 1 > SPINE and random.random() < 0.6) else ri(1, n // 10)
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

random.seed(230104)
MAXN, MAXQ = 100_000, 100_000


def add(n, edges, qs, tree_ok=False):
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
                 + "".join(f"{u} {v}\n" for u, v in qs))


def make(n, kind, q, far=False, split=False, root=False):
    par = shape(n, kind)
    edges, lab = relabel(par, root_first=root or kind in ("lopsided", "comb"))
    deep = LONG if kind == "lopsided" else SPINE
    rnd = random.random
    m = min(n, 100)
    qs = []
    for _ in range(q):
        if split:
            u = lab[deep - 1 - int(rnd() * 3000)]
            v = lab[deep + int(rnd() * (n - deep))] if split == 1 else lab[n - 1 - int(rnd() * 3000)]
        elif far:
            u = lab[int(rnd() * m)] if rnd() < 0.5 else lab[n // 2 - int(rnd() * m)]
            v = lab[n - 1 - int(rnd() * m)]
        else:
            u, v = 1 + int(rnd() * n), 1 + int(rnd() * n)
            if rnd() < 0.05:
                v = u
        qs.append((u, v) if rnd() < 0.5 else (v, u))
    add(n, edges, qs, True)


def spiky(n, q):
    s = n // 3
    par = [0, 0] + [i - 1 for i in range(2, s + 1)] + [1 + (i - s - 1) % s for i in range(s + 1, n + 1)]
    edges, lab = relabel(par)
    rnd = random.random
    qs = [(lab[int(rnd() * 50)], lab[s - 1 - int(rnd() * 50)]) for _ in range(q)]
    add(n, edges, qs, True)


add(8, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7), (6, 8)], [(4, 6), (7, 7), (8, 3), (5, 4)])
add(6, [(1, 2), (3, 1), (1, 4), (5, 1), (1, 6)], [(2, 3), (4, 4)])
add(1, [], [(1, 1)])
add(6, [(5, 2), (2, 6), (6, 1), (1, 4), (4, 3)], [(5, 3), (2, 4), (3, 3), (1, 6)])
add(9, [(3, 9), (9, 1), (9, 4), (4, 7), (4, 2), (2, 5), (1, 8), (8, 6)], [(5, 6), (7, 3), (9, 9), (2, 4), (6, 8)])

add(2, [(1, 2)], [(1, 2), (2, 2), (1, 1)])
make(10, "random", 50)
make(40, "binary", 100)
make(60, "caterpillar", 200)
spiky(300, 300)
make(3000, "path", 3000, far=True)
make(4000, "chains", 4000)

make(MAXN, "path", MAXQ, far=True, root=True)
make(MAXN, "caterpillar", MAXQ, far=True)
spiky(MAXN, MAXQ)
make(MAXN, "deep", MAXQ, far=True)
make(MAXN, "twopaths", MAXQ, far=True)
make(MAXN, "broom", MAXQ, far=True)
make(MAXN, "lopsided", MAXQ, split=2)
make(MAXN, "lopsided", MAXQ, split=1)
make(MAXN, "comb", MAXQ, split=1)
make(MAXN, "lopsided", MAXQ)
make(MAXN, "comb", MAXQ)
make(MAXN, "lopsided", MAXQ, split=2)

make(20_000, "chains", 20_000)
make(20_000, "random", 20_000)
make(20_000, "star", 20_000)

write_all()

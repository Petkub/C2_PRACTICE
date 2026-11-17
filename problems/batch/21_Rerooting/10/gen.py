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
        elif kind == "spider":
            p = 1 if i <= b + 1 else i - b
        elif kind == "bushy":
            p = 1 if i <= b + 1 else ri(2, b + 1)
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


def write_tests():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(2110)
MAXN, MAXA = 100_000, 10**8


def add(n, a, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(a) == n and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, mode="signed", lo=-MAXA, hi=MAXA, root_first=False):
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        if mode == "signed":
            x = ri(lo, hi)
        elif mode == "positive":
            x = ri(1, hi)
        elif mode == "pairs":
            x = ri(1, hi) if i % 2 else -ri(1, hi)
        elif mode == "sided":
            x = ri(0, hi) if i <= n // 2 else -ri(0, hi)
        else:
            raise ValueError(mode)
        a[lab[i - 1]] = x
    add(n, a[1:], edges, True)


def make_plant(n, kind, lim, tgt, pairs):
    par = shape(n, kind)
    sz = [1] * (n + 1)
    for i in range(n, 1, -1):
        sz[par[i]] += sz[i]
    a = [0] + [ri(1, lim) if tgt is None else ri(-lim, lim) for _ in range(n)]
    cand = [i for i in range(2, n + 1) if n // 6 <= sz[i] <= n // 3] or list(range(2, n + 1))
    B = MAXA - 3 * lim
    used = []
    for k in range(pairs):
        c = cand[ri(0, len(cand) - 1)]
        while c in used or par[c] in used:
            c = ri(2, n)
        used += [c, par[c]]
        a[c] += B >> k
        a[par[c]] -= B >> k
    need = 0 if tgt is None else tgt - sum(a)
    while need:
        j = ri(1, n)
        d = max(-lim, min(lim, need))
        if abs(a[j] + d) <= MAXA:
            a[j] += d
            need -= d
    edges, lab = relabel(par)
    b = [0] * (n + 1)
    for i in range(1, n + 1):
        b[lab[i - 1]] = a[i]
    assert tgt is None or sum(b) == tgt
    add(n, b[1:], edges, True)


add(6, [1, -1, -4, 3, -5, 1], [(1, 2), (2, 3), (3, 4), (3, 5), (1, 6)])
add(4, [5, -1, -1, -5], [(1, 2), (2, 3), (3, 4)])
add(1, [-7], [])
add(4, [3, -1, -1, 3], [(1, 2), (2, 3), (3, 4)])
add(7, [3, -5, -2, -1, -2, 3, 2], [(1, 2), (2, 4), (3, 4), (3, 5), (3, 7), (4, 6)])


add(2, [MAXA, -MAXA], [(1, 2)])
add(7, [-2, 6, -3, 4, -6, 1, 2], [(1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (6, 7)])
add(9, [2, -4, 2, -4, 2, 2, -6, 1, 6], [(1, 5), (2, 4), (2, 7), (2, 8), (3, 4), (5, 7), (6, 7), (7, 9)])
add(12, [-2, 2, 5, 1, -5, -4, 2, -2, -2, 6, 2, 1],
    [(1, 12), (2, 3), (2, 7), (2, 8), (2, 9), (4, 6), (5, 6), (5, 12), (6, 8), (6, 11), (10, 11)])
add(13, [-73, -91, 31, -35, -39, 89, 80, 0, -35, 7, 52, 25, -25], [(min(9, v), max(9, v)) for v in range(1, 14) if v != 9])
make(300, "broom", "positive")
make_plant(300, "caterpillar", 1000, None, 1)
make(2000, "path", "positive", root_first=True)
make_plant(5000, "chains", 3, 2, 1)
make_plant(8000, "spider", 50, 3, 1)

N = MAXN
make(N, "path", "sided", hi=MAXA)
make(N, "path", "signed", -2, 2)
make(N, "deep", "signed")
make(N, "caterpillar", "pairs")
make(N, "random", "signed")

make_plant(N, "path", 1000, None, 1)
make_plant(N, "caterpillar", 1000, None, 1)
make_plant(N, "chains", 1000, None, 1)
make_plant(N, "deep", 5, -1, 2)
make_plant(N, "broom", 1000, 2, 1)
make_plant(N, "twopaths", 100, None, 1)
make_plant(N, "bushy", 5, 1, 1)
make_plant(N, "random", 1000, 5, 2)
make_plant(N, "spider", 1000, None, 1)

make(N, "binary", "pairs", root_first=True)
write_tests()

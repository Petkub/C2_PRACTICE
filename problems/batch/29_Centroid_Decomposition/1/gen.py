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

random.seed(290401)
MAXN, MAXQ = 100_000, 100_000


def add(n, edges, qs, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)
    tests.append(f"{n} {len(qs)}\n" + "".join(["%d %d\n" % e for e in edges]) + "".join(["%d %d\n" % x for x in qs]))


def make(n, kind, q, far=True):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    edges = [(lab[i], lab[par[i]]) if rnd() < 0.5 else (lab[par[i]], lab[i]) for i in range(2, n + 1)]
    qs = []
    for _ in range(q):
        if rnd() < 0.01:
            x = ri(1, n)
            qs.append((lab[x], lab[x]))
        elif far:
            qs.append((lab[ri(1, max(1, n // 10))], lab[ri(n // 2, n)]))
        else:
            qs.append((lab[ri(1, n)], lab[ri(1, n)]))
    add(n, edges, qs, True)


add(2, [(2, 1)], [(1, 2), (2, 2)])
add(6, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], [(2, 6), (4, 6), (1, 4), (5, 5)])
add(7, [(1, 4), (2, 4), (3, 4), (4, 5), (5, 6), (5, 7)], [(1, 2), (6, 7), (1, 6)])
add(5, [(1, 2), (2, 3), (3, 4), (3, 5)], [(1, 5), (4, 5)])
add(5, [(5, 1), (5, 2), (2, 3), (3, 4)], [(1, 4), (3, 4)])

make(3, "path", 9, False)
make(4, "star", 16, False)
make(10, "random", 50, False)
make(16, "binary", 100, False)
make(64, "path", 200, False)
make(300, "caterpillar", 500, False)
make(2000, "random", 2000, False)
make(5000, "binary", 2000, False)
make(5000, "star", 2000, False)

make(MAXN, "path", MAXQ)
make(MAXN, "path", MAXQ, False)
make(MAXN, "deep", MAXQ)
make(MAXN, "twopaths", MAXQ)
make(MAXN, "broom", MAXQ)
make(MAXN, "caterpillar", MAXQ)
make(MAXN, "twopaths", MAXQ, False)
make(MAXN, "longrandom", MAXQ)
make(MAXN, "deep", MAXQ, False)
make(MAXN - 1, "path", MAXQ)

write_all()

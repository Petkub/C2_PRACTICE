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

random.seed(290701)
MAXN, MAXA = 100_000, 10 ** 9


def add(n, L, a, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= L <= n - 1 and len(a) == n
    assert all(-MAXA <= x <= MAXA for x in a)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {L}\n" + " ".join(map(str, a)) + "\n" + "".join(["%d %d\n" % e for e in edges]))


def make(n, kind, L, pos=0.5, lo=1, hi=MAXA):
    rnd = random.random
    a = [ri(lo, hi) * (1 if rnd() < pos else -1) for _ in range(n)]
    add(n, L, a, tree_edges(n, kind), True)


add(6, 2, [3, -1, 4, 5, -9, 2], [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6)])
add(4, 1, [-5, -2, -7, -1], [(1, 2), (1, 3), (1, 4)])
add(5, 4, [1, 1, 1, 1, 1], [(1, 2), (2, 3), (3, 4), (4, 5)])
add(7, 3, [2, 6, -3, 4, 1, -8, 5], [(1, 2), (1, 3), (3, 4), (4, 5), (2, 6), (6, 7)])
add(6, 1, [10, -20, 10, -20, 10, 30], [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])

add(2, 1, [-10 ** 9, -10 ** 9], [(1, 2)])
make(10, "random", 3)
make(40, "caterpillar", 6, 0.6)
make(200, "binary", 5, 0.7, 1, 1000)
make(1000, "path", 300, 0.55)
make(3000, "random", 8, 0.8)
make(3000, "spider", 50, 0.9)

make(MAXN, "path", MAXN - 1, 1.0, MAXA - 1000, MAXA)
make(MAXN, "path", 50_000, 0.7)
make(MAXN, "deep", 40_000, 0.8)
make(MAXN, "twopaths", 60_000, 0.95)
make(MAXN, "spider", 1_000, 0.9)
make(MAXN, "caterpillar", 30_000, 0.85)
make(MAXN, "broom", 70_000, 0.9)
make(MAXN, "longrandom", 40_000, 0.75)
make(MAXN, "random", 25, 0.9)
make(MAXN, "star", 2, 0.5)
make(MAXN, "binary", 20, 0.9)
make(MAXN, "sqrtstar", 400, 0.95)
make(MAXN, "deep", MAXN - 1, 0.0)

write_all()

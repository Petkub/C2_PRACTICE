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

random.seed(290101)
MAXN = 200_000


def add(n, L, R, s, edges, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= L <= R <= n - 1
    assert len(s) == n and set(s) <= set("AB.")
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n} {L} {R}\n{s}\n" + "".join(["%d %d\n" % e for e in edges]))


def types(n, pa, pb):
    rnd = random.random
    out = []
    for _ in range(n):
        x = rnd()
        out.append("A" if x < pa else "B" if x < pa + pb else ".")
    return "".join(out)


def make(n, kind, L, R, pa=0.4, pb=0.4):
    add(n, L, R, types(n, pa, pb), tree_edges(n, kind), True)


add(7, 2, 3, "AB.BA.B", [(1, 2), (2, 3), (3, 4), (3, 5), (5, 6), (6, 7)])
add(6, 1, 1, "ABABAB", [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)])
add(5, 3, 4, "A...B", [(1, 2), (2, 3), (3, 4), (4, 5)])
add(8, 2, 5, "BA.AB.BA", [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)])
add(6, 4, 5, "AABB..", [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6)])

add(2, 1, 1, "AB", [(2, 1)])
add(3, 2, 2, "BA.", [(1, 3), (3, 2)])
make(10, "random", 1, 9)
make(40, "caterpillar", 3, 10)
make(200, "binary", 4, 9)
make(1000, "chains", 20, 60, 0.3, 0.3)
make(3000, "path", 1000, 2999, 0.5, 0.5)
make(20_000, "random", 3, 8)
make(20_000, "spider", 50, 400)

make(MAXN, "path", 1, MAXN - 1, 0.5, 0.5)
make(MAXN, "path", 50_000, 150_000)
make(MAXN, "deep", 1, MAXN - 1)
make(MAXN, "twopaths", 30_000, 120_000)
make(MAXN, "spider", 100, 1_000)
make(MAXN, "caterpillar", 2, 80_000)
make(MAXN, "broom", 1, MAXN - 1)
make(MAXN, "longrandom", 10, 60_000)
make(MAXN, "random", 5, 30)
make(MAXN, "star", 2, 2, 0.5, 0.5)
make(MAXN, "sqrtstar", 3, 400)
make(MAXN, "binary", 10, 30)

write_all()

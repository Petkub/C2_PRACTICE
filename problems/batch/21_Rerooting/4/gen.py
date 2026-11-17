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

random.seed(2102)
MAXN = 200_000


def add(n, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, root_first=False):
    edges, lab = relabel(shape(n, kind), root_first)
    add(n, edges, True)


add(6, [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6)])
add(4, [(1, 2), (1, 3), (4, 1)])
add(1, [])
add(2, [(2, 1)])
add(9, [(1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (7, 5), (1, 8), (8, 9)])

add(3, [(1, 2), (2, 3)])
make(10, "random")
make(30, "deep")
make(60, "star")
make(300, "caterpillar")
make(1000, "binary")
make(3000, "path", root_first=True)
make(6000, "spider")
make(9000, "broom")

N = MAXN
make(N, "path")
make(N, "path", root_first=True)
make(N, "deep")
make(N, "twopaths", root_first=True)
make(N, "caterpillar")
make(N, "broom")
make(N, "random")
make(N, "star")
make(N, "chains")
make(N, "bushy")
write_tests()

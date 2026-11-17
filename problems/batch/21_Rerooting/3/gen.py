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
        elif kind == "hubrand":
            p = 1 if random.random() < 0.5 else ri(1, i - 1)
        elif kind == "doublestar":
            p = 1 if i == 2 or i % 2 else 2
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

random.seed(2103)
MAXN, MAXH = 100_000, 10**9


def add(n, h, edges, from_shape=False):
    assert 1 <= n <= MAXN and len(h) == n and len(edges) == n - 1
    if not from_shape:
        check_tree(n, edges)
    assert all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def make(n, kind, mode, lo=1, hi=MAXH, root_first=False):
    par = shape(n, kind)
    edges, lab = relabel(par, root_first)
    h = [0] * (n + 1)
    for i in range(1, n + 1):
        if mode == "random":
            x = ri(lo, hi)
        elif mode == "flat":
            x = hi
        elif mode == "few":
            x = ri(lo, lo + 2)
        elif mode == "mountain":
            x = hi if i == 1 else max(lo, h[lab[par[i] - 1]] - ri(0, 1))
        elif mode == "valley":
            x = lo if i == 1 else min(hi, h[lab[par[i] - 1]] + ri(0, 2))
        elif mode == "hublow":
            x = lo if i <= 2 else ri(lo, lo + 2)
        elif mode == "mostlylow":
            x = lo if random.random() < 0.9 else lo + 1
        else:
            raise ValueError(mode)
        h[lab[i - 1]] = x
    add(n, h[1:], edges, True)


add(5, [5, 3, 3, 1, 4], [(1, 2), (2, 3), (3, 4), (1, 5)])
add(4, [2, 2, 1, 2], [(1, 2), (2, 3), (3, 4)])
add(1, [7], [])
add(6, [4, 4, 4, 4, 4, 4], [(1, 2), (1, 3), (3, 4), (3, 5), (5, 6)])
add(7, [6, 2, 6, 3, 8, 1, 6], [(1, 2), (1, 3), (3, 4), (5, 3), (4, 6), (7, 3)])

add(2, [MAXH, 1], [(2, 1)])
make(10, "random", "few", 1, 10)
make(30, "deep", "random", 1, 20)
make(60, "star", "few", 5, 10)
make(300, "caterpillar", "mountain", 1, 100)
make(2000, "twopaths", "few", root_first=True)
make(5000, "chains", "valley")
make(8000, "spider", "few", 1, 10**9)

N = MAXN
make(N, "path", "flat")
make(N, "path", "mountain", root_first=True)
make(N, "deep", "mountain")
make(N, "hubrand", "valley")
make(N, "broom", "mountain")
make(N, "broom", "valley", root_first=True)
make(N, "hubrand", "mountain")
make(N, "random", "mostlylow")
make(N, "binary", "mostlylow", root_first=True)
make(N, "star", "hublow")
make(N, "bushy", "mostlylow")
make(N, "doublestar", "hublow")
write_tests()

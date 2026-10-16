# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100119)
MAXN, MAXA = 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, edges):
    """a[1..n] values (index 0 unused), edges (u, v)"""
    n = len(a) - 1
    assert 2 <= n <= MAXN and len(edges) == n - 1
    assert all(-MAXA <= x <= MAXA for x in a[1:])
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v in edges:
        x, y = find(u), find(v)
        assert x != y
        root[x] = y
    tests.append(f"{n}\n" + " ".join(map(str, a[1:])) + "\n" + "".join(f"{u} {v}\n" for u, v in edges))


def shape(n, kind):
    """parent of point i (2..n) is par[i] < i, in creation order"""
    par = [0, 0]
    for i in range(2, n + 1):
        if kind == "random":
            p = ri(1, i - 1)
        elif kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "deep":
            p = ri(max(1, i - 4), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "cater":
            p = i - 1 if i <= n // 2 else ri(1, n // 2)
        elif kind == "spider":                     # a few long legs from point 1
            p = 1 if i <= 6 else i - 5
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def build(n, kind, val):
    """val(i, n) gives the value of the i-th created city; labels are shuffled"""
    par = shape(n, kind)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[lab[i]] = val(i, n)
    edges = []
    for i in range(2, n + 1):
        u, v = lab[i], lab[par[i]]
        if random.random() < 0.5:
            u, v = v, u
        edges.append((u, v))
    random.shuffle(edges)
    add(a, edges)


def uni(lo, hi):
    return lambda i, n: ri(lo, hi)


def islands(i, n):
    """mostly losses, with a few rich pockets"""
    return ri(MAXA // 2, MAXA) if random.random() < 0.08 else -ri(1, MAXA)


def lean(i, n):
    """small losses and gains, sums stay close to zero"""
    return ri(-1000, 900)


# samples
add([0, 3, -2, -1, 4, 5], [(1, 2), (1, 3), (3, 4), (3, 5)])
add([0, -5, -3, -8, -1], [(1, 2), (2, 3), (2, 4)])
add([0, 7, 7], [(1, 2)])
add([0, 2, -4, 6, -1, 3, 5, -7], [(2, 1), (3, 2), (4, 2), (4, 5), (6, 3), (7, 6)])
add([0, 1000000000, 1000000000, 1000000000, -1000000000], [(1, 2), (2, 3), (3, 4)])
# hidden: small
add([0, -1, 1], [(2, 1)])
build(8, "random", uni(-9, 9))
build(12, "star", uni(-20, 10))
build(40, "path", lean)
build(300, "random", islands)
build(1000, "cater", uni(-MAXA, MAXA))
build(2000, "deep", lean)
build(3000, "spider", islands)
build(3000, "binary", uni(-MAXA, -1))
# hidden: maximum size
N = MAXN
build(N, "path", uni(MAXA, MAXA))                      # the largest sums
build(N, "path", lean)
build(N, "random", uni(-MAXA, MAXA))
build(N, "star", uni(-MAXA, MAXA))
build(N, "star", lambda i, n: MAXA if i == 1 else -ri(1, MAXA))   # closing the centre leaves only losses
build(N, "deep", islands)
build(N, "binary", lean)
build(N, "spider", uni(-MAXA, MAXA))
build(N, "random", uni(-MAXA, -1))                     # every value negative
build(N, "deep", lambda i, n: MAXA if i % 1000 == 0 else ri(-MAXA, MAXA // 10))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

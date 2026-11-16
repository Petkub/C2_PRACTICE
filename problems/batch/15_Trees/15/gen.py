# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100115)
MAXN, MAXW = 100_000, 10_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


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
        elif kind == "deep":                       # long random branches
            p = ri(max(1, i - 4), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "cater":                      # spine 1..n/2, the rest are legs
            p = i - 1 if i <= n // 2 else ri(1, n // 2)
        elif kind == "broom":                      # a long handle, then a star
            p = i - 1 if i <= n // 2 else n // 2
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def add(n, kinds, edges):
    """kinds: string over H S .; edges: (u, v, w) with labels 1..n"""
    assert 1 <= n <= MAXN and len(kinds) == n and set(kinds) <= set("HS.")
    assert len(edges) == n - 1
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in edges)
    root = list(range(n + 1))                      # it really is a tree (union-find)

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v, w in edges:
        a, b = find(u), find(v)
        assert a != b
        root[a] = b
    tests.append(f"{n}\n{kinds}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def build(n, kind, kinds_of, wgen):
    """kinds_of(i) gives the letter of the i-th created point; labels are shuffled afterwards"""
    par = shape(n, kind)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    letters = [""] * (n + 1)
    for i in range(1, n + 1):
        letters[lab[i]] = kinds_of(i)
    edges = []
    for i in range(2, n + 1):
        u, v = lab[i], lab[par[i]]
        if random.random() < 0.5:
            u, v = v, u
        edges.append((u, v, wgen()))
    random.shuffle(edges)
    add(n, "".join(letters[1:]), edges)


def mix(ph, ps):
    def f(i):
        r = random.random()
        return "H" if r < ph else ("S" if r < ph + ps else ".")
    return f


# samples
add(4, "HS.H", [(1, 2, 3), (2, 3, 2), (3, 4, 5)])
add(5, ".HHSS", [(1, 2, 1), (1, 3, 2), (1, 4, 3), (1, 5, 4)])
add(3, "HH.", [(1, 2, 7), (3, 2, 1)])
add(7, "SH.HSHS", [(1, 2, 4), (2, 3, 1), (2, 4, 6), (1, 5, 2), (5, 6, 3), (5, 7, 8)])
add(6, "HHHSSS", [(1, 2, 10000), (2, 3, 10000), (3, 4, 10000), (4, 5, 10000), (5, 6, 10000)])
# hidden: small
add(1, "H", [])
add(2, "SH", [(2, 1, 9999)])
add(2, "SS", [(1, 2, 5)])
build(10, "random", mix(0.4, 0.4), lambda: ri(1, 10))
build(60, "path", mix(0.3, 0.3), lambda: ri(1, 100))
build(300, "random", mix(0.3, 0.5), lambda: ri(1, MAXW))
build(2000, "cater", mix(0.5, 0.5), lambda: ri(1, MAXW))
build(3000, "deep", mix(0.2, 0.2), lambda: ri(1, 50))
build(5000, "star", mix(0.5, 0.4), lambda: ri(1, MAXW))
# hidden: maximum size
N = MAXN
build(N, "path", lambda i: "H" if i <= N // 2 else "S", lambda: MAXW)      # the largest answer
build(N, "path", lambda i: "HS"[i % 2], lambda: ri(1, MAXW))
build(N, "random", mix(0.5, 0.5), lambda: ri(1, MAXW))
build(N, "star", mix(0.5, 0.5), lambda: MAXW)
build(N, "cater", mix(0.45, 0.45), lambda: ri(1, MAXW))
build(N, "broom", lambda i: "H" if i <= N // 2 else "S", lambda: MAXW)
build(N, "binary", mix(0.5, 0.5), lambda: ri(1, MAXW))
build(N, "random", lambda i: "S" if i == 1 else "H", lambda: ri(1, MAXW))  # one shop, everybody else a house
build(N, "deep", lambda i: "H", lambda: MAXW)                              # no shop at all
build(N, "cater", lambda i: "H" if i <= N // 2 else "S", lambda: MAXW)    # houses on the spine, shops on legs

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

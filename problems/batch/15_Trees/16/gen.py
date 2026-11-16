# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100116)
MAXN, MAXQ, MAXW = 80_000, 80_000, 10**6
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
        elif kind == "spider":                     # a few long legs from point 1
            p = 1 if i <= 4 else i - 3
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def add(n, edges, qs):
    q = len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(edges) == n - 1
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in edges)
    assert all(1 <= x <= n for t in qs for x in t)
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v, w in edges:
        a, b = find(u), find(v)
        assert a != b
        root[a] = b
    tests.append(f"{n} {q}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
                 + "".join(f"{a} {b} {c}\n" for a, b, c in qs))


def build(n, kind, wgen, q, qgen):
    """qgen(lab, n) returns one query (labels already shuffled)"""
    par = shape(n, kind)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    edges = []
    for i in range(2, n + 1):
        u, v = lab[i], lab[par[i]]
        if random.random() < 0.5:
            u, v = v, u
        edges.append((u, v, wgen()))
    random.shuffle(edges)
    add(n, edges, [qgen(lab, n) for _ in range(q)])


def anyq(lab, n):
    return (ri(1, n), ri(1, n), ri(1, n))


def tail(frac):
    """three points created late (deep in path-like shapes)"""
    def g(lab, n):
        lo = max(1, int(n * (1 - frac)))
        return (lab[ri(lo, n)], lab[ri(lo, n)], lab[ri(lo, n)])
    return g


def repeat(lab, n):
    a, b = ri(1, n), ri(1, n)
    return random.choice([(a, a, a), (a, a, b), (a, b, a), (b, a, a), (a, b, b)])


def mixq(lab, n):
    r = random.random()
    if r < 0.1:
        return repeat(lab, n)
    if r < 0.5:
        return tail(0.3)(lab, n)
    return anyq(lab, n)


# samples
add(7, [(1, 2, 2), (2, 3, 1), (2, 4, 5), (1, 5, 3), (5, 6, 4), (5, 7, 2)],
    [(3, 4, 6), (6, 7, 1), (3, 3, 4)])
add(4, [(1, 2, 10), (2, 3, 20), (3, 4, 30)], [(1, 4, 2), (4, 4, 4), (1, 3, 4)])
add(1, [], [(1, 1, 1)])
add(4, [(4, 1, 7), (4, 2, 1), (4, 3, 8)], [(1, 2, 3), (2, 2, 1)])
add(3, [(1, 2, 1000000), (2, 3, 1000000)], [(1, 3, 3), (3, 1, 1)])
# hidden: small
add(2, [(1, 2, 3)], [(1, 1, 2), (2, 2, 1), (1, 2, 2), (2, 1, 1), (1, 1, 1), (2, 2, 2)])
build(10, "random", lambda: ri(1, 10), 50, mixq)
build(40, "path", lambda: ri(1, 100), 100, mixq)
build(300, "random", lambda: ri(1, MAXW), 300, mixq)
build(1000, "cater", lambda: ri(1, MAXW), 1000, mixq)
build(2000, "spider", lambda: ri(1, 20), 1000, mixq)
build(3000, "binary", lambda: ri(1, MAXW), 2000, mixq)
# hidden: maximum size
N, Q = MAXN, MAXQ
build(N, "path", lambda: MAXW, Q, anyq)                 # the largest totals
build(N, "path", lambda: ri(1, MAXW), Q, mixq)
build(N, "random", lambda: ri(1, MAXW), Q, anyq)
build(N, "random", lambda: ri(1, MAXW), Q, repeat)
build(N, "star", lambda: ri(1, MAXW), Q, anyq)
build(N, "cater", lambda: ri(1, MAXW), Q, mixq)
build(N, "deep", lambda: ri(1, MAXW), Q, tail(0.5))
build(N, "deep", lambda: MAXW, Q, mixq)
build(N, "binary", lambda: ri(1, MAXW), Q, anyq)
build(N, "spider", lambda: ri(1, MAXW), Q, tail(0.2))
build(N, "spider", lambda: ri(1, MAXW), Q, anyq)
build(N, "cater", lambda: MAXW, Q, tail(0.6))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

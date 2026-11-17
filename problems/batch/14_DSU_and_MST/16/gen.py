# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90115)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, qs, shuffle=True):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ and len(edges) == n - 1
    assert all(1 <= w <= MAXW for _, _, w in edges) and all(1 <= x <= MAXW for x in qs)
    par = list(range(n + 1))                     # n - 1 roads without a cycle form a tree
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        while par[u] != u:
            par[u] = par[par[u]]
            u = par[u]
        while par[v] != v:
            par[v] = par[par[v]]
            v = par[v]
        assert u != v
        par[u] = v
    if shuffle:                                  # labels are random: sorting mixes the structure
        edges = sorted(edges)
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
                 + " ".join(map(str, qs)) + "\n")


def shape(n, kind):
    """parent of vertex i (2..n) for a tree shape, then random labels"""
    p = [0, 0]
    for i in range(2, n + 1):
        if kind == "path":
            p.append(i - 1)
        elif kind == "star":
            p.append(1)
        elif kind == "cater":                    # a spine with legs
            p.append(i - 1 if i <= n // 2 else ri(1, n // 2))
        elif kind == "binary":
            p.append(i // 2)
        elif kind == "deep":                     # random but deep
            p.append(ri(max(1, i - 5), i - 1))
        else:
            p.append(ri(1, i - 1))
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    return [(lab[i], lab[p[i]]) for i in range(2, n + 1)]


def weigh(pairs, lo, hi):
    r, d = random.random, hi - lo + 1
    return [(u, v, lo + int(r() * d)) for u, v in pairs]


def near(edges, q):
    """abilities equal to a slope or one less"""
    ws = [w for _, _, w in edges]
    m = len(ws)
    return [max(1, ws[int(random.random() * m)] - (random.random() < 0.5)) for _ in range(q)]


# samples
add(5, [(1, 2, 3), (2, 3, 1), (2, 4, 5), (4, 5, 2)], [1, 2, 3, 5, 4], False)
add(2, [(1, 2, 7)], [6, 7], False)
add(4, [(1, 2, 2), (2, 3, 2), (3, 4, 2)], [1, 2, 1000000], False)
add(6, [(3, 1, 4), (3, 6, 8), (2, 6, 3), (5, 3, 6), (4, 2, 1)], [5, 8, 3, 6, 1, 4], False)
add(3, [(1, 3, 1000000), (2, 3, 999999)], [999999, 1000000, 999998], False)
# hidden: small
add(2, [(2, 1, 1)], [1, 1000000, 1])
for n, kind in ((7, "rnd"), (10, "path"), (12, "star"), (30, "cater"), (60, "rnd"), (200, "deep")):
    e = weigh(shape(n, kind), 1, 3 * n)
    add(n, e, near(e, 2 * n) + [ri(1, 3 * n) for _ in range(n)])
e = weigh(shape(300, "rnd"), 1, 5)                                  # many equal slopes
add(300, e, [ri(1, 6) for _ in range(300)])
e = weigh(shape(1500, "binary"), 1, MAXW)
add(1500, e, near(e, 1500))
# hidden: maximum size
N, Q = MAXN, MAXQ
for kind in ("rnd", "path", "star", "cater", "binary", "deep"):
    e = weigh(shape(N, kind), 1, MAXW)
    big = sorted(w for _, _, w in e)[N // 2:]
    add(N, e, [max(1, big[int(random.random() * len(big))] - (random.random() < 0.5)) for _ in range(Q)])   # mostly large abilities
e = weigh(shape(N, "rnd"), MAXW, MAXW)                              # every pair: 4999950000
add(N, e, [MAXW] * (Q - 1) + [MAXW - 1])
e = weigh(shape(N, "path"), 1, 100)
add(N, e, [ri(90, 100) for _ in range(Q)])
pairs = shape(N, "path")                                            # slopes rise along the path
e = [(u, v, MAXW - N + i) for i, (u, v) in enumerate(pairs)]
add(N, e, [MAXW - ri(0, 3000) for _ in range(Q)])
e = weigh(shape(N, "rnd"), 1, MAXW)
add(N, e, sorted(near(e, Q), reverse=True))
e = weigh(shape(N, "star"), 1, 10)
add(N, e, [ri(1, 10) for _ in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

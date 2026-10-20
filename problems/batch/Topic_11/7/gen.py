# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90707)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, req):
    m, k = len(edges), len(req)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= m
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= w <= MAXW for u, v, w in edges)
    assert len(set(req)) == k and all(1 <= i <= m for i in req)
    tests.append(f"{n} {m} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges) + " ".join(map(str, req)) + "\n")


def flip(u, v, w):
    return (u, v, w) if random.random() < 0.5 else (v, u, w)


def tree(vs, wlo, whi, shape="random"):
    res = []
    for i in range(1, len(vs)):
        j = i - 1 if shape == "path" else (max(0, i - ri(1, 3)) if shape == "deep" else ri(0, i - 1))
        res.append(flip(vs[i], vs[j], ri(wlo, whi)))
    return res


def labels(n):
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


def build(n, m, k, wlo=1, whi=MAXW, rlo=None, rhi=None, shape="random", cycle=None):
    """a connected graph; k required links taken from a random spanning tree (so they form no cycle),
    optionally with their own cost range; cycle=c adds one extra required link closing a cycle of c tree links"""
    p = labels(n)
    t = tree(p, wlo, whi, shape)
    rest = [(ri(1, n), ri(1, n), ri(wlo, whi)) for _ in range(m - (n - 1))]
    ids = list(range(n - 1))
    random.shuffle(ids)
    chosen = set(ids[:k])
    if rlo is not None:
        t = [(a, b, ri(rlo, rhi)) if i in chosen else (a, b, w) for i, (a, b, w) in enumerate(t)]
    edges = [(e, i in chosen) for i, e in enumerate(t)] + [(e, False) for e in rest]
    if cycle is not None and shape == "path":
        # tree links i..i+cycle-1 of the path, all required, plus the link closing them
        s = ri(0, n - 1 - cycle)
        for i in range(s, s + cycle):
            edges[i] = (edges[i][0], True)
        edges.append(((p[s], p[s + cycle], ri(wlo, whi)), True))
        edges.pop(n - 1)                                        # keep m links
    random.shuffle(edges)
    req = [i + 1 for i, (e, r) in enumerate(edges) if r]
    random.shuffle(req)
    return n, [e for e, r in edges], req


# samples
add(4, [(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 4, 10), (1, 3, 4)], [4])
add(4, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (3, 4, 5)], [1, 2, 3])
add(4, [(1, 2, 4), (2, 3, 1), (3, 4, 2), (4, 1, 3)], [1, 3])
add(4, [(1, 2, 3), (2, 3, 4), (1, 3, 1)], [2])
add(3, [(1, 2, 9), (1, 2, 2), (3, 3, 1), (3, 1, 4)], [1])
# hidden: small
add(1, [(1, 1, 5)], [1])                                        # a self-loop can never be used
add(2, [(1, 2, 7), (1, 2, 3)], [1])
add(2, [(1, 2, 7), (2, 1, 3)], [1, 2])                          # two links between the same pair
add(5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 1, 100), (2, 4, 1)], [5])
add(6, [(1, 2, 5), (2, 3, 5), (3, 1, 5), (4, 5, 1), (5, 6, 1), (6, 4, 1), (3, 4, 9), (1, 6, 2)], [1, 2, 7])
add(*build(8, 14, 3))
add(*build(9, 16, 4, 1, 20))
add(*build(10, 18, 6, 1, 5, 50, 60))
add(*build(12, 20, 1, 1, 9))
add(*build(300, 900, 100, 1, 10**6, 10**5, 10**6))
add(*build(2000, 6000, 500, shape="path", cycle=40))
n, e, r = build(3000, 8000, 1000)
e.append((5, 5, 1))
add(n, e, r + [len(e)])                                         # plus a required self-loop: -1
# hidden: maximum size
N, M = MAXN, MAXM
add(*build(N, M, 30_000))
add(*build(N, M, 30_000, 1, 10**6, MAXW - 10**4, MAXW))         # required links are the expensive ones
add(*build(N, N - 1, N - 1, MAXW, MAXW))                        # every link is required
add(*build(N, M, 1, 1, MAXW, MAXW, MAXW))
add(*build(N, M, 50_000, shape="path", cycle=50_000))            # a long required cycle: -1
add(*build(N, M, 20_000, shape="path", cycle=2))                 # a required cycle of three links: -1
n, e, r = build(N, M - 1, 40_000, 1, 10**6, 10**8, 10**9)
e.append((e[r[0] - 1][1], e[r[0] - 1][0], 1))                   # a cheap copy of a required link
add(n, e, r + [len(e)])                                         # both required: -1
n, e, r = build(N, M - 1, 40_000, 1, 10**6, 10**8, 10**9)
e.append((e[r[0] - 1][1], e[r[0] - 1][0], 1))
add(n, e, r)                                                    # only the expensive copy is required
p = labels(N)
e = [flip(p[0], p[i], i) for i in range(1, N)] + [(p[1], p[2], MAXW)]   # a star, cheap links in turn
add(N, e, [N])
e = [(1, i, i) for i in range(2, N + 1)] + [(2, 3, 1)]
add(N, e, [N])
e = [(i, 1, i) for i in range(2, N + 1)] + [(N, N - 1, 1)]
add(N, e, [1, N])
n, e, r = build(N - 1, M - 1, 10_000)
add(N, e + [(N - 1, N - 1, 1)], r)                              # vertex N has no link: -1

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

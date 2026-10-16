# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90303)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= w <= MAXW for u, v, w in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def flip(u, v, w):
    return (u, v, w) if random.random() < 0.5 else (v, u, w)


def tree(n, wlo, whi, shape="random"):
    """edges of a spanning tree over a random labelling of 1..n"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    res = []
    for i in range(1, n):
        if shape == "path":
            j = i - 1
        elif shape == "deep":
            j = max(0, i - ri(1, 3))
        else:
            j = ri(0, i - 1)
        res.append(flip(p[i], p[j], ri(wlo, whi)))
    return res


def extra(n, m, wlo, whi, loops=0.0):
    res = []
    for _ in range(m):
        u = ri(1, n)
        v = u if random.random() < loops else ri(1, n)
        res.append((u, v, ri(wlo, whi)))
    return res


def mixed(*parts):
    e = [x for p in parts for x in p]
    random.shuffle(e)
    return e


# samples
add(4, [(1, 2, 3), (2, 3, 1), (3, 4, 4), (1, 3, 2), (4, 1, 5)])
add(4, [(1, 2, 5), (2, 1, 3), (3, 3, 1)])
add(1, [(1, 1, 7)])
add(3, [(1, 2, 10), (1, 2, 4), (2, 3, 6), (3, 1, 6)])
add(6, [(1, 2, 8), (2, 3, 2), (3, 1, 3), (4, 5, 2), (5, 6, 9), (6, 4, 4), (3, 4, 7), (2, 5, 5)])
# hidden: small
add(1, [])
add(2, [(1, 2, MAXW), (2, 1, MAXW), (1, 1, 1)])
add(5, [(1, 2, 1), (2, 3, 1), (3, 1, 1), (4, 5, 1)])          # two groups: -1
add(8, mixed(tree(8, 1, 10), extra(8, 6, 1, 10, 0.3)))
add(30, mixed(tree(30, 1, 100), extra(30, 40, 1, 100)))
add(200, mixed(tree(200, 1, MAXW), extra(200, 300, 1, MAXW, 0.1)))
add(1000, mixed(tree(1000, 1, 5), extra(1000, 2000, 1, 5)))   # many equal costs
add(2000, mixed(tree(1999, 1, 1000), extra(1999, 5000, 1, 1000)) + [(2000, 2000, 1)])  # 2000 is alone
add(3000, mixed(tree(3000, 1, MAXW, "path"), extra(3000, 7000, 1, MAXW)))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, mixed(tree(N, 1, MAXW), extra(N, M - N + 1, 1, MAXW)))
add(N, tree(N, MAXW - 1000, MAXW, "path") + [(1, 1, 1)])       # the answer is near 2 * 10^14
add(N, mixed(tree(N, MAXW, MAXW), extra(N, M - N + 1, MAXW, MAXW)))
add(N, mixed(tree(N, 1, 1), extra(N, M - N + 1, 1, 1)))
n = 50_000
add(n, mixed(tree(n, 1, MAXW, "deep"), extra(n, M - n + 1, 1, MAXW, 0.2)))
p = list(range(1, N + 1))
random.shuffle(p)
add(N, mixed([flip(p[0], p[k], k) for k in range(1, N)], [(1, 1, 5)]))   # a star, cheap edges in turn
add(N, [(1, k, k) for k in range(2, N + 1)] + [(1, 1, 1)])
add(N, [(k, 1, k) for k in range(2, N + 1)] + [(1, 2, MAXW)])
add(N, [(k, k + 1, N - k) for k in range(1, N)] + [(N, 1, 1)])  # a path, the far end is cheapest
e = mixed(tree(N - 1, 1, MAXW), extra(N - 1, M - N + 1, 1, MAXW))   # vertex N has no edge: -1
add(N, e)
add(N, mixed(tree(1000, 1, 10**6), extra(1000, M - 999, 1, 10**6)))   # vertices 1001.. have no edge
n = 1000
add(n, mixed(tree(n, 10**6, MAXW), extra(n, M - n + 1, 1, MAXW)))     # dense: many useless edges

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(7008)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n for a, b in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def relabel(order, edges):
    res = [(order[a], order[b]) for a, b in edges]
    random.shuffle(res)
    return res


def random_order(n):
    mid = list(range(2, n))
    random.shuffle(mid)
    return [1] + mid + [n]


def dag(n, m, span):
    edges = [(ri(max(0, i - span), i - 1), i) for i in range(1, n)]
    has_out = [False] * n
    for a, b in edges:
        has_out[a] = True
    edges += [(i, ri(i + 1, min(n - 1, i + span))) for i in range(n - 1) if not has_out[i]]
    assert len(edges) <= m
    while len(edges) < m:
        a = ri(0, n - 2)
        edges.append((a, ri(a + 1, min(n - 1, a + span))))
    return edges


def big_with_extra(n, m, span, mode):
    k = max(1, n // 10)
    core = n - k
    edges = dag(core, m - 3 * k, span)
    for j in range(core, n):
        if mode == "dead":
            edges.append((ri(0, core - 2), j))
        else:
            edges.append((j, ri(1, core - 1)))
        edges.append((j, ri(core, n - 1)))
        edges.append((ri(core, n - 1), j))
    mid = list(range(2, n))
    random.shuffle(mid)
    order = [1] + mid[:core - 2] + [n] + mid[core - 2:]
    return order, edges


add(4, [(1, 2), (1, 3), (2, 4), (3, 4), (2, 3)])
add(4, [(1, 2), (2, 3), (3, 2), (3, 4)])
add(3, [(2, 1), (2, 3)])
add(2, [(1, 1), (1, 2)])
add(5, [(1, 2), (1, 2), (2, 5), (2, 3), (3, 4), (4, 3), (4, 4)])
add(6, [(1, 2), (2, 3), (1, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 5)])

add(2, [(1, 2)])
add(2, [(2, 1)])
add(3, [(1, 3), (3, 1), (2, 2)])
add(3, [(1, 2), (2, 2), (1, 3)])
add(4, [(4, 4), (1, 2), (2, 4), (3, 1), (3, 3)])
for n, m, mode, cyc in ((8, 16, "dead", 0), (10, 25, "source", 0), (12, 30, "dead", 1),
                        (15, 40, "source", 0), (20, 60, "dead", 1), (30, 90, "source", 1)):
    order, edges = big_with_extra(n, m, 3, mode)
    if cyc:
        a = ri(1, n - n // 3 - 3)
        edges.append((a + 2, a))
    add(n, relabel(order, edges))
order = random_order(1500)
add(1500, relabel(order, dag(1500, 3000, 4)))
order = random_order(2000)
add(2000, relabel(order, dag(2000, 5000, 6)))


N = MAXN
H = MAXN // 2
add(H, relabel(random_order(H), dag(H, MAXM, 3)))
add(H - 1, relabel(random_order(H - 1), dag(H - 1, MAXM, 40)))
n = MAXM // 2 + 1
add(n, [(i, i + 1) for i in range(1, n) for _ in range(2)])
add(N, [(i, i + 1) for i in range(1, N)])
w = 500
edges = []
layers = (H - 2) // w
for i in range(w):
    edges.append((0, 1 + i))
for L in range(layers - 1):
    base = 1 + L * w
    for i in range(w):
        edges.append((base + i, base + w + ri(0, w - 1)))
        edges.append((base + ri(0, w - 1), base + w + i))
last = 1 + (layers - 1) * w
n = last + w + 1
for i in range(w):
    edges.append((last + i, n - 1))
add(n, relabel(list(range(1, n + 1)), edges))
s = 316
n = s * s
edges = []
for r in range(s):
    for c in range(s):
        if c + 1 < s:
            edges.append((r * s + c, r * s + c + 1))
        if r + 1 < s:
            edges.append((r * s + c, (r + 1) * s + c))
add(n, relabel(list(range(1, n + 1)), edges))
order, edges = big_with_extra(H, MAXM, 4, "dead")
add(H, relabel(order, edges))
order, edges = big_with_extra(H, MAXM, 4, "source")
add(H, relabel(order, edges))
edges = dag(H, MAXM - 1, 3)
edges.append((H // 2 + 2, H // 2 - 1))
add(H, relabel(random_order(H), edges))
edges = dag(H, MAXM - 1, 3)
edges.append((H // 3, H // 3))
add(H, relabel(random_order(H), edges))
edges = dag(H, MAXM - 1, 3)
edges.append((H - 7, 0))
add(H, relabel(random_order(H), edges))
edges = dag(H, MAXM, 3)
edges = [(a, b) for a, b in edges if b != H - 1]
edges.append((H - 1, H - 2))
add(H, relabel(random_order(H), edges))
edges = dag(H, MAXM - 1, 3)
edges.append((H - 1, H - 6))
add(H, relabel(random_order(H), edges))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

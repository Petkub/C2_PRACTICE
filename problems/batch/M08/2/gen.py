# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4202)
MAXN = MAXQ = 200000
tests = []


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    for o in ops:
        if o[0] == 1:
            assert len(o) == 3 and 1 <= o[1] <= n and 1 <= o[2] <= n
        elif o[0] == 2:
            assert len(o) == 2 and 1 <= o[1] <= n
        else:
            assert o == (3,)
    assert any(o[0] != 1 for o in ops)
    tests.append(f"{n} {q}\n" + "".join(" ".join(map(str, o)) + "\n" for o in ops))


def ask(n):
    return (2, random.randint(1, n)) if random.random() < 0.8 else (3,)


def rand_ops(n, q, p_edge, back=0.0):
    ops = []
    for _ in range(q):
        if random.random() < p_edge:
            u, v = random.randint(1, n), random.randint(1, n)
            if (u > v) != (random.random() < back):
                u, v = v, u
            ops.append((1, u, v))
        else:
            ops.append(ask(n))
    if all(o[0] == 1 for o in ops):
        ops[-1] = (3,)
    return ops


def mix(edges, n, q):
    k = q - len(edges)
    assert k >= 1
    pos = sorted(random.sample(range(q), k))
    ops, e, j = [], iter(edges), 0
    for i in range(q):
        if j < k and pos[j] == i:
            ops.append(ask(n))
            j += 1
        else:
            ops.append((1,) + next(e))
    return ops


add(5, [(3,), (1, 1, 2), (1, 2, 3), (2, 3), (2, 4), (1, 3, 5), (3,)])
add(4, [(1, 1, 3), (1, 3, 4), (2, 4), (2, 2), (3,)])
add(1, [(2, 1), (3,)])
add(3, [(1, 2, 2), (1, 1, 1), (1, 1, 2), (1, 1, 2), (2, 2), (3,)])
add(6, [(1, 1, 2), (1, 4, 5), (1, 2, 6), (2, 5), (2, 6), (3,)])

add(8, [(1, 5, 2), (2, 2), (1, 1, 5), (2, 2), (1, 3, 2), (2, 3), (3,)])
add(5, [(1, 2, 1), (1, 3, 2), (2, 3), (3,), (1, 1, 4), (1, 4, 3), (2, 3), (3,)])
add(6, [(1, 5, 6), (1, 4, 5), (1, 3, 4), (1, 2, 3), (3,), (1, 1, 2), (3,), (2, 6)])
for n, q in ((10, 40), (10, 60), (50, 200)):
    add(n, rand_ops(n, q, 0.6, 0.5))
add(1000, rand_ops(1000, 3000, 0.7, 0.5))
add(2000, rand_ops(2000, 5000, 0.5, 0.3))

N = Q = MAXN

k = 100000
edges = [(i, i + 1) for i in range(k, 0, -1)]
ops = mix(edges[:-1], N, k + 20000) + [(1, 1, 2)] + [ask(N) for _ in range(Q - k - 20001)]
add(N, ops)

n = 50000
edges = [(i, i + 1) for i in range(1, n)]
for _ in range(80000):
    u, v = random.randint(1, n), random.randint(1, n)
    edges.append((max(u, v), min(u, v)))
random.shuffle(edges)
ops = mix(edges, n, len(edges) + 10000)
add(n, ops + [ask(n) for _ in range(Q - len(ops))])

for n, m, back in ((30000, 100000, 0.5), (20000, 120000, 0.3), (40000, 140000, 0.4)):
    edges = [(random.randint(1, n), random.randint(1, n)) for _ in range(m)]
    edges = [(u, v) if (u < v) != (random.random() < back) else (v, u) for u, v in edges]
    add(n, mix(edges, n, Q))

n, edges = 60000, []
groups = [list(range(2 + 2000 * g, 2 + 2000 * (g + 1))) for g in range(29)]
for g in groups:
    for i in range(len(g) - 1, 0, -1):
        edges.append((g[i - 1], g[i]))
        edges.append((g[i], random.choice(g)))
random.shuffle(edges)
edges += [(1, g[0]) for g in groups]
add(n, [(1,) + e for e in edges] + [ask(n) for _ in range(Q - len(edges))])

n = 80000
edges = [(i, i % (n - 1) + 2) for i in range(2, n + 1)]
random.shuffle(edges)
ops = [(1,) + e for e in edges] + [(1, 1, random.randint(2, n))] + [(2, random.randint(1, n)) if i % 3 else (3,) for i in range(Q - n)]
add(n, ops)

n = 70000
edges = [(random.randint(2, i - 1) if i > 2 else 2, i) for i in range(3, n + 1)]
edges += [(x, x) for x in random.sample(range(1, n + 1), 20000)] + random.sample(edges, 20000)
random.shuffle(edges)
ops = mix(edges, n, len(edges) + 10000) + [(1, 1, 2)]
add(n, ops + [ask(n) for _ in range(Q - len(ops))])

n, k = N, 90000
edges = [(random.randint(1, i - 1), i) for i in range(2, k + 1)]
edges += [(random.randint(2, k), random.randint(1, n)) for _ in range(10000)]
random.shuffle(edges)
add(n, mix(edges, n, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

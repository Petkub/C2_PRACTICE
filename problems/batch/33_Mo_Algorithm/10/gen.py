# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(33009)
MAXN, MAXQ = 100_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add_raw(n, c, par, qs):
    q = len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(c) == n and len(par) == n - 1
    assert all(1 <= x <= n for x in c)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in qs)

    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for i, p in enumerate(par, 2):
        assert 1 <= p <= n and p != i
        a, b = find(i), find(p)
        assert a != b
        root[a] = b
    tests.append(f"{n} {q}\n" + " ".join(map(str, c)) + "\n" + " ".join(map(str, par)) + "\n"
                 + "".join(f"{u} {v}\n" for u, v in qs))


def add_tree(n, edges, c, qs_of):
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[lab[a - 1]].append(lab[b - 1])
        adj[lab[b - 1]].append(lab[a - 1])
    par = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[1] = True
    order = [1]
    for v in order:
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                par[w] = v
                order.append(w)
    assert len(order) == n

    qs = [(lab[u - 1], lab[v - 1]) for u, v in qs_of()]
    add_raw(n, c, par[2:], qs)


def path_edges(n):
    return [(i, i + 1) for i in range(1, n)]


def chain_edges(n, k):
    return [(i, i - ri(1, min(k, i - 1))) for i in range(2, n + 1)]


def caterpillar_edges(n, spine):
    e = [(i, i + 1) for i in range(1, spine)]
    e += [(i, ri(1, spine)) for i in range(spine + 1, n + 1)]
    return e


def random_edges(n):
    return [(i, ri(1, i - 1)) for i in range(2, n + 1)]


def colours(n, k):
    k = max(1, min(n, k))
    return [ri(1, k) for _ in range(n)]


def skew(n, share):
    return [1 if random.random() < share else ri(2, n) for _ in range(n)]


def ends_q(n, q, lo_end, hi_end):
    return lambda: [(ri(1, lo_end), ri(n - hi_end + 1, n)) for _ in range(q)]


def any_pairs(n, q):
    return lambda: [(ri(1, n), ri(1, n)) for _ in range(q)]


add_raw(8, [1, 1, 3, 2, 3, 1, 3, 1], [1, 2, 3, 4, 2, 6, 5], [(6, 2), (1, 7), (8, 4)])
add_raw(7, [2, 3, 2, 2, 3, 3, 2], [1, 2, 3, 2, 3, 4], [(7, 1), (6, 3), (2, 7)])
add_raw(2, [2, 2], [1], [(1, 2), (2, 2)])
add_raw(6, [2, 1, 3, 3, 3, 2], [1, 1, 1, 3, 3], [(3, 2), (4, 5), (1, 6)])
add_raw(7, [1, 1, 2, 2, 2, 2, 3], [1, 1, 1, 1, 4, 2], [(6, 3), (4, 6), (6, 6)])

add_tree(9, random_edges(9), colours(9, 2), any_pairs(9, 81))
add_tree(30, path_edges(30), colours(30, 3), any_pairs(30, 300))
add_tree(60, caterpillar_edges(60, 20), colours(60, 4), any_pairs(60, 500))
add_tree(200, chain_edges(200, 3), colours(200, 5), any_pairs(200, 500))
add_tree(500, random_edges(500), colours(500, 3), any_pairs(500, 500))
add_tree(1500, chain_edges(1500, 2), colours(1500, 20), any_pairs(1500, 1000))

N, Q = MAXN, MAXQ
add_tree(N, path_edges(N), [1] * N, ends_q(N, Q, 10000, 10000))
add_tree(N, path_edges(N), skew(N, 0.9), ends_q(N, Q, 8000, 8000))
add_tree(N, path_edges(N), colours(N, N), ends_q(N, Q, 5000, 5000))
add_tree(N, chain_edges(N, 2), colours(N, 3), ends_q(N, Q, 3000, 3000))
add_tree(N, chain_edges(N, 4), colours(N, 300), ends_q(N, Q, 20000, 30000))
add_tree(N, caterpillar_edges(N, 70000), colours(N, 2), lambda: [(ri(1, 30000), ri(40000, 70000)) for _ in range(Q)])
add_tree(N, caterpillar_edges(N, 60000), colours(N, 50),
         lambda: [(ri(1, 20000) if random.random() < 0.5 else ri(60001, N), ri(40000, 60000)) for _ in range(Q)])
add_tree(N, chain_edges(N, 3), colours(N, 1), ends_q(N, Q, 15000, 15000))
add_tree(N, path_edges(N), colours(N, 10), lambda: [(ri(1, N), ri(1, N)) for _ in range(Q)])
add_tree(N, [(i, 1 if i == N // 2 + 1 else i - 1) for i in range(2, N + 1)], skew(N, 0.97),
         lambda: [(ri(N // 2 - 5000, N // 2), ri(N - 5000, N)) for _ in range(Q)])
add_tree(N, path_edges(N), skew(N, 0.99), ends_q(N, Q, 1000, 1000))
add_tree(N, caterpillar_edges(N, 90000), skew(N, 0.95),
         lambda: [(ri(1, 3000), ri(85000, 90000)) if random.random() < 0.7 else (ri(1, N), ri(1, N)) for _ in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

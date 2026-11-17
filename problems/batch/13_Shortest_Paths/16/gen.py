# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131515)
MAXN, MAXM, MAXA, MAXP, LIMIT = 100_000, 150_000, 10**9, 10**12, 10**18
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def before(kind, a, y):
    return y + a if kind == 1 else y + (y + a - 2) // (a - 1)


def add(n, t, p, cities, roads, mix=True):
    roads = list(roads)
    if mix:
        shuffle(roads)
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= t <= n and 1 <= p <= MAXP and len(cities) == n
    for k, a in cities:
        assert (k == 1 and 1 <= a <= MAXA) or (k == 2 and 2 <= a <= MAXA)
    adj = [[] for _ in range(n + 1)]
    for u, v in roads:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        adj[u].append(v)
        adj[v].append(u)
    # every answer is at most the load needed along a BFS tree towards t: check that bound
    ub = [None] * (n + 1)
    ub[t] = p
    queue = [t]
    for v in queue:
        x = before(cities[v - 1][0], cities[v - 1][1], ub[v])
        assert x <= LIMIT
        for u in adj[v]:
            if ub[u] is None:
                ub[u] = x
                queue.append(u)
    tests.append(f"{n} {m} {t} {p}\n" + "".join(f"{k} {a}\n" for k, a in cities)
                 + "".join(f"{u} {v}\n" for u, v in roads))


def city(flat_lo, flat_hi, share_lo, share_hi, share_prob=0.5):
    if random.random() < share_prob:
        return (2, ri(share_lo, share_hi))
    return (1, ri(flat_lo, flat_hi))


def cities(n, *args):
    return [city(*args) for _ in range(n)]


def rnd_connected(n, m):
    e = [(ri(1, v - 1), v) for v in range(2, n + 1)]
    while len(e) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            e.append((u, v))
    return e


def relabel(n, roads, t):
    """random city numbers, the old city 1 becomes t"""
    p = list(range(1, n + 1))
    shuffle(p)
    i = p.index(t)
    p[0], p[i] = p[i], p[0]
    return [(p[u - 1], p[v - 1]) for u, v in roads]


def chain(n, m, span=3):
    e = [(v, v + 1) for v in range(1, n)]
    while len(e) < m:
        u = ri(1, n - 1)
        v = min(n, u + ri(2, span))
        if u != v:
            e.append((u, v))
    return e


def ladder(n, m):
    """two long parallel lines 1..h and h+1..2h joined at both ends and by some rungs"""
    h = n // 2
    e = [(v, v + 1) for v in range(1, h)] + [(h + v, h + v + 1) for v in range(1, h)]
    e += [(1, h + 1), (h, 2 * h)]
    while len(e) < m:
        v = ri(1, h)
        e.append((v, h + v))
    return e


# samples
add(4, 4, 30, [(1, 1), (2, 10), (1, 5), (1, 2)], [(1, 2), (2, 4), (1, 3), (3, 4)], False)
add(4, 4, 1000, [(1, 1), (2, 10), (1, 5), (1, 2)], [(1, 2), (2, 4), (1, 3), (3, 4)], False)
add(3, 1, 50, [(2, 100), (2, 100), (1, 7)], [(1, 2), (2, 3)], False)
add(4, 2, 12, [(1, 4), (1, 3), (2, 50), (1, 1)], [(1, 2), (3, 4)], False)
add(2, 2, 1, [(1, 3), (2, 2)], [(1, 2)], False)
# hidden: small (checked against the brute force)
add(1, 1, MAXP, [(2, 2)], [])
add(3, 2, 7, [(1, MAXA), (2, MAXA), (2, 2)], [(1, 2)])
for n, m, p, fl, sh in ((6, 8, 20, 5, 10), (8, 10, 100, 20, 30), (10, 15, 1000, 50, 40), (15, 20, 50, 3, 5),
                        (20, 30, 10**6, 10**5, 1000), (30, 45, MAXP, MAXA, MAXA), (40, 60, 10**9, 10**6, 100)):
    t = ri(1, n)
    add(n, t, p, cities(n, 1, fl, 2, sh), relabel(n, rnd_connected(n, m), t))
add(50, 1, 500, cities(50, 1, 30, 2, 60), relabel(50, ladder(50, 60), 1))
# hidden: maximum size
N, M = MAXN, MAXM
t = ri(1, N)
add(N, t, MAXP, cities(N, 1, MAXA, 10, MAXA), relabel(N, rnd_connected(N, M), t))
t = ri(1, N)
add(N, t, MAXP - ri(0, 10**6), cities(N, 1, MAXA, 10**7, MAXA, 0.7), relabel(N, rnd_connected(N, M), t))
add(N, 1, MAXP, cities(N, 10**8, MAXA, 10**5, MAXA), relabel(N, chain(N, M), 1))
add(N, 1, 10**9, cities(N, 1, 10**4, 10**5, 10**6, 0.6), relabel(N, chain(N, M), 1))
add(N, 1, 10**6, [(1, ri(1, 3000)) for _ in range(N // 2)] + [(2, ri(10**5, MAXA)) for _ in range(N - N // 2)],
    relabel(N, ladder(N, M), 1))
add(N, 1, MAXP, [(1, ri(10**6, MAXA)) for _ in range(N // 2)] + [(2, ri(10**6, 10**8)) for _ in range(N - N // 2)],
    relabel(N, ladder(N, M), 1))
t = ri(1, N)
add(N, t, ri(1, 100), cities(N, 1, 5, 2, 40, 0.5), relabel(N, rnd_connected(N, M), t))
# a part of the country cannot reach the target
e = rnd_connected(N - 2000, M - 3000) + [(u + N - 2000, v + N - 2000) for u, v in rnd_connected(2000, 3000)]
add(N, 1, MAXP, cities(N, 1, MAXA, 10**3, MAXA), relabel(N, e, 1))
e = [(1, v) for v in range(2, N + 1)] + [(v, v + 1) for v in range(2, M - N + 3)]   # a star around the target
add(N, 1, MAXP, cities(N, 1, MAXA, 2, MAXA), e)
t = ri(1, N)
add(N, t, MAXP, cities(N, MAXA, MAXA, MAXA, MAXA), relabel(N, chain(N, M, 6), t))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

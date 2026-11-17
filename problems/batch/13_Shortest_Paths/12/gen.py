# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(130202)
MAXN, MAXM, MAXW = 50_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, edges, mix=True):
    edges = list(edges)
    if mix:
        shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and n - 1 <= m <= MAXM
    deg = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW
        deg[u] += 1
        deg[v] += 1
        adj[u].append(v)
        adj[v].append(u)
    assert sum(d % 2 for d in deg) <= 6
    seen = [False] * (n + 1)
    seen[1] = True
    stack = [1]
    while stack:
        for u in adj[stack.pop()]:
            if not seen[u]:
                seen[u] = True
                stack.append(u)
    assert all(seen[1:])
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def perm(n):
    p = list(range(1, n + 1))
    shuffle(p)
    return p


def cycle(vs, lo, hi):
    return [(vs[i], vs[(i + 1) % len(vs)], ri(lo, hi)) for i in range(len(vs))]


def closed_walk(n, length, lo, hi):
    """a random closed walk (every vertex on it gets an even number of new roads)"""
    while True:
        vs = [ri(1, n) for _ in range(length)]
        if all(vs[i] != vs[(i + 1) % length] for i in range(length)):
            return cycle(vs, lo, hi)


def path(vs, lo, hi):
    return [(vs[i], vs[i + 1], ri(lo, hi)) for i in range(len(vs) - 1)]


def eulerian(n, m, lo, hi):
    """connected, every degree even: a big cycle through all vertices plus random closed walks"""
    e = cycle(perm(n), lo, hi)
    assert m - len(e) != 1
    while len(e) < m:
        rem = m - len(e)
        L = rem if rem <= 40 else ri(2, 40)
        e += closed_walk(n, L, lo, hi)
    return e


def with_odd(n, m, k, lo, hi, plen=(1, 30)):
    """eulerian base plus k/2 random paths -> at most k odd vertices (k <= 6)"""
    e = []
    for _ in range(k // 2):
        L = min(ri(*plen), n - 1)
        e += path(random.sample(range(1, n + 1), L + 1), lo, hi)
    if m - len(e) - n == 1:
        e.pop()
        e += path(random.sample(range(1, n + 1), 3), lo, hi)
    return eulerian(n, m - len(e), lo, hi) + e


def chain_trap(n, m, k, x, base_lo, base_hi):
    """odd vertices o1..ok joined by light paths o1~o2 (length x), o3~o4, ... and doubled roads of length 1
    between o2-o3, o4-o5 (they stay even); pairing the closest two first is a bad choice"""
    vs = random.sample(range(1, n + 1), k)
    others = [v for v in range(1, n + 1) if v not in vs]
    e = []
    for i in range(0, k, 2):
        a, b = vs[i], vs[i + 1]
        mid = random.sample(others, 2)
        e += [(a, mid[0], x // 3), (mid[0], mid[1], x // 3), (mid[1], b, x - 2 * (x // 3))]
    for i in range(1, k - 1, 2):
        e += [(vs[i], vs[i + 1], 1), (vs[i + 1], vs[i], 1)]
    return eulerian(n, m - len(e), base_lo, base_hi) + e


# samples
add(4, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1), (2, 4, 5)], False)
add(3, [(1, 2, 4), (2, 3, 6), (3, 1, 5), (1, 3, 2), (3, 1, 3)], False)
add(5, [(1, 2, 3), (1, 3, 1), (1, 4, 2), (1, 5, 4)], False)
add(2, [(1, 2, 7)], False)
add(6, [(1, 2, 2), (1, 3, 2), (1, 4, 2), (4, 5, 3), (4, 6, 3)], False)
# hidden: small (checked against the brute force)
add(2, [(2, 1, 1), (1, 2, 1)])
add(3, [(1, 2, MAXW), (2, 3, MAXW)])
add(30, chain_trap(30, 60, 4, 30, 100, 200))
add(40, chain_trap(40, 90, 6, 60, 300, 400))
for n, m, k, hi in ((8, 12, 6, 10), (10, 20, 4, 5), (30, 50, 6, 100), (60, 120, 6, MAXW), (200, 500, 2, 1000),
                    (300, 900, 6, 50)):
    add(n, with_odd(n, m, k, 1, hi))
add(400, chain_trap(400, 1000, 6, 900, 10**4, 10**5))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, chain_trap(N, M, 6, 3000, 10**6, 10**7))
add(N, chain_trap(N, M, 4, 10**6, 10**8, MAXW))
add(N, chain_trap(N, M, 6, 10**8, MAXW, MAXW))
add(N, with_odd(N, M, 6, 1, MAXW))
add(N, with_odd(N, M, 6, MAXW, MAXW, (1000, 5000)))
add(N, with_odd(N, M, 4, 1, 1000))
add(N, with_odd(N, M, 2, MAXW // 2, MAXW))
add(5000, eulerian(5000, 8000, 1, MAXW))                              # no odd intersection
p = perm(N)
e = path(p, MAXW - 1000, MAXW)                                      # a long line with 6 odd intersections
for i in range(0, N - 3, 2):
    if len(e) + 2 > M - 2:
        break
    e += [(p[i], p[i + 2], ri(1, MAXW)), (p[i + 2], p[i], ri(1, MAXW))]
e += [(p[N // 3], p[2 * N // 3], MAXW), (p[N // 4], p[N // 2], MAXW)]
add(N, e)
add(N, chain_trap(N, M, 6, 10**5, 10**7, 10**8))
add(N, chain_trap(N, M, 4, 500, 10**4, 10**5))
add(N, with_odd(N, M, 6, 1, 100, (2000, 10000)))
add(N, with_odd(N, M, 4, MAXW // 2, MAXW, (100, 1000)))
add(N, chain_trap(N, M, 6, 10**7, 10**8, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

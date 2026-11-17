# Test generator of this problem (the judge runs it to rebuild the big tests).
import math, operator, os, random

random.seed(12006)
MAXN = MAXM = 200000
tests = []
rr = random.random


def rnd(n):
    return int(rr() * n)


def rint(a, b):
    return a + int(rr() * (b - a + 1))


def acyclic(n, edges):
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    for a, b in edges:
        adj[a].append(b)
        deg[b] += 1
    q = [v for v in range(1, n + 1) if deg[v] == 0]
    for u in q:
        for v in adj[u]:
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)
    return len(q) == n


def add(n, edges, known_acyclic=False):
    m = len(edges)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    if m:
        xs, ys = [a for a, _ in edges], [b for _, b in edges]
        assert 1 <= min(xs) and max(xs) <= n and 1 <= min(ys) and max(ys) <= n
        assert all(map(operator.ne, xs, ys))
    assert known_acyclic or acyclic(n, edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def finish(n, edges, order="shuffle", relabel=True, tree=False):
    assert tree or all(map(operator.lt, [a for a, _ in edges], [b for _, b in edges]))
    p = list(range(1, n + 1))
    if relabel:
        k = random.randrange(1, n) if n > 1 else 1
        while math.gcd(k, n) != 1:
            k += 1
        c = random.randrange(n)
        p = [(k * x + c) % n + 1 for x in range(n)]
    e = [(p[a], p[b]) for a, b in edges]
    if order == "shuffle":
        k1, k2 = random.randrange(1, 10**6), random.randrange(1, 10**6)
        e.sort(key=lambda t: (t[0] * k1 + t[1] * k2) % 1000003)
    elif order == "reverse":
        e.reverse()
    add(n, e, True)


def fwd(n, m, span):
    e = []
    while len(e) < m:
        a = rnd(n - 1)
        b = a + rint(1, span)
        if b < n:
            e.append((a, b))
    return e


def chain(lo, hi):
    return [(i, i + 1) for i in range(lo, hi - 1)]


def shortcuts(n, m, maxlen):
    e = []
    for _ in range(m):
        a = rnd(n - 1)
        e.append((a, rint(a + 1, min(n - 1, a + maxlen))))
    return e


add(5, [(1, 2), (2, 3), (1, 4), (5, 4)])
add(5, [(2, 1), (4, 3), (3, 5)])
add(3, [])
add(4, [(1, 2), (1, 3), (2, 4), (3, 4)])
add(6, [(2, 1), (2, 3), (4, 3), (4, 5), (6, 5)])
add(8, [(3, 1), (3, 8), (5, 8), (5, 6), (1, 7), (8, 7), (6, 4), (7, 2), (4, 2)])

add(1, [])
add(2, [(2, 1), (2, 1)])
add(4, [(4, 1), (4, 3), (3, 2), (2, 1)])
add(7, [(1, 2), (2, 3), (3, 4), (1, 5), (5, 4), (6, 7), (6, 4)])
for n in (8, 9, 10, 10):
    finish(n, fwd(n, rint(n, 2 * n), 3) + shortcuts(n, 3, n))
finish(10, [(0, 9)] + chain(0, 10))

finish(1000, chain(0, 600) + shortcuts(1000, 1500, 1000) + fwd(1000, 400, 2))
pt = []
for v in range(1, 5000):
    u = rint(max(0, v - 3), v - 1)
    pt.append((u, v) if random.random() < 0.5 else (v, u))
finish(5000, pt, tree=True)

N = MAXN
finish(N, chain(0, N) + shortcuts(N, MAXM - N + 1, N))
finish(N, chain(0, N) + shortcuts(N, MAXM - N + 1, 50), "reverse")
e = chain(0, 100000) + [(0, rint(1, 99999)) for _ in range(30000)]
e = [(0, x) for _, x in e[99999:]] + e[:99999][::-1]
e += fwd(N, MAXM - len(e), 1000)
finish(N, e, "keep", relabel=False)
spine = chain(0, 60000)
for v in range(60000, N):
    u = rnd(v)
    spine.append((u, v) if random.random() < 0.5 else (v, u))
finish(N, spine, tree=True)
L = 20000
e = []
for lv in range(L - 1):
    e.append((lv * 10, (lv + 1) * 10))
    for k in range(6):
        e.append((lv * 10 + rnd(10), (lv + 1) * 10 + rnd(10)))
    if lv + 5 < L:
        e.append((lv * 10 + rnd(10), (lv + rint(2, 5)) * 10 + rnd(10)))
finish(N, e)
finish(N, chain(0, 60000) + fwd(N, MAXM - 59999, 4))
e, pos = [], 0
for ln in [70000, 50000, 30000] + [1000] * 40 + [10] * 1000:
    if pos + ln > N:
        break
    e += chain(pos, pos + ln)
    pos += ln
finish(N, e, "reverse")
e = [(i, i + 2) for i in range(N - 2)]
e = e[:120000]
while len(e) < MAXM:
    a = rnd(N - 30)
    e.append((a, a + 2 * rint(1, 15) - 1))
finish(N, e)
e = chain(50000, N)
for v in range(50000):
    e.append((v, rint(50001, N - 1)))
e += [(e[i][0], e[i][1]) for i in range(MAXM - len(e))]
finish(N, e)
finish(N, chain(0, 80000) + fwd(N, MAXM - 79999, 60))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(131107)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, forced, relabel=True):
    edges = list(edges)
    forced = dict(forced)
    if relabel:
        q = list(range(1, n))
        random.shuffle(q)
        q = [0] + q + [n]
        rr = random.random
        edges = [(q[a], q[b], w) if rr() < 0.5 else (q[b], q[a], w) for a, b, w in edges]
        forced = {q[c]: q[t] for c, t in forced.items()}
        random.shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= w <= MAXW for a, b, w in edges)
    pairs = {a * 200_003 + b if a < b else b * 200_003 + a for a, b, w in edges}
    assert len(pairs) == m
    p = [0] * (n + 1)
    for c, t in forced.items():
        assert 1 <= c < n and 1 <= t <= n and pair_key(c, t) in pairs
        p[c] = t
    assert p[n] == 0
    tests.append(f"{n} {m}\n" + " ".join(map(str, p[1:])) + "\n" + "".join(["%d %d %d\n" % e for e in edges]))


def pair_key(a, b):
    return a * 200_003 + b if a < b else b * 200_003 + a


class Roads:

    def __init__(self):
        self.e = []
        self.seen = set()

    def put(self, a, b, w):
        key = a * 200_003 + b if a < b else b * 200_003 + a
        if a == b or key in self.seen:
            return False
        self.seen.add(key)
        self.e.append((a, b, w))
        return True


def rnd(n, m, wfun, g=None):
    g = g or Roads()
    rr, put = random.random, g.put
    while len(g.e) < m:
        put(1 + int(rr() * n), 1 + int(rr() * n), wfun())
    return g


def chain(n, wfun):
    g = Roads()
    for i in range(1, n):
        g.put(i, i + 1, wfun())
    return g


def band(n, m, width, wfun):
    g = chain(n, wfun)
    while len(g.e) < m:
        a = ri(1, n - 1)
        g.put(a, min(n, a + ri(2, width)), wfun())
    return g


def grid(r, c, wfun):
    g = Roads()
    for i in range(r):
        for j in range(c):
            v = i * c + j + 1
            if j + 1 < c:
                g.put(v, v + 1, wfun())
            if i + 1 < r:
                g.put(v, v + c, wfun())
    return g


def tree(n, window, wfun):
    g = Roads()
    for i in range(2, n + 1):
        g.put(ri(max(1, i - window), i - 1), i, wfun())
    return g


def neighbours(n, g):
    adj = [[] for _ in range(n + 1)]
    for a, b, _ in g.e:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def force_random(n, g, share, pick=None, near=True):
    adj = neighbours(n, g)
    skip = set() if near else set(adj[n])
    f = {}
    for c in range(1, n):
        if adj[c] and c not in skip and random.random() < share:
            f[c] = pick(c, adj[c]) if pick else adj[c][ri(0, len(adj[c]) - 1)]
    return f


def line(n, m, share, width, wfun, bfun):
    g = Roads()
    f = {}
    w = [0] + [wfun() for _ in range(n)]
    c = 2
    while c < n - 1:
        if random.random() < share:
            f[c] = c - 1 if random.random() < 0.5 else c + 1
            g.put(c - 1, c + 1, bfun())
            if f[c] == c + 1:
                w[c] = MAXW if random.random() < 0.5 else w[c]
            c += 2
        else:
            c += 1
    for i in range(1, n):
        g.put(i, i + 1, w[i])
    while len(g.e) < m:
        a = ri(1, n - 2)
        g.put(a, min(n, a + ri(2, width)), bfun())
    return g, f


def highest(c, nb):
    return max(nb)


W1 = lambda: 1
WBIG = lambda: MAXW
wr = lambda lo, hi: (lambda: ri(lo, hi))


add(5, [(1, 2, 2), (2, 5, 10), (2, 3, 1), (3, 5, 3), (1, 4, 4), (4, 5, 9)], {2: 5}, False)
add(5, [(1, 2, 4), (2, 3, 1), (3, 5, 7), (4, 5, 2)], {1: 2, 2: 1}, False)
add(4, [(1, 2, 5), (2, 4, 5), (1, 4, 1), (3, 1, 1)], {1: 2, 2: 4}, False)
add(5, [(1, 5, 8), (1, 2, 3), (2, 5, 4), (3, 4, 6)], {}, False)
add(2, [(1, 2, MAXW)], {1: 2}, False)


add(2, [(2, 1, 1)], {})
add(3, [(1, 2, MAXW), (2, 3, MAXW), (1, 3, MAXW)], {1: 2})
for n, m, share, wf in ((5, 7, 0.5, wr(1, 5)), (7, 12, 0.6, wr(1, 9)), (8, 14, 0.3, W1),
                        (10, 18, 0.5, WBIG), (12, 30, 0.35, wr(1, 20))):
    g = rnd(n, m, wf)
    add(n, g.e, force_random(n, g, share))
g = rnd(60, 150, wr(1, 30))
add(60, g.e, force_random(60, g, 0.3))
g, f = line(400, 900, 0.3, 5, wr(1, 50), wr(10**8, MAXW))
add(400, g.e, f)
g = grid(30, 40, wr(1, 6))
add(1200, g.e, force_random(1200, g, 0.25), False)
g = rnd(3000, 5500, wr(1, MAXW), tree(3000, 40, wr(1, MAXW)))
add(3000, g.e, force_random(3000, g, 0.2))
g, f = line(4000, 7000, 0.35, 4, wr(1, 3), wr(1, 9))
add(4000, g.e, f)


N, M = MAXN, MAXM
FIRST_MAX = len(tests) + 1
g = rnd(80_000, M, wr(1, MAXW), tree(80_000, 80_000, wr(1, MAXW)))
add(80_000, g.e, force_random(80_000, g, 0.1), False)
g = Roads()
for _ in range(4):
    g.put(50_000, ri(1, 49_999), ri(1, MAXW))
g = rnd(50_000, M, wr(1, MAXW), g)
add(50_000, g.e, force_random(50_000, g, 0.3, None, False), False)
g = rnd(40_000, M, wr(1, 10))
add(40_000, g.e, force_random(40_000, g, 0.5, None, False), False)
g = chain(N, WBIG)
g.put(1, N // 2, MAXW)
add(N, g.e, {}, False)
g, f = line(70_000, M, 0.1, 6, wr(1, 1000), wr(10**6, MAXW))
add(70_000, g.e, f, False)
g, f = line(60_000, M, 0.3, 8, wr(1, 5), wr(1, 12))
add(60_000, g.e, f, False)

n, L = 60_000, 20_000
g = Roads()
f = {}
for c in range(n - L, n):
    g.put(c, c + 1, ri(10**8, MAXW))
    f[c] = c + 1
for c in range(1, n - L - 1):
    g.put(c, c + 1, ri(1, 10**6))
while len(g.e) < M:
    k = ri(1, 3)
    if k == 1:
        g.put(ri(1, n - L - 1), ri(n - L, n), ri(1, MAXW))
    elif k == 2:
        a = ri(n - L, n - 2)
        g.put(a, min(n, a + ri(2, 50)), ri(1, 10**6))
    else:
        a = ri(1, n - L - 2)
        g.put(a, min(n - L - 1, a + ri(2, 30)), ri(1, 10**6))
add(n, g.e, f, False)
g = grid(200, 250, wr(1, MAXW))
add(50_000, g.e, force_random(50_000, g, 0.2), False)
g = grid(20, 2500, wr(10**8, MAXW))
add(50_000, g.e, force_random(50_000, g, 0.08), False)
g = rnd(50_000, M, WBIG)
add(50_000, g.e, force_random(50_000, g, 0.5, highest, False), False)
g = tree(60_000, 300, wr(1, MAXW))
while len(g.e) < M:
    a = ri(1, 59_990)
    g.put(a, a + ri(2, 10), ri(1, MAXW))
add(60_000, g.e, force_random(60_000, g, 0.03), False)

n, H = 70_000, 40_000
bid = lambda i: n if i == H else i + 1
g0 = band(H, 45_000, 3, wr(1, 1000))
g = Roads()
for a, b, w in g0.e:
    g.put(bid(a), bid(b), w)
f = {}
g.put(1, 2, ri(1, MAXW))
f[1] = 2
for c in range(H + 1, n):
    g.put(1, c, ri(1, MAXW))
    if len(g.e) < M - (n - 1 - c):
        t = ri(2, H)
        g.put(c, t, ri(1, MAXW))
        k = ri(1, 3)
        if k < 3:
            f[c] = 1 if k == 1 else t
assert len(g.e) == M
add(n, g.e, f, False)

assert len(tests) - FIRST_MAX + 1 >= 0.4 * len(tests)
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

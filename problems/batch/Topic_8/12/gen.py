# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7012)
MAXN, MAXM = 5_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rshuffle(a):
    """Fisher-Yates with random.random() (faster than random.shuffle, still deterministic)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def pick(a):
    return a[int(random.random() * len(a))]


def add(n, edges, shuffle=True):
    m = len(edges)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    assert len(set(a * (n + 1) + b if a < b else b * (n + 1) + a for a, b in edges)) == m
    if shuffle:
        perm = list(range(1, n + 1))
        rshuffle(perm)
        rnd = random.random
        edges = [(perm[a - 1], perm[b - 1]) if rnd() < 0.5 else (perm[b - 1], perm[a - 1])
                 for a, b in edges]
        rshuffle(edges)
    # the graph must be bipartite
    adj = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    col = [-1] * (n + 1)
    for s in range(1, n + 1):
        if col[s] < 0:
            col[s] = 0
            st = [s]
            while st:
                u = st.pop()
                for v in adj[u]:
                    if col[v] < 0:
                        col[v] = 1 - col[u]
                        st.append(v)
                    assert col[v] != col[u]
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


class Builder:
    """collects components; every component is a bipartite graph on new vertices"""

    def __init__(self):
        self.n = 0
        self.edges = []

    def bip(self, p, q, extra=0):
        """connected bipartite component with sides p >= 1 and q (q = 0 only if p = 1):
        a random spanning tree between the sides plus `extra` random cross edges"""
        A = list(range(self.n + 1, self.n + p + 1))
        B = list(range(self.n + p + 1, self.n + p + q + 1))
        self.n += p + q
        if q == 0:
            assert p == 1
            return
        seen = set()
        order = [(0, x) for x in A] + [(1, x) for x in B]
        rshuffle(order)
        # first vertex of each side placed, then attach every other vertex to an earlier one of the other side
        placed = [[A[0]], [B[0]]]
        e = [(A[0], B[0])]
        for side, x in order:
            if x in (A[0], B[0]):
                continue
            y = pick(placed[1 - side])
            e.append((x, y))
            placed[side].append(x)
        for a, b in e:
            seen.add((min(a, b), max(a, b)))
        tries = 0
        while extra > 0 and tries < 10 * extra + 100:
            tries += 1
            a, b = pick(A), pick(B)
            if (min(a, b), max(a, b)) not in seen:
                seen.add((min(a, b), max(a, b)))
                e.append((a, b))
                extra -= 1
        self.edges += e

    def complete(self, p, q):
        A = range(self.n + 1, self.n + p + 1)
        B = range(self.n + p + 1, self.n + p + q + 1)
        self.n += p + q
        self.edges += [(a, b) for a in A for b in B]

    def star(self, leaves):
        self.bip(1, leaves) if leaves else self.bip(1, 0)

    def done(self):
        add(self.n, self.edges)


def build(parts):
    b = Builder()
    for p in parts:
        b.bip(*p)
    b.done()


# samples
add(6, [(1, 2), (2, 3), (4, 5)], False)
add(4, [(1, 3), (1, 4), (2, 3), (2, 4)], False)
add(1, [], False)
add(5, [], False)
add(7, [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7)], False)
add(8, [(1, 2), (1, 3), (1, 4), (5, 6)], False)
# hidden: small (every split tried)
add(2, [(1, 2)])
add(3, [(1, 2)])
build([(4, 1), (4, 1), (3, 1), (3, 1), (3, 1)])                 # differences 3 3 2 2 2 (22 people)
build([(3, 1), (2, 1), (2, 1), (1, 0), (1, 1)])
build([(5, 4, 6), (3, 3, 4), (2, 0 + 1)])
build([(1, 0)] * 6 + [(6, 1), (2, 2, 1)])
build([(ri(1, 3), ri(1, 3)) for _ in range(5)])
build([(7, 1), (1, 1), (1, 1), (1, 1), (2, 1), (1, 0)])
b = Builder()                                                   # a complete bipartite group: 0 new pairs
b.complete(10, 10)
b.done()
# hidden: medium
build([(ri(1, 40), ri(1, 40), ri(0, 20)) for _ in range(60)])
build([(ri(1, 8), ri(0, 1) and ri(1, 3) or 1) for _ in range(800)])
b = Builder()                                                   # few large differences
for _ in range(20):
    d = ri(50, 150)
    q = ri(1, 5)
    b.bip(d + q, q, ri(0, q))
b.done()
# hidden: large
N = MAXN
add(N, [])                                                      # nobody is a rival yet
b = Builder()
b.bip(3000, 2000, MAXM - N + 1)                                 # one group, many pairs
b.done()
b = Builder()                                                   # stars of many sizes
while b.n < N - 40:
    b.star(ri(0, 30))
while b.n < N:
    b.bip(1, 0)
b.done()
b = Builder()                                                   # differences 3 3 2 2 2 repeated an odd number of times
for _ in range(155):
    for p, q in ((5, 2), (5, 2), (4, 2), (4, 2), (4, 2)):
        b.bip(p, q, 1)
b.done()
b = Builder()                                                   # differences 30 30 20 20 20, 37 times
for _ in range(37):
    for d in (30, 30, 20, 20, 20):
        b.bip(d + 1, 1)
b.done()
b = Builder()                                                   # about 25 groups with differences 100..300
while True:
    d = ri(100, 300)
    q = ri(1, 10)
    if b.n + d + 2 * q > N:
        break
    b.bip(d + q, q, ri(0, 3 * q))
b.done()
b = Builder()                                                   # large differences only, no small groups
while True:
    p = ri(20, 200)
    q = ri(1, p // 3)
    if b.n + p + q > N:
        break
    b.bip(p, q, ri(0, p))
b.done()
b = Builder()                                                   # many groups with equal sides plus a few lopsided ones
while b.n < N - 510:
    s = ri(1, 30)
    b.bip(s, s, ri(0, s))
for p in (201, 100, 99, 30, 15):
    b.bip(p, 1)
b.done()
b = Builder()                                                   # random small trees and isolated people
while b.n < N - 20:
    if random.random() < 0.3:
        b.bip(1, 0)
    else:
        b.bip(ri(1, 12), ri(1, 12), ri(0, 3))
b.done()
b = Builder()                                                   # paths and even cycles (differences 0 and 1)
while b.n < N - 200:
    L = ri(2, 200)
    b.bip((L + 1) // 2, L // 2, 0)
b.done()
b = Builder()                                                   # one huge lopsided group and many isolated people
b.bip(3500, 2, 0)
while b.n < N:
    b.bip(1, 0)
b.done()
b = Builder()                                                   # mostly isolated people plus a few big groups
for d in (900, 701, 503, 301):
    b.bip(d + 2, 2, 1)
while b.n < N:
    b.bip(1, 0)
b.done()
b = Builder()                                                   # powers of two differences
for e in range(11):
    b.bip(2 ** e + 1, 1)
while b.n + 100 <= N:
    b.bip(ri(1, 50), ri(1, 50), ri(0, 50))
b.done()
b = Builder()                                                   # big groups with many pairs
while b.n + 600 <= N:
    p = ri(1, 300)
    b.bip(p, ri(1, p), ri(0, p * 30))
b.done()

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

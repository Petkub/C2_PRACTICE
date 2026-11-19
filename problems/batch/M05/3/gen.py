# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45003)
MAXN, MAXE, MAXF = 100_000, 150_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, k, ent, edges):
    e, m = len(edges), len(ent)
    assert 2 <= n <= MAXN and 0 <= e <= MAXE and 1 <= m <= n and 1 <= k <= n
    assert len(set(ent)) == m and all(1 <= x <= n for x in ent)
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 0 <= f <= MAXF for u, v, f in edges)
    tests.append(f"{n} {e} {m} {k}\n" + " ".join(map(str, ent)) + "\n"
                 + "".join(f"{u} {v} {f}\n" for u, v, f in edges))


def shuffled(n, k, ent, edges):
    p = list(range(1, n))
    random.shuffle(p)
    p = [0] + p + [n]
    ent = [p[x] for x in ent]
    random.shuffle(ent)
    edges = [(p[u], p[v], f) for u, v, f in edges]
    random.shuffle(edges)
    add(n, k, ent, edges)


class G:
    def __init__(self):
        self.n = 0
        self.edges = []
        self.ent = []

    def node(self):
        self.n += 1
        return self.n

    def chain(self, start, length, flo, fhi):
        cur = start
        for _ in range(length):
            x = self.node()
            self.edges.append((x, cur, ri(flo, fhi)))
            cur = x
        return cur

    def finish(self, k, extra_dead=0):
        for _ in range(extra_dead):
            self.node()
        n = self.n + 1
        fix = lambda x: n if x == 0 else x
        edges = [(fix(u), fix(v), f) for u, v, f in self.edges]
        shuffled(n, k, [fix(x) for x in self.ent], edges)


def random_body(g, nodes, edges, flo, fhi, back=0.3):
    base = g.n
    ids = [g.node() for _ in range(nodes)]
    order = [0] + ids
    for i in range(1, len(order)):
        g.edges.append((order[i], order[max(0, i - ri(1, 30))], ri(flo, fhi)))
    while len(g.edges) < edges:
        i, j = ri(1, len(order) - 1), ri(0, len(order) - 1)
        if i == j:
            continue
        if j > i and random.random() > back:
            i, j = j, i
        g.edges.append((order[i], order[j], ri(flo, fhi)))
    return ids


def plant_loop(g, k, fee):
    s = g.chain(0, k, 0, 0)
    g.edges.append((s, 0, fee))
    g.ent.append(s)


def plant_tail(g, k, fee):
    s = g.chain(0, k, 0, 0)
    g.edges[-1] = (g.edges[-1][0], g.edges[-1][1], fee)
    g.ent.append(s)


add(6, 2, [2, 4, 5], [(2, 1, 1), (3, 4, 4), (5, 2, 4), (4, 6, 4), (4, 3, 0), (1, 3, 9), (1, 4, 5)])
add(5, 2, [3, 4], [(2, 1, 4), (1, 5, 3), (4, 5, 1), (5, 3, 2), (4, 2, 6)])
add(5, 2, [1, 2, 4, 5], [(2, 1, 0), (3, 2, 3), (4, 5, 3), (1, 3, 2), (3, 4, 6)])
add(6, 3, [1, 3, 5, 6], [(4, 3, 9), (1, 4, 5), (3, 5, 9), (5, 6, 5), (1, 2, 6), (4, 2, 1), (1, 4, 8)])
add(5, 2, [1, 4, 5], [(1, 2, 3), (2, 4, 6), (4, 5, 2), (2, 3, 6), (3, 4, 7), (3, 2, 1), (4, 1, 2)])

add(2, 1, [1], [])
add(2, 1, [1, 2], [(1, 2, MAXF), (2, 1, 0)])
add(3, 3, [1, 2], [(1, 2, 5), (2, 3, 5), (2, 1, 0)])
for nodes, e, k in [(8, 14, 2), (12, 25, 3), (20, 40, 3), (40, 70, 4)]:
    g = G()
    random_body(g, nodes, e, 0, 9)
    g.ent = random.sample(range(1, g.n + 1), max(1, g.n // 3))
    if random.random() < 0.5:
        plant_loop(g, k, 30)
    else:
        plant_tail(g, k, 0)
    g.finish(k, extra_dead=1)
g = G()
random_body(g, 3000, 8000, 0, 1000)
g.ent = random.sample(range(1, g.n + 1), 1000)
plant_loop(g, 6, 10**4)
plant_tail(g, 6, 3)
g.finish(6, extra_dead=50)


def big(nodes, e, k, flo, fhi, nent, loops=0, tails=0, back=0.3):
    g = G()
    random_body(g, nodes, e - loops * (k + 1) - tails * k, flo, fhi, back)
    g.ent = random.sample(range(1, g.n + 1), nent)
    for _ in range(loops):
        plant_loop(g, k, MAXF)
    for _ in range(tails):
        plant_tail(g, k, 0)
    g.finish(k, extra_dead=MAXN - 1 - g.n)


big(MAXN - 200, MAXE, 8, 0, MAXF, 50_000, loops=3)
big(MAXN - 200, MAXE, 10, 0, MAXF, 60_000, tails=2)
big(MAXN - 200, MAXE, 12, 0, 3, 80_000, loops=2, tails=2)
big(MAXN - 200, MAXE, 5, 0, 0, 40_000)
big(MAXN - 200, MAXE, 30, MAXF // 2, MAXF, 99_000)
big(MAXN - 200, MAXE, 9, 0, MAXF, 50_000, loops=4, back=0.6)

g = G()
w, layers = 2, 37_000
prev = [0]
for _ in range(layers):
    cur = [g.node() for _ in range(w)]
    for x in cur:
        for y in prev:
            g.edges.append((x, y, ri(MAXF // 2, MAXF)))
    prev = cur
g.ent = random.sample(range(1, g.n + 1), 30_000)
g.finish(20_000, extra_dead=MAXN - 1 - g.n)

g = G()
s = g.chain(0, MAXN - 1, MAXF - 10, MAXF)
for x in range(1, MAXN):
    if x > 3 and len(g.edges) < MAXE:
        g.edges.append((x, x - ri(2, 3), MAXF))
g.ent = random.sample(range(1, MAXN), 70_000)
g.finish(MAXN // 2)
big(MAXN - 200, MAXE // 2, 7, 0, MAXF, MAXN - 300, loops=2, tails=1)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

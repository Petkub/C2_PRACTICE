# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80190)
MAXN, MAXM, MAXW = 100_000, 120_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads):
    m = len(roads)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    A, B, W = zip(*roads)
    assert 1 <= min(A) and max(A) <= n and 1 <= min(B) and max(B) <= n and all(map(int.__ne__, A, B))
    assert 1 <= min(W) and max(W) <= MAXW
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in roads))


def shuffle(lst):
    """a random order (faster than random.shuffle, still deterministic)"""
    lst.sort(key=lambda _: random.random())


def relabel(n, roads, first, last):
    """junction `first` becomes 1, `last` becomes n, the others get random numbers; roads shuffled"""
    others = [v for v in range(1, n + 1) if v != first and v != last]
    nums = list(range(2, n))
    shuffle(nums)
    mp = [0] * (n + 1)
    mp[first], mp[last] = 1, n
    for v, x in zip(others, nums):
        mp[v] = x
    rnd = random.random
    res = [(mp[a], mp[b], w) if rnd() < 0.5 else (mp[b], mp[a], w) for a, b, w in roads]
    shuffle(res)
    return res


class G:
    def __init__(self):
        self.n = 0
        self.roads = []

    def new(self, k=1):
        self.n += k
        return self.n - k + 1 if k > 1 else self.n

    def road(self, a, b, w):
        self.roads.append((a, b, w))

    def chain(self, a, b, length, inner):
        """a route from a to b of total length `length` through `inner` new junctions"""
        assert length >= inner + 1
        cuts = sorted(random.sample(range(1, length), inner))
        prev, pos = a, 0
        for c in cuts:
            v = self.new()
            self.road(prev, v, c - pos)
            prev, pos = v, c
        self.road(prev, b, length - pos)

    def count_gadget(self, a, p):
        """junction b with exactly p shortest routes from a, all of length 2k + 1 (k = bit length of p)"""
        k = p.bit_length()
        xs = [a]
        for _ in range(k):
            x, y, z = self.new(), self.new(), self.new()
            self.road(xs[-1], x, 1)
            self.road(xs[-1], y, 1)
            self.road(x, z, 1)
            self.road(y, z, 1)
            xs.append(z)
        b = self.new()
        for j in range(k + 1):
            if p >> j & 1:
                self.road(xs[j], b, 2 * (k - j) + 1)
        return b, 2 * k + 1

    def filler(self, attach, cnt, extra, wlo):
        """cnt junctions hanging around (long roads, never on a shortest route)"""
        vs = [self.new() for _ in range(cnt)]
        pool = list(attach)
        rnd, span = random.random, MAXW - wlo + 1
        for v in vs:
            self.roads.append((v, pool[int(rnd() * len(pool))], wlo + int(rnd() * span)))
            pool.append(v)
        for _ in range(extra):
            a, b = vs[int(rnd() * cnt)], pool[int(rnd() * len(pool))]
            if a != b:
                self.roads.append((a, b, wlo + int(rnd() * span)))


def collision(p, big):
    """the routes through one junction v plus p other shortest routes: v is NOT on every shortest route,
    but counting routes modulo p (or with 64-bit overflow when p = 2^64) says it is"""
    g = G()
    s = g.new()
    b, L = g.count_gadget(s, p)
    t = g.new()
    g.road(b, t, 1)
    v = g.new()
    g.road(s, v, ri(1, L))
    g.road(v, t, L + 1 - g.roads[-1][2])
    if big:
        g.filler([s, t, v, b], MAXN - g.n, MAXM - len(g.roads) - (MAXN - g.n), 10**5)
    return g.n, relabel(g.n, g.roads, s, t)


def blobs(n_target, m_target, seg, wmax, p_single=0.3, p_jump=0.2):
    """a chain of cut junctions; between two of them several routes of equal length (sometimes only one),
    sometimes one direct road of the same length, and some longer routes"""
    g = G()
    s = g.new()
    cur = s
    while g.n < n_target - 5 * seg - 2 and len(g.roads) < m_target - 5 * seg - 7:
        nxt = g.new()
        L = ri(seg + 1, seg * wmax)
        routes = 1 if random.random() < p_single else ri(2, 4)
        for _ in range(routes):
            g.chain(cur, nxt, L, ri(0, min(seg, L - 1)))
        if random.random() < p_jump:
            g.road(cur, nxt, L)
        if random.random() < 0.5:
            g.chain(cur, nxt, L + ri(1, 5), ri(0, min(seg, L)))
        cur = nxt
    return g.n, relabel(g.n, g.roads, s, cur)


def rnd_graph(n, m, wmax):
    roads = [(i, ri(1, i - 1), ri(1, wmax)) for i in range(2, n + 1)]
    while len(roads) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            roads.append((a, b, ri(1, wmax)))
    return relabel(n, roads, ri(1, n // 2), ri(n // 2 + 1, n))


def grid(R, C, wmax):
    roads = []
    for r in range(R):
        for c in range(C):
            v = r * C + c + 1
            if c + 1 < C:
                roads.append((v, v + 1, ri(1, wmax)))
            if r + 1 < R:
                roads.append((v, v + C, ri(1, wmax)))
    return R * C, relabel(R * C, roads, 1, R * C)


# samples
add(6, [(1, 2, 2), (2, 3, 2), (1, 4, 1), (4, 3, 3), (3, 5, 1), (5, 6, 4), (3, 6, 6)])
add(3, [(1, 2, 3), (2, 3, 3), (1, 3, 6)])
add(4, [(1, 2, 5), (3, 4, 5)])
add(2, [(2, 1, 7)])
add(7, [(1, 2, 4), (2, 3, 1), (1, 3, 5), (3, 4, 2), (4, 7, 3), (3, 5, 1), (5, 6, 1), (6, 7, 4), (2, 6, 9)])
# hidden: small
add(2, [(1, 2, MAXW), (1, 2, MAXW - 1)])
add(5, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (1, 5, 4)])
for n, m, w in ((6, 8, 2), (9, 14, 3), (12, 20, 2), (30, 50, 3), (200, 350, 4)):
    add(n, rnd_graph(n, m, w))
for p in (10**9 + 7, 998_244_353):
    add(*collision(p, False))
add(*collision(1 << 64, False))
add(*blobs(1500, 3000, 4, 3))
add(*grid(30, 40, 2))
# hidden: largest
N, M = MAXN, MAXM
add(N, relabel(N, [(i, i + 1, ri(1, MAXW)) for i in range(1, N)], 1, N))      # a path: every junction
add(*blobs(N, M, 5, 4))
add(*blobs(N, M, 3, 2, 0.6, 0.4))
add(*blobs(N, M, 8, 50, 0.4, 0.1))
add(*blobs(60_000, 80_000, 2, 3, 0.9, 0.05))
add(*grid(170, 350, 1))                                                      # astronomically many routes
add(*grid(170, 345, 3))
for p in (10**9 + 7, 1 << 64):
    add(*collision(p, True))
add(N, rnd_graph(N, M, 3))
# a long path with direct roads over some stretches (same length): junctions inside them can be avoided
L = N
pos = [0]
for i in range(1, L):
    pos.append(pos[-1] + ri(1, 20))
roads = [(i, i + 1, pos[i] - pos[i - 1]) for i in range(1, L)]
while len(roads) < M:
    a = ri(1, L - 1)
    b = min(L, a + ri(2, 8))
    roads.append((a, b, pos[b - 1] - pos[a - 1] + (0 if random.random() < 0.5 else 1)))
add(N, relabel(N, roads, 1, N))
roads = rnd_graph(N // 2, M // 2, 10)
roads += [(a + N // 2, b + N // 2, w) for a, b, w in rnd_graph(N // 2, M // 2, 10)]
add(N, relabel(N, roads, 1, N))                                              # two separate halves: -1

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

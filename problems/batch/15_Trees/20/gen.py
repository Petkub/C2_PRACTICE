# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100120)
MAXN, MAXQ, MAXW, MAXT = 60_000, 60_000, 10**5, 10**10
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def pick(seq):
    return seq[int(random.random() * len(seq))]


def add(n, edges, qs):
    q = len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(edges) == n - 1
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in edges)
    assert all(1 <= u <= n and 1 <= v <= n and 0 <= t <= MAXT for u, v, t in qs)
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for u, v, w in edges:
        a, b = find(u), find(v)
        assert a != b
        root[a] = b
    tests.append(f"{n} {q}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
                 + "".join(f"{u} {v} {t}\n" for u, v, t in qs))


def shape(n, kind):
    """parent of point i (2..n) is par[i] < i, in creation order"""
    par = [0, 0]
    for i in range(2, n + 1):
        if kind == "random":
            p = ri(1, i - 1)
        elif kind == "path":
            p = i - 1
        elif kind == "twoarms":                    # a path with point 1 in the middle
            p = 1 if i <= 3 else i - 2
        elif kind == "star":
            p = 1
        elif kind == "deep":
            p = ri(max(1, i - 4), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "cater":
            p = i - 1 if i <= n // 2 else ri(1, n // 2)
        elif kind == "spider":
            p = 1 if i <= 6 else i - 5
        else:
            raise ValueError(kind)
        par.append(p)
    return par


class Tree:
    """a tree in creation order (par[i] < i, root 1) with jump tables, to build queries quickly"""

    def __init__(self, n, kind, wgen):
        self.n = n
        self.par = shape(n, kind)
        self.w = [0, 0] + [wgen() for _ in range(n - 1)]
        D = [0] * (n + 1)
        for i in range(2, n + 1):
            D[i] = D[self.par[i]] + self.w[i]
        self.D = D
        p0 = self.par[:]
        p0[1] = 1
        self.jump = [p0]                           # jump[k][x] = 2^k-th ancestor (1 if none)
        for _ in range(16):
            j = self.jump[-1]
            self.jump.append([j[j[x]] for x in range(n + 1)])
        self.kids = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            self.kids[self.par[i]].append(i)

    def ancestor(self, x, k):
        b = 0
        while k:
            if k & 1:
                x = self.jump[b][x]
            k >>= 1
            b += 1
        return x

    def down(self, x, steps):
        for _ in range(steps):
            if not self.kids[x]:
                break
            x = pick(self.kids[x])
        return x


def q_random(T):
    """any two points; t anywhere up to D[u] + D[v] (at least the distance, often more)"""
    u, v = ri(1, T.n), ri(1, T.n)
    hi = T.D[u] + T.D[v]
    r = random.random()
    t = ri(0, hi) if r < 0.85 else (hi + ri(0, 10**6) if r < 0.95 else MAXT)
    return u, v, min(t, MAXT)


def q_line(T):
    """v is an ancestor of u (or the other way round); t hits points exactly or just misses them"""
    u = ri(1, T.n)
    v = T.ancestor(u, ri(0, T.n))
    a = T.ancestor(u, ri(0, T.n))
    if T.D[a] < T.D[v]:
        a = v
    d = T.D[u] - T.D[v]
    if random.random() < 0.5:                      # walking up from u
        t = T.D[u] - T.D[a]
        t = max(0, min(d, t + pick((0, 0, -1, 1))))
        return u, v, t
    t = T.D[a] - T.D[v]                            # walking down from v to u
    t = max(0, min(d + 1, t + pick((0, 0, -1, 1))))
    return v, u, t


def q_fork(T):
    """u and v in different branches below l, t near points on the way, including l itself"""
    l = ri(1, T.n)
    ks = T.kids[l]
    u = T.down(pick(ks), ri(0, 12)) if ks else l
    v = T.down(pick(ks), ri(0, 12)) if len(ks) >= 2 else l
    du, dv = T.D[u] - T.D[l], T.D[v] - T.D[l]
    r = random.random()
    if r < 0.3:
        t = du
    elif r < 0.5:
        a = T.ancestor(u, ri(0, 12))
        t = T.D[u] - T.D[a] if T.D[a] >= T.D[l] else du
    elif r < 0.7:
        b = T.ancestor(v, ri(0, 12))
        t = du + T.D[b] - T.D[l] if T.D[b] >= T.D[l] else du
    else:
        t = ri(0, du + dv)
    t = max(0, t + pick((0, 0, 0, -1, 1)))
    if random.random() < 0.5:
        return v, u, t if t <= du + dv + 1 else 0
    return u, v, t


def q_mix(T):
    r = random.random()
    if r < 0.4:
        return q_random(T)
    if r < 0.7:
        return q_line(T)
    return q_fork(T)


def build(n, kind, wgen, q, qgen):
    T = Tree(n, kind, wgen)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    edges = []
    for i in range(2, n + 1):
        u, v = lab[i], lab[T.par[i]]
        if random.random() < 0.5:
            u, v = v, u
        edges.append((u, v, T.w[i]))
    random.shuffle(edges)
    qs = []
    for _ in range(q):
        u, v, t = qgen(T)
        qs.append((lab[u], lab[v], t))
    add(n, edges, qs)


# samples
add(6, [(1, 2, 3), (2, 3, 2), (2, 4, 4), (1, 5, 5), (5, 6, 1)], [(3, 6, 4), (3, 6, 9), (6, 3, 3)])
add(3, [(1, 2, 10), (2, 3, 10)], [(1, 3, 15), (3, 1, 20), (1, 3, 99)])
add(1, [], [(1, 1, 0), (1, 1, 5)])
add(4, [(2, 1, 1), (3, 2, 1), (4, 3, 1)], [(4, 1, 2), (1, 4, 0), (2, 4, 1)])
add(4, [(1, 2, 100000), (1, 3, 100000), (1, 4, 100000)], [(2, 3, 150000), (3, 4, 1)])
# hidden: small
add(2, [(2, 1, 7)], [(1, 2, t) for t in range(0, 9)] + [(2, 1, t) for t in range(0, 9)] + [(1, 1, 3), (2, 2, 0)])
build(10, "random", lambda: ri(1, 5), 100, q_mix)
build(50, "path", lambda: ri(1, 3), 200, q_mix)
build(300, "random", lambda: ri(1, MAXW), 300, q_mix)
build(1000, "cater", lambda: ri(1, 20), 1000, q_mix)
build(2000, "spider", lambda: ri(1, MAXW), 1000, q_mix)
build(3000, "binary", lambda: 1, 2000, q_mix)
# hidden: maximum size
N, Q = MAXN, MAXQ
build(N, "path", lambda: MAXW, Q, q_mix)
build(N, "twoarms", lambda: ri(1, MAXW), Q, q_random)
build(N, "random", lambda: ri(1, MAXW), Q, q_mix)
build(N, "star", lambda: ri(1, MAXW), Q, q_mix)
build(N, "deep", lambda: ri(1, MAXW), Q, q_mix)
build(N, "deep", lambda: 1, Q, q_line)
build(N, "cater", lambda: ri(1, MAXW), Q, q_mix)
build(N, "spider", lambda: ri(MAXW - 5, MAXW), Q, q_mix)
build(N, "binary", lambda: ri(1, MAXW), Q, q_fork)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

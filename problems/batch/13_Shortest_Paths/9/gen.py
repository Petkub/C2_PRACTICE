# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80909)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, shuffle=True, relabel=True):
    """relabel: cities other than 1 and n get random numbers"""
    edges = list(edges)
    if relabel:
        p = list(range(2, n))
        random.shuffle(p)
        p = [0, 1] + p + [n]
        edges = [(p[a], p[b], w) for a, b, w in edges]
    if shuffle:
        random.shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 0 <= w <= MAXW for a, b, w in edges)
    # no cycle made only of length-0 roads (Kahn on the length-0 roads)
    zout = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    for a, b, w in edges:
        if w == 0:
            zout[a].append(b)
            deg[b] += 1
    st = [v for v in range(1, n + 1) if deg[v] == 0]
    seen = 0
    while st:
        v = st.pop()
        seen += 1
        for u in zout[v]:
            deg[u] -= 1
            if deg[u] == 0:
                st.append(u)
    assert seen == n
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges))


def rnd(n, m, wlo, whi, pzero=0.0):
    """random roads; length-0 roads only go forward in a hidden random order"""
    rank = list(range(n + 1))
    random.shuffle(rank)
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a == b:
            continue
        if random.random() < pzero:
            if rank[a] > rank[b]:
                a, b = b, a
            res.append((a, b, 0))
        else:
            res.append((a, b, ri(wlo, whi)))
    return res


def diamonds(k, wmax, zero=False):
    """k blocks in a row from city 1; each block has two routes of equal length with different road counts"""
    e, cur, nxt = [], 1, 2
    for _ in range(k):
        x, y, z = nxt, nxt + 1, nxt + 2
        nxt += 3
        s = ri(2, wmax)
        t = ri(1, s - 1)
        if zero and random.random() < 0.5:
            t = 0
        e += [(cur, x, t), (x, z, s - t), (cur, y, s // 2), (y, z, s - s // 2), (cur, z, s)]
        cur = z
    return cur, e


def layers(sizes, wfun):
    """complete connections between consecutive layers; first layer = {1}, last = {n}"""
    ids, nxt = [], 1
    for s in sizes:
        ids.append(list(range(nxt, nxt + s)))
        nxt += s
    e = []
    for L in range(len(ids) - 1):
        for u in ids[L]:
            for v in ids[L + 1]:
                e.append((u, v, wfun(L)))
    return nxt - 1, e


def zero_layers(groups, size, extra):
    """groups of cities at the same distance joined by length-0 roads in a hidden order"""
    e, prev, nxt = [], [1], 2
    for g in range(groups):
        cur = list(range(nxt, nxt + size))
        nxt += size
        step = ri(1, 3)
        for v in cur:
            for _ in range(2):
                e.append((random.choice(prev), v, step))
        for _ in range(extra):
            i, j = sorted(random.sample(range(size), 2))
            e.append((cur[i], cur[j], 0))
        prev = cur
    n = nxt
    for v in prev:
        e.append((v, n, 1))
    return n, e


def zero_dag(n, m):
    """only length-0 roads, each going a little forward in a hidden order that starts at 1 and ends at n"""
    order = list(range(2, n))
    random.shuffle(order)
    order = [1] + order + [n]
    e = [(order[i], order[i + 1], 0) for i in range(n - 1)]
    while len(e) < m:
        i = ri(0, n - 2)
        j = min(n - 1, i + ri(1, 6))
        e.append((order[i], order[j], 0))
    return n, e


# samples
add(5, [(1, 2, 2), (1, 3, 1), (3, 2, 1), (2, 5, 4), (3, 4, 2), (4, 5, 3)], False, False)
add(4, [(1, 2, 0), (2, 3, 0), (1, 3, 0), (3, 4, 5), (4, 1, 1)], False, False)
add(4, [(1, 3, 2), (1, 2, 2), (3, 2, 0), (2, 4, 1)], False, False)
add(3, [(1, 2, 1), (1, 2, 1), (2, 3, 1), (2, 3, 1), (1, 3, 2)], False, False)
add(3, [(2, 1, 4), (3, 2, 4)], False, False)
# hidden: small
add(2, [(1, 2, 0)])
add(2, [(1, 2, MAXW), (1, 2, MAXW), (2, 1, 0)])
for n, m, whi, pz in ((6, 15, 3, 0.3), (8, 25, 2, 0.4), (10, 40, 1, 0.5), (12, 50, 4, 0.2), (30, 90, 10, 0.1)):
    add(n, rnd(n, m, 1, whi, pz))
n, e = diamonds(12, 6, True)
add(n, e)
n, e = layers([1, 3, 4, 3, 4, 1], lambda L: 1 if L % 2 else 0)
add(n, e)
n, e = zero_layers(5, 5, 6)
add(n, e)
add(9, rnd(9, 30, 1, 1, 0.6) + [(1, 9, 9)])
add(1000, rnd(1000, 5000, 1, 20, 0.05))
add(5000, rnd(5000, 20000, 1, 5, 0.3))
# hidden: maximum size
N, M = MAXN, MAXM
n, e = diamonds(20_000, 2000, True)
add(n, e)
n, e = diamonds(19_000, 1000)
add(n, e + rnd(n, M - len(e), 10**8, MAXW))
n, e = zero_layers(900, 30, 40)
add(n, e + rnd(n, M - len(e), 10**6, MAXW))
n, e = zero_layers(3000, 8, 15)
add(n, e)
add(10_000, rnd(10_000, M, 1, 1, 0.3))
add(40_000, rnd(40_000, M - 10, 1, MAXW) + [(ri(2, 39_999), 40_000, ri(1, MAXW)) for _ in range(5)]
    + [(1, ri(2, 39_999), ri(1, MAXW)) for _ in range(5)])
add(N, [(i, i + 1, MAXW) for i in range(1, N)], True, False)            # length close to 10^14
n, e = layers([1] + [10] * 1000 + [1], lambda L: L % 3)
add(n, e)
add(*zero_dag(30_000, M))                                                # every road has length 0
e = rnd(N - 1, M - 1, 1, 10)                                             # city n cannot be reached
add(N, e + [(N, 1, 1)], True, False)
n, e = layers([1] + [3] * 11_000 + [1], lambda L: 1 + L % 2)
add(n, e)
add(5000, rnd(5000, M, 1, 3, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

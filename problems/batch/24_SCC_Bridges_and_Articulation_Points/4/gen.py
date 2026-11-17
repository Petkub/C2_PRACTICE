# Test generator of this problem (the judge runs it to rebuild the big tests).
import gc, os, random

random.seed(2404)
gc.disable()
rnd = random.random
MAXN, MAXM, MAXC = 200_000, 200_000, 10**9
tests = []


def shuffled(a):
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, c, edges):
    assert 1 <= n <= MAXN and 0 <= len(edges) <= MAXM and len(c) == n
    assert all(1 <= x <= MAXC for x in c)
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {len(edges)}\n" + " ".join(map(str, c)) + "\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, c, edges):
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    c2 = [0] * n
    for i in range(n):
        c2[lab[i] - 1] = c[i]
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return n, c2, e


def blocks(n, m, size_fn, back=0.0):
    e, bl, start = [], [], 1
    while start <= n:
        s = min(size_fn(), n - start + 1)
        bl.append((start, start + s - 1))
        if s >= 2:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        start += s
    where = [0] * (n + 1)
    for j, (a, b) in enumerate(bl):
        for x in range(a, b + 1):
            where[x] = j
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v and where[u] < where[v]:
            e.append((u, v))
        elif u != v and where[u] == where[v] and random.random() < back:
            e.append((u, v))
    return e[:m], bl


def rand_edges(n, m):
    e = []
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
    return e


def rc(n, lo=1, hi=MAXC):
    return [ri(lo, hi) for _ in range(n)]


def spine(sp_n, size_fn, sinks, m):
    e, bl, start = [], [], 1
    while start <= sp_n:
        sz = min(size_fn(), sp_n - start + 1)
        bl.append((start, start + sz - 1))
        if sz >= 2:
            e += [(i, i + 1) for i in range(start, start + sz - 1)] + [(start + sz - 1, start)]
        start += sz
    for (x, y), (z, w) in zip(bl, bl[1:]):
        e.append((ri(x, y), ri(z, w)))
    where = [0] * (sp_n + 1)
    for j, (x, y) in enumerate(bl):
        for v in range(x, y + 1):
            where[v] = j
    c = [ri(1, 9) for _ in range(sp_n)]
    sk, start = [], sp_n + 1
    for costs in sinks:
        sz = len(costs)
        sk.append((start, start + sz - 1))
        if sz >= 2:
            e += [(i, i + 1) for i in range(start, start + sz - 1)] + [(start + sz - 1, start)]
        c += costs
        e.append((ri(max(1, sp_n - 2000), sp_n), ri(start, start + sz - 1)))
        start += sz
    n = start - 1
    e.append((sp_n, sp_n + 1))
    while len(e) < m:
        u = 1 + int(rnd() * sp_n)
        if rnd() < 0.5:
            v = 1 + int(rnd() * sp_n)
            if where[u] < where[v]:
                e.append((u, v))
        elif u > sp_n - 2000:
            x, y = sk[int(rnd() * len(sk))]
            e.append((u, ri(x, y)))
    assert len(e) <= m
    return n, c, e


add(5, [4, 3, 5, 2, 6], [(1, 2), (2, 1), (2, 3), (4, 5)])
add(4, [3, 3, 1, 5], [(1, 2), (2, 1), (3, 4), (4, 3)])
add(1, [7], [])
add(3, [2, 2, 2], [])
add(3, [4, 4, 4], [(1, 2), (2, 3), (3, 1)])
add(6, [5, 1, 1, 1, 4, 9], [(2, 3), (3, 4), (4, 2), (4, 5), (1, 6), (6, 1)])

add(3, [MAXC] * 3, [(1, 2), (2, 3), (3, 1)])
add(2, [5, 5], [(1, 2)])
add(2, [5, 5], [(1, 2), (2, 1)])
for n, m in ((6, 6), (8, 10), (10, 9), (12, 16), (14, 12)):
    add(n, rc(n, 1, 6), rand_edges(n, m))
e, bl = blocks(2000, 4000, lambda: ri(1, 4))
add(*relabel(2000, rc(2000, 1, 50), e))
add(3000, rc(3000, 1, 3), rand_edges(3000, 2500))

n = 100_000
add(*relabel(n, [MAXC] * n, [(i, i + 1) for i in range(1, n)] + [(n, 1)]))
add(n, [1] * n, [])
add(n, rc(n, 1, 2), rand_edges(n, n // 2))

N = 190_000
add(*relabel(N, rc(N, 1, 99), [(i, i + 1) for i in range(1, N)]))
c = rc(N, 1, 9)
for i in random.sample(range(N), 2000):
    c[i] = MAXC
add(*relabel(N, c, [(i, i + 1) for i in range(1, N)] + [(N, 1)]))
add(*relabel(*spine(80_000, lambda: ri(1, 3), [[ri(1, 2), ri(1, 2)] for _ in range(22_000)], N)))
n = 120_000
e, bl = blocks(n, 200_000, lambda: ri(50, 500), back=0.3)
c = [1] * n
for x in range(bl[-1][0], bl[-1][1] + 1):
    c[x - 1] = MAXC
add(*relabel(n, c, e))
add(*relabel(*spine(110_000, lambda: ri(1, 4), [[ri(4 * 10**8, MAXC) for _ in range(ri(3, 6))]
                                                 for _ in range(8_000)], N)))
add(*relabel(*spine(145_000, lambda: 1, [[MAXC] * 3 for _ in range(10_000)], N)))

h, p = 99_000, 50_000
e = [(i, i + 1) for i in range(1, h)]
c = [1] * h
for j in range(p):
    a, b = h + 2 * j + 1, h + 2 * j + 2
    e += [(a, b), (b, a)]
    c += [5, 5]
    if j < 1000:
        e.append((ri(h - 1000, h), a))
e.append((h, h + 1))
add(*relabel(h + 2 * p, c, e))

add(200_000, [1 + i % 10 for i in range(199_999)] + [MAXC], [(i, i + 1) for i in range(1, 200_000)])
e, bl = blocks(150_000, 200_000, lambda: 20_000)
c = rc(150_000, 1, 9)
for i in random.sample(range(150_000), 1500):
    c[i] = MAXC
add(*relabel(150_000, c, e))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(13001)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def connected(n, fuses):
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v, _ in fuses:
        parent[find(u)] = find(v)
    return len({find(x) for x in range(1, n + 1)}) == 1


def add(n, fuses):
    m = len(fuses)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and 1 <= w <= MAXW for u, v, w in fuses)
    assert connected(n, fuses)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in fuses))


def shuffled(n, fuses):
    p = list(range(2, n + 1))
    random.shuffle(p)
    p = [0, 1] + p
    res = [(p[u], p[v], w) if random.random() < 0.5 else (p[v], p[u], w) for u, v, w in fuses]
    random.shuffle(res)
    add(n, res)


def rnd_tree(n, wl, wh):
    return [(i, ri(max(1, i - ri(1, 50) if random.random() < 0.5 else 1), i - 1), ri(wl, wh)) for i in range(2, n + 1)]


def extra(n, k, wl, wh, loops=True):
    res = []
    while len(res) < k:
        u, v = ri(1, n), ri(1, n)
        if u == v and not loops:
            continue
        res.append((u, v, ri(wl, wh)))
    return res


add(4, [(1, 2, 4), (2, 3, 3), (1, 3, 6), (3, 4, 2)])
add(3, [(1, 2, 2), (1, 3, 3), (2, 3, 4)])
add(1, [(1, 1, 7)])
add(3, [(2, 3, 4), (1, 3, 1), (2, 1, 1)])
add(5, [(1, 2, 3), (2, 3, 5), (4, 2, 1), (3, 5, 2), (5, 4, 9)])

add(2, [(1, 2, 1)])
add(2, [(2, 1, 10), (1, 2, 3), (2, 2, 1)])
add(3, [(1, 2, 5), (2, 3, 5), (3, 3, 1), (1, 1, 11)])
for n, m, wh in [(5, 8, 10), (8, 14, 20), (10, 20, 7), (30, 60, 100), (60, 90, 1000), (200, 400, 10**9)]:
    f = rnd_tree(n, 1, wh) + extra(n, m - (n - 1), 1, wh)
    shuffled(n, f)
n = 3000
f = rnd_tree(n, 1, 10**6) + extra(n, 3000, 1, 10**6)
shuffled(n, f)
n = 2000
t = rnd_tree(n, 1, 1000)
f = t + [(u, v, w + ri(1000, 5000)) for u, v, w in random.sample(t, 1000)]
shuffled(n, f)
n = 5000
f = rnd_tree(n, 1, 10**4) + extra(n, 2000, 1, 10**4, loops=False)
f += [(u, v, w * ri(2, 50)) for u, v, w in random.sample(f, 3000)]
shuffled(n, f)


N, M = MAXN, MAXM
f = rnd_tree(N, 1, MAXW) + extra(N, M - (N - 1), 1, MAXW)
shuffled(N, f)
f = [(i, i + 1, ri(MAXW // 2, MAXW)) for i in range(1, N)] + [(N, N, MAXW)]
shuffled(N, f)
f = [(i, i % N + 1, ri(1, MAXW)) for i in range(1, N + 1)]
shuffled(N, f)
f = [(1, i, ri(1, MAXW)) for i in range(2, N)] + [(i, i, ri(1, MAXW)) for i in range(2, 4)]
shuffled(N - 1, f[:MAXM])
f = rnd_tree(N, 1, 1000) + extra(N, M - (N - 1), 1, 1000)
shuffled(N, f)
f = rnd_tree(N, 1, 10)
f += [(u, v, w + ri(1, 10**6)) for u, v, w in random.sample(f, M - (N - 1))]
shuffled(N, f)
f = rnd_tree(N - 5_000, 1, MAXW // 1000) + extra(N - 5_000, 2_500, 1, MAXW // 1000, loops=False)
f += [(u, v, w * ri(2, 1000)) for u, v, w in random.sample(f, M - len(f))]
shuffled(N - 5_000, f)
side = 316
idx = lambda r, c: r * side + c + 1
f = [(idx(r, c), idx(r, c + 1), ri(1, MAXW)) for r in range(side) for c in range(side - 1)]
f += [(idx(r, 0), idx(r + 1, 0), ri(1, MAXW)) for r in range(side - 1)]
while len(f) < M:
    r, c = ri(0, side - 2), ri(1, side - 1)
    f.append((idx(r, c), idx(r + 1, c), ri(1, MAXW)))
shuffled(side * side, f)
f = [(i, i + 1, MAXW) for i in range(1, N)] + [(1, N, MAXW)]
shuffled(N, f)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

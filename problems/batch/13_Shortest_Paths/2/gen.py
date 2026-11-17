# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(130909)
MAXN, MAXM, MAXK, MAXW = 100_000, 150_000, 5, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, k, edges, mix=True):
    edges = list(edges)
    if mix:
        shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= MAXK
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW
    tests.append(f"{n} {m} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def perm(n):
    p = list(range(2, n + 1))
    shuffle(p)
    return [1] + p


def rnd_edges(n, m, lo, hi):
    e = []
    while len(e) < m:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            e.append((u, v, ri(lo, hi)))
    return e


def backbone(n, m, lo, hi, spans, elo, ehi, start=None):
    p = perm(n)
    e = [(p[i], p[i + 1], ri(lo, hi)) for i in range(n - 1)]
    while len(e) < m:
        i = ri(0, n - 1)
        j = i + random.choice(spans)
        if j < n:
            e.append((p[i], p[j], ri(elo, ehi)))
    return e


def caterpillar(n, m, lo, hi):
    p = perm(n)
    spine = n // 2
    e = [(p[i], p[i + 1], ri(lo, hi)) for i in range(spine - 1)]
    for i in range(spine, n):
        e.append((p[ri(0, spine - 1)], p[i], ri(lo, hi)))
    while len(e) < m:
        u, v, _ = e[ri(0, n - 2)]
        e.append((u, v, ri(lo, hi)))
    return e


add(3, 3, [(1, 2, 5), (2, 3, 4)], False)
add(4, 2, [(1, 2, 3), (2, 3, 2), (3, 4, 4), (4, 1, 1)], False)
add(5, 1, [(1, 2, 7), (2, 3, 1), (1, 3, 10), (4, 5, 2)], False)
add(5, 4, [(1, 2, 3), (1, 3, 1), (3, 4, 2), (4, 5, 1)], False)
add(5, 5, [(1, 2, 2), (2, 3, 3), (2, 4, 1), (4, 5, 6)], False)

add(2, 2, [(1, 2, MAXW)])
add(2, 3, [(2, 1, 1), (1, 2, 3)])
for n, m, k, hi in ((6, 7, 3, 10), (8, 12, 4, 5), (10, 14, 5, 20), (30, 45, 3, 100), (50, 60, 2, 50),
                    (80, 150, 5, MAXW), (150, 200, 4, 1000)):
    add(n, k, rnd_edges(n, m, 1, hi))
add(200, 3, backbone(200, 300, 1, 10, (2, 3), 5, 40))
add(300, 4, backbone(300, 450, 1, 10, (1, 3), 1, 30))

N, M = MAXN, MAXM
add(N, 3, backbone(N, M, 1, 10, (2, 3), 5, 40))
add(N, 5, backbone(N, M, 10**7, 10**9, (2, 4), 10**8, MAXW))
add(N, 4, backbone(N, M, 10**4, 10**6, (2, 3, 5), 10**5, 10**7))
add(N, 2, backbone(N, M, 1, 10, (1, 3), 1, 30))
add(N, 4, backbone(N, M, 1, 10, (3, 5), 10, 50))
add(N, 5, backbone(N, M, MAXW - 100, MAXW, (2, 3), MAXW - 100, MAXW))
add(N, 3, backbone(N, M, MAXW // 2, MAXW, (2,), MAXW // 2, MAXW))
add(N, 3, caterpillar(N, M, 1, MAXW))
add(N, 2, caterpillar(N, M, 1, 1000))
e = backbone(N - 1000, M - 3000, 1, 50, (2, 3, 4), 20, 200)
e += [(u + N - 1000, v + N - 1000, w) for u, v, w in rnd_edges(1000, 3000, 1, 50)]
add(N, 5, e)
add(N, 1, backbone(N, M, 1, MAXW, (2, 3), 1, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

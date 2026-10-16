# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90120)
MAXN, MAXM, MAXW = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads, shuffle=True, relabel=True):
    m = len(roads)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    us, vs, ws = zip(*roads)
    assert 1 <= min(us) and max(us) <= n and 1 <= min(vs) and max(vs) <= n
    assert 1 <= min(ws) and max(ws) <= MAXW and all(u != v for u, v, _ in roads)
    K = n + 1                                    # no two roads join the same two districts
    assert len({u * K + v if u < v else v * K + u for u, v, _ in roads}) == m
    if relabel:
        lab = list(range(1, n + 1))
        random.shuffle(lab)
        lab = [0] + lab
        roads = [(lab[u], lab[v], w) for u, v, w in roads]
    if shuffle:
        roads = roads[:]
        random.shuffle(roads)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def rnd(n, m, wlo, whi, used=None):
    """m new random roads; used holds the pairs taken so far as a * (n + 1) + b with a < b"""
    used = set() if used is None else used
    roads, K, r, d = [], n + 1, random.random, whi - wlo + 1
    while len(roads) < m:
        a = 1 + int(r() * n)
        b = 1 + int(r() * (n - 1))
        b += b >= a
        k = a * K + b if a < b else b * K + a
        if k in used:
            continue
        used.add(k)
        roads.append((a, b, wlo + int(r() * d)))
    return roads


def triangles(k, heavy, light, extra=0):
    """k triangles of dear roads in a row, joined by cheap roads (taking every triangle is best);
    extra: also some cheap roads between random triangles"""
    roads = []
    for t in range(k):
        a, b, c = 3 * t + 1, 3 * t + 2, 3 * t + 3
        for x, y in ((a, b), (b, c), (a, c)):
            roads.append((x, y, ri(*heavy)))
        if t:
            x, y = 3 * t - ri(0, 2), 3 * t + 1 + ri(0, 2)
            roads.append((x, y, ri(*light)))
    n = 3 * k
    used = {min(x, y) * (n + 1) + max(x, y) for x, y, _ in roads}
    while extra:
        a, b = ri(1, n), ri(1, n)
        key = min(a, b) * (n + 1) + max(a, b)
        if (a - 1) // 3 != (b - 1) // 3 and key not in used:
            used.add(key)
            roads.append((a, b, ri(*light)))
            extra -= 1
    return n, roads


def cycles_tree(n, m, wlo, whi):
    """a random tree, then extra roads: a few dear ones (create cycles early), the rest cheap"""
    roads, used = [], set()
    for i in range(2, n + 1):
        p = ri(max(1, i - 50), i - 1)
        roads.append((i, p, ri(wlo, whi)))
        used.add(p * (n + 1) + i)
    mid = (wlo + whi) // 2
    roads += rnd(n, (m - (n - 1)) // 10, mid, whi, used)
    roads += rnd(n, m - len(roads), wlo, mid, used)
    return roads


def islands(n, size, wlo, whi):
    """many separate dense little groups (and some districts without roads)"""
    roads = []
    start = 1
    while start + size - 1 <= n and len(roads) + size * (size - 1) // 2 <= MAXM:
        for a in range(start, start + size):
            for b in range(a + 1, start + size):
                roads.append((a, b, ri(wlo, whi)))
        start += size + ri(0, 2)
    return roads


# samples
add(4, [(1, 2, 5), (2, 3, 4), (3, 1, 3), (3, 4, 2), (1, 4, 1)], False, False)
add(6, [(1, 2, 9), (2, 3, 9), (1, 3, 9), (4, 5, 8), (5, 6, 8), (4, 6, 8), (3, 4, 1)], False, False)
add(3, [(1, 2, 1000000000), (2, 3, 1000000000)], False, False)
add(4, [(1, 2, 2), (2, 3, 2), (3, 4, 2), (4, 1, 2)], False, False)
add(6, [(1, 2, 3), (2, 3, 4), (1, 3, 7), (3, 4, 6), (4, 1, 5), (5, 6, 1)], False, False)
# hidden: small (every choice is tried)
add(5, [(1, 2, 2), (1, 3, 2), (1, 4, 2), (1, 5, 2), (2, 3, 2), (3, 4, 2), (4, 5, 2)])
add(7, [(1, 2, 3), (2, 3, 4), (3, 4, 6), (4, 1, 5), (1, 3, 7), (5, 6, 1), (6, 7, 2), (2, 4, 1)])
add(2, [(1, 2, 1)])
add(4, [(1, 2, 3), (2, 3, 3), (3, 4, 3), (1, 4, 3), (1, 3, 3), (2, 4, 3)])    # all pairs, equal
for n, m, wmax in ((5, 8, 5), (6, 12, 3), (7, 14, 10), (8, 16, 2), (9, 18, MAXW), (12, 20, 6)):
    add(n, rnd(n, m, 1, wmax))
add(*triangles(4, (10, 20), (1, 5)))
add(*triangles(5, (5, 9), (1, 9), 1))
add(300, cycles_tree(300, 900, 1, 1000))
add(*triangles(500, (100, 200), (1, 150), 200))
add(2000, rnd(2000, 3000, 1, MAXW))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, rnd(N, M, 1, MAXW))
add(N, rnd(N, M, 1, 3))                                         # many equal benefits
add(N // 2, rnd(N // 2, M, 1, MAXW))                            # more roads than districts
add(N, rnd(N, M, MAXW, MAXW))                                   # every road at the largest benefit
add(*triangles(25_000, (MAXW // 2, MAXW), (1, MAXW // 2)))
add(*triangles(20_000, (500, 1000), (1, 900), M - 79_999))
add(N, cycles_tree(N, M, 1, MAXW))
add(N // 4, cycles_tree(N // 4, M, 1, 10**6))
add(N, islands(N, 5, 1, MAXW))
add(N, islands(N, 30, 1, 100))
add(N, [(i, i + 1, ri(1, MAXW)) for i in range(1, N)] + [(1, N, 1)])   # one long cycle
add(10, rnd(10, 45, 1, MAXW))
add(N // 10, cycles_tree(N // 10, M, MAXW - 1000, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80180)
MAXN, MAXM, MAXK, MAXW = 100_000, 100_000, 10, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, k, roads):
    m = len(roads)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= MAXK
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n} {m} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def rnd_edges(n, cnt, wlo, whi, lo=1, hi=None):
    hi = hi or n
    res = []
    while len(res) < cnt:
        u, v = ri(lo, hi), ri(lo, hi)
        if u != v:
            res.append((u, v, ri(wlo, whi)))
    return res


def relabel(n, roads):
    """random numbers for junctions 2..n-1 (1 and n keep their numbers)"""
    mid = list(range(2, n))
    random.shuffle(mid)
    mp = {1: 1, n: n}
    for i, x in enumerate(mid):
        mp[i + 2] = x
    roads = [(mp[u], mp[v], w) for u, v, w in roads]
    random.shuffle(roads)
    return roads


def backbone(n, m, wlo, whi):
    """a path 1 -> 2 -> ... -> n plus random roads"""
    roads = [(i, i + 1, ri(wlo, whi)) for i in range(1, n)]
    return roads + rnd_edges(n, m - len(roads), wlo, whi)


# samples
add(4, 3, [(1, 2, 1), (2, 4, 2), (1, 3, 2), (3, 4, 2), (2, 1, 1)])
add(3, 4, [(1, 2, 5), (1, 2, 5), (2, 3, 1)])
add(3, 4, [(1, 3, 10), (3, 2, 1), (2, 3, 1)])
add(3, 2, [(2, 3, 5), (3, 1, 2)])
add(5, 6, [(1, 2, 3), (2, 3, 1), (3, 1, 2), (2, 5, 9), (3, 4, 4), (4, 5, 1), (5, 4, 6)])
# hidden: small
add(2, 1, [(1, 2, MAXW)])
add(2, 10, [(1, 2, 7), (2, 1, 3)])
for n, m, k, wmax in ((6, 10, 5, 5), (10, 20, 10, 9), (20, 30, 10, 20), (40, 60, 7, 10), (60, 150, 10, 30)):
    add(n, k, relabel(n, backbone(n, m, 1, wmax)))
add(30, 10, relabel(30, [(i, i + 1, 2) for i in range(1, 30)] * 2))     # 2^29 routes of the same cost
add(25, 10, relabel(25, [(i, j, j - i) for i in range(1, 25) for j in range(i + 1, min(26, i + 3))]))  # no cycle
add(300, 10, relabel(300, backbone(300, 900, 1, 40)))
add(3000, 10, relabel(3000, backbone(3000, 9000, 1, MAXW)))
# hidden: largest
N, M, K = MAXN, MAXM, MAXK
add(30_000, K, relabel(30_000, backbone(30_000, M, 1, MAXW)))
add(10_000, K, relabel(10_000, backbone(10_000, M, 1, 1000)))
roads = [(i, i + 1, MAXW) for i in range(1, N)] + [(N, N - 1, MAXW)]   # largest costs
add(N, K, roads)
# a cheap tangle near 1, then one very expensive road to n: every junction is taken k times
part = 40_000
roads = [(i, i + 1, ri(1, 5)) for i in range(1, part)] + rnd_edges(part, M - part, 1, 5, 1, part)
roads.append((part, N, MAXW))
add(N, K, relabel(N, roads))
roads = [(i, i + 1, ri(1, 5)) for i in range(1, part)] + rnd_edges(part, M - part - 2, 1, 5, 1, part)
roads += [(part, N, MAXW), (ri(1, part // 2), N, MAXW), (N, ri(1, part), 1)]  # and n leads back into the tangle
add(N, K, relabel(N, roads))
# deep: a long cheap path 1 -> ... -> n with cheap roads going back (cycles) and costly roads going forward
def deep(n, m, back):
    roads = [(i, i + 1, ri(1, 10)) for i in range(1, n)]
    while len(roads) < m:
        u = ri(2, n - 1)
        if random.random() < 0.8:
            v = max(1, u - ri(1, back))
            roads.append((u, v, ri(1, 10)))
        else:
            v = min(n, u + ri(1, back))
            roads.append((u, v, ri(10 * (v - u) + 1, 10 * (v - u) + 50)))
    return relabel(n, roads)


add(50_000, K, deep(50_000, M, 20))
add(40_000, K, deep(40_000, M, 3000))
add(60_000, 7, deep(60_000, M, 5))
# n sits on a cheap cycle far from 1: later routes pass n and come back
L = 49_990
roads = [(i, i + 1, ri(10**6, 10**7)) for i in range(1, L)] + [(L, N, 5)]
roads += [(N, L + 1, 1)] + [(i, i + 1, 1) for i in range(L + 1, N - 2)] + [(N - 2, N, 1)]
roads.append((L + 7, L + 3, 1))                                          # one shorter cycle inside
add(N, K, relabel(N, roads))
# many routes of the same cost: two parallel roads at every step
L = 60_000
roads = []
for i in range(1, L):
    w = ri(1, 1000)
    roads += [(i, i + 1, w), (i, i + 1, w)] if i % 3 == 0 else [(i, i + 1, w)]
roads += [(ri(2, L), ri(2, L), ri(1, 1000)) for _ in range(M - len(roads))]
add(L, K, relabel(L, [r for r in roads if r[0] != r[1]]))
# a DAG with only a few routes: the last answers are -1
roads = [(i, i + 1, ri(1, MAXW)) for i in range(1, N)]
a = ri(1, N - 10)
roads.append((a, ri(a + 1, N), ri(1, MAXW)))
add(N, K, relabel(N, roads))
n = 20_000
roads = rnd_edges(n, M - 1, 1, MAXW)
roads = [(u, v, w) for u, v, w in roads if v != n] + [(n - 1, n, 1)]  # n reachable only from n - 1
add(n, K, roads)
add(N, K, [(i, i + 1, 1) for i in range(2, N)] + [(N, 2, 1)])           # 1 has no road out
add(50_000, 1, relabel(50_000, backbone(50_000, M, 1, 100)))            # k = 1
# a grid of 100 x 500 junctions, roads right and down plus some going back
R, C = 100, 500
roads = []
for r in range(R):
    for c in range(C):
        v = r * C + c + 1
        if c + 1 < C:
            roads.append((v, v + 1, ri(1, 3)))
        if r + 1 < R and random.random() < 0.5:
            roads.append((v, v + C, ri(1, 3)))
add(R * C, K, roads + rnd_edges(R * C, M - len(roads), 1, 3))
# star: junction 2 has a road to every junction, every junction has a road to 2
roads = [(1, 2, 1)] + [(2, v, ri(1, 10**4)) for v in range(3, N + 1)]
roads += [(v, 2, ri(1, 10**4)) for v in range(3, 3 + M - len(roads))]
add(N, K, roads[:M])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

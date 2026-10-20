# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(8006)
MAXN, MAXM, MAXQ, MAXW = 100_000, 100_000, 100_000, 10**6
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads, qs):
    m, q = len(roads), len(qs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= a <= n and 1 <= b <= n and 1 <= w <= MAXW for a, b, w in roads)
    assert all(1 <= k <= n for k in qs)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in roads)
                 + f"{q}\n" + " ".join(map(str, qs)) + "\n")


def relabel(n, roads):
    """random numbers for towns 2..n-1 (1 and n stay), random order of roads"""
    p = list(range(2, n))
    random.shuffle(p)
    p = [0, 1] + p + [n]
    res = [(p[a], p[b], w) for a, b, w in roads]
    random.shuffle(res)
    return res


def rnd_roads(n, m, wmax=MAXW, wmin=1):
    return [(ri(1, n), ri(1, n), ri(wmin, wmax)) for _ in range(m)]


def rnd_qs(n, q):
    return [ri(1, n) for _ in range(q)]


def two_chains(n, m, fw, bw, extra_w):
    """a chain 1 -> 2 -> ... -> n and a chain back n -> ... -> 1 with other weights, plus random roads"""
    r = [(i, i + 1, ri(1, fw)) for i in range(1, n)] + [(i + 1, i, ri(1, bw)) for i in range(1, n)]
    return r + rnd_roads(n, m - len(r), extra_w, extra_w // 2)


# samples
add(5, [(1, 2, 2), (2, 5, 3), (1, 3, 4), (3, 5, 1), (5, 4, 1), (4, 2, 1)], [2, 3, 4, 1, 5])
add(4, [(1, 2, 5), (2, 4, 5), (3, 2, 1), (2, 2, 7)], [3, 2, 4])
add(4, [(1, 2, 1), (2, 3, 4), (3, 2, 4), (2, 4, 1), (1, 4, 3)], [3, 2, 1])
add(4, [(1, 2, MAXW), (2, 4, MAXW), (2, 3, MAXW), (3, 2, MAXW)], [3, 2])
add(1, [], [1])
# hidden: small
add(2, [(2, 1, 5)], [1, 2])
add(2, [(1, 2, 5), (1, 2, 3), (2, 1, 1)], [1, 2])
add(8, rnd_roads(8, 16, 10), list(range(1, 9)))
add(30, relabel(30, two_chains(30, 70, 5, 50, 100)), list(range(1, 31)))
add(100, rnd_roads(100, 300, 1000), rnd_qs(100, 100))
add(300, relabel(300, two_chains(300, 700, 10, 1000, 10**4)), rnd_qs(300, 300))
add(2000, rnd_roads(2000, 5000, MAXW), rnd_qs(2000, 500))
# hidden: large
N, M, Q = MAXN, MAXM, MAXQ
add(N, rnd_roads(N, M), rnd_qs(N, Q))                              # many towns unreachable
n = M // 2 - 1000
add(n, relabel(n, two_chains(n, M, 100, MAXW, MAXW)), rnd_qs(n, Q))
add(n, relabel(n, two_chains(n, M, MAXW, 1, MAXW)), list(range(1, n + 1)) + rnd_qs(n, Q - n))
add(N, [(i, i + 1, MAXW) for i in range(1, N)] + [(N, 1, MAXW)], list(range(N, 0, -1)))  # one big cycle
r = [(i, i + 1, ri(1, 10)) for i in range(1, N)]                   # one-way chain: going back is impossible
add(N, relabel(N, r + [(b, a, w) for a, b, w in rnd_roads(N, M - N + 1, 10) if a < b]), rnd_qs(N, Q))
h = N // 2                                                         # 1 -> left half -> right half -> N
r = [(ri(1, h), ri(1, h), ri(1, 1000)) for _ in range(M // 2)]
r += [(ri(h + 1, N), ri(h + 1, N), ri(1, 1000)) for _ in range(M // 2 - 10)]
r += [(ri(1, h), ri(h + 1, N), ri(1, MAXW)) for _ in range(10)]
add(N, relabel(N, r), rnd_qs(N, Q))
k = 30_000                                                         # a hub that is improved many times
r = [(1, i, i) for i in range(2, k + 2)] + [(i, N, 3 * k + 10 - 2 * i) for i in range(2, k + 2)]
r += [(N, x, ri(1, 5)) for x in range(k + 2, N)][:M - len(r) - 1000]
r += [(x, 1, ri(1, MAXW)) for x in range(k + 2, k + 1002)]
add(N, r, rnd_qs(N, Q))
side = 250                                                         # one-way grid: right and down are cheap
r = []
for i in range(side):
    for j in range(N // side):
        v = i * (N // side) + j + 1
        if j + 1 < N // side:
            r.append((v, v + 1, ri(1, 10)))
        if i + 1 < side:
            r.append((v + N // side, v, ri(1, MAXW)))
add(N, r[:M], rnd_qs(N, Q))
add(n, relabel(n, two_chains(n, M, 3, 3, 6)), rnd_qs(n, Q))       # many equal distances
n = M // 2
add(n, relabel(n, [(i, i + 1, MAXW) for i in range(1, n)] + [(i + 1, i, MAXW) for i in range(1, n)]),
    [1, n] * (Q // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

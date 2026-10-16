# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(81010)
MAXN, MAXM, MAXQ, MAXC = 500, 5000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges, qs, shuffle=True):
    edges = list(edges)
    if shuffle:
        random.shuffle(edges)
    m, q = len(edges), len(qs)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM and 1 <= q <= MAXQ
    assert all(1 <= a <= n and 1 <= b <= n and a != b and 1 <= c <= MAXC for a, b, c in edges)
    assert all(1 <= t <= n and 1 <= k <= n for t, k in qs)
    tests.append(f"{n} {m} {q}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in edges)
                 + "".join(f"{t} {k}\n" for t, k in qs))


def rnd_edges(n, m, clo, chi):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b, ri(clo, chi)))
    return res


def rnd_q(n, q, kmax=None):
    kmax = kmax or n
    return [(ri(1, n), ri(1, kmax)) for _ in range(q)]


def perm(n):
    p = list(range(2, n + 1))
    random.shuffle(p)
    return [1] + p


def staircase(n, m, cmax):
    """cities on a line; a flight over d cities costs more than d short flights, so more flights is cheaper"""
    p = perm(n)
    e = [(p[i], p[i + 1], ri(cmax // 2, cmax)) for i in range(n - 1)]
    while len(e) < m:
        i = ri(0, n - 2)
        j = min(n - 1, i + ri(2, 60))
        e.append((p[i], p[j], min(MAXC, (j - i) * cmax + ri(1, cmax))))
    return e


def chain_q(n, q):
    """queries near the number of flights the cheapest route needs"""
    return [(ri(1, n), max(1, min(n, ri(1, n) if random.random() < 0.3 else ri(n - 80, n)))) for _ in range(q)]


# samples
add(4, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (1, 4, 10), (1, 3, 5)], [(4, 1), (4, 2), (4, 3)], False)
add(3, [(1, 2, 4), (3, 1, 2)], [(1, 1), (2, 2), (3, 3)], False)
add(4, [(1, 2, 2), (2, 3, 7), (1, 3, 20), (3, 4, 1), (2, 4, 30)], [(4, 2), (4, 3)], False)
add(3, [(1, 2, MAXC), (2, 3, MAXC), (1, 2, 1)], [(3, 2), (2, 1)], False)
add(3, [(1, 2, 5), (2, 1, 1), (2, 3, 1)], [(1, 3), (3, 3)], False)
# hidden: small
add(2, [(2, 1, 1)], [(1, 1), (2, 2)])
for n, m, chi, q in ((5, 10, 10, 20), (6, 15, 5, 30), (8, 20, 100, 40), (8, 30, 3, 40), (10, 40, MAXC, 50)):
    add(n, rnd_edges(n, m, 1, chi), rnd_q(n, q))
add(12, staircase(12, 30, 10), rnd_q(12, 60))
add(30, staircase(30, 100, 1000), rnd_q(30, 300))
add(60, rnd_edges(60, 300, 1, 50), rnd_q(60, 500))
add(100, staircase(100, 600, 10**6), chain_q(100, 1000))
# hidden: maximum size
N, M, Q = MAXN, MAXM, MAXQ
add(N, staircase(N, M, 10**6), chain_q(N, Q))
add(N, staircase(N, M, MAXC // 60), chain_q(N, Q))
p = perm(N)
e = [(p[i], p[i + 1], MAXC) for i in range(N - 1)]               # one route, up to 499 * 10^9
while len(e) < M:
    i, j = sorted(random.sample(range(N), 2))
    e.append((p[j], p[i], ri(1, MAXC)))                          # flights back along the route
add(N, e, chain_q(N, Q))
add(N, staircase(N, M, 1000), chain_q(N, Q), False)              # flights listed along the route
add(N, rnd_edges(N, M, 1, MAXC), rnd_q(N, Q))
add(N, rnd_edges(N, M, 1, 10), rnd_q(N, Q, 10))
add(N, staircase(N, M, 10**4), [(t, k) for t, k in chain_q(N, Q)])
p = perm(N)
e = [(p[i], p[i + 1], ri(1, 10)) for i in range(N // 2)]         # half of the cities unreachable
while len(e) < M:
    i, j = ri(0, N - 1), ri(0, N // 2)
    if i != j:
        e.append((p[i], p[j], ri(1, MAXC)))
add(N, e, chain_q(N, Q))
e = []
for i in range(2, N + 1):                                        # every city: direct expensive flight, cheaper via hubs
    e.append((1, i, ri(10**8, MAXC)))
e += staircase(N, M - len(e), 10**5)
add(N, e, rnd_q(N, Q))
add(N, staircase(N, M, 10**6), [(ri(1, N), N) for _ in range(Q)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(80160)
MAXN = 500
tests = []


def add(n, res):
    m = len(res)
    assert 1 <= n <= MAXN and 0 <= m <= n * (n - 1) // 2
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in res)
    assert len({(min(a, b), max(a, b)) for a, b in res}) == m       # every pair plays at most once
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in res))


def from_order(order, pairs):
    """results of the given pairs (positions in order) when order[0] is the best player"""
    return [(order[i], order[j]) if i < j else (order[j], order[i]) for i, j in pairs]


def rnd_dag(n, m, spread=None):
    """m results consistent with a random hidden order; spread limits how far apart the two players are"""
    order = list(range(1, n + 1))
    random.shuffle(order)
    chosen = set()
    while len(chosen) < m:
        i = random.randrange(n)
        j = random.randrange(n) if spread is None else i + random.randint(1, spread)
        if j < n and i != j:
            chosen.add((min(i, j), max(i, j)))
    res = from_order(order, sorted(chosen))
    random.shuffle(res)
    return res


def all_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def flip(res, k):
    """reverse k random results (usually creates a contradiction)"""
    res = res[:]
    for i in random.sample(range(len(res)), k):
        res[i] = (res[i][1], res[i][0])
    return res


# samples
add(4, [(1, 2), (2, 3), (1, 4)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(3, [])
add(5, [(2, 4), (4, 1), (1, 5), (5, 3), (2, 5), (4, 3)])
add(6, [(3, 1), (3, 2), (1, 4), (2, 4), (4, 5), (6, 5)])
# hidden: small (every order is tried)
add(1, [])
add(2, [(2, 1)])
add(8, rnd_dag(8, 9))
add(8, flip(rnd_dag(8, 12), 1))
add(7, rnd_dag(7, 5))
add(8, [(1, 5), (5, 2), (2, 7), (7, 1), (3, 4), (4, 6), (8, 3)])         # a cycle of four
add(8, [(1, 2), (3, 4), (5, 6), (7, 8), (2, 3), (6, 7)])
# hidden: medium
add(60, rnd_dag(60, 300))
add(100, rnd_dag(100, 250, spread=3))
# hidden: largest
N = MAXN
order = list(range(1, N + 1))
random.shuffle(order)
res = from_order(order, all_pairs(N))
random.shuffle(res)
add(N, res)                                                      # complete: every rank known
res2 = [r for r in res if not (r == (order[200], order[201]) or r == (order[201], order[200]))]
add(N, res2)                                                     # one missing result: two players swap
res3 = [(b, a) if (a, b) == (order[10], order[300]) else (a, b) for a, b in res]
add(N, res3)                                                     # one wrong result: a cycle of three
chain = from_order(order, [(i, i + 1) for i in range(N - 1)])
random.shuffle(chain)
add(N, chain)                                                    # only neighbours: still all known
add(N, rnd_dag(N, 20000))
add(N, rnd_dag(N, 1700, spread=4))
add(N, from_order(order, random.sample(all_pairs(N), 100000)))
add(N, flip(chain, 1))                                           # one reversed result in a chain: no longer a chain
long_cycle = [(order[i], order[(i + 1) % N]) for i in range(N)]
add(N, long_cycle)
add(N, flip(rnd_dag(N, 15000, spread=40), 1))                                                      # one reversed result among many
add(N, [])
add(N, [(1, b) for b in range(2, N + 1)])                        # player 1 beats everybody
half = [(a, b) for a in range(1, 251) for b in range(251, N + 1)]
random.shuffle(half)
add(N, half[:N * (N - 1) // 2])                                  # two groups, every rank in a range of 250
two = from_order(order, [(i, i + 2) for i in range(N - 2)])
add(N, two)                                                      # two interleaved chains
add(N, from_order(order, random.sample(all_pairs(N), 124000)))   # almost complete

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

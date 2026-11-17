# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(80160)
MAXN = 500
tests = []


def add(n, res):
    m = len(res)
    assert 1 <= n <= MAXN and 0 <= m <= n * (n - 1) // 2
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in res)
    assert len({(min(a, b), max(a, b)) for a, b in res}) == m
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in res))


def from_order(order, pairs):
    return [(order[i], order[j]) if i < j else (order[j], order[i]) for i, j in pairs]


def rnd_dag(n, m, spread=None):
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
    res = res[:]
    for i in random.sample(range(len(res)), k):
        res[i] = (res[i][1], res[i][0])
    return res


add(4, [(1, 2), (2, 3), (1, 4)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(3, [])
add(5, [(2, 4), (4, 1), (1, 5), (5, 3), (2, 5), (4, 3)])
add(6, [(3, 1), (3, 2), (1, 4), (2, 4), (4, 5), (6, 5)])

add(1, [])
add(2, [(2, 1)])
add(8, rnd_dag(8, 9))
add(8, flip(rnd_dag(8, 12), 1))
add(7, rnd_dag(7, 5))
add(8, [(1, 5), (5, 2), (2, 7), (7, 1), (3, 4), (4, 6), (8, 3)])
add(8, [(1, 2), (3, 4), (5, 6), (7, 8), (2, 3), (6, 7)])

add(60, rnd_dag(60, 300))
add(100, rnd_dag(100, 250, spread=3))

N = MAXN
order = list(range(1, N + 1))
random.shuffle(order)
res = from_order(order, all_pairs(N))
random.shuffle(res)
add(N, res)
res2 = [r for r in res if not (r == (order[200], order[201]) or r == (order[201], order[200]))]
add(N, res2)
res3 = [(b, a) if (a, b) == (order[10], order[300]) else (a, b) for a, b in res]
add(N, res3)
chain = from_order(order, [(i, i + 1) for i in range(N - 1)])
random.shuffle(chain)
add(N, chain)
add(N, rnd_dag(N, 20000))
add(N, rnd_dag(N, 1700, spread=4))
add(N, from_order(order, random.sample(all_pairs(N), 100000)))
add(N, flip(chain, 1))
long_cycle = [(order[i], order[(i + 1) % N]) for i in range(N)]
add(N, long_cycle)
add(N, flip(rnd_dag(N, 15000, spread=40), 1))
add(N, [])
add(N, [(1, b) for b in range(2, N + 1)])
half = [(a, b) for a in range(1, 251) for b in range(251, N + 1)]
random.shuffle(half)
add(N, half[:N * (N - 1) // 2])
two = from_order(order, [(i, i + 2) for i in range(N - 2)])
add(N, two)
add(N, from_order(order, random.sample(all_pairs(N), 124000)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

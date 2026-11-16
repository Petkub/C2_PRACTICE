# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7007)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, pairs):
    m = len(pairs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in pairs)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in pairs))


def dag(n, m, order=None, near=0):
    """random pairs that agree with a hidden order (random unless given); near > 0: pairs between close tasks"""
    p = order if order is not None else random.sample(range(1, n + 1), n)
    res = []
    while len(res) < m:
        i = ri(0, n - 1)
        j = ri(0, n - 1) if near == 0 else min(n - 1, i + ri(1, near))
        if i == j:
            continue
        if i > j:
            i, j = j, i
        res.append((p[i], p[j]))
    random.shuffle(res)
    return res


def with_back(pairs):
    """add one pair against the order of an existing chain a -> b (a cycle)"""
    a, b = pairs[ri(0, len(pairs) - 1)]
    return pairs + [(b, a)]


# samples
add(5, [(4, 3), (3, 1), (5, 2), (2, 1)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(1, [])
add(4, [])
add(4, [(2, 1), (2, 1), (4, 3)])
add(6, [(6, 2), (3, 6), (1, 5), (5, 4), (2, 4)])
# hidden: small (every order is tried)
add(2, [(2, 1)])
add(2, [(1, 2), (2, 1)])
add(3, [(3, 2), (3, 2), (3, 1)])
add(5, [(5, 4), (4, 3), (3, 2), (2, 1)])
add(6, dag(6, 5))
add(7, dag(7, 8))
add(8, dag(8, 10))
add(8, with_back(dag(8, 6)))
add(8, [(1, 8), (2, 8), (3, 7), (7, 1)])
# hidden: medium (the slow scan still finishes)
add(100, dag(100, 300))
add(2000, dag(2000, 5000, near=5))
add(5000, with_back(dag(5000, 8000)))
add(20000, dag(20000, 20000))
# hidden: large
N = MAXN
add(N, [(i + 1, i) for i in range(1, N)])                   # N before N-1 before ... before 1
add(N, [])                                                  # no condition at all
add(N, dag(N, MAXM))
add(N, dag(N, MAXM, near=3))                                # long chains of conditions
add(N, dag(N, MAXM, order=list(range(N, 0, -1)), near=10))  # mostly larger tasks first
add(N, with_back(dag(N, MAXM - 1, near=2)))                 # a long cycle hidden inside
add(N, [(i, 1) for i in range(2, N + 1)])                   # task 1 last
add(N, [(1, i) for i in range(2, N + 1)])
order = list(range(N // 2 + 1, N + 1)) + list(range(1, N // 2 + 1))
add(N, dag(N, MAXM, order=order, near=4))                   # the second half before the first half
add(N, [(i + 1, i) for i in range(1, N - 1)] + [(1, N - 1)])   # a cycle through almost all tasks

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

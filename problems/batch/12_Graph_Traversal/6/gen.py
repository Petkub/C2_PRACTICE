# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(7007)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, pairs):
    m = len(pairs)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in pairs)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in pairs))


def dag(n, m, order=None, near=0):
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
    a, b = pairs[ri(0, len(pairs) - 1)]
    return pairs + [(b, a)]


add(5, [(4, 3), (3, 1), (5, 2), (2, 1)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(1, [])
add(4, [])
add(4, [(2, 1), (2, 1), (4, 3)])
add(6, [(6, 2), (3, 6), (1, 5), (5, 4), (2, 4)])

add(2, [(2, 1)])
add(2, [(1, 2), (2, 1)])
add(3, [(3, 2), (3, 2), (3, 1)])
add(5, [(5, 4), (4, 3), (3, 2), (2, 1)])
add(6, dag(6, 5))
add(7, dag(7, 8))
add(8, dag(8, 10))
add(8, with_back(dag(8, 6)))
add(8, [(1, 8), (2, 8), (3, 7), (7, 1)])

add(100, dag(100, 300))
add(2000, dag(2000, 5000, near=5))
add(5000, with_back(dag(5000, 8000)))
add(20000, dag(20000, 20000))

N = MAXN
add(N, [(i + 1, i) for i in range(1, N)])
add(N, [])
add(N, dag(N, MAXM))
add(N, dag(N, MAXM, near=3))
add(N, dag(N, MAXM, order=list(range(N, 0, -1)), near=10))
add(N, with_back(dag(N, MAXM - 1, near=2)))
add(N, [(i, 1) for i in range(2, N + 1)])
add(N, [(1, i) for i in range(2, N + 1)])
order = list(range(N // 2 + 1, N + 1)) + list(range(1, N // 2 + 1))
add(N, dag(N, MAXM, order=order, near=4))
add(N, [(i + 1, i) for i in range(1, N - 1)] + [(1, N - 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

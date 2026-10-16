# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90606)
MAXN, MAXM, MAXV = 100_000, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, b, a, roads):
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM and 1 <= b <= MAXV and len(a) == n
    assert all(1 <= x <= MAXV for x in a)
    assert all(1 <= u <= n and 1 <= v <= n for u, v in roads)
    tests.append(f"{n} {m} {b}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{u} {v}\n" for u, v in roads))


def flip(u, v):
    return (u, v) if random.random() < 0.5 else (v, u)


def groups(n, k, extra=0.3, shape="random"):
    """roads making k connected groups over a random labelling (tree edges + some extra roads)"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    cuts = sorted(random.sample(range(1, n), k - 1)) if k > 1 else []
    parts, last = [], 0
    for c in cuts + [n]:
        parts.append(p[last:c])
        last = c
    roads = []
    for g in parts:
        for i in range(1, len(g)):
            j = i - 1 if shape == "path" else ri(0, i - 1)
            roads.append(flip(g[i], g[j]))
        for _ in range(int(len(g) * extra)):
            roads.append((random.choice(g), random.choice(g)))
    random.shuffle(roads)
    return roads


def costs(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def around(n, b, spread):
    """library costs on both sides of b"""
    return [max(1, min(MAXV, b + ri(-spread, spread))) for _ in range(n)]


# samples
add(4, 2, [6, 4, 8, 5], [(1, 2), (2, 3), (3, 4)])
add(3, 1, [5, 4, 7], [(1, 2)])
add(4, 3, [2, 10, 1, 5], [(1, 2), (2, 3), (3, 4)])               # a mixed plan wins (no explanation)
add(2, 5, [3, 8], [])
add(3, 100, [1, 2, 3], [(1, 2), (2, 3)])
# hidden: small
add(3, MAXV, [MAXV] * 3, [(1, 2), (2, 3), (1, 3), (2, 2)])   # largest answer (was sample 6)
add(1, 1, [1], [])
add(1, 7, [3], [(1, 1)])
add(5, 4, [9, 9, 9, 9, 9], [(1, 2), (2, 3), (3, 4), (4, 5)])
add(6, 10, [11, 3, 12, 9, 20, 10], [(1, 2), (2, 3), (4, 5), (5, 6), (6, 4)])
add(10, 50, around(10, 50, 30), groups(10, 3))
add(100, 1000, around(100, 1000, 800), groups(100, 7))
add(1000, 5, costs(1000, 1, 100), groups(1000, 40, 0.5))
add(3000, 10**6, around(3000, 10**6, 10**6), groups(3000, 100))
add(5000, MAXV, costs(5000, 1, MAXV), groups(5000, 1))
# hidden: maximum size
N, M = MAXN, MAXM
add(N, 500_000, around(N, 500_000, 500_000), groups(N, 1000, 0.004))
add(N, MAXV, [MAXV] * N, groups(N, 1, 0, "path"))               # one group, everything at the maximum
add(N, 1, [MAXV] * N, groups(N, 2, 0))                          # roads are almost free
add(N, MAXV, costs(N, 1, MAXV), groups(N, 25_000, 0.2))
add(N, MAXV, [MAXV] * N, [])                                    # no roads: N * 10^9
add(N, 10**5, around(N, 10**5, 10**5 - 1), groups(N, 10, 0))
add(N, 3, costs(N, 1, 6), groups(N, 1, 0))
add(N, 10**8, around(N, 10**8, 10**3), groups(N, 300, 0))       # costs very close to b
a = [MAXV] * N                                                  # only one cheap city
a[ri(0, N - 1)] = 1
add(N, 10**9 - 1, a, groups(N, 1, 0))
add(N, 10**6, around(N, 10**6, 10**6), [(ri(1, N), ri(1, N)) for _ in range(M)])
b = 5 * 10**8
a = [b + 1 if i % 2 else b - 1 for i in range(N)]               # half just above b, half just below
add(N, b, a, groups(N, 2500, 0))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

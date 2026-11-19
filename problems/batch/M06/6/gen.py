# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4606)
MAXN, MAXQ, MAXC, MAXT = 100, 100000, 10**9, 10**9
tests = []


def add(n, study, trails, queries):
    m, q = len(trails), len(queries)
    assert 1 <= n <= MAXN and 0 <= m <= n * (n - 1) // 2 and 1 <= q <= MAXQ
    assert len(study) == 4 and all(0 <= x <= MAXT for x in study)
    seen = set()
    for u, v, c, t in trails:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= c <= MAXC and 1 <= t <= 4
        key = (min(u, v), max(u, v))
        assert key not in seen
        seen.add(key)
    assert all(1 <= s <= n and 1 <= e <= n for s, e in queries)
    tests.append(f"{n} {m} {q}\n" + " ".join(map(str, study)) + "\n"
                 + "".join(f"{u} {v} {c} {t}\n" for u, v, c, t in trails)
                 + "".join(f"{s} {e}\n" for s, e in queries))


def graph(n, m, clo, chi, terr=(1, 2, 3, 4), tw=None, comps=1):
    group = [i % comps for i in range(n + 1)]
    pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if group[u] == group[v]]
    m = min(m, len(pairs))
    trails = []
    for u, v in random.sample(pairs, m):
        if random.random() < 0.5:
            u, v = v, u
        trails.append((u, v, random.randint(clo, chi), random.choices(terr, tw)[0]))
    return trails


def path(n, clo, chi):
    order = random.sample(range(1, n + 1), n)
    return [(order[i], order[i + 1], random.randint(clo, chi), random.randint(1, 4)) for i in range(n - 1)]


def queries(n, q, same=0.02):
    out = []
    for _ in range(q):
        s = random.randint(1, n)
        out.append((s, s) if random.random() < same else (s, random.randint(1, n)))
    return out


def rnd4(lo, hi):
    return [random.randint(lo, hi) for _ in range(4)]


add(6, [4, 1, 6, 2], [(1, 2, 3, 1), (2, 3, 3, 1), (1, 4, 2, 2), (4, 3, 2, 3), (3, 5, 1, 1)],
    [(1, 3), (1, 5), (2, 6), (6, 6)])
add(4, [10, 0, 0, 0], [(1, 2, 1, 1), (2, 4, 1, 1), (1, 3, 5, 2), (3, 4, 5, 3)], [(1, 4), (4, 1)])
add(1, [5, 5, 5, 5], [], [(1, 1)])
add(3, [0, 0, 0, 0], [(1, 2, 7, 4), (2, 3, 8, 4), (1, 3, 20, 2)], [(1, 3), (3, 2), (2, 1)])
add(5, [100, 1, 1, 1], [(1, 2, 2, 1), (2, 3, 2, 2), (3, 4, 2, 3), (4, 5, 2, 4), (1, 5, 50, 1)],
    [(1, 5), (5, 3)])

add(2, [0, 0, 0, 0], [(1, 2, MAXC, 3)], [(1, 2), (2, 1), (2, 2)])
add(2, [3, 3, 3, 3], [], [(1, 2)])
n = 6
add(n, rnd4(0, 20), graph(n, 15, 1, 10), queries(n, 30))
n = 8
add(n, rnd4(0, 50), graph(n, 12, 1, 20), queries(n, 50))
n = 10
add(n, rnd4(0, MAXT), graph(n, 25, 1, MAXC, comps=2), queries(n, 60))
n = 12
add(n, [1000, 1000, 1000, 1000], graph(n, 40, 1, 300), queries(n, 80))
n = 15
add(n, rnd4(0, 100), path(n, 1, 30), queries(n, 80))
n = 20
add(n, rnd4(0, 1000), graph(n, 60, 1, 400), queries(n, 100))
n = 30
add(n, rnd4(0, MAXT), graph(n, 200, 1, MAXC), queries(n, 150))

N, Q = MAXN, MAXQ
FULL = N * (N - 1) // 2
add(N, rnd4(0, MAXT), graph(N, FULL, 1, MAXC), queries(N, Q))
add(N, [MAXT] * 4, graph(N, FULL, MAXC - 1000, MAXC), queries(N, Q))
add(N, rnd4(0, 1000), graph(N, 3000, 1, 1000), queries(N, Q))
add(N, [0, 0, 0, 0], graph(N, 2500, 1, MAXC), queries(N, Q))
add(N, rnd4(10**8, MAXT), graph(N, 4500, 1, 10**6, tw=[10, 1, 1, 1]), queries(N, Q))
add(N, [MAXT, 1, 1, MAXT], graph(N, 4000, 1, 10**7), queries(N, Q))
add(N, rnd4(0, MAXT), graph(N, 3000, 1, MAXC, comps=3), queries(N, Q))
trails = path(N, MAXC - 10, MAXC) + graph(N, 2500, MAXC // 2, MAXC)
seen, uniq = set(), []
for u, v, c, t in trails:
    key = (min(u, v), max(u, v))
    if key not in seen:
        seen.add(key)
        uniq.append((u, v, c, t))
add(N, rnd4(0, 10**6), uniq, queries(N, Q))
add(N, rnd4(0, 10**5), graph(N, FULL, 1, 10**5, tw=[1, 1, 1, 5]), queries(N, Q))
add(N, rnd4(MAXT // 2, MAXT), graph(N, 3500, 1, MAXC // 1000), queries(N, Q))
add(N, rnd4(0, 50), graph(N, 2000, 1, 100), queries(N, Q))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

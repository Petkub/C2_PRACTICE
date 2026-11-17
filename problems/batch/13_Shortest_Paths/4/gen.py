# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(8004)
MAXN, MAXM, MAXC = 3000, 6000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads):
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and -MAXC <= c <= MAXC for a, b, c in roads)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in roads))


def relabel(n, roads, keep_order=False):
    p = list(range(2, n + 1))
    random.shuffle(p)
    p = [0, 1] + p
    res = [(p[a], p[b], c) for a, b, c in roads]
    if not keep_order:
        random.shuffle(res)
    return res


def potential_roads(n, m, lo, hi, spread, h=None):
    if h is None:
        h = [0] + [ri(-spread, spread) for _ in range(n)]
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        c = ri(lo, hi) + h[b] - h[a]
        if -MAXC <= c <= MAXC:
            res.append((a, b, c))
    return res


def dag_roads(n, m, lo, hi):
    res = [(i, i + 1, ri(lo, hi)) for i in range(1, n)]
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a < b:
            res.append((a, b, ri(lo, hi)))
    return res


add(5, [(1, 2, 4), (1, 3, 2), (3, 2, -3), (2, 4, 5), (5, 4, -10)])
add(4, [(1, 2, 1), (2, 3, -4), (3, 2, 2), (3, 4, 1)])
add(4, [(1, 2, 3), (3, 4, -5), (4, 3, 1), (2, 1, -1)])
add(3, [(1, 2, -2), (2, 3, 5), (3, 1, -3)])
add(3, [(1, 2, 7), (2, 2, -1), (2, 3, 1)])
add(2, [(1, 1, 0), (1, 2, -MAXC), (1, 2, MAXC)])

add(1, [])
add(1, [(1, 1, -1)])
add(8, relabel(8, potential_roads(8, 15, 0, 5, 10)))
add(8, [(i, i + 1, -1) for i in range(1, 8)] + [(8, 1, 7)])
add(8, [(i, i + 1, -1) for i in range(1, 8)] + [(8, 1, 6)])
add(30, relabel(30, potential_roads(30, 80, 0, 100, 1000)))
add(30, relabel(30, potential_roads(30, 80, 0, 100, 1000) + [(15, 16, -100), (16, 15, 99)]))
add(60, [(i, i + 1, ri(-5, 5)) for i in range(1, 30)] + [(40, 41, -3), (41, 40, 2), (40, 50, 1)])
add(100, relabel(100, dag_roads(100, 300, -MAXC, MAXC)))
add(200, relabel(200, potential_roads(200, 600, 0, 50, 10**6)))
add(300, relabel(300, [(i, i + 1, -MAXC) for i in range(1, 300)]))

N, M = MAXN, MAXM
add(N, [(i, i + 1, ri(-MAXC, MAXC)) for i in range(N - 1, 0, -1)] + dag_roads(N, M - N + 1, -MAXC, MAXC)[N - 1:])
add(N, [(i, i + 1, -MAXC) for i in range(N - 1, 0, -1)])
add(N, [(i, i + 1, MAXC) for i in range(N - 1, 0, -1)])
r = [(i, i + 1, -1) for i in range(N - 1, 0, -1)] + [(N, 1, N - 1)]
add(N, r + potential_roads(N, M - N, 0, 10, 0, [0] + [-(i - 1) for i in range(1, N + 1)]))
r = [(i, i + 1, -1) for i in range(N - 1, 0, -1)] + [(N, N - 1, 0)]
add(N, r + [(a, b, c) for a, b, c in dag_roads(N, M - N, 0, MAXC) if b < N - 1])
add(N, relabel(N, potential_roads(N, M, 0, 10**6, 10**8)))
r = potential_roads(N, M - 2, 0, 3, 10**8)
x, y = ri(2, N), ri(2, N)
add(N, relabel(N, r + [(x, y, 5), (y, x, -6)]))
h = N // 2
r = relabel(h, potential_roads(h, M // 2, 0, 1000, 10**6))
r += [(a + h, b + h, c) for a, b, c in potential_roads(N - h, M // 2 - 22, 0, 1000, 10**6)]
r += [(N - 1, N, -5), (N, N - 1, 4)] + [(ri(h + 1, N), ri(1, h), -MAXC) for _ in range(20)]
add(N, r)
r = [(i, i + 1, -MAXC) for i in range(h + 1, N)] + [(N, h + 1, -MAXC)]
r += [(ri(h + 1, N), ri(1, h), ri(-MAXC, 0)) for _ in range(100)]
add(N, relabel(h, potential_roads(h, M - len(r), 0, 10, 1000)) + r)
r = dag_roads(N, M - 2, -MAXC, MAXC)
add(N, relabel(N, r + [(N - 5, N - 4, MAXC - 1), (N - 4, N - 5, -MAXC)]))
r = dag_roads(N, M - 1, -10, MAXC)
add(N, relabel(N, r + [(N, N, -1)]))
add(N, relabel(N, [(i, i + 1, -MAXC) for i in range(1, N)] + [(N, 1, MAXC)] * 2
                  + potential_roads(N, M - N - 1, MAXC // 2, MAXC, 0)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

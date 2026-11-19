# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45006)
MAXN, MAXM, MAXK = 200_000, 200_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, m, dels):
    k = len(dels)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= MAXK
    assert all(1 <= a <= n and 1 <= c <= n and 1 <= b <= m and 1 <= d <= m for a, b, c, d in dels)
    tests.append(f"{n} {m} {k}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in dels))


def rnd(n, m, k):
    return [(ri(1, n), ri(1, m), ri(1, n), ri(1, m)) for _ in range(k)]


def flat(n, m, k, ylo, yhi, dy, dxlo, dxhi):
    res = []
    for _ in range(k):
        dx = ri(dxlo, dxhi)
        a = ri(1, n - dx)
        b = ri(ylo, yhi)
        d = max(1, min(m, b + ri(-dy, dy)))
        res.append((a, b, a + dx, d) if random.random() < 0.5 else (a + dx, d, a, b))
    return res


add(6, 5, [(1, 3, 6, 4), (6, 3, 4, 4), (4, 1, 2, 2)])
add(8, 5, [(2, 2, 1, 2), (6, 4, 2, 3), (6, 3, 6, 1)])
add(4, 3, [(2, 1, 2, 3), (3, 3, 3, 1)])
add(5, 1, [(1, 1, 5, 1), (2, 1, 4, 1)])
add(9, 6, [(6, 3, 2, 3), (5, 1, 4, 1), (4, 1, 9, 4), (7, 6, 2, 1)])

add(1, 1, [(1, 1, 1, 1)])
add(9, 1, [(1, 1, 9, 1)] * 3)
add(20, 20, [(1, 1, 20, 1), (20, 20, 1, 20)])
add(20, 20, [(1, 10, 9, 10), (3, 12, 8, 12), (2, 7, 7, 7)])
for n, m, k in [(5, 8, 6), (12, 12, 10), (20, 20, 30), (40, 10, 30)]:
    add(n, m, rnd(n, m, k))
add(20, 20, flat(20, 20, 25, 1, 20, 1, 4, 19))

add(2000, 2000, flat(2000, 2000, 2000, 1, 2000, 3, 50, 1999))
add(2000, 2000, rnd(2000, 2000, 2000))
add(MAXN, 5, rnd(MAXN, 5, MAXK))

N, M, K = MAXN, MAXM, MAXK
add(N, M, rnd(N, M, K))
add(N, M, flat(N, M, K, 1, M, 2, 1, N - 1))
add(N, M, flat(N, M, K, 1, 3000, 0, 1000, N - 1))
add(N, M, flat(N, M, K, M - 3000, M, 5, 1000, N - 1))
add(N, M, [(1, 1, N, M)] * K)
add(N, M, [(x, 1, x, M) for x in (ri(1, N) for _ in range(K))])
dels = flat(N, M, K // 2, 50_000, 50_000, 0, 1, 40_000) + flat(N, M, K - K // 2, 150_000, 150_000, 0, 1, 40_000)
add(N, M, dels)
add(N, M, flat(N, M, K, 1, M, 30, 1, 4000))
dels = [(ri(1, 100), r, ri(N - 100, N), r + ri(0, 1)) for r in (ri(1, M - 1) for _ in range(K))]
add(N, M, dels)
add(N, M, flat(N, M, K, 1, M, 0, 40_000, N - 1))
add(N, M, flat(N, M, K, M // 2 - 20_000, M // 2 + 20_000, 40_000, 100, N - 1))
add(N, M, [(1, 1 + 2 * (i % 2), N, 1 + 2 * (i % 2)) for i in range(K)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

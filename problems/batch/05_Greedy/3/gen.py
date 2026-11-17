# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(3002)
MAXN, MAXD, MAXC = 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(D, C, p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert 2 <= D <= MAXD and 1 <= C <= MAXC
    assert all(0 < x < D for x in p) and all(p[i] < p[i + 1] for i in range(n - 1))
    tests.append(f"{n} {D} {C}\n" + " ".join(map(str, p)) + "\n")


def need(D, p):
    return max(max(b - a for a, b in zip([0] + p, p)), 2 * (D - p[-1]))


def stations(n, D):
    if n * 3 > D:
        return sorted(random.sample(range(1, D), n))
    s = set()
    while len(s) < n:
        s.add(ri(1, D - 1))
    return sorted(s)


add(10, 8, [3, 6, 8])
add(10, 5, [4, 7])
add(5, 10, [2])
add(6, 6, [3])
add(30, 9, [4, 9, 12, 17, 20, 26])
add(100, 30, [40, 60])

add(2, 1, [1])
add(2, 2, [1])
add(2, 4, [1])
add(7, 4, [1, 3, 5])
add(7, 3, [1, 3, 5])
add(12, 5, [2, 5, 9])
for D, n in [(20, 5), (30, 8), (40, 12), (60, 20), (100, 30), (1000, 300), (50, 6), (80, 15)]:
    p = stations(n, D)
    add(D, need(D, p) + ri(0, 2 * need(D, p)), p)
D = 10**6
add(D, 4000, stations(3000, D))
add(MAXD, 10**8, stations(5000, MAXD))
p = stations(3000, 10**5)
add(10**5, need(10**5, p), p)

N = MAXN
add(MAXD, 4 * 10**8, stations(N, MAXD))
add(MAXD, 2 * 10**8 + 7, stations(N, MAXD))
add(MAXD, 3 * 10**7, stations(N, MAXD))
add(MAXD, 2 * 10**4, stations(N, MAXD))
p = [4900 * (i + 1) for i in range(N)]
D = p[-1] + 2450
add(D, 4900, p)
add(D, 9800, p)
add(MAXD, MAXC, stations(N, MAXD))
add(MAXD - 1, MAXC, stations(N, MAXD - 1))
p = stations(N, MAXD // 2)
add(MAXD, 6 * 10**8, p)
p = stations(N - 1, MAXD // 2) + [MAXD - 3 * 10**8]
add(MAXD, 6 * 10**8, p)
p = []
for c in range(20):
    base = 25_000_000 + c * 48_000_000
    p += [base + 1000 * k + ri(0, 999) for k in range(N // 20)]
gap = need(MAXD, p)
add(MAXD, gap, p)
add(MAXD, gap - 1, p)
p = list(range(1, N + 1))
add(N + 1, 7, p)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

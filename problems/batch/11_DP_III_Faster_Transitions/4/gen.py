# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11005)
MAXN, MAXM, MAXT, MAXC = 200_000, 20, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(t, passes):
    n, m = len(t), len(passes)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= x <= MAXT for x in t) and all(t[i] < t[i + 1] for i in range(n - 1))
    assert all(1 <= d <= MAXT and 1 <= c <= MAXC for d, c in passes)
    tests.append(f"{n} {m}\n" + " ".join(map(str, t)) + "\n" + "".join(f"{d} {c}\n" for d, c in passes))


def days(n, hi):
    """n distinct sorted days in 1..hi"""
    assert n <= hi
    if hi <= 4 * n:
        return sorted(random.sample(range(1, hi + 1), n))
    s = set()
    while len(s) < n:
        s.add(ri(1, hi))
    return sorted(s)


def rpasses(m, dlo, dhi, clo, chi):
    return [(ri(dlo, dhi), ri(clo, chi)) for _ in range(m)]


# samples
add([2, 3, 5, 9, 10, 15], [(1, 3), (5, 8)])
add([2, 5, 6, 8, 9, 21], [(1, 2), (7, 7), (30, 16)])
add([100], [(1, 50), (1000, 10)])
add([1, 2, 3, 4, 5, 6, 7, 8], [(3, 5), (2, 4)])
add([1, 1000000000], [(999999999, 7), (1000000000, 9), (1, 5)])
add([3, 5, 8, 13, 21, 34, 55], [(4, 6), (11, 13), (25, 24)])
# hidden: small
add([1], [(1, 1)])
add([5, 6], [(2, 1000000000), (1, 1)])
add(days(15, 40), rpasses(3, 1, 10, 1, 20))
add(days(20, 100), rpasses(5, 1, 30, 1, 100))
add(days(18, 25), rpasses(4, 1, 8, 1, 10))
add(days(25, 1000), rpasses(20, 1, 300, 1, 1000))
add(list(range(1, 31)), [(1, 2), (2, 3), (3, 5), (4, 6)])
# hidden: medium
add(days(3000, 1_000_000), rpasses(10, 1, 50_000, 1, 10**6))
add(days(5000, 6000), rpasses(6, 1, 300, 5 * 10**8, MAXC))
add(list(range(1, 5001)), [(1, MAXC)])                          # answer 5000 * 10^9
# hidden: maximum size (long passes cover many trips; days spread up to 10^9)
N = MAXN
add(list(range(1, N + 1)), rpasses(MAXM, N // 50, N // 5, 6 * 10**8, MAXC))
add(days(N, MAXT), [(d * 40_000_000, d * 3 + 1) for d in range(1, MAXM + 1)])
add(days(N, MAXT), rpasses(MAXM, 1, MAXT, 1, MAXC))
add(days(N, MAXT), rpasses(MAXM, 5 * 10**6, 3 * 10**7, 5 * 10**8, MAXC))
add(days(N, MAXT // 2), rpasses(MAXM, 10**6, 5 * 10**7, 3 * 10**8, MAXC))
add(days(N, 10 * N), [(10**9, 10**9)] + rpasses(MAXM - 1, 1, 50, 1, 1000))
add([MAXT - N + 1 + i for i in range(N)], [(1, MAXC)] + rpasses(MAXM - 1, 1000, 10_000, MAXC - 10**6, MAXC))
add(days(N, 20 * N), [(1, MAXC), (2, MAXC)] + rpasses(MAXM - 2, 20_000, 100_000, MAXC - 100, MAXC))
add(list(range(1, N + 1)), [(N, MAXC), (N - 1, 1)] + rpasses(MAXM - 2, 1, N, 10**8, MAXC))
add(days(N, MAXT), [(4 * 10**7 * k, 6 * k + 5) for k in range(1, MAXM + 1)])
add(days(N, 5 * N), [(1000 * k, 6 * k + 5) for k in range(1, MAXM + 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

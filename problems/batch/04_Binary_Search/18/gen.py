# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20217)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def total(n, L):
    m = n - L + 1
    return m * (m + 1) // 2


def add(L, K, a):
    n = len(a)
    assert 1 <= L <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    assert 1 <= K <= total(n, L)
    if len(tests) >= 6:                       # brute.cpp lists every route: keep small inputs small
        assert n <= 5000 or n * 7 > 300_000
    tests.append(f"{n} {L} {K}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def rk(n, L, lo_frac=0.0, hi_frac=1.0):
    t = total(n, L)
    return max(1, min(t, int(t * lo_frac) + ri(0, max(0, int(t * (hi_frac - lo_frac))))))


# samples
add(2, 4, [3, 1, 4, 1, 5])
add(1, 5, [2, 2, 2])
add(1, 1, [MAXA])
add(4, 1, [6, 1, 8, 2])
add(3, 7, [5, 9, 2, 6, 5, 3])
add(1, 21, [4, 7, 1, 1, 9, 2])
# hidden: small
add(1, 1, [1])
add(2, 1, [1, 2])
add(1, 3, [5, 5])
for n in (8, 30, 200, 1000, 3000):
    L = ri(1, n)
    add(L, rk(n, L), rnd(n, 1, 10 if n < 100 else MAXA))
add(1, total(5000, 1) // 2, [7] * 5000)
add(2500, total(5000, 2500), rnd(5000, 1, MAXA))
# hidden: large (K is large in most of them)
N = MAXN
add(1, rk(N, 1, 0.3, 0.7), rnd(N, 1, MAXA))
add(1, total(N, 1), [MAXA] * N)                      # the whole array: 2 * 10^14
add(1, total(N, 1) - 1, [MAXA] * N)
add(1, total(N, 1) // 2 + 1, [1] * N)                # many equal lengths
add(ri(1, 1000), rk(N, 1000, 0.5, 1.0), rnd(N, 1, MAXA))
L = ri(50_000, 150_000)
add(L, rk(N, L), rnd(N, 1, MAXA))
add(N, 1, rnd(N, 1, MAXA))                           # only one route
add(N // 2, rk(N, N // 2, 0.98, 1.0), rnd(N, 1, MAXA))
add(1, total(N, 1), rnd(N, 1, MAXA))
add(10, 1, rnd(N, 1, MAXA))                          # the cheapest window of length 10
a = [MAXA if i % 2 else 1 for i in range(N)]
add(2, rk(N, 2, 0.1, 0.9), a)
a = rnd(N - N // 10, 1, 3) + rnd(N // 10, MAXA - 10, MAXA)   # cheap prefix, expensive tail
add(1, rk(len(a), 1, 0.4, 0.6), a)
add(5, rk(N, 5, 0.9, 1.0), rnd(N, 1, 100))
add(3, rk(N, 3, 0.0, 0.05), sorted(rnd(N, 1, MAXA), reverse=True))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

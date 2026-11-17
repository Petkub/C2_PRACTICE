# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180006)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, s, qs):
    n, q = len(s), len(qs)
    assert 1 <= k <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in s)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {k} {q}\n" + " ".join(map(str, s)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_q(n):
    l = ri(1, n)
    return (l, ri(l, n))


def long_q(n):
    l = ri(1, max(1, n // 10))
    return (l, ri(max(l, n - n // 10), n))


def near_k(n, k):
    """ranges of length close to K (some too short)"""
    ln = max(1, min(n, k + ri(-2, 3)))
    l = ri(1, n - ln + 1)
    return (l, l + ln - 1)


def queries(n, k, q, long_frac, near_frac=0.1):
    res = []
    for _ in range(q):
        x = random.random()
        res.append(near_k(n, k) if x < near_frac else long_q(n) if x < near_frac + long_frac else rnd_q(n))
    return res


# samples
add(3, [4, 8, 6, 2, 9, 7, 5], [(1, 7), (1, 4), (2, 5), (3, 4)])
add(1, [3, 1, 4, 1], [(1, 4), (2, 2), (4, 4)])
add(1, [MAXV], [(1, 1)])
add(4, [5, 5, 5, 1, 5, 5, 5, 5], [(1, 8), (1, 7), (2, 7), (5, 8), (1, 3)])
add(2, [6, 2, 7, 7, 1, 8, 3, 9], [(1, 8), (1, 2), (2, 3), (5, 8), (3, 4), (8, 8)])
# hidden: small
for k in (1, 2, 5, 10):
    s = [ri(1, 20) for _ in range(10)]
    add(k, s, [(l, r) for l in range(1, 11) for r in range(l, 11)])
s = [ri(1, 1000) for _ in range(300)]
add(7, s, queries(300, 7, 500, 0.3, 0.3))
s = [ri(1, MAXV) for _ in range(2000)]
add(40, s, queries(2000, 40, 2000, 0.3, 0.3))
s = [ri(1, MAXV) for _ in range(2000)]
add(2000, s, queries(2000, 2000, 2000, 0.3, 0.3))                       # K = N: a single stage
# hidden: maximum size (values kept short so the input stays <= 3 MB)
N = MAXN
for k, q in ((1, 120_000), (2, 120_000), (50, 120_000), (700, 120_000), (N // 2, 110_000), (5000, 120_000)):
    add(k, [ri(1, 999_999) for _ in range(N)], queries(N, k, q, 0.8))
s = [MAXV] * N
add(N // 3, s, queries(N, N // 3, 50_000, 0.8))                         # all equal
s = list(range(1, N + 1))                                              # increasing: best stage at the right end
add(1000, s, queries(N, 1000, 130_000, 0.8))
s = [ri(1, 999_999) for _ in range(N)]
for i in range(0, N, 300):
    s[i] = 1                                                           # weak plank every 300: stages of 300 always hit one
add(300, s, queries(N, 300, 120_000, 0.8, 0.2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180009)
MAXN, MAXQ, MAXV, MAXK = 200_000, 200_000, 10**9, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n and 1 <= k <= r - l + 1 for l, r, k in qs)
    assert sum(k for _, _, k in qs) <= MAXK
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r} {k}\n" for l, r, k in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def long_qs(n, q, kmax):
    """long ranges, small k: the per-round O(r - l) way is slow"""
    res = []
    for _ in range(q):
        l = ri(1, max(1, n // 20))
        r = ri(max(l, n - n // 20), n)
        res.append((l, r, ri(1, min(kmax, r - l + 1))))
    return res


def rnd_qs(n, q, kmax):
    res = []
    for _ in range(q):
        l = ri(1, n)
        r = ri(l, n)
        res.append((l, r, ri(1, min(kmax, r - l + 1))))
    return res


# samples
add([3, 9, 5, 9, 1, 8, 2], [(1, 7, 3), (3, 6, 2), (5, 7, 3), (1, 3, 1)])
add([5, 5, 5, 5], [(2, 4, 2)])
add([MAXV], [(1, 1, 1)])
add([2, 7, 7, 1, 7, 3, 3, 1], [(1, 8, 4), (1, 8, 8), (4, 8, 2), (2, 3, 1), (6, 8, 2)])
add([1, 2, 3, 4, 5, 6], [(1, 6, 3), (1, 4, 4), (2, 5, 1), (3, 6, 2), (1, 6, 6)])
# hidden: small
a = [ri(1, 4) for _ in range(10)]
add(a, [(l, r, k) for l in range(1, 11) for r in range(l, 11) for k in range(1, r - l + 2)])
a = [ri(1, 10) for _ in range(300)]
add(a, rnd_qs(300, 300, 300))
a = [ri(1, MAXV) for _ in range(2000)]
add(a, rnd_qs(2000, 500, 50) + long_qs(2000, 100, 10))
a = [ri(1, 3) for _ in range(5000)]                                         # many ties
add(a, long_qs(5000, 2000, 30))
add(list(range(4000, 0, -1)), rnd_qs(4000, 1000, 100))                     # decreasing: take the first k
# hidden: maximum size (values kept short so the input stays <= 3 MB)
N = MAXN
add([ri(1, 999_999) for _ in range(N)], long_qs(N, 75_000, 4))
add([ri(1, 20) for _ in range(N)], long_qs(N, 75_000, 4))                  # ties everywhere
add(list(range(1, N + 1)), long_qs(N, 75_000, 4))                          # increasing: the last k cards
add([N + 1 - i for i in range(1, N + 1)], long_qs(N, 75_000, 4))           # decreasing
add([777_777] * N, long_qs(N, 75_000, 4))                                  # all equal
a = [ri(1, 999_999) for _ in range(N)]
add(a, [(1, N, 200_000)])                                                  # one round taking every card
a = [ri(1, 999_999) for _ in range(N)]
add(a, [(1, N, 100_000), (1, N, 50_000)] + long_qs(N, 50_000, 1))
a = [ri(1, 100) for _ in range(N)]
for i in range(N - 1000, N):
    a[i] = 1000 + ri(0, 5)                                                 # the best cards are at the far right
add(a, long_qs(N, 80_000, 3))
a = [(i % 1000) + 1 for i in range(N)]                                     # saw-tooth
add(a, long_qs(N, 80_000, 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

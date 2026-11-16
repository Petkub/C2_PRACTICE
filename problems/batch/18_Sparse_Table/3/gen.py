# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180003)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(b, qs):
    n, q = len(b), len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= v <= MAXV for v in b)
    assert all(1 <= l < r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, b)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_q(n):
    l = ri(1, n - 1)
    return (l, ri(l + 1, n))


def long_q(n):
    l = ri(1, max(1, n // 10))
    return (l, ri(max(l + 1, n - n // 10), n))


def queries(n, q, long_frac):
    return [long_q(n) if random.random() < long_frac else rnd_q(n) for _ in range(q)]


# samples
add([5, 8, 3, 8, 2, 6], [(1, 3), (2, 4), (5, 6)])
add([7, 7, 7], [(1, 3), (2, 3)])
add([1, MAXV], [(1, 2)])
add([4, 9, 9, 1, 9, 3, 2], [(1, 7), (3, 7), (4, 5), (6, 7), (1, 2)])
add([10, 20, 30, 40, 50, 40], [(1, 5), (1, 6), (5, 6), (2, 3), (4, 6)])
# hidden: small
add([ri(1, 5) for _ in range(10)], [(l, r) for l in range(1, 10) for r in range(l + 1, 11)])   # every round
add([ri(1, 100) for _ in range(100)], queries(100, 500, 0.3))
add([ri(1, 3) for _ in range(500)], queries(500, 1000, 0.3))                  # many ties
add([ri(1, MAXV) for _ in range(3000)], queries(3000, 3000, 0.3))
add(list(range(1, 2001)), queries(2000, 2000, 0.3))                             # winner is always r
add(list(range(2000, 0, -1)), queries(2000, 2000, 0.3))                         # winner is always l
# hidden: maximum size (bids kept short so the input stays <= 3 MB)
N = MAXN
add([ri(1, 999_999) for _ in range(N)], queries(N, 120_000, 0.9))
add([ri(1, 50) for _ in range(N)], queries(N, 150_000, 0.9))                    # ties everywhere
add([MAXV] * N, queries(N, 60_000, 0.9))                                        # all equal
add([i * 4 for i in range(1, N + 1)], queries(N, 130_000, 0.9))
add([(N - i) * 4 + 1 for i in range(N)], queries(N, 130_000, 0.9))
b = [ri(1, 10**5) for _ in range(N)]
for _ in range(20):
    b[ri(0, N - 1)] = 999_999                                                  # a few equal top bids
add(b, queries(N, 120_000, 0.8))
b = [ri(1, 10**5) for _ in range(N)]
b[N // 2] = 999_999                                                            # one peak, often at an end of a range
add(b, [(ri(1, N // 2), N // 2 + 1) if j % 2 else (N // 2 + 1, ri(N // 2 + 2, N)) for j in range(130_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random
from collections import deque

random.seed(160104)
MAXN, MAXV, MAXD = 150_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def best(n, k, d, a, b, key):
    """max of b_j - a_i - d (j - i), 1 <= j - i <= k, with the window minimum taken by key(i)"""
    dq, res = deque(), None
    for j in range(2, n + 1):
        while dq and key(dq[-1]) >= key(j - 1):
            dq.pop()
        dq.append(j - 1)
        while dq[0] < j - k:
            dq.popleft()
        i = dq[0]
        p = b[j - 1] - a[i - 1] - d * (j - i)
        res = p if res is None else max(res, p)
    return res


def answers(n, k, d, a, b):
    right = best(n, k, d, a, b, lambda i: a[i - 1] - d * i)
    plain = best(n, k, d, a, b, lambda i: a[i - 1])
    nolimit = best(n, n, d, a, b, lambda i: a[i - 1] - d * i)
    return right, plain, nolimit


def add(k, d, a, b, same=False):
    n = len(a)
    assert 2 <= n <= MAXN and len(b) == n and 1 <= k <= n - 1 and 0 <= d <= MAXD
    assert all(1 <= v <= MAXV for v in a) and all(1 <= v <= MAXV for v in b)
    if same:                                   # samples: the tempting shortcuts give the right answer here
        r, p, q = answers(n, k, d, a, b)
        assert r == p == q
    tests.append(f"{n} {k} {d}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")
    assert len(tests[-1]) <= 3_100_000


# samples
add(2, 3, [5, 9, 2, 8, 7, 6], [4, 12, 10, 9, 15, 6], True)
add(1, 10, [20, 30, 25], [25, 21, 33], True)
add(1, 0, [7, 7], [7, 7], True)
add(3, 100, [500, 900, 450, 700, 800, 300, 999], [100, 650, 300, 990, 600, 520, 700], True)
add(4, 1000000000, [1000000000, 1, 1000000000, 1000000000, 1], [1, 1, 1, 1, 1], True)
# hidden: small
add(1, 5, [10, 1, 10], [1, 30, 1])
add(3, 2, [9, 1, 9, 9, 3], [1, 1, 1, 1, 12])              # cheapest is far: shipping eats it
add(2, 0, [5, 1, 5, 5, 5, 5], [1, 1, 1, 1, 9, 1])          # the cheap village is too far away
n = 12
add(ri(1, n - 1), ri(0, 5), [ri(1, 30) for _ in range(n)], [ri(1, 30) for _ in range(n)])
n = 300
add(ri(1, 100), ri(0, 50), [ri(1, 1000) for _ in range(n)], [ri(1, 1000) for _ in range(n)])
n = 3000
add(ri(1, n - 1), ri(0, 10**6), [ri(1, MAXV) for _ in range(n)], [ri(1, MAXV) for _ in range(n)])
n = 10000
add(500, 100, [ri(10**8, MAXV) for _ in range(n)], [ri(1, 10**8) for _ in range(n)])     # every trade loses
n = 20000
add(n - 1, 1, [n + 1 - i for i in range(n)], [ri(1, 50) for _ in range(n)])
def far_cheap(n, k, d, spots):
    """very cheap villages at the given spots; selling pays well only far below them"""
    a = [ri(5 * 10**8, MAXV) for _ in range(n)]
    for s in spots:
        a[s] = ri(1, 1000)
    last = max(spots)
    b = [ri(1, 10**8) if i <= last + k else ri(9 * 10**8, MAXV) for i in range(n)]
    return k, d, a, b


for n, k, d in ((50, 7, 2), (5000, 300, 10), (20000, 4000, 1000)):
    spots = sorted(random.sample(range(n // 3), 3))
    add(*far_cheap(n, k, d, spots))
# hidden: maximum size (k large, so looking back over the whole window is slow)
N = MAXN
big = [
    (N - 1, MAXD, [MAXV] * N, [1] * N),                                            # largest loss
    (N // 2, 10, [10**8 + 3 * i for i in range(N)], [ri(1, 10**6) for _ in range(N)]),  # slowly dearer: ship short
    (N // 3, 5000, [ri(1, MAXV) for _ in range(N)], [ri(1, MAXV) for _ in range(N)]),
    (N // 2, 1, [1 + i if i < 1000 else ri(5 * 10**8, MAXV) for i in range(N)],
     [ri(1, 10**8) if i < 90_000 else ri(9 * 10**8, MAXV) for i in range(N)]),     # cheap at the top, dear far below
    (100_000, 3, [ri(1, 10**6) for _ in range(N)], [ri(1, 10**6) for _ in range(N)]),
    far_cheap(N, N // 3, 50, [5, 20_000, 30_000]),
    (N // 2, 4000, [10**8 + 3000 * i + ri(0, 2999) for i in range(N)], [ri(1, MAXV) for _ in range(N)]),
    (N - 1, 0, [MAXV - i for i in range(N)], [ri(1, MAXV) for _ in range(N)]),
    (N // 4, MAXD // 2, [ri(1, MAXV) for _ in range(N)], [ri(1, MAXV) for _ in range(N)]),
    (2 * N // 3, 13, [ri(1, 10**5) * 10 for _ in range(N)], [ri(1, MAXV) for _ in range(N)]),
    (N // 3, 1, [N - i if i < N // 2 else ri(10**6, MAXV) for i in range(N)],
     [ri(1, 10**6) if i < N // 2 + N // 3 else ri(10**6, 2 * 10**6) for i in range(N)]),
    (N // 2 + 7, 2, [ri(1, 3) * 10**5 + (i % 1000) for i in range(N)], [ri(1, 10**6) for _ in range(N)]),
]
for k, d, a, b in big:
    add(k, d, a, b)
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

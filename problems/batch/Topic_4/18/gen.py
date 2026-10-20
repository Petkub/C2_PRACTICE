# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30318)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert 1 <= k and 2 * k - 1 <= n
    assert all(-MAXV <= x <= MAXV for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def triples(n, lo, hi):
    """x, x + d, x again and again: the best single slot of each block is a trap"""
    res = []
    while len(res) < n:
        x = ri(lo, hi - 10)
        d = ri(1, 9)
        res += [x, x + d, x]
    return res[:n]


def hills(n, h):
    """1, 2, ..., h, ..., 2, 1 repeated: long chains of changed minds"""
    one = list(range(1, h + 1)) + list(range(h - 1, 0, -1))
    res = []
    while len(res) < n:
        res += one
    return res[:n]


# samples
add(2, [5, 6, 5, 1])
add(3, [-1, 4, -2, 3, -5])
add(1, [-7])
add(2, [3, 8, 2, 7, 9, 1, 4])
add(3, [-4, 10, 6, -3, 7, 8, -2, 5])
add(3, [2, 9, 8, 9, 2, 1])
# hidden (small)
add(1, [MAXV])
add(1, [-MAXV, -MAXV + 1])
add(2, [1, 2, 3])
add(4, rnd(9, -10, 10))
add(5, triples(12, 1, 30))
add(30, rnd(100, -MAXV, MAXV))
add(700, rnd(2000, -1000, 1000))
add(1000, hills(2000, 37))
add(6000, rnd(20_000, -MAXV, MAXV))
add(10_000, rnd(19_999, 1, MAXV))
# large
N = MAXN
add(N // 4, rnd(N, -MAXV, MAXV))
add(N // 5, rnd(N, 1, MAXV))
add(N // 3, rnd(N, -MAXV, MAXV))
add(N // 4, [MAXV // 2] * N)
add((N - 1 + 1) // 2, [MAXV] * (N - 1))                  # forced: every second slot, largest total
add(N // 2, [-MAXV] * N)
add(N // 3, triples(N, 1, MAXV))
add(N // 4, triples(N, -MAXV, MAXV))
add(N // 4, sorted(rnd(N, -MAXV, MAXV)))
add(N // 3, [ri(MAXV - 1000, MAXV) if i % 2 else ri(-MAXV, -MAXV + 1000) for i in range(N)])
add(N // 4, rnd(N, -5, 5))
add(N // 4 + 7, hills(N, 1000))
add(N // 2, rnd(N, -MAXV, MAXV))                         # an even N with K = N / 2 still leaves choices
add(2 * N // 7, hills(N, 3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

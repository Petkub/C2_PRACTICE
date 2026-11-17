# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(60019)
MAXN, MAXA, MAXS = 200_000, 10**9, 10**15
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(s, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= s <= MAXS
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n} {s}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def window(a, w):
    """S such that a typical piece may hold about w elements"""
    return max(max(a), sum(a) * w // len(a))


def add_w(w, a):
    add(window(a, w), a)


# samples
add(10, [4, 6, 3, 5, 2])
add(5, [1, 2, 3, 1, 1])
add(7, [3, 8, 2])
add(100, [5, 9, 2, 7])
add(9, [9, 9, 9])
add(12, [2, 3, 7, 1, 1, 4, 4, 3, 6, 2])
# hidden: small (every set of cuts is tried)
add(1, [1])
add(MAXS, [MAXA])
add(8, [2, 3, 7, 1, 1, 4, 4, 3])
add(6, [5, 1, 1, 5, 1, 1, 5, 1])
add(10, [1, 2] * 9)
add(30, rnd(18, 1, 10))
add(1000, sorted(rnd(18, 1, 300), reverse=True))
add_w(4, rnd(18, 1, 5))
add_w(3, rnd(17, 1, MAXA))
add(4, rnd(18, 1, 3))
add(13, rnd(18, 1, 12) + [14])                   # the last element does not fit
# hidden: medium (the O(N^2) DP of brute.cpp checks these)
add_w(50, rnd(3000, 1, 1000))
add_w(300, rnd(3000, 1, 3))
# hidden: maximum size
N = MAXN
add_w(20000, rnd(N, 1, MAXA))
runs = []
while len(runs) < N:                                     # decreasing runs longer than a piece
    runs += sorted(rnd(ri(20000, 60000), 1, ri(MAXA // 2, MAXA)), reverse=True)
add_w(30000, runs[:N])
add_w(30000, sorted(rnd(N, 1, MAXA), reverse=True))    # many suffix maxima at once
add_w(20000, sorted(rnd(N, 1, MAXA)))
add_w(10000, rnd(N, 1, 3))                               # many ties
add_w(50000, rnd(N, 1, 2))
saw = []
for b in range(200):
    saw += sorted(rnd(1000, 1, MAXA), reverse=True)
add(window(saw, 15000), saw)
x = [N - i for i in range(N)]
add(sum(x), x)                          # one piece holds everything
add(MAXA, [MAXA] * N)                                                  # every piece has one element
x = sorted(rnd(N, 1, MAXA), reverse=True)
add(window(x, 30000), x[:-1] + [MAXA])             # the last one beats every earlier maximum
x = rnd(N, 1, 10**6)
add(window(x, 1000), x[:N // 2] + [MAXA] + x[N // 2 + 1:])           # the big one does not fit
add_w(25000, [ri(1, 1000) if i % 100 else ri(10**8, MAXA) for i in range(N)])
add(7, rnd(N, 1, 3))                                                   # short pieces, ties decide the count
add(30, rnd(N, 1, 10))
add(300, rnd(N, 1, 100))
add(5, [random.choice((1, 1, 2, 3)) for _ in range(N)])         # many equal-cost splits
saw = []
for b in range(4):
    saw += sorted(rnd(N // 4, 1, MAXA), reverse=True)
add_w(30000, saw)
add_w(40000, [MAXA - 4000 * i - ri(0, 20000) for i in range(N)])      # decreasing with small bumps

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

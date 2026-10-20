# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20209)
MAXN, MAXX = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def distinct(n, lo, hi):
    """n distinct integers in [lo, hi], in random order"""
    s = set()
    while len(s) < n:
        s.add(ri(lo, hi))
    a = sorted(s)
    random.shuffle(a)
    return a


def add(k, x):
    n = len(x)
    assert 2 <= k <= n <= MAXN
    assert all(0 <= v <= MAXX for v in x)
    assert len(set(x)) == n
    tests.append(f"{n} {k}\n" + " ".join(map(str, x)) + "\n")


# samples
add(3, [1, 2, 8, 4, 9])
add(4, [10, 0, 3, 7])
add(2, [5, 100, 37])
add(3, [0, MAXX, 500_000_000, 1, 2, 999_999_999])
add(4, [3, 9, 1, 15, 6, 12, 20])
add(4, [14, 2, 30, 7, 22, 11, 27, 4])
# hidden: small
add(2, [0, 1])
add(2, [MAXX, 0])
add(3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10][::-1])
add(5, distinct(12, 0, 60))
add(7, distinct(40, 0, 1000))
add(20, distinct(100, 0, MAXX))
add(150, distinct(200, 0, 2000))
add(9, distinct(250, 0, 300))
# hidden: maximum size (uneven spreads: the answer is far from both 1 and (max - min) / (K - 1))
N = MAXN


def skewed(n, power, hi=MAXX):
    """n distinct points, dense near 0 and sparse near hi"""
    s = set()
    while len(s) < n:
        s.add(int(hi * random.random() ** power))
    a = sorted(s)
    random.shuffle(a)
    return a


def clusters(n, c, width):
    """n distinct points in c random clusters of the given width"""
    centers = [ri(0, MAXX - width) for _ in range(c)]
    s = set()
    while len(s) < n:
        s.add(centers[ri(0, c - 1)] + ri(0, width))
    a = sorted(s)
    random.shuffle(a)
    return a


add(2, distinct(N, 0, MAXX))                       # answer = max - min, huge
add(3, distinct(N - 1, 0, 1_000_000) + [MAXX])
add(1000, skewed(N, 2))
add(30_000, skewed(N, 3))
add(N // 2, skewed(N, 2))
x = distinct(N // 2, 0, 1_000_000) + distinct(N // 2, MAXX - 1_000_000, MAXX)
random.shuffle(x)
add(50, x)                                          # two far clusters
add(5000, clusters(N, 20, 20_000_000))
add(300, clusters(N, 7, 30_000_000))
x = [i * i for i in range(N)]
x = [v for v in x if v <= MAXX]
random.shuffle(x)
add(len(x) // 3, x)                                 # gaps grow along the road
add(N, distinct(N, 0, MAXX))                        # every point is used
x = distinct(N - 10, 0, 10**6) + [MAXX - i * 50_000_000 for i in range(10)]
random.shuffle(x)
add(20, x)                                          # a dense block and a few far points
add(77_777, skewed(N, 4))
add(5, skewed(N, 1.5))
add(6, sorted(skewed(N, 5)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

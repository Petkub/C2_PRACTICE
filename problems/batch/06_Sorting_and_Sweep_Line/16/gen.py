# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(41600)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN
    ps = [p for p, r in h]
    rs = [r for p, r in h]
    assert 1 <= min(ps) and max(ps) <= MAXV and 1 <= min(rs) and max(rs) <= MAXV
    tests.append(f"{n}\n" + "".join(f"{p} {r}\n" for p, r in h))


def increasing(n, lo, hi, step):
    """n values from lo, strictly increasing by multiples of step, ending near hi (never above it)"""
    gap = max(1, 9 * (hi - lo) // (10 * n * step))  # average gap in units of step
    out, v = [], lo
    for _ in range(n):
        out.append(v)
        v += step * ri(1, 2 * gap - 1)
    assert out[-1] <= hi
    return out


def staircase(n, pmax, rmax, pstep=1):
    """n hotels, price and rating both strictly increasing: nobody is better than anybody"""
    return list(zip(increasing(n, 1, pmax, pstep), increasing(n, 2, rmax, 1)))


def shuffled(h):
    h = list(h)
    random.shuffle(h)
    return h


# samples
add([(1000, 7), (800, 6), (1200, 9), (900, 6), (1500, 8)])
add([(500, 5), (500, 5), (500, 4), (400, 3)])
add([(100, 1)])
add([(3, 3), (2, 4), (1, 5)])
add([(1, 1), (2, 2), (3, 3), (4, 4)])
add([(7, 2), (5, 9), (7, 9), (5, 9), (6, 10), (8, 10)])
# hidden: small
add([(5, 5), (5, 5)])
add([(1, 2), (2, 1)])
add([(ri(1, 4), ri(1, 4)) for _ in range(10)])
add([(ri(1, 10), ri(1, 10)) for _ in range(60)])
add(shuffled(staircase(300, 1000, 1000) * 2))
add([(ri(1, 50), ri(1, 50)) for _ in range(2000)])
h = staircase(1500, 3000, 3000)
add(shuffled(h + [(p + 1, r) for p, r in h] + [(p, r - 1) for p, r in h]))   # equal rating or equal price nearby
# large
N = MAXN
add(shuffled(staircase(N, 10**6, 10**6)))                   # everybody survives
add(shuffled(staircase(130_000, MAXV, MAXV)))
add([(123456, 654321)] * N)                                   # all identical: all survive
h = staircase(N // 2, 10**6, 10**6)
add(shuffled(h * 2))                                        # every survivor has a twin
h = staircase(N // 2, 10**6, 10**6)
add(shuffled(h + [(p, r - 1) for p, r in h]))               # same price, lower rating: beaten
h = staircase(N // 2, 10**6, 10**6)
add(shuffled(h + [(p + 1, r) for p, r in h]))               # higher price, same rating: beaten (prices kept distinct)
h = staircase(N // 4, 10**6, 10**6, pstep=2)
add(shuffled(h * 2 + [(p + 1, r) for p, r in h] + [(p, r - 1) for p, r in h]))
h = staircase(N // 2, 10**6, 10**6)
add(shuffled(h + [(ri(2, 10**6), ri(1, 10**6 - 1)) for _ in range(N // 2)]))
add([(ri(1, 10**6), ri(1, 10**6)) for _ in range(N)])       # random: few survivors
add([(777, ri(1, 1000)) for _ in range(N)])                 # one price
add([(ri(1, 1000), 777) for _ in range(N)])                 # one rating
h = staircase(N - 1, 10**6, 10**6, pstep=1)
add(shuffled(h + [(1, 10**6 + 1)]))                         # one hotel beats all others

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

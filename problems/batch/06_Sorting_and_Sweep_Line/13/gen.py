# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40112)
MAXN, MAXT = 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(segs):
    n = len(segs)
    assert 1 <= n <= MAXN
    assert all(1 <= l <= r <= MAXT for (l, r) in segs)
    tests.append(f"{n}\n" + "".join(f"{l} {r}\n" for (l, r) in segs))


def rnd(n, lo, hi, maxlen):
    res = []
    for _ in range(n):
        l = ri(lo, hi)
        res.append((l, min(hi, l + ri(0, maxlen))))
    return res


def windows(n, step, length, jitter=0):
    """bookings that slide to the right: no booking contains another (unless jitter breaks it)"""
    res = [(1 + i * step + ri(0, jitter), 0) for i in range(n)]
    res = [(l, min(MAXT, l + length + ri(0, jitter))) for (l, _) in res]
    random.shuffle(res)
    return res


# samples
add([(1, 6), (2, 4), (3, 8), (5, 6)])
add([(2, 5), (2, 5), (1, 3)])
add([(7, 7)])
add([(1, 5), (1, 3), (3, 5), (2, 9)])
add([(1, 2), (2, 3), (3, 4)])
add([(5, 5), (4, 6), (5, 5), (6, 6), (6, 9)])
# hidden: small
add([(1, 1), (1, 1)])
add([(1, 10), (1, 9), (2, 10), (1, 10), (3, 3)])
add(rnd(8, 1, 10, 5))
add(rnd(30, 1, 20, 10))
add(rnd(200, 1, 100, 30))
add(rnd(2000, 1, MAXT, MAXT // 10))
add(windows(3000, 100, 5000, 120))
add(rnd(5000, 1, 50, 50))
# hidden: maximum size
N = MAXN
add(rnd(N, 1, MAXT, MAXT))
add(windows(N, 6000, 10**8))                                    # nothing is nested
add(windows(N, 6000, 10**8, 6100))                              # a few nested pairs
w = windows(N - 3, 6000, 10**8)
add(w + [(1, MAXT), (5 * 10**8, 5 * 10**8 + 10**8), (3 * 10**8, 3 * 10**8)])   # one outer, one copy, one point
add([(5 * 10**8, 5 * 10**8 + 7)] * N)                           # all identical
s = [(i + 1, MAXT - i) for i in range(N)]                       # a chain of nested bookings
random.shuffle(s)
add(s)
add(rnd(N, 1, 1000, 100))                                       # many identical ones
s = [(ri(1, 50), ri(10**8, MAXT)) for _ in range(N)]            # many equal starts
add(s)
s = [(ri(1, 10**8), MAXT - ri(0, 50)) for _ in range(N)]        # many equal ends
add(s)
add(rnd(N, 1, MAXT, 10**4))
x = windows(N // 2, 12000, 10**8)                               # sliding windows plus their exact copies
add(x + x[:N // 2])
add([(l, l) for l in (ri(1, MAXT) for _ in range(N))])          # single days only

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

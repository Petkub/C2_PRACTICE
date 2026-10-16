# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30109)
MAXN = 200_000
MAXT = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(lec):
    n = len(lec)
    assert 1 <= n <= MAXN
    assert all(0 <= s < e <= MAXT for s, e in lec)
    tests.append(f"{n}\n" + "".join(f"{s} {e}\n" for s, e in lec))


def rnd(n, tmax, lenmax):
    res = []
    for _ in range(n):
        s = ri(0, tmax - 1)
        res.append((s, min(tmax, s + ri(1, lenmax))))
    return res


def adv(n, h):
    """h long lectures that end late, then n - h short ones in a row while all long ones still run"""
    lec = [(ri(0, h), ri(MAXT // 2, MAXT)) for _ in range(h)]
    step = (MAXT // 2 - h - 10) // (n - h)
    lec += [(h + 1 + k * step, h + 1 + k * step + ri(1, step)) for k in range(n - h)]
    random.shuffle(lec)
    return lec


# samples
add([(1, 4), (2, 5), (4, 7), (5, 6)])
add([(1, 5), (1, 3), (2, 4), (6, 8)])
add([(0, 1000000000)])
add([(3, 9), (1, 2), (3, 4), (0, 3), (2, 6)])
add([(7, 9), (1, 3), (5, 7), (3, 5)])
add([(2, 8), (0, 4), (6, 7), (1, 3), (3, 6), (0, 2), (4, 10)])
# hidden: small
add([(5, 6), (5, 6)])
for n, tmax, ln in ((6, 10, 4), (8, 15, 6), (10, 20, 5), (12, 12, 12), (40, 50, 10), (300, 1000, 100)):
    add(rnd(n, tmax, ln))
add([(i, i + 1) for i in range(30)][::-1])                       # touching only: one room
add(rnd(12000, MAXT, MAXT // 20))
# hidden: large
N = 150_000                                                     # 10-digit times: about 3 MB
add(rnd(N, MAXT, MAXT))                                         # tens of thousands of rooms
add(adv(N, N // 2))
add([(0, MAXT)] * MAXN)                                         # every lecture at once
add([(i, 2 * MAXN - i) for i in range(MAXN)][::-1])                   # nested
add([(3 * i, 3 * i + 3) for i in range(MAXN)])                   # back to back
h = MAXN // 2                                                   # many long lectures, then short ones that
add([(0, MAXT)] * h + [(2 * i + 1, 2 * i + 2) for i in range(MAXN - h)])   # all need the room after them
h = N // 2
lec = [(0, MAXT - i) for i in range(h)]                         # rooms become free one by one from the top
lec += [(MAXT - h + 2 * i, MAXT - h + 2 * i + 1) for i in range(1, (N - h) // 2)]
add(lec[:N])
add(rnd(N, MAXT, 5000))                                         # few rooms
add(rnd(MAXN, 10**6, 10**4))                                      # thousands of rooms, many equal times
add(rnd(MAXN, 1000, 1000))                                       # many equal start times (index order)
lec = []
for i in range(MAXN // 2):                                      # pairs [a, b), [b, c): touching does not clash
    a = 4 * i
    lec += [(a, a + 2), (a + 2, a + 4)]
random.shuffle(lec)
add(lec)
lec = rnd(N // 2, MAXT // 2, MAXT // 2) + [(MAXT // 2 + ri(0, 1000), MAXT) for _ in range(N // 2)]
random.shuffle(lec)
add(lec)                                                        # every room frees, then the smallest numbers reuse
add(adv(N, N // 3))
h = MAXN // 3                                                   # like adv() with small times, at full size
lec = [(ri(0, h), 10**6 + ri(0, 10**6)) for _ in range(h)]
lec += [(h + 1 + 2 * k, h + 2 + 2 * k + ri(0, 1)) for k in range(MAXN - h)]
random.shuffle(lec)
add(lec)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

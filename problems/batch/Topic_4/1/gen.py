# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3001)
MAXN, MAXT = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(films):
    n = len(films)
    assert 1 <= n <= MAXN
    assert all(0 <= s < e <= MAXT for s, e in films)
    tests.append(f"{n}\n" + "".join(f"{s} {e}\n" for s, e in films))


def rnd(n, T, maxlen):
    res = []
    for _ in range(n):
        ln = ri(1, maxlen)
        s = ri(0, T - ln)
        res.append((s, s + ln))
    return res


# samples
add([(1, 4), (3, 5), (0, 6), (4, 7), (5, 9), (8, 10)])
add([(1, 10), (2, 3), (3, 4), (5, 6)])
add([(2, 5), (2, 5), (2, 5)])
add([(0, 1000000000)])
add([(0, 3), (1, 2), (2, 3), (0, 1)])
add([(3, 6), (9, 12), (1, 4), (5, 8), (7, 10), (11, 14), (2, 3)])
# hidden: small
add([(5, 6)])
add([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])          # touching chain
add([(0, 10), (10, 20), (9, 11), (9, 11), (9, 11)])     # the shortest film blocks two others
add([(0, 5), (6, 8), (9, 12), (1, 2), (2, 3), (3, 4)])  # the earliest start is a bad choice
for n, T, L in [(8, 20, 6), (10, 30, 8), (12, 40, 10), (15, 50, 12), (60, 200, 30), (300, 2000, 100)]:
    add(rnd(n, T, L))
add(rnd(3000, 10**6, 2000))
add(rnd(12000, MAXT, 300000))
# hidden: maximum size
N = MAXN
add([(i, i + 1) for i in range(N)])                     # every film fits: answer N
f = [(i, i + 1) for i in range(N)]
random.shuffle(f)
add(f)                                                  # the same chain, shuffled
add([(7, 77)] * N)                                      # all equal: answer 1
add([(i, 2 * N - i) for i in range(N)])                 # nested: answer 1
f = [(0, MAXT)] + [(5 * i + 1, 5 * i + 3) for i in range(N // 2)]
f += [(ri(0, 1000), MAXT - ri(0, 1000)) for _ in range(N - len(f))]
random.shuffle(f)
add(f)                                                  # many long films covering a chain of short ones
f = []
for i in range(N // 3):                                 # long films [10i, 10i+10) and short [10i+9, 10i+11)
    f.append((10 * i, 10 * i + 10))
    f.append((10 * i + 9, 10 * i + 11))
    f.append((10 * i + 9, 10 * i + 11))
random.shuffle(f)
add(f)
BIG = 140_000                                           # largest N whose input with 10-digit times stays near 3 MB
add(rnd(BIG, MAXT, 10**4))
add(rnd(BIG, MAXT, 10**6))
add(rnd(BIG, MAXT, MAXT))
add(rnd(N, 10**6, 50))                                  # many ties of end times
f = [(ri(0, 10**6 - 1), 10**6) for _ in range(N)]         # every film ends at the same time
add(f)
f = []
t = 0
while len(f) < BIG:                                       # random chain with touching ends and gaps
    ln = ri(1, 3000)
    f.append((t, t + ln))
    if ri(0, 1):
        f.append((t + ri(0, ln - 1), t + ln + ri(1, 3000)))
    t += ln + ri(0, 1)
f = f[:BIG]
random.shuffle(f)
add(f)

for t in tests:
    assert len(t) <= 3_100_000
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30110)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(D, F, st, shuffle=True):
    n = len(st)
    assert 1 <= n <= MAXN
    assert 1 <= D <= MAXV and 1 <= F <= MAXV
    assert all(1 <= p < D and 1 <= f <= MAXV for p, f in st)
    st = list(st)
    if shuffle:
        random.shuffle(st)
    tests.append(f"{n} {D} {F}\n" + "".join(f"{p} {f}\n" for p, f in st))


def rnd(n, D, flo, fhi):
    return [(ri(1, D - 1), ri(flo, fhi)) for _ in range(n)]


# samples
add(100, 10, [(10, 60), (20, 30), (30, 30), (60, 40)], False)
add(50, 5, [(10, 100), (5, 4)], False)
add(20, 25, [(5, 1), (10, 1)], False)
add(30, 4, [(12, 9), (4, 3), (4, 5), (7, 6), (16, 20)], False)
add(40, 6, [(6, 6), (12, 6), (18, 6), (24, 6), (30, 6), (36, 6)], False)
add(60, 15, [(15, 10), (14, 30), (40, 5), (25, 20), (50, 10), (5, 1)], False)
# hidden: small (every set of stops is tried)
add(10, 9, [(9, 1)])                                   # reach the station with 0 litres left
add(10, 8, [(9, 5)])
for n in (5, 8, 10, 12, 14, 16, 16):
    D = ri(20, 100)
    add(D, ri(1, D // 3), rnd(n, D, 1, D // 4))
add(1000, 10, [(10 * i, 10) for i in range(1, 16)] + [(5, 1000)])
add(10**6, 50, rnd(3000, 10**6, 1, 700))
add(10**5, 20, rnd(5000, 10**5, 1, 30))
# hidden: large
N = 180_000                                            # 10-digit positions: about 3 MB
add(MAXV, 5000, rnd(N, MAXV, 1, 12000))                # tens of thousands of stops
add(MAXV, 5000, rnd(N, MAXV, 1, 10000))                # total fuel just around D
st = rnd(N - 20, MAXV, 1, 100) + [(ri(1, 10**6), ri(5 * 10**7, 10**8)) for _ in range(20)]
add(MAXV, 10**6, st)                                   # only a few stops needed
add(MAXV, MAXV, rnd(N, MAXV, 1, 10**6))                # no stop needed
add(MAXV, MAXV - 1, [(ri(1, MAXV - 1), 1) for _ in range(N)])
add(MAXV, 1, [(1, ri(1, 10000)) for _ in range(MAXN)]) # every station at position 1
step = MAXV // N                                       # farther stations give less fuel
add(MAXV, step, [(k * step, max(1, 3 * step - k // 20)) for k in range(1, N)])
st = [(k, 1) for k in range(1, MAXN - 10)] + [(MAXN - 10, MAXV)]
add(MAXV, 1, st)                                       # many tiny stops to reach the big one
st = [(k * 5000, 5000) for k in range(1, N)]          # one stop at each, exactly enough
add(N * 5000, 5000, st)
st = [(k * 5000, 5000) for k in range(1, N)]
st[N // 2] = (st[N // 2][0], 4999)                     # one litre short
add(N * 5000, 5000, st)
st = rnd(N, MAXV, 1, 20000)
gap = 600_000_000                                      # nothing between 6 * 10^8 and 7 * 10^8
st = [(p, f) for p, f in st if not gap <= p < gap + 10**8]
add(MAXV, 30000, st)
add(MAXV // 10, 1000, rnd(MAXN, MAXV // 10, 1, 1500))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

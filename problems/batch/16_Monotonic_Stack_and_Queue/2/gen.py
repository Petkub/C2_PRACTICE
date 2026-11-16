# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160002)
MAXN, MAXT, MAXD, MAXV = 150_000, 10**9, 10**9, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(d, tv):
    n = len(tv)
    assert 1 <= n <= MAXN and 0 <= d <= MAXD
    assert all(1 <= t <= MAXT and 0 <= v <= MAXV for t, v in tv)
    assert all(tv[i][0] < tv[i + 1][0] for i in range(n - 1))
    tests.append(f"{n} {d}\n" + "".join(f"{t} {v}\n" for t, v in tv))
    assert len(tests[-1]) <= 3_100_000


def times(n, maxgap, start=1):
    ts, t = [], start
    for _ in range(n):
        ts.append(t)
        t += ri(1, maxgap)
    assert ts[-1] <= MAXT
    return ts


# samples
add(10, [(1, 5), (4, 3), (12, 7), (13, 2), (22, 4), (40, 1)])
add(0, [(2, 9), (3, 1), (5, 4), (6, 4)])
add(5, [(100, 42)])
add(1000, [(1, 2), (2, 8), (3, 3), (10, 9), (20, 1)])
add(3, [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3)])
# hidden: small
add(1, [(1, 0), (3, 5), (4, 0), (5, 0), (7, 1)])
ts = times(50, 5)
add(7, [(t, ri(0, 9)) for t in ts])
ts = times(500, 100)
add(ri(0, 3000), [(t, ri(0, MAXV)) for t in ts])
ts = times(2000, 3)
add(40, [(t, 2000 - i) for i, t in enumerate(ts)])            # decreasing values
ts = times(5000, 1000)
add(MAXD, [(t, ri(0, 50)) for t in ts])
ts = times(10000, 10)
add(ri(5, 500), [(t, ri(0, MAXV)) for t in ts])
# hidden: maximum size
N = MAXN
ts = times(N, 6000)
add(MAXD, [(t, N - i) for i, t in enumerate(ts)])             # everything stays in the window, decreasing
add(MAXD, [(t, MAXV) for t in ts])                             # all equal
add(MAXD, [(t, i % 1000) for i, t in enumerate(ts)])          # saw teeth
add(ts[-1] // 2, [(t, N - i) for i, t in enumerate(ts)])      # half the history, decreasing
add(ts[-1] // 3, [(t, ri(0, MAXV)) for t in ts])
add(ts[-1] - ts[0] - 1, [(t, i) for i, t in enumerate(ts)])  # increasing: the newest always wins
ts = times(N, 3)
add(ri(100, 200), [(t, ri(0, MAXV)) for t in ts])
add(0, [(t, ri(0, MAXV)) for t in ts])
ts = [MAXT - N + 1 + i for i in range(N)]                       # consecutive seconds near 10^9
add(N - 2, [(t, MAXV - i // 2) for i, t in enumerate(ts)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

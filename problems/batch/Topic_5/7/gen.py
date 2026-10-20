# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40407)
MAXN, MAXT = 150_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, shuffle=True):
    a = list(a)
    if shuffle:
        random.shuffle(a)
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(0 <= s < e <= MAXT for s, e in a)
    tests.append(f"{n}\n" + "".join(f"{s} {e}\n" for s, e in a))


def chain(n, start, gap_max, len_max):
    """n bookings one after another, never overlapping (touching allowed)"""
    out, t = [], start
    for _ in range(n):
        t += ri(0, gap_max)
        d = ri(1, len_max)
        out.append((t, t + d))
        t += d
    return out


# samples
add([(10, 20), (30, 40), (15, 18), (18, 35)], False)
add([(0, 10), (10, 20), (10, 15), (12, 13)], False)
add([(1, 5), (5, 9), (9, 12)], False)
add([(0, 1)], False)
add([(3, 10), (0, 3), (3, 4), (3, 6), (20, 30)], False)
add([(0, MAXT), (0, MAXT)], False)
# hidden: small
add([(5, 6), (0, 5)])
add([(0, 2), (1, 3)])
add(chain(10, 0, 3, 5))                                  # OK
add(chain(30, 0, 2, 10)[:29] + [(ri(0, 100), ri(101, 200))])
a = chain(200, 0, 0, 20)                                  # touching everywhere, then one overlap late
a.append((a[150][0] + 1, a[150][1] + 1))
add(a)
add([(ri(0, 1000), ri(1001, 2000)) for _ in range(300)])
a = chain(2000, 0, 5, 1000)
x = a[1500]
a += [(x[0], x[1])] * 3 + [(x[0], x[0] + 1)]              # several start together at t
add(a)
a = chain(4000, 0, 10, 10**5)
add(a)                                                    # OK, large values
# hidden: large (O(N^2) pair checks are too slow)
N = MAXN
a = chain(N, 0, 1000, 5000)
add(a)                                                    # OK
a = chain(N - 1, 0, 1000, 5000)
y = a[N - 10]
add(a + [(y[1] - 1, y[1] + 5)])                           # the only overlap is near the end
a = chain(N - 1, 0, 0, 6000)
y = a[N // 2]
add(a + [(y[0], y[0] + 1)])                               # touching chain, overlap in the middle
a = chain(N // 2, 0, 0, 6000)
t0 = a[-1][1]
a += [(t0, t0 + ri(1, 1000)) for _ in range(N - N // 2)]  # half start at the same time t0
add(a)
starts = [ri(0, MAXT - 10**6) for _ in range(N)]
add([(v, v + ri(1, 10**6)) for v in starts])             # random, overlap early
a = chain(N - 2, 0, 0, 6000)
z = a[N // 3]
add(a + [(z[0] - 1, z[1]), (z[0], z[1] + 1)])             # a long one already in use before
add([(0, MAXT)] + [(ri(1, MAXT - 1), MAXT) for _ in range(N - 1)])  # one long, then everything
a = chain(N - 1, 0, 0, 6000)
w = a[N - 3]
add(a + [(w[0] - 1, w[1] + 1)], False)                     # covers a whole booking, given last
a = [(t, t + 1) for t in range(N)]                         # unit bookings, touching
a[N - 1] = (N - 2, N)
add(a)
add([(5000, 6000)] * N)                                    # all identical: every booking is listed
a = chain(N - 1, 0, 0, 6000)
add(a[::-1] + [(a[0][0], a[0][1])], False)                 # reverse order, overlap at the very start

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

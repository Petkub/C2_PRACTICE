# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20211)
MAXN, MAXT, MAXD = 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(T, d):
    n = len(d)
    assert 1 <= n <= MAXN
    assert 1 <= T <= MAXT
    assert all(1 <= x <= MAXD for x in d)
    tests.append(f"{n} {T}\n" + " ".join(map(str, d)) + "\n")


def arrival_minutes(v, d):
    """exact arrival time in minutes as a fraction (num, den) at speed v"""
    h = sum((x + v - 1) // v for x in d[:-1])
    return 60 * h * v + 60 * d[-1], v


def exact_T(v, d):
    """T equal to the arrival time at speed v (d[-1] chosen so that it is a whole number of minutes)"""
    num, den = arrival_minutes(v, d)
    assert num % den == 0
    return num // den


# samples
add(400, [10, 7, 12])
add(120, [1, 1, 1])
add(45, [90])
add(105, [30, 45])
add(61, [10**6, 10**6])
add(600, [3, 9, 4, 7])
# hidden: small
add(1, [1])
add(1, [MAXD])                                 # one leg: 60 * 10^9 km/h
add(60, [1, 1])                                # exactly the waiting hour: impossible
add(121, [5, 5, 5])
add(10**6, rnd(1, 1, MAXD))
d = rnd(30, 1, 100)
add(60 * 29 + 17, d)
d = rnd(50, 1, 10_000)
add(60 * sum(d) // 70, d)
d = rnd(80, 1, 1000) + [600]
add(exact_T(120, d), d)                        # arrival exactly at T
d = rnd(100, 1, 100_000) + [7 * 11 * 13]
add(exact_T(1001, d), d)                       # arrival exactly at T
add(MAXT, rnd(100, 1, 100_000))
# hidden: maximum size
N = MAXN
add(60 * (N - 1) + 1, rnd(N, 1, MAXD))        # one minute for the last leg
add(60 * (N - 1) + 59, rnd(N, 1, MAXD))
add(60 * (N - 1), rnd(N, 1, MAXD))            # impossible
add(MAXT, rnd(N, 1, MAXD))                     # many hours of driving per leg
add(MAXT, [MAXD] * N)
add(MAXT // 3, rnd(N, 1, MAXD))
add(70 * N, rnd(N, 1, MAXD))
d = rnd(N - 1, 1, MAXD) + [MAXD]
add(MAXT - 7, d)
d = rnd(N - 1, 1, 10**6) + [6 * 10**5]
add(exact_T(12_000, d), d)                     # arrival exactly at T
d = rnd(N - 1, 10**8, MAXD) + [MAXD]
add(60 * (N - 1) + 1, d)                       # answer 6 * 10^10
add(ri(60 * N, MAXT), sorted(rnd(N, 1, MAXD)))
add(ri(60 * N, MAXT), rnd(N, 1, 1000))
add(90 * N, [1] * (N - 1) + [MAXD])
add(MAXT, rnd(N, 999_000_000, MAXD))
add(60 * (N - 1) + 30, rnd(N, 1, MAXD))
add(120 * N, rnd(N, 1, MAXD))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

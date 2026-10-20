# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(41500)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(jobs):
    n = len(jobs)
    assert 1 <= n <= MAXN
    assert all(0 <= a <= MAXV and 1 <= t <= MAXV for a, t in jobs)
    tests.append(f"{n}\n" + "".join(f"{a} {t}\n" for a, t in jobs))


def rnd(n, amax, tmax):
    return [(ri(0, amax), ri(1, tmax)) for _ in range(n)]


# samples
add([(0, 3), (1, 5), (2, 1), (2, 2), (20, 1)])
add([(5, 2), (3, 2), (3, 2), (0, 4)])
add([(7, 7)])
add([(0, 5), (5, 1), (1, 3)])
add([(100, 100), (0, 100), (99, 1), (100, 1)])
# hidden: small
add([(0, 1), (0, 1)])
add([(3, 1), (0, 1), (1, 1)])
add(rnd(8, 5, 3))                       # many ties on length and arrival
add(rnd(30, 20, 4))
add(rnd(200, 100, 10))
add(rnd(1000, 10**6, 1000))             # long idle stretches
add([(0, ri(1, 5)) for _ in range(2000)])
add(rnd(3000, 5000, 3))
# large (N = MAXN, or about 130 000 when every value has 10 digits so the input stays near 3 MB)
N = MAXN
# shorter jobs all arrive late: scanning jobs sorted by length from the start meets them every time
add([(0, 2)] * (N // 2) + [(MAXV, 1)] * (N // 2))
add([(0, ri(1, 10**4)) for _ in range(N)])                 # everybody waits from the start
add([(0, 7)] * N)                                          # all equal: order by index
add([(i, ri(1000, 10**4)) for i in range(N)])              # one arrival per minute, queue keeps growing
jobs = [(N - i, ri(1, 3)) for i in range(N)]               # later index arrives earlier, many equal lengths
add(jobs)
add([(ri(0, 20) * 1000, ri(1, 10)) for _ in range(N)])     # bursts, ties on length and arrival
jobs = [(0, ri(2, 20)) for _ in range(N // 2)] + [(ri(0, 2 * 10**6), 1) for _ in range(N // 2)]
random.shuffle(jobs)                                       # short jobs keep arriving while long ones wait
add(jobs)
jobs = [(ri(0, 1000), ri(1, 5)) for _ in range(N // 3)] + \
       [(ri(10**6, 10**6 + 1000), ri(1, 5)) for _ in range(N // 3)] + \
       [(MAXV, 1) for _ in range(N - 2 * (N // 3))]
random.shuffle(jobs)
add(jobs)
M = 130_000
add([(ri(0, MAXV), ri(MAXV - 10**6, MAXV)) for _ in range(M)])  # total time far beyond 32 bits
add([(MAXV - i, MAXV - ri(0, 2)) for i in range(M)])
jobs = [(ri(0, 99), ri(1, 3)) for _ in range(N - 1)] + [(MAXV, 1)]
add(jobs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

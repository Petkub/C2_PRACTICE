# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(30113)
MAXN = 100_000
MAXT = 10**6
MAXD = 10**11
MAXW = 1000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(jobs):
    n = len(jobs)
    assert 1 <= n <= MAXN
    assert all(1 <= t <= MAXT and 1 <= d <= MAXD and 1 <= w <= MAXW for t, d, w in jobs)
    tests.append(f"{n}\n" + "".join(f"{t} {d} {w}\n" for t, d, w in jobs))


def rnd(n, tmax, slack, wmax=MAXW):
    """durations 1..tmax, deadlines spread over [1, total * slack], weights 1..wmax"""
    ts = [ri(1, tmax) for _ in range(n)]
    hi = max(1, min(MAXD, int(sum(ts) * slack)))
    return [(t, ri(1, hi), ri(1, wmax)) for t in ts]


def tight(n, tmax, extra, wmax=MAXW):
    """a schedule with no fine exists: deadlines = finish times in a random order + a little"""
    ts = [ri(1, tmax) for _ in range(n)]
    now, res = 0, []
    for t in ts:
        now += t
        res.append((t, min(MAXD, now + ri(0, extra)), ri(1, wmax)))
    random.shuffle(res)
    return res


# samples
add([(2, 2, 1), (2, 3, 5), (3, 10, 2)])
add([(5, 5, 3), (1, 10, 7)])
add([(MAXT, 1, MAXW)])
add([(2, 6, 1), (3, 6, 4), (1, 6, 2), (4, 3, 3)])
add([(1, 2, 1), (10, 13, 2), (5, 9, 3)])
add([(4, 7, 2), (2, 15, 1), (6, 9, 5), (3, 4, 1), (5, 20, 3), (1, 11, 4)])
# hidden: small (every order is tried)
add([(1, 1, 1)])
add([(2, 1, 1), (1, 3, 9)])
for n, wmax in ((5, 3), (10, 1000), (14, 1000), (16, 50)):
    add(rnd(n, 10, 0.8, wmax))
add(tight(16, 20, 2))
add([(ri(1, MAXT), ri(1, 10**7), ri(1, MAXW)) for _ in range(16)])
add([(ri(1, 5), 7, ri(1, 9)) for _ in range(12)])               # equal deadlines
add(rnd(16, 10, 0.6, 1))                                        # all weights 1
add(rnd(3000, 1000, 0.5))
# hidden: large
N = MAXN
add(rnd(N, MAXT, 1.0))
add(rnd(N, MAXT, 0.3))
add(tight(N, MAXT, 0))                                          # answer 0, only one good order up to ties
add(tight(N, 10**4, 3))
add([(ri(1, 10**4), 10**8, ri(1, MAXW)) for _ in range(N)])     # all deadlines equal
add([(MAXT, ri(1, 10**6), MAXW) for _ in range(N)])             # the largest fines
add(rnd(N, MAXT, 0.7, 1))                                       # all weights 1
jobs = [(N - i, i + 1, ri(1, MAXW)) for i in range(N)]          # long jobs have early deadlines
add(jobs)
jobs = []
for i in range(N):                                              # costly jobs with later deadlines
    t = ri(1, 10**4)
    if i % 10 == 0:
        jobs.append((t, ri(10**7, 10**8), MAXW))
    else:
        jobs.append((t, ri(1, 10**8), 1))
random.shuffle(jobs)
add(jobs)
jobs = []
for i in range(N):                                              # weights 1 or 1000
    t = ri(1, 10**5)
    jobs.append((t, ri(1, 4 * 10**9), random.choice((1, MAXW))))
add(jobs)
add(tight(N, MAXT, 10**6))
add(rnd(N, 999, 0.7))
add([(MAXT, MAXD, MAXW)] * N)                                   # everything finishes exactly on time

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

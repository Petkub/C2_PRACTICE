# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(41500)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(jobs):
    n = len(jobs)
    assert 1 <= n <= MAXN
    assert all(0 <= a <= MAXV and 1 <= t <= MAXV for a, t in jobs)
    tests.append(f"{n}\n" + "".join(f"{a} {t}\n" for a, t in jobs))


def rnd(n, amax, tmax):
    return [(ri(0, amax), ri(1, tmax)) for _ in range(n)]


add([(0, 3), (1, 5), (2, 1), (2, 2), (20, 1)])
add([(5, 2), (3, 2), (3, 2), (0, 4)])
add([(7, 7)])
add([(0, 5), (5, 1), (1, 3)])
add([(100, 100), (0, 100), (99, 1), (100, 1)])

add([(0, 1), (0, 1)])
add([(3, 1), (0, 1), (1, 1)])
add(rnd(8, 5, 3))
add(rnd(30, 20, 4))
add(rnd(200, 100, 10))
add(rnd(1000, 10**6, 1000))
add([(0, ri(1, 5)) for _ in range(2000)])
add(rnd(3000, 5000, 3))

N = MAXN

add([(0, 2)] * (N // 2) + [(MAXV, 1)] * (N // 2))
add([(0, ri(1, 10**4)) for _ in range(N)])
add([(0, 7)] * N)
add([(i, ri(1000, 10**4)) for i in range(N)])
jobs = [(N - i, ri(1, 3)) for i in range(N)]
add(jobs)
add([(ri(0, 20) * 1000, ri(1, 10)) for _ in range(N)])
jobs = [(0, ri(2, 20)) for _ in range(N // 2)] + [(ri(0, 2 * 10**6), 1) for _ in range(N // 2)]
random.shuffle(jobs)
add(jobs)
jobs = [(ri(0, 1000), ri(1, 5)) for _ in range(N // 3)] + \
       [(ri(10**6, 10**6 + 1000), ri(1, 5)) for _ in range(N // 3)] + \
       [(MAXV, 1) for _ in range(N - 2 * (N // 3))]
random.shuffle(jobs)
add(jobs)
M = 130_000
add([(ri(0, MAXV), ri(MAXV - 10**6, MAXV)) for _ in range(M)])
add([(MAXV - i, MAXV - ri(0, 2)) for i in range(M)])
jobs = [(ri(0, 99), ri(1, 3)) for _ in range(N - 1)] + [(MAXV, 1)]
add(jobs)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

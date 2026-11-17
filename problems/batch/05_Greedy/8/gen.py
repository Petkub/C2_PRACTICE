# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30108)
MAXN = 200_000
MAXSUM = 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(jobs):
    n = len(jobs)
    assert 1 <= n <= MAXN
    assert all(t >= 1 and w >= 1 for t, w in jobs)
    assert sum(t for t, _ in jobs) <= MAXSUM
    assert sum(w for _, w in jobs) <= MAXSUM
    tests.append(f"{n}\n" + "".join(f"{t} {w}\n" for t, w in jobs))


def rnd(n, tlo, thi, wlo, whi):
    return [(ri(tlo, thi), ri(wlo, whi)) for _ in range(n)]


def mixed(n, nbig, big_lo, big_hi, small_hi):
    jobs = [(ri(big_lo, big_hi), ri(big_lo, big_hi)) for _ in range(nbig)]
    jobs += [(ri(1, small_hi), ri(1, small_hi)) for _ in range(n - nbig)]
    random.shuffle(jobs)
    return jobs


add([(3, 1), (1, 3), (2, 2)])
add([(1, 1), (4, 10)])
add([(10**9, 10**9)])
add([(2, 1), (6, 3), (4, 2)])
add([(5, 2), (3, 7), (8, 8), (1, 1), (6, 4), (2, 9)])
add([(4, 1), (4, 5), (4, 3), (4, 2), (4, 4)])

add([(1, 2), (2, 1)])
for n in (6, 10, 14, 18, 20):
    add(rnd(n, 1, 20, 1, 20))
add(rnd(20, 1, 10**7, 1, 10**7))
add([(ri(1, 3), ri(1, 3)) for _ in range(20)])
add([(400_000_000, 399_999_999), (400_000_001, 400_000_000), (199_999_999, 199_999_998)])
add(rnd(2000, 1, 1000, 1, 1000))

N = MAXN
add(rnd(N, 1, 5000, 1, 5000))
add(rnd(N, 1, 9000, 1, 9000))
add([(5000, 5000)] * N)
add([(5000, 1)] * (N // 2) + [(1, 5000)] * (N // 2))
add([((N - i) // 40 + 1, i // 40 + 1) for i in range(N)])
add(rnd(N, 1, 10, 1, 9000))
add(rnd(N, 1, 9000, 1, 10))
add(mixed(N, 1000, 100_000, 400_000, 2000))
add(mixed(N, 1500, 200_000, 300_000, 1000))
add(mixed(N, 2, 100_000_000, 400_000_000, 1000))
jobs = [(ri(1, 4000), 0) for _ in range(N)]
jobs = [(t, max(1, t + ri(-3, 3))) for t, _ in jobs]
add(jobs)
k = 499_000_000
add([(k + 1, k), (k, k - 1)] + rnd(N - 2, 1, 4, 1, 4))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

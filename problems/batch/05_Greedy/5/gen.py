# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(3004)
MAXN, MAXK, MAXT = 200_000, 200_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, t):
    n = len(t)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK
    assert all(1 <= x <= MAXT for x in t)
    tests.append(f"{n} {k}\n" + " ".join(map(str, t)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


add(2, [4, 1, 3, 2, 5])
add(1, [7, 2, 4])
add(5, [3, 3, 3])
add(1, [1000000])
add(3, [8, 1, 6, 2, 9, 4])
add(2, [5, 5, 1, 7, 3, 2, 6])

add(1, [1])
add(4, [2, 9])
add(1, [3, 1, 2, 5, 4, 8, 6, 7])
add(2, [10, 1, 1, 1, 1, 10])
add(3, [7, 7, 7, 7, 7, 7, 7])
add(8, [5, 4, 3, 2, 1, 6, 7, 8])
add(7, [9, 8, 7, 6, 5, 4, 3, 2])
add(3, rnd(8, 1, 20))
add(4, rnd(8, 1, 100))
add(2, rnd(8, 1, MAXT))
add(5, rnd(6, 1, 10))

add(3, rnd(100, 1, 1000))
add(17, rnd(1000, 1, MAXT))
add(400, rnd(3000, 1, MAXT))

N = MAXN
add(1, [MAXT] * N)
add(1, rnd(N, 1, MAXT))
add(2, rnd(N, 1, MAXT))
add(N // 2, rnd(N, 1, MAXT))
add(N // 3 + 1, rnd(N, 1, 1000))
add(N - 1, rnd(N, 1, MAXT))
add(N, rnd(N, 1, MAXT))
add(MAXK, rnd(N // 2, 1, MAXT))
add(30_000, sorted(rnd(N, 1, MAXT)))
add(60_000, sorted(rnd(N, 1, MAXT), reverse=True))
add(99_999, [MAXT] * N)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(20212)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def add(L, a):
    n = len(a)
    assert 1 <= L <= n <= MAXN
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n} {L}\n" + " ".join(map(str, a)) + "\n")


def bumpy(n, period):
    return [ri(-MAXA, MAXA) // 4 + (MAXA // 2 if (i // period) % 3 == 0 else -MAXA // 2) for i in range(n)]


add(2, [3, -1, 4, 1, 5])
add(3, [-1, -2, -2])
add(1, [2, 7, -3, 7])
add(1, [-MAXA])
add(2, [10, 0, 10])
add(3, [-4, 6, -2, 5, 5, -9, 3])

add(1, [MAXA])
add(2, [-1, 0])
add(4, [-7, -7, -7, -7, -7])
add(3, rnd(10, -10, 10))
add(5, rnd(40, -100, 100))
add(17, rnd(100, -MAXA, MAXA))
add(60, rnd(300, -1000, 1000))
add(100, [MAXA, -MAXA] * 100)
add(250, rnd(800, -MAXA, -MAXA + 1000))
add(1, rnd(500, -5, 5))

N = MAXN
add(N // 2, rnd(N, -MAXA, MAXA))
add(N // 3, rnd(N, -MAXA, MAXA))
add(N // 10, bumpy(N, 30_000))
add(15_000, bumpy(N, 6000))
add(N // 8, bumpy(N, 10_000))
add(N // 4, [MAXA] * N)
add(N // 2 + 1, [-MAXA] * N)
add(N, rnd(N, -MAXA, MAXA))
add(N // 5, rnd(N, -3, 2))
add(N // 2, sorted(rnd(N, -MAXA, MAXA)))
add(N // 3, sorted(rnd(N, -MAXA, MAXA), reverse=True))
a = rnd(N, -MAXA, -MAXA // 2)
add(N // 6, a)
add(7, rnd(N, -MAXA, MAXA))
a = [ri(-10, 10) for _ in range(N)]
add(N // 2 - 1, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

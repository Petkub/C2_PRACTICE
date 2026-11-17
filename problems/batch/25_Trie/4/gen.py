# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(250004)
MAXN, MAXV = 200_000, (1 << 20) - 1
tests = []


def add(a, k):
    n = len(a)
    assert 1 <= n <= MAXN and len(k) == n
    assert all(0 <= x <= MAXV for x in a + k)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, k)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


add([5, 1, 7], [4, 6, 3])
add([0, 0, 0], [9, 2, 9])
add([7], [7])
add([12, 3, 3, 8], [1, 15, 3, 9])
add([6, 0, 11, 6, 2], [6, 13, 2, 4, 6])

add([0, 1], [1, 0])
add(rnd(10, 0, 15), rnd(10, 0, 15))
add(rnd(100, 0, 7), rnd(100, 0, 7))
add(rnd(1000, 0, MAXV), rnd(1000, 0, MAXV))
add(rnd(3000, 0, 1023), rnd(3000, 0, 1023))
a = rnd(2000, 0, MAXV)
add(a, random.sample(a, len(a)))

N = MAXN
add(rnd(N, 0, MAXV), rnd(N, 0, MAXV))
a = rnd(N, 0, MAXV)
add(a, random.sample(a, N))
add([MAXV] * N, rnd(N, 0, MAXV))
add(rnd(N, 0, MAXV), [random.choice([0, MAXV])] * N)
add(rnd(N, 0, 63), rnd(N, 0, 63))
add(rnd(N, 0, (1 << 10) - 1), rnd(N, (1 << 19), MAXV))
add(sorted(rnd(N, 0, MAXV)), sorted(rnd(N, 0, MAXV), reverse=True))
a = rnd(N, 0, MAXV)
add(a, [x ^ random.choice([1, 2, 4, 1 << 15]) for x in a])
add([random.randint(0, 3) << 18 for _ in range(N)], rnd(N, 0, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

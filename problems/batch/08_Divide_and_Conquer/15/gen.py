# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90902)
MAXN = 200_000
MAXV = 10**6
tests = []


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= v <= MAXV for v in a)
    tests.append(f"{n}\n{' '.join(map(str, a))}\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def walk(n, step):
    a, v = [], MAXV // 2
    for _ in range(n):
        v = min(MAXV, max(1, v + random.randint(-step, step)))
        a.append(v)
    return a


add([1, 3, 2])
add([2, 5, 5, 1])
add([7])
add([1, 2, 3, 4, 5])
add([6, 2, 9, 4, 4, 1, 8, 3])

add([1, MAXV])
add([MAXV] * 7)
add(rnd(10, 1, 10))
add(rnd(100, 1, 3))
add(rnd(1000, 1, MAXV))
add(walk(5000, 100))
add(rnd(20000, 1, MAXV))
add([MAXV if i % 2 else 1 for i in range(25000)])

N = MAXN
add(rnd(N, 1, MAXV))
add([MAXV if i % 2 else 1 for i in range(N)])
add(list(range(1, N + 1)))
add(list(range(MAXV, MAXV - N, -1)))
add([MAXV] * N)
a = rnd(N, 1, 2)
a[N // 2] = 3
add(a)
a = rnd(N, 2, 10)
a[N // 3], a[2 * N // 3] = 1, 11
add(a)
add([min(i, N - i) * 5 + 1 for i in range(N)])
add([MAXV - min(i, N - i) * 5 for i in range(N)])
add(walk(N, 1000))
add([(i % 500) * 2000 + 1 for i in range(N)])
add(sorted(rnd(N // 2, 1, MAXV)) + sorted(rnd(N // 2, 1, MAXV), reverse=True))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(50002)
MAXN = 200000
MAXV = 10 ** 9
tests = []


def add(v, d):
    n = len(v)
    assert 1 <= n <= MAXN and len(d) == n
    assert all(0 <= x <= MAXV for x in v)
    assert all(1 <= x <= MAXV for x in d)
    tests.append(f"{n}\n{' '.join(map(str, v))}\n{' '.join(map(str, d))}\n")


def falling(n, top, step, noise, dmax):
    v = [top - i * step - random.randint(0, noise) for i in range(n)]
    d = [random.randint(1, dmax) for _ in range(n)]
    return v, d


def rounding_trap(v, d, first):
    v[-1], d[-1] = 1000, 1
    v[-2], d[-2] = 1999, 1000
    d[first] = 1001
    v[first] = 1000 + 1001 * random.randint(1, 900000)


add([7, 3, 9, 8, 12], [2, 1, 2, 3, 5])
add([6, 5, 1, 4], [2, 3, 3, 1])
add([0, 2, 2, 5, 5, 9], [3, 1, 4, 2, 7, 1])
add([4, 3, 8], [5, 1, 2])
add([13, 5, 21, 7, 9, 11, 20], [2, 4, 1, 2, 3, 1, 6])
add([20, 11, 15, 15, 30, 25], [4, 1, 6, 2, 9, 10])

add([0], [1])
add([5, 4, 3], [1, 1, 1])
add([9, 8, 7, 6, 5, 4, 3, 2], [1, 2, 1, 3, 1, 2, 1, 1])
add([30, 25, 24, 18, 17, 12, 11, 5, 9], [4, 3, 5, 2, 6, 1, 4, 2, 3])
v, d = [50, 40, 30, 1999, 1000], [7, 3, 1001, 1000, 1]
v[2] = 1000 + 1001 * 2
add(v, d)
for n, top in [(10, 60), (12, 200), (15, 400)]:
    v = sorted((random.randint(top // 2, top) for _ in range(n)), reverse=True)
    add(v, [random.randint(1, 6) for _ in range(n)])
add([random.randint(0, 40) for _ in range(14)], [random.randint(1, 5) for _ in range(14)])

v, d = falling(3000, 20000, 1, 0, 3)
add(v, d)
v = sorted(random.randint(0, MAXV) for _ in range(40000))
add(v, [random.randint(1, MAXV) for _ in range(40000)])

add([MAXV - i for i in range(MAXN)], [1] * MAXN)
add(*falling(MAXN, MAXV, 4000, 999, 100))
add(*falling(MAXN, MAXV, 4000, 3000, 999))
add(*falling(MAXN, MAXV, 4500, 200, 1))
v = [MAXV] * (MAXN // 2) + [MAXV - 3000 * i for i in range(1, MAXN - MAXN // 2 + 1)]
add(v, [random.randint(1, 50) for _ in range(MAXN)])
v, d = falling(MAXN, MAXV, 4000, 999, 100)
v[-1] = 0
add(v, d)
v, d = falling(MAXN, MAXV, 4000, 999, 100)
rounding_trap(v, d, 0)
add(v, d)
v, d = falling(MAXN, MAXV, 4000, 999, 100)
rounding_trap(v, d, MAXN // 2)
add(v, d)
v, d = falling(MAXN, MAXV, 2000, 1500, 20)
for i in range(0, MAXN, 5):
    v[i:i + 5] = sorted(v[i:i + 5])
add(v, d)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

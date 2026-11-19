# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4806)
MAXN, MAXB = 200000, 10**9
tests = []


def add(b):
    n = len(b)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXB for x in b)
    tests.append(f"{n}\n" + " ".join(map(str, b)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def heavy_tail(n, light, tail_lo, tail_hi, draws):
    for _ in range(draws):
        k = random.randint(2, 4)
        b = rnd(n - k, 1, light) + rnd(k, tail_lo, tail_hi)
    return b


add([3, 5, 2, 11, 10])
add([1, 6, 10, 7])
add([5])
add([4, 8, 6, 1, 6, 3])
add([MAXB, MAXB, 1])

add([1])
add([1, 1, 1, 20, 17])
add(rnd(8, 1, 10))
add(rnd(10, 1, 3))
add(rnd(12, 1, MAXB))
add([1] * 6 + [100] + [1] * 3)
add(rnd(30, 1, 50))
add(heavy_tail(12, 2, 6, 40, 8))
add(heavy_tail(40, 3, 30, 200, 9)[::-1])

add(rnd(1500, 1, 1000))
add(rnd(3000, 1, MAXB))

N = MAXN
add([MAXB] * N)
add(rnd(N, 1, MAXB))
add(rnd(N, 1, 10))
add(sorted(rnd(N, 1, MAXB)))
add(sorted(rnd(N, 1, MAXB), reverse=True))


def walls(n, seg, lo, hi, wall_lo):
    b = []
    while len(b) < n:
        b += rnd(random.randint(1, seg), lo, hi)
        b.append(random.randint(wall_lo, MAXB))
    return b[:n]


add([random.choice([1, MAXB]) for _ in range(N)])
add(walls(N, 2000, 1, 10**5, MAXB - 10**6))
add(walls(N, 30000, 1, 10**4, 10**8)[::-1])
b = walls(N, 5000, 1, 1000, 10**7)
b[N // 2:] = rnd(N - N // 2, MAXB // 2, MAXB)
add(b[::-1])
add(heavy_tail(N, 2, N // 2, 3 * N, 2))
add(heavy_tail(N, 3, N, 4 * N, 10))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

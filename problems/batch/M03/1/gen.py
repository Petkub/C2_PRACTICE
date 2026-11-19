# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43001)
MAXN, MAXF = 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(f, a, b):
    n = len(a)
    assert 1 <= n <= MAXN and len(b) == n and 1 <= f <= MAXF
    assert all(0 <= x < f for x in a) and all(0 <= x < f for x in b)
    tests.append(f"{n} {f}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def rnd(n, f, alo=0, ahi=None, blo=0, bhi=None):
    ahi = f - 1 if ahi is None else ahi
    bhi = f - 1 if bhi is None else bhi
    a = [ri(alo, ahi) for _ in range(n)]
    b = [ri(blo, bhi) for _ in range(n)]
    return a, b


def mix(n, f, k):
    a, b = rnd(k, f, f // 5, f // 2, f * 4 // 7, f * 4 // 5)
    a2, b2 = rnd(n - k, f, f // 2, f - 1, 0, f // 2)
    a, b = a + a2, b + b2
    random.shuffle(a)
    random.shuffle(b)
    return a, b


add(10, [2, 6, 4], [7, 3, 8])
add(100, [50, 60], [40, 70])
add(20, [15, 0, 10, 5], [19, 18, 18, 19])
add(20, [5, 2, 4, 9, 15], [5, 1, 2, 19, 17])
add(10**9, [0, 999_999_999, 500_000_000], [999_999_999, 999_999_999, 750_000_000])


add(1, [0], [0])
add(7, [6], [6])
add(10, [0, 5], [8, 5])
for n, f in [(6, 10), (8, 20), (10, 7), (40, 100), (150, 1000), (400, 10**9)]:
    a, b = rnd(n, f)
    add(f, a, b)
a, b = mix(500, 10**6, 300)
add(10**6, a, b)
a, b = rnd(1000, 50)
add(50, a, b)


N = MAXN
a, b = rnd(N, MAXF)
add(MAXF, a, b)
a, b = rnd(N, MAXF, 0, MAXF - 1, MAXF // 2, MAXF - 1)
add(MAXF, a, b)
a, b = mix(N, MAXF, N * 3 // 4)
add(MAXF, a, b)
a, b = rnd(N, MAXF, MAXF // 5, MAXF // 2, MAXF * 4 // 7, MAXF * 4 // 5)
add(MAXF, a, b)
add(MAXF, [MAXF - 2] * N, [MAXF - 1] * N)
a = list(range(0, N))
b = [ri(MAXF // 2 - 2 * N, MAXF - 1) for _ in range(N)]
random.shuffle(a)
add(MAXF, a, b)
a, b = rnd(N, MAXF, MAXF // 2, MAXF - 1, 0, MAXF // 2)
add(MAXF, a, b)
a, b = rnd(N, 1000)
add(1000, a, b)
x = [ri(0, MAXF - 1) for _ in range(N)]
a = x[:]
b = [min(MAXF - 1, max(0, v + ri(-1000, 2000))) for v in x]
random.shuffle(b)
add(MAXF, a, b)
a, b = rnd(N, MAXF, 0, MAXF // 3, MAXF // 2, MAXF * 2 // 3)
add(MAXF, a, b)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

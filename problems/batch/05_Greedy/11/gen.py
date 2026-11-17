# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(5009)
MAXN, MAXK, MAXD, MAXC = 200_000, 10**9, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(K, D, x, c):
    n = len(x)
    assert 1 <= n <= MAXN and len(c) == n
    assert 1 <= K <= MAXK and 2 <= D <= MAXD
    assert 0 < x[0] and x[-1] < D and all(x[i] < x[i + 1] for i in range(n - 1))
    assert all(1 <= v <= MAXC for v in c)
    tests.append(f"{n} {K} {D}\n" + " ".join(map(str, x)) + "\n" + " ".join(map(str, c)) + "\n")


def positions(n, D):
    if n * 3 > D:
        return sorted(random.sample(range(1, D), n))
    s = set()
    while len(s) < n:
        s.add(ri(1, D - 1))
    return sorted(s)


def slow_start(x, c, k, gap):
    first = [gap * (i + 1) for i in range(k)]
    rest = [v + first[-1] for v in x]
    return first + rest, [1] * k + c


add(2, 10, [2, 3, 5, 7, 8], [1, 1, 1, 1, 1])
add(3, 12, [3, 6, 7, 9], [1, 5, 1, 1])
add(1, 20, [4, 9, 15], [2, 1, 3])
add(4, 30, [5, 8, 12, 17, 21, 26], [2, 3, 1, 4, 1, 2])
add(5, 40, [3, 7, 10, 16, 19, 25, 31, 34], [2, 4, 1, 3, 2, 5, 1, 2])
add(3, 50, [10, 20, 30, 40, 45], [3, 3, 3, 3, 3])

add(1, 2, [1], [1])
add(2, 2, [1], [1])
add(10, 100, [10, 50, 90], [3, 4, 2])
add(3, 20, [2, 4, 6, 8, 11, 13, 15, 17], [1, 1, 1, 1, 1, 1, 1, 1])
x, c = slow_start([3, 5, 6, 8, 9, 12, 14], [2, 2, 3, 1, 2, 2, 3], 2, 9)
add(3, x[-1] + 4, x, c)
for n, D, K, C in [(10, 40, 2, 2), (15, 200, 5, 4), (40, 1000, 7, 3), (300, 10**6, 20, 5),
                   (2000, 10**9, 300, 2 * 10**8)]:
    x = positions(n, D)
    add(K, D, x, [ri(1, C) for _ in range(n)])
x = positions(3000, 10**7)
x, c = slow_start(x, [ri(1, 10) for _ in x], 20, 4000)
add(40, x[-1] + 1000, x, c)

N = MAXN
x = positions(N, MAXD)
add(1000, MAXD, x, [ri(1, 3) for _ in range(N)])
x = positions(N, 10**8)
add(10**7, 10**8, x, [ri(1, 30_000) for _ in range(N)])
x = positions(N, 10**8)
add(10**6, 10**8, x, [ri(1, 40_000) for _ in range(N)])
x = positions(N, MAXD)
add(100_000, MAXD, x, [1] * N)
x = positions(N, 10**7)
add(10**6, 10**7, x, [10**6] * N)
x = positions(N, MAXD)
add(MAXK, MAXD, x, [ri(1, 9999) for _ in range(N)])
x = positions(N - 300, 9 * 10**8)
x, c = slow_start(x, [ri(1, 5) for _ in x], 300, 300_000)
add(2000, MAXD, x, c)
x = positions(N - 50, 9 * 10**7)
x, c = slow_start(x, [ri(1, 30_000) for _ in x], 50, 200_000)
add(500_000, 10**8, x, c)
x = positions(N, MAXD)
c = [5 * 10**8 if random.random() < 0.01 else ri(1, 2) for _ in range(N)]
add(5 * 10**8, MAXD, x, c)
x = [4999 * (i + 1) for i in range(N)]
add(1999, 4999 * (N + 1), x, [1 + (i % 3 == 0) for i in range(N)])
x = []
for k in range(40):
    base = 10**7 + k * 2 * 10**7
    x += [base + 37 * j + ri(0, 30) for j in range(N // 40)]
add(3000, MAXD, x, [ri(1, 4) for _ in range(N)])
x = positions(N, 10**8)
add(MAXK, 10**8, x, [ri(1, 99_999) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

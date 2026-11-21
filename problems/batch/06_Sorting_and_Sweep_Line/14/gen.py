# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(61406)
MAXN = 200_000
MAXK = 10 ** 9
MAXV = 10 ** 9
tests = []
rnd = random.random


def ri(lo, hi):
    return lo + int(rnd() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK
    assert all(1 <= v <= MAXV for v in a)
    tests.append(f"{n} {k}\n{' '.join(map(str, a))}\n")


def vals(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def perm(n):
    a = list(range(1, n + 1))
    random.shuffle(a)
    return a


def blocks(n, size, lo, hi):
    a = []
    while len(a) < n:
        b = vals(min(size, n - len(a)), lo, hi)
        a.extend(sorted(b, reverse=True))
    return a


def drift(n, back):
    a = [i * 10 for i in range(1, n + 1)]
    for i in range(n - 1, 0, -1):
        if rnd() < 0.5:
            j = max(0, i - ri(0, back))
            a[i], a[j] = a[j], a[i]
    return a


add(2, [5, 1, 4, 2, 3])
add(3, [2, 2, 1])
add(3, [1, 5, 5, 3, 2, 4, 2, 2])
add(5, [48, 35, 18, 24, 87, 1, 44, 65, 60])
add(3, [3, 3, 3, 1, 1, 1, 2, 2])
add(3, [76, 73, 100, 89, 12, 45, 15, 75])


add(1, [7])
add(1, [MAXV, 1])
add(4, vals(10, 1, 3))
add(2, vals(12, 1, 5))
add(6, perm(12))
add(MAXK, list(range(12, 0, -1)))


add(1, vals(2000, 1, 10))
add(30, perm(2000))
add(700, list(range(3000, 0, -1)))
add(50, vals(3000, 1, 4))
add(2, drift(3000, 5))


N = MAXN
add(50_000, perm(N))
add(100_000, vals(N, 1, MAXV))
add(150_000, vals(N, 1, 3))
add(N // 2, list(range(N, 0, -1)))
add(N - 1, list(range(N, 0, -1)))
add(30_000, vals(N, 1, 1000))
add(60_000, blocks(N, 1000, 1, 10 ** 6))
add(40_000, blocks(N, 50_000, 1, 30))
add(25_000, [MAXV - ri(0, 5) for _ in range(N)])
add(80_000, [ri(N - i, N - i + 2000) for i in range(N)])
add(20_000, drift(N, 60_000))
add(120_000, perm(N // 2) + perm(N // 2))
add(35_000, [MAXV] * (N // 4) + vals(N - N // 4, 1, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

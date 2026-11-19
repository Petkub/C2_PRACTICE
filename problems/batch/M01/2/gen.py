# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4101)
MAXN, MAXV = 200000, 10**9
tests = []


def add(k, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN
    assert all(0 <= x <= MAXV for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def spaced(n, k, lowmax, highmin, jitter):
    a = rnd(n, highmin, MAXV)
    i = random.randint(1, k)
    while i <= n:
        a[i - 1] = random.randint(0, lowmax)
        i += random.randint(max(1, k - jitter), k + jitter)
    return a


def no_low_near_banks(n, k):
    a = rnd(n, 0, 1000)
    for i in range(k + k // 3):
        a[i] = random.randint(MAXV // 2, MAXV)
        a[n - 1 - i] = random.randint(MAXV // 2, MAXV)
    return a


add(3, [2, 7, 5, 9, 4, 8, 6, 1])
add(5, [6, 3, 8, 3, 7])
add(1, [0])
add(1, [10, 1000000000, 3, 7])
add(3, [4, 1, 9, 9, 2, 6, 5, 9, 3, 8])

add(2, [5, 1, 5, 1, 5, 1, 5])
add(3, [1, 9, 9, 9, 9, 9, 1])
add(4, rnd(15, 0, 20))
add(1, rnd(12, 0, MAXV))
add(6, [MAXV] * 30)
add(50, rnd(300, 0, 10**6))
add(7, spaced(2000, 7, 100, 10**6, 2))
add(300, no_low_near_banks(5000, 300))

N = MAXN
add(N, rnd(N, 0, MAXV))
add(N // 2, spaced(N, N // 2, 10**6, MAXV // 2, 3000))
add(110000, spaced(N, 110000, MAXV // 2, MAXV // 2, 500))
add(130000, no_low_near_banks(N, 60000))
add(120000, [MAXV] * N)
add(100000, sorted(rnd(N, 0, MAXV)))
add(100000, sorted(rnd(N, 0, MAXV), reverse=True))
add(110000, [MAXV - (i % 110000) for i in range(N)])
add(100000, spaced(N, 100000, MAXV, 0, 20000))
add(100000, no_low_near_banks(N, 100000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

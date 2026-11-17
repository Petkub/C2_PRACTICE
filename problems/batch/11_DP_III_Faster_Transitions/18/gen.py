# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11019)
MAXN, MAXK, MAXV = 100_000, 400, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(K, A, B, a, p):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= K <= min(n, MAXK) and len(p) == K and 1 <= A <= B <= n
    assert all(1 <= x <= MAXV for x in a) and all(1 <= x <= MAXV for x in p)
    tests.append(f"{n} {K} {A} {B}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo=1, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


add(2, 1, 3, [4, 1, 5, 2, 3], [2, 5])
add(2, 1, 3, [1, 1, 1, 1, 1, 1, 1], [1, 1])
add(3, 2, 2, [5, 3, 8, 1, 2, 9], [3, 1, 2])
add(1, 1, 4, [7, 7, 7, 7], [10])
add(3, 1, 4, [6, 2, 9, 4, 1, 8, 3, 5], [1, 4, 2])
add(4, 2, 3, [9, 1, 1, 9, 9, 1, 1, 9, 2, 7], [5, 1, 5, 2])

add(1, 1, 1, [MAXV], [MAXV])
add(3, 2, 5, rnd(9, 1, 9), rnd(3, 1, 9))
add(4, 3, 5, rnd(11, 1, 9), rnd(4, 1, 9))
add(5, 1, 3, rnd(12, 1, 100), rnd(5, 1, 100))
add(6, 1, 12, rnd(12), rnd(6))
add(4, 2, 4, rnd(12, 1, 5), [1, 100, 1, 100])

add(30, 10, 200, rnd(2000), rnd(30))
add(100, 1, 60, rnd(3000, 1, 1000), rnd(100, 1, 1000))
add(400, 50, 50, rnd(20_000), rnd(400))
add(400, 51, 60, rnd(20_000), rnd(400))
add(400, 49, 51, rnd(20_000), rnd(400))

N, K = MAXN, MAXK
add(K, 1, N, rnd(N), rnd(K))
add(K, 1, N, [MAXV] * N, [MAXV] * K)
add(K, 100, 1000, rnd(N), rnd(K))
add(K, 150, 300, rnd(N), sorted(rnd(K)))
add(K, 1, 400, rnd(N), sorted(rnd(K), reverse=True))
add(K, 100, 600, rnd(N, MAXV - 1000, MAXV), rnd(K, MAXV - 1000, MAXV))
add(K, 1, 240, rnd(N), rnd(K))
add(K, 1, 249, rnd(N), rnd(K))
add(K, 240, 400, rnd(N), rnd(K))
add(300, 1, 5000, rnd(N, 1, 10), rnd(300))
add(K, 50, 2000, [MAXV if i % 977 < 5 else 1 for i in range(N)], rnd(K))
add(K, 1, N // 2, rnd(N), [MAXV if d % 2 else 1 for d in range(K)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

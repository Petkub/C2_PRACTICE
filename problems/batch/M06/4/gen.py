# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4605)
MAXN, MAXV = 300000, 10**6
tests = []


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= k <= MAXV and all(1 <= x <= MAXV for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def walk(n, k, steps, weights=None):
    return [k + random.choices(steps, weights)[0] for _ in range(n)]


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


add(5, [3, 7, 4, 9, 9, 3, 3])
add(10, [1, 2, 3])
add(3, [1, 5, 2, 4])
add(MAXV, [MAXV] * 4)
add(4, [4, 2, 9, 1, 8, 5, 2, 6, 6])

add(1, [1])
add(2, [1])
add(5, [1, 9, 5, 5, 1, 9])
add(3, walk(12, 3, [-2, -1, 0, 1, 2]))
add(4, walk(30, 4, [-3, -1, 1, 3]))
add(7, walk(200, 7, [-3, -2, -1, 0, 1, 2, 3]))
add(50, walk(2000, 50, list(range(-5, 6))))
add(500000, walk(20000, 500000, [-2, -1, 1, 2]))
add(3, rnd(30000, 1, 6))

N = MAXN
K = MAXV // 2
add(K, walk(N, K, [-1, 0, 1]))
add(K, walk(N, K, [-3, -2, -1, 0, 1, 2, 3]))
add(K, walk(N, K, [-1, 1]))
add(MAXV, [MAXV] * N)
add(MAXV, walk(N, MAXV, [-2, -1, 0], [1, 1, 3]))
add(1, walk(N, 1, [0, 1, 2], [5, 2, 1]))
add(K, rnd(N, 1, MAXV))
add(K, walk(N, K, [-1, 0, 1], [10, 9, 11]))
add(K, walk(N, K, [-K + 1, -1, 0, 1, K], [1, 300, 300, 300, 1]))
a = walk(N, K, [-1, 1])
for i in range(0, N, 1000):
    a[i] = random.choice([1, MAXV])
add(K, a)
add(1000, walk(N, 1000, [-999, 0, 999], [1, 2, 1]))
add(K, walk(N, K, list(range(-10, 11))))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

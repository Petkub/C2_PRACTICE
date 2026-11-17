# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(160011)
MAXN, MAXS, MAXA = 200_000, 10**15, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(s, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= s <= MAXS and all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n} {s}\n" + " ".join(map(str, a)) + "\n")


def best_sum(a):
    cur, best = 0, -10**30
    for x in a:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


add(7, [3, -2, 5, -1, 4, 2, 1])
add(5, [-1, 2, -3])
add(1, [1])
add(10, [6, -10, 5, 5, -1, 6])
add(9, [4, -1, -1, 4, 3, -5, 9, 1])

add(1, [-5])
add(3, [ri(-3, 3) for _ in range(12)])
add(40, [ri(-10, 12) for _ in range(300)])
add(5 * 10**9, [ri(-MAXA, MAXA) for _ in range(2000)])
a = [ri(-100, 101) for _ in range(5000)]
add(best_sum(a), a)
a = [ri(-MAXA, MAXA) for _ in range(10000)]
add(best_sum(a) + 1, a)

N = MAXN
a = [ri(-MAXA, MAXA) for _ in range(N)]
add(best_sum(a), a)
add(best_sum(a) + 1, a)
a = [ri(-1000, 1001) for _ in range(N)]
add(best_sum(a), a)
a = [ri(-1000, 1001) for _ in range(N)]
add(best_sum(a) - 5000, a)
add(MAXS, [MAXA] * N)
add(MAXA * (N - 3), [MAXA] * N)
a = [MAXA if i % 2 == 0 else -MAXA + 1 for i in range(N)]
add(best_sum(a), a)
a = []
while len(a) < N - 1000:
    v = ri(1, MAXA // 2)
    a += [v, -v]
a += [ri(-MAXA, MAXA) for _ in range(1000)]
add(max(ri(10**9, 3 * 10**9), best_sum(a[-1000:]) - ri(0, 10**9)), a)
a = [-MAXA] * N
for k in range(0, N, 50000):
    a[k] = MAXA
a[N - 2] = a[N - 1] = MAXA
add(2 * MAXA, a)
a = [ri(-5, 4) for _ in range(N)]
add(best_sum(a), a)
a = [-1] * N
for k in range(N - 100, N):
    a[k] = 1000
add(100_000 - 50, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

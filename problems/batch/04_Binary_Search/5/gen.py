# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(20205)
MAXN = 200_000
MAXA = 10**9
MAXK = 10**15
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= k <= MAXK
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def pieces(a, L):
    return sum(x // L for x in a)


def aim(a, L, extra=0):
    return max(1, pieces(a, L) + extra)


add(5, [10, 15, 7])
add(6, [3, 2])
add(1, [MAXA])
add(3 * MAXA, [MAXA] * 3)
add(4, [7, 7, 7])
add(10, [100, 1, 35, 64])

add(1, [1])
add(2, [1])
a = [ri(1, 50) for _ in range(10)]
add(aim(a, 7), a)
a = [ri(1, 1000) for _ in range(300)]
add(aim(a, 37, 1), a)
a = [ri(1, 3000) for _ in range(2000)]
add(sum(a), a)
add(sum(a) + 1, a)
a = [ri(1, 3000) for _ in range(2000)]
add(len(a) + 1, a)
add(len(a) // 2, [2999] * 2000)

N = MAXN
add(N + 1, [MAXA] * N)
add(N * 3 + 1, [MAXA] * N)
a = [ri(1, MAXA) for _ in range(N)]
add(aim(a, 123_456_789), a)
a = [ri(1, MAXA) for _ in range(N)]
add(aim(a, 300_000_007, 1), a)
a = [ri(MAXA // 2, MAXA) for _ in range(N)]
add(aim(a, 49_999_999), a)
a = [ri(1, MAXA) for _ in range(N)]
add(aim(a, 10_000_019), a)
a = [ri(1, 10**6) for _ in range(N)] + [MAXA]
a = a[:N]
a[ri(0, N - 1)] = MAXA
add(aim(a, 600_000), a)
add(sum([MAXA] * N), [MAXA] * N)
add(MAXK, [MAXA] * N)
a = [ri(1, MAXA) for _ in range(N)]
add(1, a)
a = [ri(1, MAXA) for _ in range(N)]
add(aim(a, 3), a)
add(2 * N + 1, [MAXA - 1] * (N - 1) + [MAXA])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

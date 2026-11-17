# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30909)
MAXN, MAXA, MAXS = 200_000, 10**9, 10**15
tests = []


def add(k, s, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN and 0 <= s <= MAXS
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n} {k} {s}\n" + " ".join(map(str, a)) + "\n")


def windows(a, k):
    out, cur = [], sum(a[:k])
    out.append(cur)
    for i in range(k, len(a)):
        cur += a[i] - a[i - k]
        out.append(cur)
    return out


def with_heavy(a, k, t):

    w = sorted(windows(a, k), reverse=True)
    if t >= len(w):
        return max(0, w[-1] - 1)
    return w[t]


def vals(n, lo=0, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]


add(2, 10, [3, 8, 1, 2, 9, 4, 0])
add(1, 5, [6, 2, 7, 7, 1])
add(1, 0, [1, 1, 1])
add(3, 100, [10, 20, 30, 40])
add(2, 10**9, [6 * 10**8, 0, 6 * 10**8, 6 * 10**8, 0])

for n, k in [(8, 3), (12, 4), (20, 1), (25, 5), (40, 7), (60, 2)]:
    a = vals(n, 0, 9)
    add(k, with_heavy(a, k, random.randint(0, 4)), a)
a = vals(80, 0, 9)
add(80, sum(a) - 1, a)
a = vals(90, 0, 3)
add(6, with_heavy(a, 6, 30), a)

a = vals(5000)
add(30, with_heavy(a, 30, 400), a)
a = [MAXA] * 3000
add(3, 3 * MAXA - 1, a)

a = vals(MAXN)
add(1000, MAXS, a)
a = vals(MAXN)
add(1000, with_heavy(a, 1000, 1), a)
a = vals(MAXN)
add(50_000, with_heavy(a, 50_000, 5), a)
a = vals(MAXN)
add(MAXN, sum(a) - 1, a)
a = vals(MAXN)
add(1, with_heavy(a, 1, 3), a)
a = vals(MAXN)
add(2, with_heavy(a, 2, 4), a)
a = [MAXA] * MAXN
add(100_000, 100_000 * MAXA - 1, a)
a = [random.choice([0, MAXA]) for _ in range(MAXN)]
add(3, with_heavy(a, 3, 0), a)
a = vals(MAXN, MAXA - 1000, MAXA)
add(7, with_heavy(a, 7, 2), a)
a = vals(MAXN, 0, 5)
add(150_000, with_heavy(a, 150_000, 10), a)
a = vals(MAXN)
add(20_000, with_heavy(a, 20_000, 8), a)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(45005)
MAXN, MAXM, MAXK = 200_000, 10**6, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(m, p, k):
    n = len(k)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM and len(p) == n - 1
    assert all(1 <= p[i - 2] < i for i in range(2, n + 1))
    assert all(0 <= v <= MAXK for v in k)
    tests.append(f"{n} {m}\n" + " ".join(map(str, p)) + "\n" + " ".join(map(str, k)) + "\n")


def rand_k(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def by_depth(p, base, step, noise):
    n = len(p) + 1
    d = [0] * (n + 1)
    for i in range(2, n + 1):
        d[i] = d[p[i - 2]] + 1
    return [max(0, min(MAXK, base + step * d[i] + ri(-noise, noise))) for i in range(1, n + 1)]


add(2, [1, 1, 2, 2], [3, 2, 4, 1, 2])
add(3, [1, 1, 2], [9, 2, 3, 4])
add(MAXM, [1], [MAXK, MAXK])
add(5, [1, 1, 1, 1, 1], [1, 3, 2, 4, 2, 2])
add(4, [1, 2, 3, 4], [2, 5, 3, 4, 8])
add(7, [1, 1], [0, 0, 0])

add(1, [1], [0, 5])
add(3, [1, 2], [5, 4, 3])
for n in (4, 5, 6, 6, 6):
    add(ri(1, 3), [ri(1, i - 1) for i in range(2, n + 1)], rand_k(n, 0, 9))

p = [ri(1, i - 1) for i in range(2, 41)]
add(20, p, by_depth(p, 10, 6, 5))
p = [ri(max(1, i - 5), i - 1) for i in range(2, 2001)]
add(30, p, by_depth(p, 1000, 50, 200))

N = MAXN
p = [ri(1, i - 1) for i in range(2, N + 1)]
add(MAXM, p, rand_k(N, 0, MAXK))
p = [ri(max(1, i - 3), i - 1) for i in range(2, N + 1)]
add(MAXM, p, by_depth(p, 10, 25, 400))
p = [i - 1 for i in range(2, N + 1)]
add(MAXM, p, rand_k(N, 0, MAXK))
p = [1] * (N - 1)
add(MAXM, p, [MAXK] * N)
p = [i // 2 for i in range(2, N + 1)]
add(MAXM, p, by_depth(p, 10, 30_000, 5_000))
p = [i // 2 for i in range(2, N + 1)]
add(MAXM, p, [MAXK] * N)
p = [i - 1 if i <= N // 2 else ri(1, N // 2) for i in range(2, N + 1)]
add(MAXM, p, by_depth(p, 2000, 10, 1500))
p = [ri(max(1, i - 50), i - 1) for i in range(2, N + 1)]
add(ri(1, MAXM), p, by_depth(p, 50, 8, 60))
p = [ri(1, min(i - 1, 300)) for i in range(2, N + 1)]
add(MAXM, p, by_depth(p, MAXK, -MAXK // 3, 20_000))
p = [ri(max(1, i - 2), i - 1) for i in range(2, N + 1)]
add(MAXM, p, rand_k(N, MAXK - 100, MAXK))
p = [1 if i <= 1001 else ri(2, 1001) for i in range(2, N + 1)]
k = [0] + [ri(0, 2 * MAXK // 10) for _ in range(1000)] + rand_k(N - 1001, 0, MAXK // 100)
k[0] = ri(MAXK // 2, MAXK)
add(MAXM, p, k)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3005)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def levels(n, sizes, blocked=False):
    """stone 1 reaches level 1; every stone of level k reaches exactly the end of level k+1 (long scans,
    few jumps). With blocked=True the last level cannot reach stone n."""
    ends = [1]
    for s in sizes:
        ends.append(ends[-1] + s)
    assert ends[-1] == n
    a = [0] * (n + 1)
    lvl = 0
    for i in range(1, n + 1):
        while ends[lvl] < i:
            lvl += 1
        if lvl + 1 < len(ends):
            a[i] = ends[lvl + 1] - i
    if blocked:
        for i in range(1, n):
            a[i] = min(a[i], n - 1 - i)
    return a[1:]


# samples
add([2, 3, 1, 1, 4, 0])
add([3, 2, 1, 0, 4])
add([0])
add([1, 1, 1, 1, 1])
add([2, 0, 3, 1, 0, 2, 5, 0])
add([10, 0, 0, 0])
# hidden: small
add([5])
add([0, 3])
add([1, 0])
add([1, 0, 1])
add([2, 0, 1, 0])
add([3, 0, 0, 0, 0])
add([1, 2, 0, 1, 1, 0, 0])
for n, hi in [(8, 2), (10, 3), (12, 2), (15, 4), (20, 3), (50, 5), (300, 6), (2000, 4)]:
    add(rnd(n, 1, hi))
for n, hi in [(10, 2), (30, 3), (200, 4)]:
    add(rnd(n, 0, hi))
add(rnd(5000, 0, 9) + [0])
# hidden: maximum size
N = MAXN
add([1] * N)                                        # N - 1 jumps
add([MAXA] * N)                                     # one jump
add([N - 1 - i for i in range(1, N)] + [0])         # everyone reaches stone N - 1 only: -1, long scans
add(levels(N, [N // 2, N // 2 - 2, 1]))             # 3 jumps, the middle level is huge
add(levels(N, [1, N // 3, N // 3, N - 1 - 1 - 2 * (N // 3)]))
add(levels(N, [N // 2, N // 2 - 2, 1], blocked=True))
add(levels(N, [N // 8] * 7 + [N - 1 - 7 * (N // 8)]))
add(rnd(N, 1, 3))
add(rnd(N, 1, 100000))
a = rnd(N, 1, 30000)
a[N // 2] = 0                                       # nobody gets past stone N / 2 + 1
for i in range(N // 2 - 30000, N // 2):
    a[i] = min(a[i], N // 2 - i)
add(a)
a = [ri(0, 1) * ri(1, MAXA) if ri(0, 99) == 0 else ri(1, 4) for _ in range(N)]
add(a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

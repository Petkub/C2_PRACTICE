# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20215)
MAXN, MAXA = 500_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([5, 2, 8, 3, 3, 9, 1])
add([6, 6, 6, 6])
add([9, 7, 4, 2, 1])
add([MAXA])
add([3, 1, 4, 1, 5, 9, 2, 6])
add([2, 5, 2, 5, 2, 5])
# hidden: small
add([1, 1])
add([2, 1])
add(rnd(10, 1, 5))
add(rnd(60, 1, 20))
add(rnd(300, 1, 3))
add(rnd(2000, 1, MAXA))
add(sorted(rnd(3000, 1, 50)))
add(rnd(30000, 1, 9))
# hidden: large (the number of tracks is large in most of them)
N = MAXN
add([7] * N)                                          # every wagon needs a new track
add(sorted(rnd(N, 1, 99)))                            # non-decreasing: N tracks
a = sorted(rnd(N, 1, 9))
for _ in range(2000):                                 # almost sorted
    i, j = ri(0, N - 1), ri(0, N - 1)
    a[i], a[j] = a[j], a[i]
add(a)
add([i // 2 * 2 + 2 - i % 2 for i in range(450_000)])     # 2 1 4 3 6 5 ...: N / 2 tracks
add([ri(1, 9) + i // 50 for i in range(N)])           # noisy staircase
add([max(1, 100_000 - i // 5) if i % 3 else 1 + i // 5 for i in range(N)])
add(rnd(N, 1, 9))                                     # random small values: many tracks
add([MAXA - i for i in range(300_000)])               # strictly decreasing: 1 track
add(rnd(300_000, 1, MAXA))                            # random: few tracks
add(rnd(N, 1, 16))
add([i // 2 + (i % 2) * 250_000 + 1 for i in range(N)])  # two interleaved rising runs
add([N - i // 3 if i % 3 == 0 else i + 1 for i in range(N)])
add([MAXA - (i % 2) * ri(0, 9) for i in range(280_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

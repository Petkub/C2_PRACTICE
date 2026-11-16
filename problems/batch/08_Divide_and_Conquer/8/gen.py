# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90801)
MAXN = 200_000
MAXV = 10**9
tests = []


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN and all(1 <= v <= MAXV for v in a)
    tests.append(f"{n}\n{' '.join(map(str, a))}\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def jitter_desc(n, swaps):
    """strictly decreasing, then some swaps of neighbours"""
    a = list(range(MAXV, MAXV - n, -1))
    for _ in range(swaps):
        i = random.randrange(n - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
    return a


# samples
add([3, 1, 2])
add([2, 2, 1])
add([7])
add([5, 4, 3, 2, 1])
add([4, 1, 7, 4, 2, 9, 3, 5])
# hidden: small (the brute force checks them)
add([2, 1])
add([1, 2])
add([5, 5, 5, 5, 5, 5])
add(rnd(10, 1, 10))
add(rnd(100, 1, 5))
add(rnd(1000, 1, MAXV))
add(rnd(5000, 1, 3))
add(rnd(20000, 1, MAXV))
add(list(range(25000, 0, -1)))
add([MAXV - i // 3 for i in range(25000)])
# hidden: large
N = MAXN
add(rnd(N, 1, MAXV))
add(list(range(MAXV, MAXV - N, -1)))                          # every pair counts
add(sorted(rnd(N, 1, 20000), reverse=True))                   # non-increasing, many ties
add(list(range(1, N + 1)))                                    # answer 0
add([MAXV] * N)                                               # answer 0
add(rnd(N, 1, 2))
add(rnd(N, 1, 10000))
add([MAXV - (i % 10000) for i in range(N)])                   # saw teeth
add(jitter_desc(N, N // 2))
add([MAXV - i if i % 2 == 0 else 1 + i for i in range(N)])    # high, low, high, low ...
p = list(range(1, N + 1))
random.shuffle(p)
add(p)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

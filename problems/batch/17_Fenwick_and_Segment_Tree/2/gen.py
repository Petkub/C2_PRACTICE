# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(110002)
MAXN, MAXV = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a):
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= v <= MAXV for v in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")


def halves(n, top):
    """values v and v // 2 or 2 v next to each other: many pairs exactly on the boundary a_i = 2 a_j"""
    a = []
    while len(a) < n:
        v = ri(1, top // 2)
        a += random.choice(([2 * v, v], [v, 2 * v], [2 * v + 1, v], [2 * v, v + 1]))
    return a[:n]


# samples
add([9, 4, 2, 8, 1])
add([8, 4, 2, 1])
add([5])
add([1, 2, 3, 4, 5, 6])
add([MAXV, 499_999_999, 1, 500_000_000])
add([7, 3, 3, 10, 1, 4, 2])
# hidden: small
add([1, 1])
add([3, 1])
add([2, 1])
for n, vmax in ((10, 10), (50, 6), (300, 1000), (2000, MAXV), (5000, 20)):
    add([ri(1, vmax) for _ in range(n)])
add(halves(3000, 100))
add(halves(4000, MAXV))
# hidden: maximum size
N = MAXN
add([ri(1, MAXV) for _ in range(N)])
add([ri(1, 10) for _ in range(N)])
add([MAXV] * (N // 2) + [1] * (N // 2))                         # about 10^10 pairs
add(sorted((ri(1, MAXV) for _ in range(N)), reverse=True))
add(sorted(ri(1, MAXV) for _ in range(N)))                      # no drop at all
add([ri(MAXV // 2, MAXV) for _ in range(N)])                    # within a factor 2: no drop
add(halves(N, MAXV))
add([MAXV >> ri(0, 29) for _ in range(N)])                      # powers of two times a constant
add([ri(1, 1000) * ri(1, 1000) for _ in range(N)])
a = [ri(MAXV // 2 + 1, MAXV) for _ in range(N // 2)] + [ri(1, MAXV // 4) for _ in range(N // 2)]
random.shuffle(a)
add(a)
add([MAXV - i for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

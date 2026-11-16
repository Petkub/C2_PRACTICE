# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10112)
MAXN = 100_000
MAXV = 10**9
tests = []


def add(h, t):
    n = len(h)
    assert 1 <= n <= MAXN and len(t) == n
    assert all(0 <= x <= MAXV for x in h + t)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n" + " ".join(map(str, t)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def tiny():
    """small enough for the BFS in brute.cpp"""
    n = random.randint(2, 5)
    h = rnd(n, 0, 3)
    t = rnd(n, 0, 3)
    return h, t


# samples
add([1, 1, 1, 1], [2, 3, 3, 2])
add([2, 2, 2], [3, 1, 3])
add([4, 7, 1], [4, 7, 1])
add([0], [MAXV])
add([5, 0, 5, 0, 5], [0, 5, 0, 5, 0])
add([3, 1, 4, 1, 5, 9], [2, 7, 1, 8, 2, 8])
# hidden (tiny, checked by BFS)
add([3], [0])
add([0, 3, 0, 3, 0, 3], [3, 0, 3, 0, 3, 0])
add([1, 2, 3, 2, 1], [3, 2, 1, 2, 3])
for _ in range(6):
    add(*tiny())
# small
add(rnd(300, 0, 5), rnd(300, 0, 5))
add(rnd(2000, 0, 20), rnd(2000, 0, 20))
# large
N = MAXN
add([0, MAXV] * (N // 2), [MAXV, 0] * (N // 2))             # the largest answer
add([0] * N, [MAXV] * N)
add(rnd(N, 0, MAXV), rnd(N, 0, MAXV))
add(rnd(N, 0, 10), rnd(N, 0, 10))
add(list(range(N)), [N - 1 - i for i in range(N)])
add([MAXV] * 50, [MAXV] * 50)
add([0] * N, [MAXV if i % 2 == 0 else 0 for i in range(N)])
add([0] * N, sorted(rnd(N, 0, MAXV)))
h = rnd(5000, 0, MAXV)
add(h, [x + random.choice([-1, 0, 1]) if 0 < x < MAXV else x for x in h])
add([0] * N, [min(i, N - 1 - i) * 10_000 for i in range(N)])       # one big mountain
add(rnd(N, MAXV - 5, MAXV), rnd(N, 0, 5))
add([random.choice([0, MAXV]) for _ in range(N)], [random.choice([0, MAXV]) for _ in range(N)])
add(rnd(N - 1, 0, 30), rnd(N - 1, 0, 30))
add(rnd(N, 0, 100), rnd(N, 0, 100))
add(rnd(N, 0, MAXV // 2), rnd(N, MAXV // 2, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

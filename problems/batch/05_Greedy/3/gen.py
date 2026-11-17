# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(5001)
MAXN, MAXV = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(D, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= D <= MAXV
    assert all(1 <= x <= MAXV for x in a)
    tests.append(f"{n} {D}\n" + " ".join(map(str, a)) + "\n")


def clamp(x):
    return max(1, min(MAXV, x))


def walk(n, D, lo_step, hi_step, start=None):
    """random walk with steps of size in [lo_step, hi_step] times D / 4, any sign"""
    x = start if start is not None else ri(MAXV // 4, 3 * MAXV // 4)
    a = []
    for _ in range(n):
        a.append(x)
        s = ri(lo_step * D // 4, hi_step * D // 4)
        x = clamp(x + (s if random.random() < 0.5 else -s))
    return a


def sawtooth(n, D):
    """notes that go up and down, each change just below or just above D, with a slow drift"""
    a, x, up = [], ri(MAXV // 3, 2 * MAXV // 3), True
    for _ in range(n):
        a.append(x)
        s = D + ri(-D // 3, D // 3)
        x = clamp(x + s if up else x - s)
        if random.random() < 0.8:
            up = not up
    return a


def trap_start(D, base, up=True):
    """x, x + D - 1, x + D + 1, x + 1 (or its mirror): the best melody uses the 1st, 3rd and 4th notes"""
    if up:
        return [base, base + D - 1, base + D + 1, base + 1]
    return [base, base - D + 1, base - D - 1, base - 1]


# samples
add(3, [2, 6, 5, 1, 7, 3, 4, 9])
add(4, [10, 8, 3, 5, 9, 2, 6])
add(10, [3, 8, 12, 5, 9])
add(1, [2, 2, 5, 5, 5, 3, 3, 6, 1])
add(2, [9, 8, 6, 5, 3, 2])
add(5, [20, 14, 17, 9, 15, 23, 21, 12, 18, 30])
# hidden: small
add(7, [42])
add(1, [5, 5])
add(5, [1, 5, 7, 2])                                   # the start decides the direction late
add(5, [9, 5, 3, 8])
add(MAXV - 1, [1, MAXV, 1, MAXV, 2, MAXV])
for n, V, D in [(10, 12, 3), (15, 9, 2), (20, 50, 7), (60, 1000, 120), (2000, 10**9, 2 * 10**8)]:
    add(D, [ri(1, V) for _ in range(n)])
add(40, trap_start(40, 500, False) + [ri(300, 700) for _ in range(30)])
D = 1000
add(D, trap_start(D, 5000) + sawtooth(3000, D))
add(D, trap_start(D, 9000, False) + sawtooth(3000, D))
# hidden: maximum size
N = MAXN
add(10**8, [ri(1, MAXV) for _ in range(N)])
add(10**8, trap_start(10**8, 5 * 10**8, False) + [ri(1, MAXV) for _ in range(N - 4)])
add(1, [ri(1, 3) for _ in range(N)])                   # many equal neighbours
add(123_456, [777_777_777] * N)                       # one note only
add(5, [1 + 5 * i for i in range(N)])                  # rising all the way
add(MAXV // 2, [1 if i % 2 == 0 else MAXV for i in range(N)])   # every note fits
D = 10**6
add(D, sawtooth(N, D))
add(D, trap_start(D, 4 * 10**8) + sawtooth(N - 4, D))
D = 5000
add(D, trap_start(D, 6 * 10**8) + walk(N - 4, D, 1, 8))
D = 3 * 10**8
add(D, trap_start(D, 7 * 10**8, False) + walk(N - 4, D, 2, 6))
D = 37
add(D, walk(N, D, 0, 7))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10013)
MAXN, MAXV = 200000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(t, c):
    n = len(t)
    assert 3 <= n <= MAXN and len(c) == n
    assert 0 <= min(t + c) and max(t + c) <= MAXV
    tests.append(f"{n}\n" + " ".join(map(str, t)) + "\n" + " ".join(map(str, c)) + "\n")


def rnd(n, lo=0, hi=MAXV):
    return [ri(lo, hi) for _ in range(n)]


def tea_lovers(n, gap):
    """tea is better for everybody by about gap: the pattern of coffee seats is forced, the seam matters"""
    c = rnd(n, 0, MAXV - gap)
    t = [x + gap - ri(0, gap // 10) for x in c]
    return t, c


# samples
add([5, 4, 6, 3], [1, 2, 1, 2])
add([10, 10, 10], [0, 0, 0])
add([3, 8, 1, 9, 2], [7, 2, 6, 1, 5])
add([4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4])
add([9, 0, 9, 0, 9, 0, 9], [0, 9, 0, 9, 0, 9, 0])
add([7, 9, 8, 9, 7, 9, 8, 6], [1, 3, 2, 4, 3, 1, 2, 5])
# hidden: small (brute.cpp tries every assignment)
add([0, 0, 0], [0, 0, 0])
add([1, 2, 3], [3, 2, 1])
add(*tea_lovers(10, 1000))
add(*tea_lovers(11, 1000))
add(rnd(16), rnd(16))
add(rnd(19, 0, 10), rnd(19, 0, 10))
add(*tea_lovers(20, 50))
# hidden: maximum size
N = MAXN
add(rnd(N), rnd(N))
add(*tea_lovers(N, 10**6))
add(*tea_lovers(N - 1, 10**6))
add(*tea_lovers(N - 2, 10**6))
add([MAXV] * N, [MAXV] * N)
add([MAXV] * (N - 1), [0] * (N - 1))
c, t = tea_lovers(N - 1, 10**8)
add(t, c)                                            # coffee lovers
add(rnd(N, 0, 3), rnd(N, 0, 3))
add([MAXV if i % 3 else 0 for i in range(N)], [0 if i % 3 else MAXV for i in range(N)])
add([MAXV - (i % 7) for i in range(N - 2)], [MAXV - 3 - (i % 5) for i in range(N - 2)])
add(*tea_lovers(N, 1))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

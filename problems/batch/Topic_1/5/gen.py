# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1105)
MAXN, MAXV = 150_000, 10**9
tests = []

def add(d, a, b):
    n, m = len(a), len(b)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 0 <= d <= MAXV
    assert all(0 <= x <= MAXV for x in a + b)
    tests.append(f"{n} {m} {d}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add(2, [5, 1, 9], [3, 8, 6, 12])
add(0, [4, 4, 7], [4, 7, 4])
add(1, [0, 10], [5, 20])
add(MAXV, [0], [MAXV])
add(3, [10, 2, 7, 15, 4], [6, 1, 13, 9, 20])
# hidden: small
add(0, [0], [1])
add(0, [5, 5, 5], [5, 5])
add(10, rnd(20, 0, 100), rnd(15, 0, 100))
add(50, rnd(300, 0, 5000), rnd(400, 0, 5000))
add(MAXV, rnd(1000, 0, MAXV), rnd(800, 0, MAXV))           # every pair
add(0, rnd(3000, 0, 50), rnd(3000, 0, 50))                 # D = 0, many equal values
add(10**6, rnd(10000, 0, MAXV), rnd(10000, 0, MAXV))
add(10**8, sorted(rnd(12000, 0, MAXV)), sorted(rnd(12000, 0, MAXV), reverse=True))
# hidden: maximum size
add(MAXV, rnd(MAXN, 0, MAXV), rnd(MAXN, 0, MAXV))          # answer N * M = 2.25e10
add(MAXV, [MAXV] * MAXN, [0] * MAXN)                       # a + D overflows int
add(MAXV - 1, [MAXV] * MAXN, [0] * MAXN)                   # nothing
add(10**8, rnd(MAXN, 0, MAXV), rnd(MAXN, 0, MAXV))
add(5 * 10**8, rnd(MAXN, 0, MAXV), rnd(MAXN, 0, MAXV))
add(0, rnd(MAXN, 0, 1000), rnd(MAXN, 0, 1000))
add(1000, rnd(MAXN, MAXV - 10**6, MAXV), rnd(MAXN, MAXV - 10**6, MAXV))
add(2 * 10**8, sorted(rnd(MAXN, 0, MAXV), reverse=True), sorted(rnd(MAXN, 0, MAXV)))
add(123_456_789, rnd(MAXN, 0, MAXV), rnd(MAXN - 1, 0, MAXV))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

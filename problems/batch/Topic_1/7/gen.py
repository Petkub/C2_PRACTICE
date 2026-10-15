# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1107)
MAXN, MAXS, MAXC = 200_000, 10**15, 10**9
tests = []

def add(s, c):
    n = len(c)
    assert 1 <= n <= MAXN and 1 <= s <= MAXS
    assert all(1 <= x <= MAXC for x in c)
    tests.append(f"{n} {s}\n" + " ".join(map(str, c)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add(10, [3, 4, 2, 6, 1])
add(5, [6, 2, 3, 7])
add(1, [1])
add(1, [2])
add(MAXS, [7, MAXC, 7])
add(4, [1, 1, 1, 1, 1, 1])
# hidden: small
add(MAXS, [MAXC])
add(5, [3, 9, 9, 2, 3, 9, 1])               # costs above S in the middle and at both ends
add(30, rnd(15, 1, 20))
add(200, rnd(100, 1, 50))
add(10**4, rnd(2000, 1, 100))
c = rnd(5000, 1, 1000)
for i in range(0, 5000, 37):
    c[i] = MAXC                              # many empty windows
add(5000, c)
add(10**12, rnd(20000, 1, MAXC))
add(MAXS, rnd(20000, 1, MAXC))               # every trip
# hidden: maximum size
add(MAXS, [MAXC] * MAXN)                     # every trip: N(N+1)/2, sums up to 2e14
add(MAXC * 60_000, [MAXC] * MAXN)            # windows of exactly 60000
add(MAXC * 70_000 - 1, rnd(MAXN, 1, MAXC))
add(MAXC * 100_000, rnd(MAXN, MAXC // 2, MAXC))
add(150_000, [1] * MAXN)                     # windows of exactly 150000
c = rnd(MAXN, 1, 10**4)
for i in range(1, MAXN, 50_000):
    c[i] = MAXC                              # a few costs above S
add(MAXC - 1, c)
add(MAXS, rnd(MAXN, 1, MAXC))
add(30_000_000_000, rnd(MAXN, 1, 10**6))
add(MAXC * 40_000, sorted(rnd(MAXN, 1, MAXC)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

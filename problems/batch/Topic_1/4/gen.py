# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1104)
MAXN, MAXA = 500_000, 10**9
BIGN = 250_000                                # largest N whose input with 10-digit values stays near 3 MB
tests = []

def add(k, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return random.choices(range(lo, hi + 1), k=n)

# samples
add(3, [2, -1, 3, 4, -2, 5, 1])
add(2, [3, 1, -5, 4, 0, 2])
add(2, [-5, -3, -8, -1])
add(1, [0, -2, 7, 7, 3])
add(1, [-10**9])
add(4, [5, -1, -1, 5])
# hidden: small
add(1, [7])
add(2, [-1, -1, -1, -1, -1])                  # all ties: s = 1
add(3, rnd(10, -10, 10))
add(5, rnd(50, -100, 100))
add(30, rnd(300, -1000, 1000))
add(400, rnd(2000, -MAXA, MAXA))
add(5000, rnd(12000, -5, 5))                  # many ties likely
add(10000, [-MAXA] * 20000)
add(9000, [MAXA] * 20000)
# hidden: maximum size (K near N / 2 so that the O(N K) way has to do about N^2 / 4 additions)
add(MAXN // 2, rnd(MAXN, -1000, 1000))
add(BIGN // 2, rnd(BIGN, -MAXA, MAXA))
add(BIGN // 2, [MAXA] * BIGN)                 # all equal: answer at s = 1, sum beyond 32 bits
add(BIGN // 2 - 1, [-MAXA] * BIGN)
add(200_000, rnd(MAXN, -999, -1))             # every window negative
a = random.choices([-MAXA, -MAXA + 1, MAXA - 1, MAXA], k=BIGN)
add(BIGN // 2 + 1, a)
a = [1] * MAXN                                # a strictly better window appears late, then ties
a[400_000] = 3
add(250_000, a)
a = [(-1) ** i for i in range(MAXN)]          # alternating: many ties
add(MAXN // 2 + 1, a)
add(MAXN // 2 - 12_345, rnd(MAXN, -9999, 9999))
add(MAXN // 3, rnd(MAXN, 0, 99))
add(MAXN, rnd(MAXN, -1000, 1000))
add(1, rnd(MAXN, -1000, 1000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

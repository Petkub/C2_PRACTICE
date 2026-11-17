# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(30607)
MAXN, MAXA = 400_000, 10 ** 6
tests = []

def add(a):
    assert 1 <= len(a) <= MAXN and all(1 <= x <= MAXA for x in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo=1, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([3, 1, 4, 1, 5])
add([2, 7, 1, 8])
add([1000000])
add([5] * 6)
add([5, 2, 6, 6, 3, 9, 1, 4])
# hidden: small
add([7, 7])
add([1, 2])
add([4, 9, 2])
add(rnd(11, 1, 9))
add(rnd(20, 1, 3))
add(list(range(1, 31)))
add(rnd(999, 1, 100))
add(rnd(4000))
add([MAXA - (i % 2) for i in range(6001)])
# hidden: maximum size
add(rnd(MAXN))
add(rnd(MAXN - 1))
add([MAXA] * MAXN)
add(list(range(MAXA - MAXN + 1, MAXA + 1)))            # increasing
add(list(range(MAXA, MAXA - MAXN + 1, -1))[:MAXN - 1])  # decreasing, odd length
add([random.choice([1, MAXA]) for _ in range(MAXN)])
add(rnd(MAXN, 1, 2))
add([MAXA - abs(i - MAXN // 2) for i in range(MAXN)])  # a peak in the middle
add(rnd(MAXN, MAXA - 1000, MAXA))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

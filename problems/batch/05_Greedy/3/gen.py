# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3003)
MAXN, MAXV = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(g, s):
    n, m = len(g), len(s)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN
    assert all(1 <= x <= MAXV for x in g + s)
    tests.append(f"{n} {m}\n" + " ".join(map(str, g)) + "\n" + " ".join(map(str, s)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([5, 2, 8, 4, 7], [3, 6, 4, 1])
add([3, 1], [3, 2])
add([10, 20], [5, 9])
add([4, 4, 4], [4, 4])
add([7, 3, 9, 1, 5, 6], [2, 8, 6, 6, 1, 10, 4])
add([1000000000], [999999999])
# hidden: small
add([1], [1])
add([2, 1], [1])
add([1, 2, 3], [3])                        # giving the big snack to the small child loses
add([3, 1, 2], [2, 3, 1])
add([5, 5, 5, 5], [6, 4, 5, 7, 3])
for n, m, v in [(5, 5, 6), (6, 8, 10), (8, 6, 10), (9, 9, 5), (10, 12, 30), (12, 10, 20), (40, 40, 50),
                (200, 150, 300), (300, 500, 10**9)]:
    add(rnd(n, 1, v), rnd(m, 1, v))
add(rnd(3000, 1, 5000), rnd(2500, 1, 5000))
# hidden: maximum size
N = MAXN
B = 135_000                                # largest size whose input with 10-digit values stays near 3 MB
add(rnd(B, 1, MAXV), rnd(B, 1, MAXV))
add(rnd(N, 1, 1000), rnd(N, 1, 1000))      # many equal values
add([MAXV] * B, [MAXV] * B)                # everyone, with equality
add([MAXV] * B, [MAXV - 1] * B)            # nobody
g = rnd(B, 1, MAXV - 3)
add(g, [x + ri(0, 3) for x in g])          # almost a perfect fit
add(rnd(B, 5 * 10**8, MAXV), rnd(B, 1, 6 * 10**8))   # snacks mostly too small
add(rnd(B, 1, 10**8), rnd(B, 9 * 10**8, MAXV))       # every snack fits everyone
g = list(range(1, N + 1))
s = list(range(N, 0, -1))
add(g, s)
add(rnd(N // 2, 1, MAXV), rnd(N, 1, MAXV))
add(rnd(N, 1, MAXV), rnd(N // 4, 1, MAXV))
g = [2 * i + 2 for i in range(N)]          # snack 2i+1 is too small for child 2i+2, snack 2i+3 fits
random.shuffle(g)
s = [2 * i + 1 for i in range(N)]
random.shuffle(s)
add(g, s)

for t in tests:
    assert len(t) <= 3_100_000
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

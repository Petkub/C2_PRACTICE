# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3007)
MAXN, MAXV = 100_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, b):
    m = len(a)
    assert m == len(b) and m % 2 == 0 and 1 <= m // 2 <= MAXN
    assert all(1 <= x <= MAXV for x in a + b)
    tests.append(f"{m // 2}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def rnd(m, lo, hi):
    return [ri(lo, hi) for _ in range(m)]


# samples
add([15, 40, 300, 25], [30, 180, 60, 20])
add([1, 2, 3, 4], [10, 10, 10, 10])
add([5, 7], [6, 3])
add([7] * 6, [7] * 6)
add([4, 9, 2, 8, 5, 6], [3, 5, 7, 1, 9, 6])
add([MAXV, MAXV], [MAXV, MAXV])
# hidden: small
add([1, 1], [1, 1])
add([1, 100], [2, 1000])                     # both prefer A by cost, the cheaper overall goes to B
add([10, 10, 10, 10], [1, 2, 3, 4])
add([5, 1, 9, 2, 8, 3], [1, 5, 2, 9, 3, 8])
for m, v in [(4, 10), (6, 10), (8, 20), (10, 100), (12, 5), (20, 1000), (60, MAXV), (400, 10**6)]:
    add(rnd(m, 1, v), rnd(m, 1, v))
add(rnd(4000, 1, MAXV), rnd(4000, 1, MAXV))
a = rnd(6000, 1, 1000)
add(a, [x + ri(-3, 3) if x > 3 else x for x in a])
# hidden: maximum size (values up to 10^5 keep the files near 3 MB)
M, V = 2 * MAXN, 10**5
add(rnd(M, 1, V), rnd(M, 1, V))
add(rnd(M, 1, V), rnd(M, 1, V))
add(rnd(M, 1, V // 2), rnd(M, V // 2, V))     # everyone prefers A
add(rnd(M, V // 2, V), rnd(M, 1, V // 2))     # everyone prefers B
add([V] * M, [V] * M)                        # all equal
a = rnd(M, 1, V)
add(a, a[:])                                 # every difference is 0
a = rnd(M, 1, V)
add(a, [V + 1 - x for x in a])
a = sorted(rnd(M, 1, V))
add(a, sorted(rnd(M, 1, V)))
add(rnd(M, 1, 10), rnd(M, 1, 10))            # many ties
# the largest values, at full size (a line of 2N ten-digit values would be too big, so mix in short ones)
add([MAXV] * M, rnd(M, 1, 9))                 # everyone prefers B, but N of them must pay 10^9 in A
add(rnd(M, 1, 9), [MAXV - ri(0, 9) for _ in range(M)])
big = [ri(0, 2) == 0 for _ in range(M)]
add([ri(1, MAXV) if x else ri(1, 99) for x in big], [ri(1, MAXV) if x else ri(1, 99) for x in big])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("largest test", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

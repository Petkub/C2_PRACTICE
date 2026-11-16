# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20204)
MAXN = 200_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, b):
    n, q = len(a), len(b)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    assert all(-MAXV <= x <= MAXV for x in a + b)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def around(a, q, spread):
    """houses on, next to and between the stations"""
    s = sorted(set(a))
    res = []
    for _ in range(q):
        k = ri(0, len(s) - 1)
        r = random.random()
        if r < 0.3 and k + 1 < len(s):
            v = (s[k] + s[k + 1]) // 2 + ri(0, 1)       # in the middle of a gap (ties)
        elif r < 0.5:
            v = s[k]
        else:
            v = s[k] + ri(-spread, spread)
        res.append(max(-MAXV, min(MAXV, v)))
    return res


# samples
add([1, 8, 4, 15], [3, 8, 10, 20, 0])
add([6, 6, -2], [-10, 2, 7])
add([0], [-MAXV, MAXV, 0, 7])
add([-MAXV, -MAXV], [MAXV, -999_999_999, -MAXV])
add([10, -5, 3, 3, 20], [4, -100, 12, 16, 3, 0])
add([7, 1], [4, 5, 1, 7])
# hidden: small
add([5], [5])
add([3, 3, 3], rnd(20, -10, 10))
a = rnd(100, -1000, 1000)
add(a, around(a, 200, 5))
a = rnd(3000, -MAXV, MAXV)
add(a, around(a, 3000, 10**6) + rnd(1000, -MAXV, MAXV))
a = rnd(2000, 0, 100)
add(a, rnd(2000, -500, 600))
add([MAXV] * 1000, [-MAXV] * 1000 + [MAXV])
a = [ri(-50, 50) * 1000 for _ in range(1000)]
add(a, around(a, 2000, 600))
# hidden: maximum size (positions up to 10^6 in absolute value keep the files near 3 MB)
N, H = MAXN, 10**6
a = rnd(N, -H, H)
add(a, rnd(N, -H, H))
a = rnd(N, -H, H)
add(a, around(a, N, 3))
a = rnd(N, -H, -H + 1000)                              # every house to the right of every station
add(a, rnd(N, H - 1000, H))
a = rnd(N, H - 1000, H)                                # every house to the left of every station
add(a, rnd(N, -H, -H + 1000))
a = [ri(-1000, 1000) * 1000 for _ in range(N)]         # many repeats, houses in the middle of gaps
add(a, around(a, N, 500))
a = [ri(-H, H) // 2 * 2 for _ in range(N)]
add(a, [x + 1 for x in rnd(N, -H, H - 2)])
add([0] * N, rnd(N, -H, H))
# the largest distances
add([MAXV] * N, [-MAXV] * 100_000)
add(rnd(N, MAXV - 10**6, MAXV), rnd(100_000, -MAXV, -MAXV + 10**6))
a = rnd(100_000, -MAXV, MAXV)
add(a, around(a, 100_000, 10**7))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

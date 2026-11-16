# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, bisect

random.seed(20216)
MAXN = MAXQ = 200_000
MAXX, MAXB = 10**6, 10**12
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(x, bs):
    n, q = len(x), len(bs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXX for v in x)
    assert all(0 <= b <= MAXB for b in bs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, x)) + "\n" + "\n".join(map(str, bs)) + "\n")


class Dist:
    """total distance D(P) for a fixed list of positions (used to aim queries at the interesting values)"""
    def __init__(self, x):
        self.s = sorted(x)
        self.pre = [0]
        for v in self.s:
            self.pre.append(self.pre[-1] + v)

    def __call__(self, p):
        s, pre, n = self.s, self.pre, len(self.s)
        k = bisect.bisect_right(s, p)
        return p * k - pre[k] + (pre[n] - pre[k]) - p * (n - k)

    def dmin(self):
        return self(self.s[(len(self.s) - 1) // 2])


def aimed(x, q, spread):
    """queries around the minimum, at house positions (exactly and +-1) and up to MAXB"""
    D = Dist(x)
    lo = D.dmin()
    bs = []
    for _ in range(q):
        t = ri(0, 5)
        if t == 0:
            b = lo + ri(-3, 3)
        elif t <= 2:
            b = D(D.s[ri(0, len(x) - 1)]) + ri(-1, 1)
        elif t <= 4:
            b = lo + ri(0, spread)
        else:
            b = ri(0, MAXB)
        bs.append(min(MAXB, max(0, b)))
    return bs


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add([1, 4, 6], [4, 5, 7])
add([3, 8], [5, 6, 7])
add([0], [0, MAXB])
add([5, 5, 5, 5], [0, 3, 4, 9])
add([7, 2, 9, 2, 12, 5], [20, 21, 30, 19, 26, 100])
# hidden: small
add([0, MAXX], [MAXX - 1, MAXX, MAXX + 1, MAXX + 2, MAXX + 3])
for n, xm in ((5, 20), (12, 100), (40, 1000)):
    x = rnd(n, 0, xm)
    add(x, aimed(x, 50, n * xm))
x = rnd(2000, 0, MAXX)
add(x, aimed(x, 2000, 10**10))
x = rnd(1999, 0, 1000)
add(x, aimed(x, 2000, 10**8))
x = [ri(0, 1) * MAXX for _ in range(3000)]
add(x, aimed(x, 2000, 10**10))
# hidden: large
N = MAXN
x = rnd(N, 0, MAXX)
add(x, aimed(x, 100_000, MAXB))
x = rnd(N // 2, 0, MAXX)
add(x, aimed(x, 180_000, MAXB))
x = rnd(N - 1, 0, MAXX)                               # odd count: a single best point
add(x, aimed(x, 100_000, 10**10))
add([MAXX] * N, [MAXB] + aimed([MAXX] * N, 100_000, MAXB))
x = [0] * (N // 2) + [MAXX] * (N // 2)                # a long flat bottom
random.shuffle(x)
add(x, aimed(x, 100_000, MAXB))
x = [ri(0, 1000) if ri(0, 2) else ri(990_000, MAXX) for _ in range(N)]   # two unequal clusters
add(x, aimed(x, 100_000, MAXB))
add([ri(0, MAXX)], rnd(MAXQ, 0, MAXB))                # one friend
add([0, MAXX], rnd(MAXQ, 0, MAXB))
x = [ri(0, 20) * 50_000 for _ in range(N)]           # few, widely spaced positions, each repeated
add(x, aimed(x, 100_000, MAXB))
x = [ri(0, 30) for _ in range(N)]                     # everyone close together: huge answers
add(x, aimed(x, 100_000, MAXB))
x = [i * 5 for i in range(N)]                         # evenly spread, every query aimed at a house
D = Dist(x)
bs = [min(MAXB, D(x[ri(0, N - 1)]) + ri(-1, 1)) for _ in range(100_000)]
add(x, bs)
x = rnd(N, 0, MAXX)
add(x, rnd(100_000, 0, MAXB))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

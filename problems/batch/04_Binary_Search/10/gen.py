# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random
from bisect import bisect_right

random.seed(40901)
MAXK = 50_000
MAXQ = 50_000
MAXU = 10**12
MAXP = 10**6
MAXA = 10**18
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


class Tariff:
    def __init__(self, steps):
        self.u = [s[0] for s in steps]
        self.p = [s[1] for s in steps]
        self.C = [0]
        for j in range(1, len(steps)):
            self.C.append(self.C[-1] + (self.u[j] - self.u[j - 1]) * self.p[j - 1])
        # the largest total use whose bill is at most 10^18
        j = bisect_right(self.C, MAXA) - 1
        self.maxT = self.u[j] - 1 + (MAXA - self.C[j]) // self.p[j]
        if j + 1 < len(steps):
            self.maxT = min(self.maxT, self.u[j + 1] - 1)

    def f(self, m):
        if m <= 0:
            return 0
        j = bisect_right(self.u, m) - 1
        return self.C[j] + (m - self.u[j] + 1) * self.p[j]

    def query(self, x, y):
        assert 1 <= x <= y and x + y <= self.maxT
        return self.f(x + y), self.f(y) - self.f(x)

    def pick(self, kind, tmax=None):
        """a pair (x, y) of the given kind"""
        top = self.maxT if tmax is None else min(self.maxT, tmax)
        if kind == "big":                     # total use near the largest allowed
            T = ri(max(2, top - top // 10), top)
        elif kind == "edge":                  # x and y at step boundaries
            j, k = ri(0, len(self.u) - 1), ri(0, len(self.u) - 1)
            x, y = self.u[j] - 1 + ri(0, 1), self.u[k] - 1 + ri(0, 1)
            x, y = max(1, min(x, y)), max(1, max(x, y))
            if x + y <= top:
                return x, y
            T = ri(2, top)
        else:
            T = ri(2, top)
        r = ri(0, 9)
        if r == 0:
            x = T // 2                        # equal or almost equal use
        elif r == 1:
            x = ri(1, min(3, T // 2))         # tiny x
        else:
            x = ri(1, T // 2)
        return x, T - x


def add(steps, qs, sample=False):
    k, q = len(steps), len(qs)
    assert 1 <= k <= MAXK and 1 <= q <= MAXQ
    assert steps[0][0] == 1 and all(steps[j][0] < steps[j + 1][0] for j in range(k - 1))
    assert steps[-1][0] <= MAXU and all(1 <= p <= MAXP for _, p in steps)
    tar = Tariff(steps)
    lines = []
    for x, y in qs:
        A, B = tar.query(x, y)
        assert 1 <= A <= MAXA and 0 <= B <= MAXA
        if sample:
            assert A <= 10**9
        lines.append(f"{A} {B}\n")
    tests.append(f"{k} {q}\n" + "".join(f"{u} {p}\n" for u, p in steps) + "".join(lines))


def rnd_steps(k, umax, plo, phi, order="any"):
    us = sorted(random.sample(range(2, umax + 1), k - 1)) if umax < 10**7 else None
    if us is None:
        s = set()
        while len(s) < k - 1:
            s.add(ri(2, umax))
        us = sorted(s)
    ps = [ri(plo, phi) for _ in range(k)]
    if order == "up":
        ps.sort()
    elif order == "down":
        ps.sort(reverse=True)
    return list(zip([1] + us, ps))


def mix(steps, q, kinds=("any", "edge", "big"), tmax=None):
    tar = Tariff(steps)
    return [tar.pick(kinds[ri(0, len(kinds) - 1)], tmax) for _ in range(q)]


# samples
add([(1, 2), (5, 3), (11, 5)], [(3, 6), (4, 10), (7, 7), (2, 20)], sample=True)
add([(1, 7)], [(2, 5), (1, 1), (3, 30)], sample=True)
add([(1, 10), (3, 1)], [(1, 4), (2, 3), (5, 5)], sample=True)
add([(1, 1000000), (1000, 1)], [(999, 1000), (5, 999999), (1, 1)], sample=True)
add([(1, 3), (16, 4), (26, 5), (36, 6), (101, 7)], [(10, 40), (50, 50), (15, 135), (1, 2)], sample=True)
# hidden: small (checked by brute force)
add([(1, 1)], [(1, 1), (1, 2), (3, 4), (500, 500), (1, 9999)])
add([(1, 5), (2, 1), (3, 5), (4, 1)], [(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3), (1, 4), (2, 7), (5, 9)])
s = rnd_steps(6, 30, 1, 10)
add(s, mix(s, 60, tmax=200))
s = rnd_steps(40, 2000, 1, 50, "up")
add(s, mix(s, 100, tmax=20000))
s = rnd_steps(200, 5000, 1, 1000, "down")
add(s, mix(s, 100, tmax=30000))
s = rnd_steps(1000, 30000, 1, 100)
add(s, mix(s, 50, ("any", "edge"), tmax=60000))
# hidden: large values, smaller sizes
s = rnd_steps(3, MAXU, MAXP - 10, MAXP)
add(s, mix(s, 3000))
s = [(1, MAXP)]                                          # one price for everything
add(s, mix(s, 3000) + [(1, (MAXA // MAXP) - 1), (MAXA // MAXP // 2, MAXA // MAXP // 2)])
s = rnd_steps(2000, MAXU, 1, MAXP)
add(s, mix(s, 3000))
# hidden: maximum size
s = rnd_steps(MAXK, MAXU, 1, MAXP, "up")
add(s, mix(s, MAXQ))
s = rnd_steps(MAXK, MAXU, 1, MAXP, "up")
add(s, mix(s, MAXQ, ("big",)))
s = rnd_steps(MAXK, MAXU, 1, MAXP)
add(s, mix(s, MAXQ))
s = rnd_steps(MAXK, MAXU, 1, MAXP, "down")
add(s, mix(s, MAXQ, ("big", "edge")))
s = rnd_steps(MAXK, MAXU, MAXP // 2, MAXP)
add(s, mix(s, MAXQ, ("edge",)))
s = rnd_steps(MAXK, 10**8, 1, 100, "up")                 # steps end early, large bills come from the last step
s[-1] = (s[-1][0], MAXP)
add(s, mix(s, MAXQ))
s = [(1 + j * 20_000_000, MAXP - j) for j in range(MAXK)]  # equal-width steps, slowly falling prices
add(s, mix(s, MAXQ))
s = rnd_steps(MAXK, MAXU, 1, 3)                          # cheap units: totals up to 10^12 only
add(s, mix(s, MAXQ))
s = rnd_steps(MAXK, MAXU, 1, MAXP)
add(s, mix(s, MAXQ, ("big", "edge")))
s = rnd_steps(MAXK, MAXU, 1, MAXP, "up")
tar = Tariff(s)
add(s, [(x, x) if ri(0, 1) else (1, 2 * x - 1) for x in (ri(1, tar.maxT // 2) for _ in range(MAXQ))])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

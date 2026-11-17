# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(41301)
MAXN = 100_000
MAXV = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def need(gates, consecutive_only=False):
    """answer by the pair formula (small tests only)"""
    best = 0
    n = len(gates)
    for i in range(n):
        for j in range(i + 1, (i + 2 if consecutive_only else n)):
            if j >= n:
                break
            ti, li, ri_ = gates[i]
            tj, lj, rj = gates[j]
            gap = max(0, lj - ri_, li - rj)
            best = max(best, -(-gap // (tj - ti)))
    return best


def add(gates, sample=False):
    n = len(gates)
    assert 1 <= n <= MAXN
    assert all(0 <= t <= MAXV and 0 <= l <= r <= MAXV for t, l, r in gates)
    assert all(gates[i][0] < gates[i + 1][0] for i in range(n - 1))
    if sample:  # samples: checking consecutive gates only gives the right answer too
        assert need(gates) == need(gates, True)
    tests.append(f"{n}\n" + "".join(f"{t} {l} {r}\n" for t, l, r in gates))


def clip(x):
    return min(MAXV, max(0, x))


def walk(n, dtlo, dthi, speed, wlo, whi, ramp=False):
    """gates around a path that moves at most `speed` metres per second (reflected at the banks);
    with ramp the speed grows along the river, so the hardest part comes last"""
    res = []
    t, p = 0, ri(0, MAXV)
    for i in range(n):
        if i:
            dt = ri(dtlo, dthi)
            t += dt
            sp = max(1, speed * i // n) if ramp else speed
            p += ri(-sp * dt, sp * dt)
            while p < 0 or p > MAXV:
                p = -p if p < 0 else 2 * MAXV - p
        w = ri(wlo, whi)
        a = ri(0, w)
        res.append((t, clip(p - a), clip(p - a + w)))
    return res


def anchors(n, dtlo, dthi, every, slack):
    """narrow gates now and then; each gate in between covers both nearby narrow gates (plus some slack),
    so two neighbouring gates always overlap"""
    xs = [ri(0, MAXV) for _ in range(n // every + 2)]
    res = []
    t = 0
    for i in range(n):
        if i:
            t += ri(dtlo, dthi)
        a, b = xs[i // every], xs[i // every + 1]
        if i % every == 0:
            res.append((t, a, a))
        else:
            res.append((t, clip(min(a, b) - ri(0, slack)), clip(max(a, b) + ri(0, slack))))
    return res


def zigzag(n, dt, lo_gate, hi_gate):
    res = []
    for i in range(n):
        g = lo_gate if i % 2 == 0 else hi_gate
        res.append((i * dt, g[0], g[1]))
    return res


def growing_zigzag(n, dt, width):
    """gates on alternate sides of the middle, further apart along the river"""
    res = []
    mid = MAXV // 2
    for i in range(n):
        amp = (MAXV // 2 - width) * (i + 1) // n
        c = mid - amp if i % 2 == 0 else mid + amp
        res.append((i * dt, clip(c - width), clip(c + width)))
    return res


# samples
add([(0, 2, 4), (2, 7, 9), (5, 1, 3), (6, 3, 8), (10, 8, 12)], sample=True)
add([(1, 0, 5), (4, 3, 8), (8, 4, 4)], sample=True)
add([(7, 3, 5)], sample=True)
add([(0, 0, 0), (1, 5, 5), (2, 10, 10)], sample=True)
add([(0, 0, 0), (3, 10, 10), (7, 2, 4)], sample=True)
# hidden: small (checked by brute force)
add([(0, 0, 0), (1, 0, MAXV), (2, MAXV, MAXV)])                  # a wide gate between two far narrow ones
add([(0, 0, 0), (1, MAXV, MAXV)])
add([(0, 5, 5), (10, 0, 100), (20, 0, 100), (30, 95, 95)])
add([(0, 0, 10), (1, 5, 15), (2, 10, 20), (3, 15, 25), (4, 40, 40)])   # a slow drift, then a jump
add(walk(10, 1, 3, 5, 0, 8))
add(walk(200, 1, 5, 1000, 0, 5000))
add(anchors(500, 1, 10, 7, 1000))
add(walk(2000, 1, 1000, 10**6, 0, 10**8))
add([(i, 7, 7) for i in range(2000)])                             # one place for everything: answer 0
# hidden: maximum size
add(walk(MAXN, 1, 5, 10**7, 0, 10**7, True))
add(walk(MAXN, 1, 3, 3 * 10**6, 10**6, 5 * 10**7, True))
add(anchors(MAXN, 1, 4, 50, 10**7))
add(anchors(MAXN, 1, 2, 1000, 10**8))
add(zigzag(MAXN, 1, (0, 0), (MAXV, MAXV)))                        # the largest answer
add(growing_zigzag(MAXN, 3, 10**7))
add(walk(MAXN, 5000, 9999, 10**5, 0, 10**6, True))                       # long times, products beyond 2^31
add(walk(MAXN, 1, 10, 10**8, 0, MAXV, True))                            # very wide gates
g = walk(MAXN - 6, 1, 4, 5 * 10**6, 0, 10**6, True)
T = g[-1][0]
far = 0 if g[-1][1] > MAXV // 2 else MAXV
g += [(T + 1 + i, 0, MAXV) for i in range(5)] + [(T + 6, far, far)]
add(g)                                                            # open gates, then a narrow gate far away
add(anchors(MAXN, 1, 3, 2, 10**8))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

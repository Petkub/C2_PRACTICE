# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(42000)
MAXN = 200_000
MAXC = 10**9
MAXH = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(bs):
    n = len(bs)
    assert 1 <= n <= MAXN
    for l, r, h in bs:
        assert 0 <= l < r <= MAXC and 1 <= h <= MAXH
    tests.append(f"{n}\n" + "".join(f"{l} {r} {h}\n" for l, r, h in bs))


def shuffled(bs):
    bs = list(bs)
    random.shuffle(bs)
    return bs


def rnd(n, cmax, hmax, wmax=None):
    out = []
    for _ in range(n):
        if wmax is None:
            l = ri(0, cmax - 1)
            r = ri(l + 1, cmax)
        else:
            l = ri(0, cmax - 1)
            r = min(cmax, l + ri(1, wmax))
        out.append((l, r, ri(1, hmax)))
    return out


# samples
add([(1, 5, 3), (2, 4, 6), (6, 8, 2)])
add([(0, 3, 4), (3, 6, 4), (6, 8, 2), (8, 9, 5)])
add([(5, 7, 1)])
add([(0, 10, 1), (0, 5, 3), (0, 2, 5)])
add([(1, 9, 9), (3, 5, 2), (2, 8, 9), (10, 12, 9)])
add([(0, 4, 5), (4, 7, 3), (2, 4, 1)])
# hidden: small
add([(0, MAXC, MAXH)])
add([(3, 4, 2), (3, 4, 2), (4, 5, 2)])
add(rnd(8, 10, 3))
add(rnd(50, 30, 5))
add(rnd(300, 1000, 10**6, 50))
add(rnd(2000, MAXC, MAXH))
add([(i, i + 1, ri(1, 3)) for i in range(3000)])                # touching unit buildings, many equal neighbours
add(shuffled([(i, 6000 - i, ri(1, 2000)) for i in range(3000)]))  # nested
# large: N = MAXN with small numbers (input near 3 MB) or N = 100 000 with full-size numbers
N = MAXN
add(shuffled([(i, 2 * N - i, 1 + 99 * i // N) for i in range(N)]))   # nested, taller inside: a staircase up and down
add(shuffled([(i, 2 * N - i, 99 - 98 * i // N) for i in range(N)]))  # nested, lower inside: only 2 points
add(shuffled([(i, 2 * N - i, ri(1, 99)) for i in range(N)]))      # nested, random heights
N2 = 150_000
add([(0, ri(1, 10**6), ri(1, 99)) for _ in range(N2)])            # all start at 0
add([(ri(0, 5 * 10**5 - 1), ri(5 * 10**5, 10**6), ri(1, 99)) for _ in range(N)])   # every building is wide
add(rnd(N, 10**6, 99))
add(rnd(N2, 10**6, 99, 10**3))
add(shuffled([(2 * i, 2 * i + 2, 1 + (i // 3) % 2) for i in range(N2)]))   # touching, equal heights in runs of 3
add(shuffled([(i, i + 1, ri(1, 2)) for i in range(N2)]))            # unit steps, drops and rises at each x
bs = [(3 * i, 3 * i + 3, 7) for i in range(N2 // 2)]                 # the tallest ends where an equal one starts
bs += [(3 * i + 1, 3 * i + 2, ri(1, 6)) for i in range(N2 // 2)]
add(shuffled(bs))
M = 100_000
add(rnd(M, MAXC, MAXH))
add([(ri(0, 10**8), ri(9 * 10**8, MAXC), ri(MAXH - 10**3, MAXH)) for _ in range(M)])
add([(ri(0, 10**5), 10**6, ri(1, 99)) for _ in range(N2)])      # all end at the same x
add([(ri(0, 5 * 10**5 - 1), ri(5 * 10**5, 10**6), 5) for _ in range(N)])   # everything the same height

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

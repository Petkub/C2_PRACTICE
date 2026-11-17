# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60116)
MAXN, MAXD, MAXV = 150_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(d, riders, shuffle=True):
    riders = list(riders)
    if shuffle:
        random.shuffle(riders)
    n = len(riders)
    assert 1 <= n <= MAXN and 1 <= d <= MAXD
    assert all(0 <= p < d and 1 <= v <= MAXV for (p, v) in riders)
    assert len(set(p for p, v in riders)) == n
    tests.append(f"{n} {d}\n" + "".join(f"{p} {v}\n" for (p, v) in riders))


def rnd(n, d, vmax=MAXV):
    return [(p, ri(1, vmax)) for p in random.sample(range(d), n)]


def farey_block(x, y, c_start, k):
    c = c_start
    while (1 + y * c) % x:
        c += 1
    e = (1 + y * c) // x
    out = []
    for _ in range(k):
        out.append((c, e))
        c += x
        e += y
    return out


def staircase(n, levels, d=MAXD):
    per = n // len(levels)
    riders, base = [], d // 10
    for j, (x, y) in enumerate(levels):
        k = per if j + 1 < len(levels) else n - per * (len(levels) - 1)
        blk = farey_block(x, y, base, k)
        riders += [(d - c, e) for (c, e) in blk]
        base = blk[-1][0] + 10**8
    assert all(c <= d for c in [d - p for p, e in riders])
    return riders


add(10, [(0, 2), (4, 1), (6, 4)], False)
add(12, [(0, 3), (4, 2), (9, 2), (5, 5)], False)
add(1000000000, [(0, 3)], False)
add(1000000000, [(0, 1000000000), (999999999, 1)], False)
add(100, [(10, 6), (40, 4), (70, 9), (20, 25), (55, 10)], False)

add(1, [(0, MAXV)])
add(100, [(90, 1), (50, 10), (0, 20)])
add(30, rnd(8, 30, 6))
add(50, rnd(20, 50, 10))
m = MAXD - 50
add(MAXD, [(MAXD - (m + k - 1), m + k) for k in range(1, 51)])
add(10**6, rnd(1000, 10**6, 1000))
add(MAXD, staircase(3000, [(1, 3), (1, 2), (2, 3), (1, 1), (3, 2), (2, 1)]))
add(MAXD, rnd(5000, MAXD))

N = MAXN
add(MAXD, rnd(N, MAXD))
add(MAXD, rnd(N, MAXD, 1000))
step = MAXD // (N + 1)
add(MAXD, [(MAXD - (k + 1) * step, 1 + k * 6000) for k in range(N)])
add(MAXD, [(k, MAXV - 3 * (N - k)) for k in range(N)])
m = MAXD - N
add(MAXD, [(MAXD - (m + k - 1), m + k) for k in range(1, N + 1)])
add(MAXD, staircase(N, [(1, 3), (1, 2), (2, 3), (1, 1), (3, 2), (2, 1)]))
add(MAXD, staircase(N, [(1, 2), (3, 5), (1, 1), (4, 3), (5, 3)]))
add(N + 5, rnd(N, N + 5, MAXV))
add(MAXD, [(p, MAXV) for p in random.sample(range(MAXD), N)])
s = [(MAXD - 1, 1)] + [(p, ri(10**8, MAXV)) for p in random.sample(range(MAXD - 1), N - 1)]
add(MAXD, s)
add(MAXD, staircase(N, [(1, 4), (2, 5), (3, 4), (5, 4), (7, 4)]), False)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

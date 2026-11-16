# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40402)
MAXN, MAXT, MAXG = 150_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(G, a, shuffle=True):
    a = list(a)
    if shuffle:
        random.shuffle(a)
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= G <= MAXG
    assert all(0 <= s < e <= MAXT for s, e in a)
    tests.append(f"{n} {G}\n" + "".join(f"{s} {e}\n" for s, e in a))


def rnd(n, T, maxlen):
    out = []
    for _ in range(n):
        s = ri(0, T - 1)
        out.append((s, min(T, s + ri(1, maxlen))))
    return out


# samples
add(10, [(95, 110), (0, 30), (200, 230), (60, 90), (35, 50)], False)
add(1, [(0, 100), (10, 20), (30, 40), (106, 110), (100, 105)], False)
add(5, [(3, 8)], False)
add(1000, [(500, 600), (0, 1), (2000, 2001)], False)
add(3, [(4, 6), (4, 6), (1, 2)], False)
add(2, [(10, 20), (1, 9), (22, 30), (11, 12)], False)
# hidden: small
add(MAXG, [(0, MAXT)])
add(1, [(0, 1), (1, 2), (2, 3), (4, 5)])
add(2, [(0, 10), (2, 3), (5, 6), (11, 12), (14, 15)])   # nested: compare with the largest end
add(3, rnd(8, 40, 5))
add(5, rnd(30, 300, 8))
add(20, rnd(100, 10_000, 50))
add(100, rnd(500, 10**6, 500))
add(1, rnd(800, 2000, 3))
a = [(0, 1000)] + [(ri(0, 990), 0) for _ in range(300)]
a = [(s, s + ri(1, 9)) if e == 0 else (s, e) for s, e in a] + [(1000 + 7 * i, 1003 + 7 * i) for i in range(300)]
add(4, a)
add(MAXG, rnd(1000, MAXT, 10))                          # everything in one group
# hidden: large
N = MAXN
add(1000, rnd(N, MAXT, 4000))
add(6000, rnd(N, MAXT, 2000))
add(1, rnd(N, MAXT, 6000))
a = [(i * 6000, i * 6000 + 3000) for i in range(N)]     # gaps of exactly G: N separate groups
add(3000, a)
a = [(i * 6000, i * 6000 + 3000 + (i % 2)) for i in range(N)]  # gaps alternate G and G - 1
add(3000, a, False)
a = []
for blk in range(N // 50):                              # long appointment covering 49 short ones, then a gap
    base = blk * 6000
    a.append((base, base + 5000))
    for j in range(49):
        s = base + ri(0, 4000)
        a.append((s, s + ri(1, 100)))
add(900, a)
a = [(MAXT - 1 - 6000 * i - 3000, MAXT - 1 - 6000 * i) for i in range(N)]
add(2999, a, False)                                     # reverse sorted input
add(MAXG, rnd(N, MAXT, 1))                              # all one group
a = [(ri(0, 10) * 1000, 0) for _ in range(N)]
a = [(s, s + 500) for s, _ in a]                        # heavy duplicates
add(500, a)
add(10, [(ri(0, MAXT - 1), MAXT) for _ in range(N)])    # all end at the latest time
add(2, [(2 * i, 2 * i + 1) for i in range(N)])          # touching nothing, gap 1 < G
add(5000, rnd(N, MAXT, 500))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47016)
MAXN, MAXV = 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(m, ps):
    n = len(ps)
    assert 1 <= m <= n <= MAXN
    assert all(1 <= s <= MAXV and 1 <= e <= MAXV for s, e in ps)
    tests.append(f"{n} {m}\n" + "".join(f"{s} {e}\n" for s, e in ps))


def rnd(n, shi, elo, ehi):
    return [(ri(1, shi), ri(elo, ehi)) for _ in range(n)]


def late_good(n, shi):
    res = []
    for _ in range(n):
        s = ri(1, shi)
        res.append((s, max(1, min(MAXV, s // 2 + ri(0, shi // 2)))))
    return res


add(2, [(3, 5), (1, 2), (6, 4), (2, 1)])
add(3, [(1, 1), (10, 2), (4, 1)])
add(1, [(7, 3)])
add(1, [(6, 7), (6, 3), (8, 6), (6, 9), (3, 9)])
add(4, [(4, 4), (1, 9), (6, 1), (3, 2), (7, 5), (2, 3)])

add(2, [(1, 1), (1000000000, 1)])
add(1, [(5, 1), (5, 1), (5, 1)])
add(3, [(2, 9), (9, 2), (4, 4), (8, 1), (1, 7)])
for n, h in [(8, 10), (10, 30), (12, 12), (14, 50), (16, 20)]:
    add(ri(1, n), rnd(n, h, 1, h))
add(30, rnd(200, 300, 1, 300))
add(1, late_good(2000, 3000))
add(1500, rnd(3000, 2500, 1, 1000))

N = MAXN
add(1, rnd(N, MAXV, 1, MAXV))
add(N // 2, rnd(N, MAXV, 1, MAXV))
add(N, rnd(N, MAXV, 1, MAXV))
add(ri(1, N), late_good(N, MAXV))
add(N // 10, late_good(N, MAXV))
add(3 * N // 4, rnd(N, MAXV, 1, 10**6))
add(10, rnd(N, 10**6, 1, 10**6))
add(N // 3, [(MAXV - ri(0, N), MAXV) for _ in range(N)])
add(1, [(i + 1, MAXV - i) for i in range(N)])
add(N - 1, rnd(N, 2 * N, 1, 2 * N))
add(N // 4, [(ri(1, MAXV), ri(1, 3)) for _ in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

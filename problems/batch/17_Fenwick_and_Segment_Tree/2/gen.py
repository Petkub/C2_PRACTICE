# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(170107)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXV <= v <= MAXV for v in a)
    lines = []
    for t, x, y in ops:
        if t == 1:
            assert 1 <= x <= n and -MAXV <= y <= MAXV
        else:
            assert t == 2 and 1 <= x <= y <= n
        lines.append(f"{t} {x} {y}")
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "\n".join(lines) + "\n")


def val(vmax, pzero):
    if random.random() < pzero:
        return 0
    return ri(1, vmax) * random.choice((1, -1))


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def ops_of(n, q, upd, rng, vmax, pzero, zpos=None):
    ops = []
    for _ in range(q):
        if random.random() < upd:
            x = val(vmax, pzero)
            i = zpos() if x == 0 and zpos else ri(1, n)
            ops.append((1, i, x))
        else:
            ops.append((2,) + rng())
    return ops


add([2, -3, 0, 4, -1], [(2, 1, 2), (2, 1, 5), (2, 4, 5), (1, 2, -2), (2, 1, 2), (2, 2, 5)])
add([-1, -1, -1], [(2, 1, 3), (1, 2, -5), (2, 1, 3), (2, 2, 2)])
add([MAXV, -MAXV], [(2, 1, 2), (1, 1, -1), (2, 1, 2)])
add([3, -2, 5, -7, 1], [(2, 1, 5), (1, 5, -3), (2, 3, 5), (2, 1, 5)])
add([0, 1], [(2, 2, 2), (2, 1, 2)])

for n, q, vmax, pzero, upd in ((1, 6, 3, 0.2, 0.5), (3, 20, 2, 0.1, 0.4), (8, 60, 10, 0.05, 0.4),
                               (30, 300, MAXV, 0.02, 0.3), (100, 800, 2, 0.01, 0.5), (300, 1500, MAXV, 0.0, 0.3),
                               (300, 1500, 1, 0.01, 0.3)):
    add([val(vmax, pzero) for _ in range(n)], ops_of(n, q, upd, lambda: any_rng(n), vmax, pzero))
n = 300
add([val(5, 0) for _ in range(n)], ops_of(n, 1500, 0.3, lambda: any_rng(n), 5, 0.2))

N = MAXN
z_end = lambda: ri(N - 20, N)
add([val(9, 0) for _ in range(N)], ops_of(N, 160_000, 0.2, lambda: long_rng(N, 50), 9, 0.002, z_end))
add([val(9, 0) for _ in range(N)], ops_of(N, 160_000, 0.05, lambda: long_rng(N, 50), 9, 0, None))
add([2] * N, ops_of(N, 160_000, 0.3, lambda: long_rng(N, 100), 2, 0.001, z_end))
add([-2] * N, ops_of(N, 160_000, 0.1, lambda: long_rng(N, 10), 2, 0.001, z_end))
n = 100_000
add([val(MAXV, 0) for _ in range(n)], ops_of(n, 110_000, 0.3, lambda: long_rng(n, 30), MAXV, 0.002,
                                             lambda: ri(n - 10, n)))
add([val(9, 0) for _ in range(N)], [(2, 1, N) if k % 3 else (1, ri(1, N), -1) for k in range(150_000)])
a = [val(9, 0) for _ in range(N)]
a[N - 1] = 0
add(a, ops_of(N, 160_000, 0.2, lambda: long_rng(N, 1000), 9, 0, None))
a = [1] * N
add(a, ops_of(N, 170_000, 0.1, lambda: long_rng(N, 20), 1, 0.001, z_end))
add([val(99, 0) for _ in range(N)], ops_of(N, 150_000, 0.4, lambda: long_rng(N, 3000), 99, 0.001, z_end))

n = 3000
add([val(MAXV, 0.01) for _ in range(n)], ops_of(n, MAXQ, 0.4, lambda: any_rng(n), MAXV, 0.02))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

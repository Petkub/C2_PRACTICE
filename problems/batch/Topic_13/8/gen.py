# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110008)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXV <= v <= MAXV for v in a)
    for op in ops:
        if op[0] == 1:
            assert 1 <= op[1] <= n and -MAXV <= op[2] <= MAXV
        else:
            assert op[0] == 2 and 1 <= op[1] <= op[2] <= n
    assert any(op[0] == 2 for op in ops)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(" ".join(map(str, op)) + "\n" for op in ops)
    assert len(t) <= 3_100_000
    tests.append(t)


def long_range(n):
    """a query range covering most of the array"""
    l = ri(1, max(1, n // 20))
    return (2, l, ri(max(l, n - n // 20), n))


def rnd_range(n):
    l = ri(1, n)
    return (2, l, ri(l, n))


def ops_mix(n, q, upd_frac, vlo, vhi, long_frac=0.9):
    ops = []
    for _ in range(q):
        if random.random() < upd_frac:
            ops.append((1, ri(1, n), ri(vlo, vhi)))
        elif random.random() < long_frac:
            ops.append(long_range(n))
        else:
            ops.append(rnd_range(n))
    if not any(op[0] == 2 for op in ops):
        ops.append((2, 1, n))
    return ops


# samples
add([3, -4, 5, -1, 2], [(2, 1, 5), (1, 2, 4), (2, 1, 5), (2, 4, 4)])
add([-5, -2, -7], [(2, 1, 3), (2, 3, 3), (1, 3, 4), (2, 1, 3)])
add([-8], [(2, 1, 1), (1, 1, 6), (2, 1, 1)])
add([4, -1, -1, 4, -9, 3], [(2, 1, 6), (2, 2, 3), (1, 5, 9), (2, 1, 6), (2, 3, 4)])
add([2, -3, 4, -1, -2, 1, 5, -3], [(2, 1, 8), (2, 2, 5), (1, 5, 2), (2, 1, 8), (2, 6, 8)])
add([MAXV, MAXV, MAXV], [(2, 1, 3), (1, 2, -MAXV), (2, 1, 3), (2, 2, 3)])
# hidden: small
add([0], [(2, 1, 1)])
add([ri(-10, 10) for _ in range(10)], ops_mix(10, 30, 0.3, -10, 10, 0.3))
add([ri(-100, 50) for _ in range(100)], ops_mix(100, 200, 0.4, -100, 50, 0.3))
add([ri(-MAXV, -1) for _ in range(200)], ops_mix(200, 300, 0.3, -MAXV, -1, 0.5))   # all negative
add([ri(-MAXV, MAXV) for _ in range(2000)], ops_mix(2000, 3000, 0.3, -MAXV, MAXV, 0.5))
add([ri(-1000, 1000) for _ in range(10000)], ops_mix(10000, 10000, 0.5, -1000, 1000, 0.5))
a = [(-1) ** i * ri(1, 5) for i in range(3000)]                                   # alternating signs
add(a, ops_mix(3000, 5000, 0.2, -5, 5, 0.6))
# hidden: maximum size
N = MAXN
add([ri(-10**4, 10**4) for _ in range(N)], ops_mix(N, 120_000, 0.2, -10**4, 10**4))
add([ri(-10**4, 10**4) for _ in range(N)], ops_mix(N, 120_000, 0.5, -10**4, 10**4))
add([ri(-10**4, 10**3) for _ in range(N)], ops_mix(N, 120_000, 0.3, -10**4, 10**4))   # mostly losses
add([ri(1, 9999) for _ in range(N)], ops_mix(N, 120_000, 0.3, 1, 9999))              # all positive: whole range
add([MAXV] * N, [(2, 1, N)] + [(2, ri(1, 9), ri(N - 9, N)) for _ in range(40_000)])  # 2 * 10^14
add([-MAXV] * N, ops_mix(N, 30_000, 0.2, -MAXV, -MAXV + 9, 1.0))                    # all -10^9
a = [ri(-MAXV, MAXV) for _ in range(N)]
add(a, ops_mix(N, 25_000, 0.3, -MAXV, MAXV, 0.8))
a = []
for i in range(N):                                     # long positive runs broken by deep holes
    a.append(-ri(5 * 10**4, 10**5) if i % 1000 == 999 else ri(0, 99))
add(a, ops_mix(N, 120_000, 0.3, -10**5, 99))
a = [(-1) ** i * ri(9000, 9999) for i in range(N)]     # alternating, the best run is short
add(a, ops_mix(N, 120_000, 0.2, -9999, 9999))
a = [ri(-10**4, 10**4) for _ in range(N)]
ops = []
for _ in range(120_000):                               # the same long range again and again, with updates
    ops.append((1, ri(1, N), ri(-10**4, 10**4)) if random.random() < 0.4 else (2, 2, N - 1))
add(a, ops)
a = [ri(-99, 99) for _ in range(N)]
add(a, [(2, 1, N) if j % 2 else (1, ri(1, N), ri(-99, 99)) for j in range(150_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

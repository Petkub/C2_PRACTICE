# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110001)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXV for v in a)
    for t, u, v in ops:
        if t == 1:
            assert 1 <= u <= n and 0 <= v <= MAXV
        else:
            assert t == 2 and 1 <= u <= v <= n
    assert any(t == 2 for t, _, _ in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n"
                 + "".join(f"{t} {u} {v}\n" for t, u, v in ops))


def rnd_ops(n, q, p_set, vmax, long_q=False, front_set=False, wide=False):
    """p_set = chance of an update; long_q: queries cover almost everything; front_set: updates near day 1"""
    ops = []
    for _ in range(q):
        if random.random() < p_set:
            i = ri(1, min(n, 99)) if front_set else ri(1, n)
            ops.append((1, i, ri(0, vmax)))
        elif long_q:
            ops.append((2, ri(1, min(n, 99)), ri(max(1, n - 99), n)))
        elif wide:
            ops.append((2, ri(1, n // 10 + 1), ri(n - n // 10, n)))
        else:
            l = ri(1, n)
            ops.append((2, l, ri(l, n)))
    if all(t == 1 for t, _, _ in ops):
        ops[-1] = (2, 1, n)
    return ops


# samples
add([3, 1, 4, 1, 5], [(2, 1, 3), (1, 2, 7), (2, 2, 5), (1, 5, 0), (2, 4, 5)])
add([10, 20, 30], [(1, 2, 5), (1, 2, 5), (2, 1, 3), (2, 2, 2)])
add([MAXV] * 3, [(2, 1, 3), (1, 2, 0), (2, 1, 3)])
add([0], [(2, 1, 1), (1, 1, 6), (2, 1, 1)])
add([5, 0, 2, 8, 6], [(1, 4, 3), (2, 3, 5), (1, 1, 9), (2, 1, 4)])
# hidden: small
add([7], [(1, 1, 7), (2, 1, 1), (1, 1, 0), (2, 1, 1)])
for n, q, vmax in ((5, 10, 9), (8, 20, 3), (30, 60, 100), (200, 500, MAXV), (2000, 2000, MAXV), (5000, 8000, 1000)):
    add([ri(0, vmax) for _ in range(n)], rnd_ops(n, q, 0.5, vmax))
a = [ri(0, 9) for _ in range(1000)]
ops = []
for _ in range(3000):                                    # the same day corrected again and again
    i = ri(1, 3)
    ops.append((1, i, ri(0, 9)) if random.random() < 0.6 else (2, 1, ri(1, 1000)))
add(a, ops)
add([MAXV] * 3000, rnd_ops(3000, 3000, 0.3, MAXV, long_q=True))
# hidden: maximum size (short numbers keep the files small; the long ranges make one pass per query too slow,
# corrections near day 1 make rebuilding the prefix sums after each correction too slow)
N, Q = MAXN, MAXQ
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.3, 9, long_q=True, front_set=True))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.5, 9, long_q=True, front_set=True))
add([ri(0, 99) for _ in range(N)], rnd_ops(N, Q, 0.7, 99, long_q=True, front_set=True))
add([ri(0, 9) for _ in range(N)], rnd_ops(N, Q, 0.1, 9, long_q=True))
add([ri(0, 999) for _ in range(N)], rnd_ops(N, 160_000, 0.4, 999, wide=True, front_set=True))
add([0] * N, [(2, 1, N)] * Q)
add([ri(0, 9) for _ in range(N)], [(1, 1, ri(0, 9)) if k % 2 == 0 else (2, 1, N) for k in range(Q)])
# largest values: sums up to about 2 * 10^14
a = [MAXV - ri(0, 9) for _ in range(N)]
add(a, [(1, ri(1, N), MAXV) if k % 3 == 0 else (2, ri(1, 50), ri(N - 50, N)) for k in range(55_000)])
a = [ri(0, MAXV) for _ in range(N)]
add(a, rnd_ops(N, 50_000, 0.3, MAXV, wide=True))
add([MAXV] * N, [(1, ri(1, N), 0) if k % 2 == 0 else (2, 1, N) for k in range(60_000)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

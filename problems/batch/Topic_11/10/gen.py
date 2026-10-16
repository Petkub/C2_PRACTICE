# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110010)
MAXN, MAXQ, MAXX = 10**6, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    for op in ops:
        assert 1 <= op[1] <= op[2] <= n
        if op[0] == 1:
            assert len(op) == 4 and 0 <= op[3] <= MAXX
        else:
            assert op[0] == 2 and len(op) == 3
    assert any(op[0] == 2 for op in ops)
    t = f"{n} {q}\n" + "".join(" ".join(map(str, op)) + "\n" for op in ops)
    assert len(t) <= 3_100_000
    tests.append(t)


def rng_long(n):
    l = ri(1, max(1, n // 10))
    return l, ri(max(l, n - n // 10), n)


def rng_any(n):
    l = ri(1, n)
    return l, ri(l, n)


def mix(n, q, set_frac, xlo, xhi, long_frac=0.9, zero_frac=0.0, short_set=0.0):
    """short_set = chance that a replanting covers at most 5 plots (many pieces of equal values)"""
    ops = []
    for _ in range(q):
        l, r = rng_long(n) if random.random() < long_frac else rng_any(n)
        if random.random() < set_frac:
            if random.random() < short_set:
                l = ri(1, n - 4)
                r = l + ri(0, 4)
            ops.append((1, l, r, 0 if random.random() < zero_frac else ri(xlo, xhi)))
        else:
            ops.append((2, l, r))
    if not any(op[0] == 2 for op in ops):
        ops.append((2, 1, n))
    return ops


# samples
add(6, [(1, 2, 5, 3), (2, 1, 6), (1, 4, 6, 5), (2, 3, 4), (2, 1, 6)])
add(5, [(1, 1, 5, 7), (1, 2, 3, 0), (2, 1, 5), (2, 2, 3)])
add(1, [(2, 1, 1)])
add(10, [(1, 1, 10, 4), (1, 3, 8, 2), (1, 5, 5, 9), (2, 1, 10), (2, 5, 9)])
add(7, [(1, 1, 7, 1000), (2, 2, 6), (1, 3, 3, 0), (1, 6, 7, 1), (2, 1, 7), (2, 7, 7)])
# hidden: small
add(1, [(1, 1, 1, MAXX), (2, 1, 1), (1, 1, 1, 0), (2, 1, 1)])
add(10, mix(10, 50, 0.5, 0, 9, 0.3, 0.2))
add(100, mix(100, 300, 0.5, 0, 100, 0.3, 0.2))
add(1000, mix(1000, 3000, 0.4, 0, MAXX, 0.4, 0.2))
add(10000, mix(10000, 10000, 0.5, 0, MAXX, 0.5, 0.1))
ops = [(1, i, i, i) for i in range(1, 2001)]               # many separate pieces, then long sums
ops += [(2, ri(1, 10), ri(1990, 2000)) for _ in range(3000)]
add(2000, ops)
ops = [(1, 1, 5000, 7)]
for _ in range(4000):                                       # zeros over non-zeros
    l, r = rng_any(5000)
    ops.append((1, l, r, 0) if random.random() < 0.3 else (1, l, r, ri(1, 9)) if random.random() < 0.3 else (2, l, r))
add(5000, ops)
# hidden: maximum size
N = MAXN
add(N, mix(N, 120_000, 0.5, 0, 9999, 0.9, 0.1))
add(N, mix(N, 120_000, 0.4, 0, 9999, 0.9, 0.0, 1.0))
add(N, mix(N, 100_000, 0.5, 0, MAXX, 0.9, 0.05))
add(N, [(1, 1, N, MAXX)] + [(2, ri(1, 99), ri(N - 99, N)) for _ in range(140_000)] + [(2, 1, N)])   # 10^15
ops = []
for j in range(60_000):                                     # 60000 separate pieces, then whole-row sums
    p = ri(1, N - 5)
    ops.append((1, p, p + ri(0, 5), ri(1, 9999)))
ops += [(2, ri(1, 50), ri(N - 50, N)) for _ in range(70_000)]
add(N, ops)
ops = []
for j in range(130_000):                                    # alternating set / sum on nearly the whole row
    l, r = rng_long(N)
    ops.append((1, l, r, ri(0, 99)) if j % 2 == 0 else (2, l, r))
add(N, ops)
ops = []
for j in range(120_000):                                    # every other plot is cleared again and again
    l, r = rng_long(N)
    ops.append((1, l, r, 0) if j % 3 == 0 else (1, ri(1, N), ri(N - 9, N), ri(1, 999)) if j % 3 == 1 else (2, l, r))
add(N, ops)
add(N, mix(N, 120_000, 0.6, 0, 9999, 0.5, 0.3, 0.995))
ops = []
for j in range(110_000):                                    # nested ranges shrinking to the middle
    k = j % 400_000
    ops.append((1, 1 + k, N - k, ri(0, 9999)) if j % 2 == 0 else (2, ri(1, 1000), ri(N - 1000, N)))
add(N, ops)
add(N, [(2, 1, N)] + mix(N, 120_000, 0.5, 0, 9999, 1.0, 0.0))
add(N, mix(N, 110_000, 0.5, MAXX - 9, MAXX, 0.9, 0.0, 1.0))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11020)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXV for v in a)
    lines = []
    for op in ops:
        assert op[0] in "AMS" and 1 <= op[1] <= op[2] <= n
        assert (op[0] == "S") == (len(op) == 3)
        if op[0] != "S":
            assert 0 <= op[3] <= MAXV
        lines.append(" ".join(map(str, op)))
    assert any(op[0] == "S" for op in ops)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "\n".join(lines) + "\n"
    assert len(t) <= 3_100_000
    tests.append(t)


def rnd_range(n):
    l = ri(1, n)
    return l, ri(l, n)


def wide_range(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack), n)


def ops_of(n, q, rng, xfun, ps=1 / 3, pm=0.5):
    """each operation is S with probability ps, otherwise M with probability pm, else A"""
    ops = []
    for _ in range(q):
        l, r = rng()
        if random.random() < ps:
            ops.append(("S", l, r))
        else:
            ops.append(("M" if random.random() < pm else "A", l, r, xfun()))
    return ops


# samples
add([1, 2, 3, 4], [("S", 1, 4), ("M", 2, 3, 10), ("S", 1, 4), ("A", 1, 2, 5), ("S", 2, 2)])
add([5, 5, 5], [("A", 1, 3, 1), ("M", 1, 2, 2), ("S", 1, 3), ("M", 2, 3, 0), ("A", 3, 3, 4), ("S", 1, 3)])
add([MAXV, MAXV], [("S", 1, 2), ("M", 1, 1, MAXV), ("S", 1, 1)])
add([0], [("A", 1, 1, 7), ("M", 1, 1, 3), ("A", 1, 1, 1), ("S", 1, 1)])
add([2, 0, 1, 7, 3], [("M", 1, 5, 3), ("A", 2, 4, 2), ("S", 3, 5), ("M", 2, 2, 5), ("S", 1, 3)])
# hidden: small
add([ri(0, 9) for _ in range(6)], ops_of(6, 25, lambda: rnd_range(6), lambda: ri(0, 9)))
add([ri(0, MAXV) for _ in range(20)], ops_of(20, 60, lambda: rnd_range(20), lambda: ri(0, MAXV)))
add([ri(0, 100) for _ in range(100)], ops_of(100, 300, lambda: rnd_range(100), lambda: ri(0, 3), 0.4))
add([ri(0, MAXV) for _ in range(2000)], ops_of(2000, 2000, lambda: rnd_range(2000), lambda: ri(0, MAXV)))
add([MAXV] * 2000, ops_of(2000, 2000, lambda: wide_range(2000, 20), lambda: MAXV - ri(0, 1)))
add([ri(0, 50) for _ in range(3000)], ops_of(3000, 3000, lambda: rnd_range(3000), lambda: ri(1, 2), 0.3, 0.9))
# hidden: maximum size
N, Q = MAXN, MAXQ
small = lambda: ri(0, 999)
add([ri(0, 999) for _ in range(N)], ops_of(N, 140_000, lambda: wide_range(N, 99), small))
add([ri(0, 999) for _ in range(N)], ops_of(N, 140_000, lambda: wide_range(N, 99), lambda: ri(2, 999), 0.3, 1.0))  # M only
add([ri(0, 999) for _ in range(N)], ops_of(N, 140_000, lambda: wide_range(N, 99), small, 0.3, 0.0))                # A only
add([MAXV] * (N // 2), ops_of(N // 2, 80_000, lambda: wide_range(N // 2, 99), lambda: MAXV - ri(0, 9)))    # the largest values
add([ri(0, MAXV) for _ in range(N // 2)], ops_of(N // 2, 80_000, lambda: rnd_range(N // 2), lambda: ri(0, MAXV)))
add([ri(0, 999) for _ in range(N)], ops_of(N, 110_000, lambda: rnd_range(N), small, 0.5))
ops = []
for i in range(70_000):                                         # M then A on the same long range, then a query
    l, r = wide_range(N, 999)
    ops.append(("M", l, r, ri(2, 999)) if i % 2 else ("A", l, r, ri(1, 999)))
    ops.append(("S",) + wide_range(N, 999))
add([ri(0, 999) for _ in range(N)], ops)
add([ri(0, 999) for _ in range(N)], ops_of(N, 140_000, lambda: wide_range(N, 99), lambda: random.choice((0, 1, 2, 999)), 0.4))
add([ri(0, 999) for _ in range(N)], ops_of(N, 110_000, lambda: (lambda i: (i, min(N, i + ri(0, 20))))(ri(1, N)), small))
add([1] * N, ops_of(N, 150_000, lambda: (1, N), lambda: ri(1, 9), 0.5))
add([ri(0, 999) for _ in range(N)], ops_of(N, 115_000, lambda: wide_range(N, N // 3), small, 0.2, 0.7))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

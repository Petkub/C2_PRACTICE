# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(170104)
MAXN, MAXQ, MAXX = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(sq, ops):
    """sq: list of (c, x); ops: (1, i, c, x) or (2, l, r, v)"""
    n, q = len(sq), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(c in (1, 2) and -MAXX <= x <= MAXX for c, x in sq)
    lines = []
    for op in ops:
        if op[0] == 1:
            _, i, c, x = op
            assert 1 <= i <= n and c in (1, 2) and -MAXX <= x <= MAXX
        else:
            _, l, r, v = op
            assert 1 <= l <= r <= n and -MAXX <= v <= MAXX
        lines.append(" ".join(map(str, op)))
    tests.append(f"{n} {q}\n" + "\n".join(f"{c} {x}" for c, x in sq) + "\n" + "\n".join(lines) + "\n")


def squares(n, preset, xmax, lo=1, hi=None):
    """reset squares with probability preset, only among positions lo..hi"""
    hi = n if hi is None else hi
    return [(2 if lo <= i <= hi and random.random() < preset else 1, ri(-xmax, xmax)) for i in range(1, n + 1)]


def ops_of(n, q, upd, rng, xmax, preset, lo=1, hi=None, vmax=None):
    """upd: share of updates; an update may make a reset square only at lo..hi; rng() -> (l, r)"""
    hi = n if hi is None else hi
    vmax = xmax if vmax is None else vmax
    ops = []
    for _ in range(q):
        if random.random() < upd:
            i = ri(1, n)
            c = 2 if lo <= i <= hi and random.random() < preset else 1
            ops.append((1, i, c, ri(-xmax, xmax)))
        else:
            ops.append((2,) + rng() + (ri(-vmax, vmax),))
    return ops


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


# samples
add([(1, 3), (2, 10), (1, -4), (1, 2)], [(2, 1, 4, 5), (1, 3, 2, 20), (2, 1, 4, 0), (2, 4, 4, -3)])
add([(2, 5), (1, -2), (1, -2)], [(2, 2, 3, 1), (2, 1, 3, -7), (1, 1, 1, 4), (2, 1, 3, -7)])
add([(2, -MAXX), (1, MAXX)], [(2, 1, 2, 5), (2, 2, 2, -MAXX), (1, 1, 1, MAXX), (2, 1, 2, -MAXX)])
add([(1, 2), (2, 1), (1, 5), (2, 0), (1, 3)], [(2, 1, 5, 10), (1, 4, 1, -9), (2, 1, 5, 10)])
add([(1, 1), (1, -1), (1, 1), (1, -1)], [(2, 1, 4, 0), (2, 2, 4, 5)])
# hidden: small (the brute force checks these)
for n, q, xmax, preset, upd in ((1, 6, 5, 0.5, 0.4), (3, 20, 5, 0.3, 0.3), (8, 60, 100, 0.2, 0.3),
                                (30, 300, MAXX, 0.1, 0.3), (100, 800, 9, 0.05, 0.4), (300, 1500, MAXX, 0.02, 0.3),
                                (300, 1500, 3, 0.5, 0.5)):
    add(squares(n, preset, xmax), ops_of(n, q, upd, lambda: any_rng(n), xmax, preset))


def edge_test(n, q, front, xmax, every):
    """reset squares only at 1..front; every `every`-th command is an update there, the next one a question
    that ends exactly on a current reset square, the others long questions"""
    sq0 = squares(n, 0.3, xmax, 1, front)
    cur = sq0[:]
    ops = []
    for k in range(q):
        if k % every == 0:
            i = ri(1, front)
            ops.append((1, i, ri(1, 2), ri(-xmax, xmax)))
            cur[i - 1] = (ops[-1][2], ops[-1][3])
        elif k % every == 1:
            ends = [i for i in range(1, front + 1) if cur[i - 1][0] == 2]
            r = random.choice(ends) if ends else front
            ops.append((2, ri(1, r), r, ri(-xmax, xmax)))
        else:
            ops.append((2,) + (long_rng(n, 50) if n > 1000 else any_rng(n)) + (ri(-xmax, xmax),))
    add(sq0, ops)


edge_test(300, 1500, 300, 1000, 3)                         # many questions end exactly on a reset square
# hidden: maximum size (inputs kept near 3 MB; the reset squares sit at the front, so the walk back from r is long)
N = MAXN
add(squares(N, 0.3, 9, 1, 20), ops_of(N, 130_000, 0.1, lambda: long_rng(N, 20), 9, 0.3, 1, 20, vmax=9))
add(squares(N, 0, 9), ops_of(N, 130_000, 0.1, lambda: long_rng(N, 50), 9, 0, vmax=9))   # no reset square at all
n = 100_000                                                 # large values: sums near 10^14
add(squares(n, 0.2, MAXX, 1, 10), ops_of(n, 60_000, 0.1, lambda: long_rng(n, 10), MAXX, 0.2, 1, 10))
add(squares(N, 0.5, 9, 1, 5), [(2, 1, N, ri(-9, 9)) if k % 5 else (1, ri(1, 5), ri(1, 2), ri(-9, 9))
                               for k in range(130_000)])
add(squares(N, 0.3, 9, 1, 100), ops_of(N, 120_000, 0.3, lambda: long_rng(N, 100), 9, 0.3, 1, 100, vmax=9))
n = 120_000                                                 # all adds at the maximum: the answer grows to 1.2 * 10^14
add([(1, MAXX)] * n, ops_of(n, 55_000, 0.05, lambda: long_rng(n, 5), MAXX, 0, vmax=MAXX))
n = 120_000
add([(1, -MAXX)] * n, ops_of(n, 55_000, 0.05, lambda: long_rng(n, 5), MAXX, 0.5, 1, 3, vmax=MAXX))
edge_test(N, 125_000, 50, 9, 10)                            # long questions plus some that end on a reset square
n = 150_000                                                 # every question starts on a reset square
sq = squares(n, 0, 9)
for i in range(1, 31):
    sq[i - 1] = (2, ri(-9, 9))
add(sq, [(2, ri(1, 30), ri(n - 30, n), ri(-9, 9)) if k % 10 else (1, ri(31, n), 1, ri(-9, 9)) for k in range(120_000)])
# hidden: many short questions
n = 2000
add(squares(n, 0.05, MAXX), ops_of(n, MAXQ // 2, 0.3, lambda: any_rng(n), MAXX, 0.05))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

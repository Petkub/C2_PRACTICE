# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(19004)
MAXN, MAXQ, MAXH = 10**6, 100_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(op[0] == 'Q' for op in ops)
    lines = []
    for op in ops:
        l, r = op[1], op[2]
        assert 1 <= l <= r <= n
        if op[0] == 'L':
            assert 0 <= op[3] <= MAXH
            lines.append(f"L {l} {r} {op[3]}")
        else:
            assert op[0] == 'Q' and len(op) == 3
            lines.append(f"Q {l} {r}")
    tests.append(f"{n} {q}\n" + "\n".join(lines) + "\n")


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_rng(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def ops_of(n, q, pa, upd, ask, val):
    """each operation levels upd() to height val() with probability pa, else asks about ask()"""
    ops = []
    for _ in range(q):
        if random.random() < pa:
            ops.append(('L',) + upd() + (val(),))
        else:
            ops.append(('Q',) + ask())
    if not any(op[0] == 'Q' for op in ops):
        ops[-1] = ('Q',) + ask()
    return ops


def few(k):
    """heights from 0..k, often 0: many ties for the greatest height"""
    return lambda: 0 if random.random() < 0.3 else ri(0, k)


def anyh():
    return ri(0, MAXH)


# samples
add(6, [('L', 2, 4, 5), ('L', 4, 6, 3), ('Q', 1, 6), ('Q', 4, 6), ('L', 2, 3, 0), ('Q', 1, 6), ('Q', 1, 3)])
add(5, [('L', 1, 5, 7), ('L', 3, 3, 9), ('Q', 1, 5), ('L', 3, 3, 7), ('Q', 2, 5), ('L', 1, 2, 0), ('Q', 1, 5)])
add(1, [('Q', 1, 1), ('L', 1, 1, MAXH), ('Q', 1, 1), ('L', 1, 1, 0), ('Q', 1, 1)])
add(9, [('L', 1, 9, 4), ('L', 3, 7, 6), ('L', 5, 5, 0), ('Q', 4, 9), ('L', 3, 4, 2), ('Q', 2, 9), ('Q', 8, 8)])
add(MAXN, [('L', 1, MAXN, 8), ('L', 500000, MAXN, 9), ('L', 1, 700000, 0), ('Q', 1, MAXN), ('Q', 1, 600000)])
# hidden: small (the brute force checks these)
for n, q, pa, d, k in ((1, 10, 0.5, 1, 2), (5, 30, 0.5, 2, 2), (12, 80, 0.5, 5, 3), (60, 400, 0.5, 20, 4),
                       (500, 3000, 0.5, 100, 6), (3000, 4000, 0.45, 800, 3)):
    add(n, ops_of(n, q, pa, lambda: short_rng(n, d) if random.random() < 0.6 else any_rng(n),
                  lambda: any_rng(n), few(k)))
n = 3000                                                    # large heights, few ties
add(n, ops_of(n, 4000, 0.5, lambda: any_rng(n), lambda: any_rng(n), anyh))
n = 2000                                                    # levelling to 0 again and again
add(n, ops_of(n, 4000, 0.6, lambda: any_rng(n), lambda: any_rng(n), lambda: random.choice((0, 0, 0, 1, MAXH))))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(N, ops_of(N, Q, 0.5, lambda: any_rng(N), lambda: any_rng(N), few(2)))
add(N, ops_of(N, Q, 0.5, lambda: long_rng(N, 1000), lambda: long_rng(N, 1000), few(3)))
add(N, ops_of(N, Q, 0.5, lambda: short_rng(N, 3000), lambda: long_rng(N, 100), few(1)))
add(N, ops_of(N, Q, 0.5, lambda: any_rng(N), lambda: any_rng(N), anyh))
add(N, ops_of(N, Q, 0.6, lambda: long_rng(N, N // 2), lambda: long_rng(N, 10),
              lambda: random.choice((0, 0, MAXH, MAXH - 1))))
add(N, ops_of(N, Q, 0.4, lambda: (1, N), lambda: any_rng(N), few(5)))           # whole land flat, leftmost = l
add(N, ops_of(N, Q, 0.5, lambda: short_rng(N, 50), lambda: long_rng(N, 3), lambda: ri(0, 1)))
add(N, ops_of(N, Q, 0.5, lambda: long_rng(N, 200), lambda: short_rng(N, 5000), few(4)))
add(N, ops_of(N, Q, 0.7, lambda: any_rng(N), lambda: long_rng(N, 20), lambda: random.choice((0, 0, 0, 7))))   # mostly back to 0
add(N, ops_of(N, Q, 0.5, lambda: short_rng(N, 200_000), lambda: any_rng(N), few(10)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

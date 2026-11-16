# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(19007)
MAXN, MAXQ, MAXX, MAXC = 500_000, 100_000, 10**6, 10**12
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(op[0] == 'M' for op in ops)
    lines = []
    for op in ops:
        l, r = op[1], op[2]
        assert 1 <= l <= r <= n
        if op[0] == 'A':
            assert 1 <= abs(op[3]) <= MAXX
            lines.append(f"A {l} {r} {op[3]}")
        elif op[0] == 'C':
            assert abs(op[3]) <= MAXC
            lines.append(f"C {l} {r} {op[3]}")
        else:
            assert op[0] == 'M' and len(op) == 3
            lines.append(f"M {l} {r}")
    tests.append(f"{n} {q}\n" + "\n".join(lines) + "\n")


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_rng(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def ops_of(n, q, pa, pc, upd, ask, addx, capc):
    """each operation: an add of addx() on upd() with probability pa, a cap at capc() on upd() with
    probability pc, otherwise a question on ask()"""
    ops = []
    for _ in range(q):
        r = random.random()
        if r < pa:
            x = addx()
            ops.append(('A',) + upd() + (x if x != 0 else 1,))
        elif r < pa + pc:
            ops.append(('C',) + upd() + (capc(),))
        else:
            ops.append(('M',) + ask())
    if not any(op[0] == 'M' for op in ops):
        ops[-1] = ('M',) + ask()
    return ops


def pm(k):
    return lambda: ri(-k, k)


def drift(k, up):
    """adds of size up to k, mostly upwards (up > 0.5): the caps keep pulling the temperatures down"""
    return lambda: ri(1, k) * (1 if random.random() < up else -1)


# samples
add(5, [('A', 1, 5, 10), ('A', 2, 3, 5), ('C', 1, 4, 12), ('M', 1, 5), ('A', 3, 5, 4), ('M', 1, 5),
        ('C', 3, 5, -1), ('M', 3, 5), ('M', 1, 5)])
add(3, [('C', 1, 3, 5), ('M', 1, 3), ('A', 1, 2, -4), ('C', 2, 3, -2), ('A', 1, 3, 3), ('M', 1, 2), ('M', 1, 3)])
add(1, [('A', 1, 1, MAXX), ('C', 1, 1, -MAXC), ('M', 1, 1), ('A', 1, 1, -MAXX), ('M', 1, 1)])
add(8, [('A', 1, 8, 6), ('C', 3, 6, 2), ('A', 2, 4, 5), ('C', 1, 3, 4), ('M', 1, 8), ('M', 3, 5), ('A', 4, 8, -9),
        ('M', 4, 8)])
add(MAXN, [('A', 1, MAXN, MAXX), ('C', 2, MAXN, 7), ('A', 1, MAXN, MAXX), ('M', 2, MAXN), ('M', 1, MAXN)])
# hidden: small (the brute force checks these)
for n, q, d in ((1, 12, 1), (5, 40, 2), (12, 100, 5), (60, 500, 20), (500, 3000, 100), (3000, 4000, 700)):
    add(n, ops_of(n, q, 0.35, 0.3, lambda: short_rng(n, d) if random.random() < 0.6 else any_rng(n),
                  lambda: any_rng(n), drift(5, 0.6), pm(12)))
n = 2000                                                    # big values
add(n, ops_of(n, 4000, 0.4, 0.25, lambda: any_rng(n), lambda: any_rng(n), drift(MAXX, 0.7), pm(3 * 10**7)))
n = 2500                                                    # caps right after adds on overlapping ranges
add(n, ops_of(n, 4000, 0.35, 0.35, lambda: short_rng(n, 300), lambda: short_rng(n, 600), drift(20, 0.6), pm(60)))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(N, ops_of(N, Q, 0.35, 0.3, lambda: any_rng(N), lambda: any_rng(N), drift(1000, 0.6), pm(3 * 10**4)))
add(N, ops_of(N, Q, 0.35, 0.3, lambda: long_rng(N, 1000), lambda: long_rng(N, 1000), drift(MAXX, 0.6),
              pm(10**8)))
add(N, ops_of(N, Q, 0.4, 0.2, lambda: short_rng(N, 5000), lambda: long_rng(N, 100), drift(100, 0.7), pm(3000)))
add(N, ops_of(N, Q, 0.4, 0.3, lambda: long_rng(N, N // 3), lambda: short_rng(N, 1000), drift(50, 0.6), pm(1500)))
add(N, ops_of(N, Q, 0.6, 0.1, lambda: any_rng(N), lambda: any_rng(N), lambda: MAXX, lambda: ri(0, 10**10)))
add(N, ops_of(N, Q, 0.35, 0.35, lambda: any_rng(N), lambda: long_rng(N, 10), drift(10, 0.5), pm(200)))
add(N, ops_of(N, Q, 0.3, 0.3, lambda: (1, N), lambda: any_rng(N), drift(10**4, 0.55), pm(10**6)))
add(N, ops_of(N, Q, 0.4, 0.3, lambda: short_rng(N, 200_000), lambda: any_rng(N), drift(MAXX, 0.5),
              pm(MAXC)))
add(N, ops_of(N, Q, 0.45, 0.2, lambda: any_rng(N), lambda: short_rng(N, 50_000), lambda: -ri(1, MAXX),
              lambda: -ri(0, 10**10)))                 # everything goes down
add(N, ops_of(N, Q, 0.3, 0.4, lambda: long_rng(N, 3000), lambda: long_rng(N, 30_000), drift(7, 0.65), pm(40)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

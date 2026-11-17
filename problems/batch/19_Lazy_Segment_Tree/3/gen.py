# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(19003)
MAXN, MAXQ, MAXX = 10**6, 100_000, 10**6
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
        if op[0] == 'A':
            assert -MAXX <= op[3] <= MAXX
            lines.append(f"A {l} {r} {op[3]}")
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
    ops = []
    for _ in range(q):
        if random.random() < pa:
            ops.append(('A',) + upd() + (val(),))
        else:
            ops.append(('Q',) + ask())
    if not any(op[0] == 'Q' for op in ops):
        ops[-1] = ('Q',) + ask()
    return ops


def anyx():
    return ri(-MAXX, MAXX)


add(5, [('A', 1, 3, 4), ('A', 2, 5, -2), ('Q', 1, 5), ('Q', 4, 5), ('A', 4, 4, 10), ('Q', 3, 5)])
add(3, [('Q', 1, 3), ('A', 1, 3, -5), ('Q', 2, 2), ('A', 2, 3, 7), ('Q', 1, 3)])
add(1, [('A', 1, 1, -1000000), ('Q', 1, 1), ('A', 1, 1, 999999), ('Q', 1, 1)])
add(8, [('A', 2, 7, 3), ('A', 1, 4, -6), ('A', 6, 8, 2), ('Q', 1, 8), ('Q', 5, 6), ('A', 1, 8, 1), ('Q', 1, 3)])
add(MAXN, [('A', 1, MAXN, MAXX), ('A', 1, MAXN, MAXX), ('A', 2, MAXN, -1), ('Q', 1, MAXN), ('Q', 1, 1)])

for n, q, pa, d in ((1, 10, 0.5, 1), (4, 30, 0.5, 2), (10, 80, 0.55, 5), (60, 400, 0.5, 20),
                    (500, 3000, 0.5, 100), (3000, 4000, 0.5, 600)):
    small = lambda: ri(-9, 9) if random.random() < 0.5 else anyx()
    add(n, ops_of(n, q, pa, lambda: short_rng(n, d) if random.random() < 0.5 else any_rng(n),
                  lambda: any_rng(n), small))
n = 2000
add(n, ops_of(n, 3000, 0.5, lambda: any_rng(n), lambda: any_rng(n), lambda: -ri(1, MAXX)))
n = 1500
add(n, [op for k in range(1500) for op in
        (('A', k % 50 + 1, n - k % 50, 7), ('A', k % 50 + 1, n - k % 50, -7), ('Q',) + any_rng(n))][:4000])

N, Q = MAXN, MAXQ
add(N, ops_of(N, Q, 0.5, lambda: long_rng(N, 100), lambda: long_rng(N, 100), anyx))
add(N, ops_of(N, Q, 0.6, lambda: long_rng(N, 10), lambda: long_rng(N, 1000), lambda: MAXX))
add(N, ops_of(N, Q, 0.6, lambda: long_rng(N, 10), lambda: any_rng(N), lambda: -MAXX))
add(N, ops_of(N, Q, 0.5, lambda: any_rng(N), lambda: any_rng(N), anyx))
add(N, ops_of(N, Q, 0.5, lambda: short_rng(N, 1000), lambda: long_rng(N, 50), anyx))
add(N, ops_of(N, Q, 0.5, lambda: (1, N), lambda: (1, N), lambda: ri(-MAXX // 3, MAXX)))
add(N, ops_of(N, Q, 0.4, lambda: long_rng(N, N // 2), lambda: short_rng(N, 3), anyx))
add(N, ops_of(N, Q, 0.5, lambda: long_rng(N, 3000), lambda: long_rng(N, 3000),
              lambda: ri(MAXX - 10, MAXX) * random.choice((1, 1, 1, -1))))
add(N, ops_of(N, Q, 0.7, lambda: any_rng(N), lambda: long_rng(N, 5), lambda: ri(-MAXX, MAXX // 2)))
add(400_000, ops_of(400_000, Q, 0.5, lambda: short_rng(400_000, 200_000), lambda: any_rng(400_000),
                     lambda: ri(-MAXX // 2, MAXX)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(19005)
MAXN, MAXQ, MAXX = 10**6, 100_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(op[0] == 'T' for op in ops)
    lines = []
    for op in ops:
        l, r = op[1], op[2]
        assert 1 <= l <= r <= n
        if op[0] == 'S':
            assert 0 <= op[3] <= MAXX
            lines.append(f"S {l} {r} {op[3]}")
        elif op[0] == 'B':
            assert 1 <= op[3] <= MAXX
            lines.append(f"B {l} {r} {op[3]}")
        else:
            assert op[0] == 'T' and len(op) == 3
            lines.append(f"T {l} {r}")
    tests.append(f"{n} {q}\n" + "\n".join(lines) + "\n")


def any_rng(n):
    l = ri(1, n)
    return l, ri(l, n)


def long_rng(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack + 1), n)


def short_rng(n, d):
    l = ri(1, n)
    return l, min(n, l + ri(0, d))


def ops_of(n, q, ps, pb, upd, ask, setx, addx):
    """each operation: a set on upd() to setx() with probability ps, an add of addx() with probability pb,
    otherwise a question on ask()"""
    ops = []
    for _ in range(q):
        r = random.random()
        if r < ps:
            ops.append(('S',) + upd() + (setx(),))
        elif r < ps + pb:
            ops.append(('B',) + upd() + (addx(),))
        else:
            ops.append(('T',) + ask())
    if not any(op[0] == 'T' for op in ops):
        ops[-1] = ('T',) + ask()
    return ops


def anyx():
    return ri(1, MAXX)


def sety():
    return 0 if random.random() < 0.2 else ri(0, MAXX)


def nested(n, q, width, far=False):
    """bursts on one spot: set, add, set, add ... on ranges that overlap only partly, then questions
    (far: the second question of each burst covers almost the whole row)"""
    ops = []
    while len(ops) < q:
        c = ri(1, n)
        for _ in range(4):
            l = max(1, c - ri(0, width))
            r = min(n, c + ri(0, width))
            if random.random() < 0.5:
                ops.append(('S', l, r, sety()))
            else:
                ops.append(('B', l, r, anyx()))
        for k in range(2):
            if far and k == 1:
                ops.append(('T',) + long_rng(n, 1000))
                continue
            l = max(1, c - ri(0, 2 * width))
            ops.append(('T', l, min(n, l + ri(0, 3 * width))))
    return ops[:q]


# samples
add(5, [('B', 1, 5, 3), ('S', 2, 4, 10), ('T', 1, 5), ('B', 3, 5, 2), ('T', 3, 4), ('S', 1, 5, 0), ('B', 2, 2, 7),
        ('T', 1, 5)])
add(4, [('S', 1, 4, 5), ('B', 1, 2, 1), ('S', 2, 3, 2), ('T', 1, 4), ('B', 1, 4, 4), ('T', 2, 3)])
add(1, [('T', 1, 1), ('B', 1, 1, MAXX), ('S', 1, 1, 0), ('T', 1, 1), ('B', 1, 1, 999999), ('T', 1, 1)])
add(7, [('B', 2, 6, 4), ('S', 4, 7, 1), ('B', 1, 5, 2), ('T', 1, 7), ('S', 3, 3, 9), ('B', 3, 4, 1), ('T', 3, 5)])
add(MAXN, [('S', 1, MAXN, MAXX), ('B', 1, MAXN, MAXX), ('B', 2, MAXN, MAXX), ('T', 1, MAXN), ('T', 1, 1)])
# hidden: small (the brute force checks these)
for n, q, d in ((1, 12, 1), (5, 40, 2), (12, 100, 5), (60, 500, 20), (500, 3000, 100), (3000, 4000, 700)):
    add(n, ops_of(n, q, 0.3, 0.35, lambda: short_rng(n, d) if random.random() < 0.6 else any_rng(n),
                  lambda: any_rng(n), lambda: random.choice((0, 1, 2, 5, MAXX)),
                  lambda: ri(1, 3) if random.random() < 0.6 else anyx()))
add(400, nested(400, 4000, 30))
add(3000, nested(3000, 4000, 200))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(N, ops_of(N, Q, 0.3, 0.3, lambda: any_rng(N), lambda: any_rng(N), sety, anyx))
add(N, ops_of(N, Q, 0.1, 0.6, lambda: long_rng(N, 1000), lambda: long_rng(N, 1000), sety, lambda: MAXX))   # largest totals
add(N, ops_of(N, Q, 0.35, 0.35, lambda: long_rng(N, N // 3), lambda: short_rng(N, 1000), sety, anyx))
add(N, nested(N, Q, 50_000))
add(N, nested(N, Q, 300, far=True))
add(N, ops_of(N, Q, 0.3, 0.4, lambda: short_rng(N, 3000), lambda: long_rng(N, 100), sety, anyx))
add(N, ops_of(N, Q, 0.25, 0.25, lambda: (1, N), lambda: any_rng(N), sety, anyx))
add(N, ops_of(N, Q, 0.4, 0.4, lambda: long_rng(N, 200_000), lambda: long_rng(N, 5), lambda: 0, anyx))
add(N, ops_of(N, Q, 0.3, 0.4, lambda: any_rng(N), lambda: short_rng(N, 20), sety, anyx))
add(N, ops_of(N, Q, 0.02, 0.7, lambda: any_rng(N), lambda: any_rng(N), sety, lambda: MAXX))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

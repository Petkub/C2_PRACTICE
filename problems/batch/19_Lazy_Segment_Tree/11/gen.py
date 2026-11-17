# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(13018)
MAXN, MAXQ = 10**6, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    made, lifted, lines = 0, set(), []
    for op in ops:
        if op[0] == 'O':
            k = op[1]
            assert 1 <= k <= made and k not in lifted
            lifted.add(k)
            lines.append(f"O {k}")
        else:
            l, r = op[1], op[2]
            assert 1 <= l <= r <= n
            made += op[0] == 'C'
            lines.append(f"{op[0]} {l} {r}")
    tests.append(f"{n} {q}\n" + "\n".join(lines) + "\n")


def ops_of(n, q, close, lift, ask, pc, po, recent=0, cap=None):
    ops, active, made = [], [], 0
    for _ in range(q):
        r = random.random()
        if r < pc and (cap is None or len(active) < cap) or (r < pc + po and not active):
            made += 1
            active.append(made)
            ops.append(('C',) + close())
        elif r < pc + po and active:
            j = len(active) - ri(1, min(recent, len(active))) if recent else ri(0, len(active) - 1)
            active[j], active[-1] = active[-1], active[j]
            ops.append(('O', active.pop()))
        else:
            ops.append(('?',) + ask())
    return ops


def any_rng(n):
    def f():
        l = ri(1, n)
        return l, ri(l, n)
    return f


def long_rng(n, slack):
    def f():
        return ri(1, slack), ri(n - slack + 1, n)
    return f


def short_rng(n, d):
    def f():
        l = ri(1, n)
        return l, min(n, l + ri(0, d))
    return f


def mixed_rng(n, d):
    f, g = short_rng(n, d), any_rng(n)
    return lambda: f() if random.random() < 0.7 else g()


add(10, [('C', 2, 5), ('C', 4, 8), ('?', 1, 10), ('O', 1), ('?', 1, 10), ('?', 3, 9)])
add(5, [('C', 1, 5), ('C', 1, 5), ('O', 2), ('?', 2, 4), ('O', 1), ('?', 2, 4)])
add(1, [('?', 1, 1), ('C', 1, 1), ('?', 1, 1), ('O', 1), ('?', 1, 1)])
add(8, [('C', 1, 8), ('C', 3, 4), ('O', 1), ('?', 1, 8), ('C', 2, 7), ('?', 1, 8)])
add(MAXN, [('C', 1, MAXN), ('?', 1, MAXN), ('O', 1), ('?', MAXN // 2, MAXN)])

for n, q, pc, po, d in ((1, 8, 0.4, 0.3, 1), (6, 30, 0.35, 0.25, 3), (12, 60, 0.35, 0.25, 6),
                        (40, 300, 0.3, 0.25, 15), (200, 2000, 0.35, 0.3, 60), (2000, 3000, 0.4, 0.3, 300)):
    add(n, ops_of(n, q, mixed_rng(n, d), None, any_rng(n), pc, po, recent=random.choice((0, 3))))
n = 3000
spots = [(ri(1, 1000), ri(1500, 3000)) for _ in range(4)] + [(1, n)]
add(n, ops_of(n, 3000, lambda: random.choice(spots), None, any_rng(n), 0.4, 0.35))

N, Q = MAXN, MAXQ
add(N, ops_of(N, Q, long_rng(N, 1000), None, long_rng(N, 1000), 0.3, 0.25, recent=5))
add(N, ops_of(N, Q, any_rng(N), None, long_rng(N, 100), 0.5, 0.0, cap=N))
add(N, ops_of(N, Q, short_rng(N, 20), None, long_rng(N, 10), 0.55, 0.05))
add(N, ops_of(N, Q, short_rng(N, 3000), None, any_rng(N), 0.4, 0.2, cap=60_000))
add(N, ops_of(N, Q, long_rng(N, N // 3), None, long_rng(N, 10), 0.45, 0.2, recent=2))
add(N, ops_of(N, Q, lambda: (1, N), None, any_rng(N), 0.3, 0.3))
add(N, ops_of(N, Q, mixed_rng(N, 10**5), None, long_rng(N, 5000), 0.45, 0.35, recent=50))
tiles = [(i * 1000 + 1, i * 1000 + 1000) for i in range(N // 1000)]
add(N, ops_of(N, Q, lambda: random.choice(tiles), None, long_rng(N, 3), 0.5, 0.45, cap=900))
add(N, ops_of(N, Q, lambda: (ri(1, 50), N - ri(0, 49)), None, lambda: (ri(1, 100), N - ri(0, 99)), 0.4, 0.15))
add(N, ops_of(N, Q, any_rng(N), None, short_rng(N, 1000), 0.4, 0.3, recent=3))
add(300_000, ops_of(300_000, Q, mixed_rng(300_000, 50), None, any_rng(300_000), 0.5, 0.3))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

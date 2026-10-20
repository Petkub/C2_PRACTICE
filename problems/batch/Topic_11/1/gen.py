# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(90101)
MAXN, MAXQ = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    q = len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert any(c == "?" for c, a, b in ops)
    for c, a, b in ops:
        assert c in "+?" and 1 <= a <= n and 1 <= b <= n
        assert c == "?" or a != b
    tests.append(f"{n} {q}\n" + "".join(f"{c} {a} {b}\n" for c, a, b in ops))


def rnd_join(n):
    a = ri(1, n)
    b = ri(1, n - 1)
    return ("+", a, b + (b >= a))


def rnd_ops(n, q, pjoin):
    ops = []
    for _ in range(q):
        if random.random() < pjoin:
            ops.append(rnd_join(n))
        else:
            ops.append(("?", ri(1, n), ri(1, n)))
    if not any(c == "?" for c, a, b in ops):
        ops.append(("?", 1, n))
    return ops


def chains(n, k):
    """joins that build k long paths over a random labelling of 1..n, in a random-looking order"""
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    groups = [perm[i::k] for i in range(k)]
    ops = []
    for g in groups:
        for i in range(1, len(g)):
            ops.append(("+", g[i - 1], g[i]) if i % 2 else ("+", g[i], g[i - 1]))
    return ops, groups


def ends_asks(groups, q):
    """asks between far ends of the paths (both answers)"""
    ops = []
    for _ in range(q):
        g = random.choice(groups)
        h = random.choice(groups)
        ops.append(("?", g[ri(0, 9)], h[-1 - ri(0, 9)]))
    return ops


# samples
add(5, [("+", 1, 2), ("+", 3, 4), ("?", 1, 3), ("+", 2, 3), ("?", 4, 1), ("?", 5, 2)])
add(2, [("?", 2, 2), ("?", 1, 2), ("+", 2, 1), ("?", 1, 2)])
add(6, [("+", 1, 2), ("+", 5, 6), ("+", 6, 4), ("?", 4, 5), ("?", 2, 3)])
add(1, [("?", 1, 1)])
add(7, [("+", 7, 1), ("?", 1, 6), ("+", 6, 5), ("+", 5, 1), ("?", 7, 6)])
# hidden: small
add(2, [("?", 1, 2), ("+", 1, 2), ("?", 2, 1), ("?", 1, 1)])
add(10, rnd_ops(10, 30, 0.3))
add(50, rnd_ops(50, 100, 0.4))
add(300, rnd_ops(300, 600, 0.45))
add(1000, rnd_ops(1000, 3000, 0.5))
ops, groups = chains(2000, 3)
add(2000, ops + ends_asks(groups, 2000))
add(5000, rnd_ops(5000, 15000, 0.55))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(N, rnd_ops(N, Q, 0.5))
add(N, rnd_ops(N, Q, 0.75))
ops, groups = chains(100_001, 2)                                # two long paths, then far asks
add(N, ops + ends_asks(groups, Q - len(ops)))
ops, groups = chains(60_000, 1)
asks = ends_asks(groups, Q - len(ops))
mix = []                                                        # asks spread while the path grows
it = iter(asks)
for i, o in enumerate(ops):
    mix.append(o)
    if i % 3 == 0:
        mix.append(next(it))
mix += list(it)
add(N, mix)
ops = [("+", 1, k) for k in range(2, 100_001)]                  # star joined from the centre
add(N, ops + [("?", ri(1, 100_000), ri(1, N)) for _ in range(Q - len(ops))])
ops = [("+", k, 1) for k in range(2, 100_001)]                  # the same star, other order
add(N, ops + [("?", ri(1, 100_000), ri(1, N)) for _ in range(Q - len(ops))])
ops = [("+", k, k + 1) for k in range(1, 100_000)]              # a path joined in order
add(N, ops + [("?", 1, 100_000 - ri(0, 1)) if i % 2 else ("?", ri(1, N), ri(1, N)) for i in range(Q - len(ops))])
ops = [("+", k + 1, k) for k in range(1, 120_000)]
add(N, ops + [("?", 1, ri(110_000, 125_000)) for _ in range(Q - len(ops))])
add(N, [("?", ri(1, N), ri(1, N)) for _ in range(Q)])           # nobody is friends: all NO except a = b
add(N, [rnd_join(N) for _ in range(Q - 1)] + [("?", 1, N)])
ops = [rnd_join(1000) for _ in range(50_000)]                   # small groups merged many times
add(N, ops + rnd_ops(1000, Q - len(ops), 0.2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(220303)
MAXQ, MAXV = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the donors 2..n (donor i joins as the (i - 1)-th event of its kind)"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    L = max(2, n // 12)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":                        # depth about n / 2, short side branches
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":                 # a spine of n / 2 donors with legs
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":                       # a long handle ending in a star
            p = i - 1 if i <= half else half
        elif kind == "chains":                      # chains of length about sqrt(n) glued at random
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        elif kind == "steps":                       # chains of length n / 12, each hung on the previous one
            k = (i - 2) // L
            p = i - 1 if (i - 2) % L else (1 if k == 0 else ri(max(2, (k - 1) * L + 2), k * L + 1))
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def add(c, ops):
    q = len(ops)
    assert 1 <= q <= MAXQ and 0 <= c <= MAXV
    m = 1
    for op in ops:
        if op[0] == 1:
            assert len(op) == 3 and 1 <= op[1] <= m and 0 <= op[2] <= MAXV
            m += 1
        else:
            assert op[0] == 2 and len(op) == 2 and 1 <= op[1] <= m
    assert any(op[0] == 2 for op in ops)
    t = (f"{q} {c}\n" + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def case(q, kind, p_join, vhi, top=None, p_top=1.0):
    """q events: joins follow the shape in order; a question asks, with probability p_top, one of the top donors
    with the smallest numbers (the biggest chains in deep shapes), else a random donor who has joined"""
    joins = sum(1 for _ in range(q) if random.random() < p_join)
    par = shape(joins + 1, kind)
    kinds = [1] * joins + [2] * (q - joins)
    random.shuffle(kinds)
    if kinds[-1] == 1 and 2 not in kinds:
        kinds[-1] = 2
    ops, m = [], 1
    for k in kinds:
        if k == 1 and m < len(par) - 1:
            m += 1
            ops.append((1, par[m], ri(0, vhi)))
        elif top and random.random() < p_top:
            ops.append((2, ri(1, min(m, top))))
        else:
            ops.append((2, ri(1, m)))
    if not any(op[0] == 2 for op in ops):
        ops[-1] = (2, 1)
    add(ri(0, vhi), ops)


# samples
add(5, [(1, 1, 3), (1, 1, 4), (1, 2, 2), (2, 2), (1, 4, 6), (2, 2), (2, 1)])
add(1, [(1, 1, 10), (2, 1), (1, 2, 100), (2, 2), (1, 3, 1000), (2, 1)])
add(0, [(2, 1), (1, 1, 0), (2, 2)])
add(7, [(1, 1, 1), (1, 1, 2), (1, 3, 3), (1, 2, 4), (1, 3, 5), (2, 3), (2, 2)])
add(2, [(2, 1), (1, 1, 5), (1, 1, 5), (2, 1), (2, 3)])
# hidden: small and medium
for q, kind in ((4, "path"), (15, "random"), (40, "deep"), (60, "star"), (100, "caterpillar"), (300, "binary")):
    case(q, kind, 0.7, 100, top=5, p_top=0.5)
case(8000, "random", 0.7, MAXV, top=30, p_top=0.5)
case(8000, "star", 0.8, MAXV, top=1, p_top=0.5)
case(8000, "chains", 0.7, MAXV, top=100, p_top=0.5)
case(8000, "path", 0.6, MAXV, top=2000, p_top=0.5)
# hidden: maximum size, long chains of inviters
case(MAXQ, "path", 0.7, 10**6, top=1000, p_top=0.7)
case(MAXQ, "path", 0.75, MAXV, top=100, p_top=0.8)
case(MAXQ, "deep", 0.7, 10**6, top=1000, p_top=0.7)
case(MAXQ, "caterpillar", 0.75, 10**6, top=3000, p_top=0.7)
case(MAXQ, "broom", 0.75, 10**6, top=50_000, p_top=0.7)
case(MAXQ, "steps", 0.75, 10**6, top=20_000, p_top=0.7)
case(MAXQ, "steps", 0.7, MAXV, top=500, p_top=0.5)
case(MAXQ, "deep", 0.85, 10**4, top=100, p_top=0.9)
case(MAXQ, "path", 0.9, 10**4, top=10, p_top=0.9)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXA, MAXD, ENC = 100_000, 100_000, 10 ** 6, 1000, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    assert all(0 <= v <= MAXA for v in a)
    for o in ops:
        if o[0] == 'A':
            assert 0 <= o[1] < ENC and 0 <= o[2] < ENC and 1 <= o[3] <= MAXD
        else:
            assert o[0] in "SHB" and all(0 <= v < ENC for v in o[1:])
            assert len(o) == {'S': 3, 'H': 4, 'B': 2}[o[0]]
    assert any(o[0] in "SH" for o in ops)
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, a)) + "\n" + "".join(" ".join(map(str, o)) + "\n" for o in ops))


def crafted(a, real):
    at, last, ops = [list(a)], 0, []
    for o in real:
        if o[0] == 'B':
            assert 0 <= o[1] < len(at)
            ops.append(('B', o[1] ^ last))
            del at[o[1] + 1:]
            continue
        l, r = o[1], o[2]
        assert 1 <= l <= r <= len(a)
        x, y = (l - 1) ^ last, (r - 1) ^ last
        if o[0] == 'A':
            b = list(at[-1])
            for i in range(l - 1, r):
                b[i] += o[3]
            at.append(b)
            ops.append(('A', x, y, o[3]))
        else:
            when = len(at) - 1
            if o[0] == 'H':
                when = o[3]
                assert 0 <= when < len(at)
                ops.append(('H', x, y, when ^ last))
            else:
                ops.append(('S', x, y))
            last = sum(at[when][l - 1:r])
    add(a, ops)


def rand_ops(q, mix, dmax=MAXD):
    ops, tot = [], sum(mix)
    for _ in range(q):
        u = random.random() * tot
        e = lambda: ri(0, RANDENC - 1)
        if u < mix[0]:
            ops.append(('A', e(), e(), ri(1, dmax)))
        elif u < mix[0] + mix[1]:
            ops.append(('S', e(), e()))
        elif u < mix[0] + mix[1] + mix[2]:
            ops.append(('H', e(), e(), e()))
        else:
            ops.append(('B', e()))
    if not any(o[0] in "SH" for o in ops):
        ops[-1] = ('S', 0, 0)
    return ops


random.seed(300401)

crafted([2, 0, 5, 1], [('A', 1, 3, 4), ('S', 2, 4), ('A', 2, 4, 1), ('H', 1, 4, 0), ('H', 1, 2, 1), ('B', 1), ('S', 1, 4)])
crafted([10, 20, 30], [('H', 1, 3, 0), ('A', 2, 2, 5), ('A', 1, 3, 1), ('S', 1, 2), ('B', 0), ('S', 2, 3)])
crafted([1000000], [('A', 1, 1, 1000), ('A', 1, 1, 1000), ('H', 1, 1, 1), ('S', 1, 1)])
crafted([0, 0, 0, 0, 0], [('A', 2, 5, 3), ('A', 1, 2, 7), ('H', 1, 5, 2), ('H', 3, 5, 1)])
crafted([5, 5, 5, 5], [('A', 1, 4, 2), ('B', 0), ('S', 1, 4), ('B', 0), ('S', 3, 4)])

add([3], rand_ops(10, (3, 1, 2, 1), 5))
add([ri(0, 5) for _ in range(3)], rand_ops(40, (3, 1, 2, 1), 5))
add([ri(0, 9) for _ in range(10)], rand_ops(300, (3, 1, 3, 1), 9))
add([ri(0, MAXA) for _ in range(60)], rand_ops(1000, (4, 1, 4, 0.3)))
add([ri(0, MAXA) for _ in range(500)], rand_ops(3000, (4, 1, 4, 0.1)))
add([0] * 3000, rand_ops(6000, (5, 1, 4, 0.02)))
add([ri(0, MAXA) for _ in range(20000)], rand_ops(20000, (5, 1, 4, 0.002)))

for first, mix1, mix2, vals in [(0.5, (9, 1, 0, 0), (0, 1, 9, 0), "max"), (0.5, (9, 1, 1, 0), (1, 1, 8, 0), "rand"),
                                (0.4, (1, 0, 0, 0), (1, 0, 9, 0), "zero"), (0.6, (8, 1, 1, 0), (0, 1, 9, 0), "max"),
                                (0.5, (9, 0, 1, 0), (0, 1, 9, 0), "rand"), (0.5, (1, 0, 0, 0), (0, 0, 1, 0), "rand"),
                                (0.45, (9, 0, 1, 0), (2, 1, 7, 0), "max"), (0.5, (9, 1, 0, 0), (1, 2, 7, 0), "zero"),
                                (0.55, (7, 1, 2, 0), (0, 1, 9, 0), "rand"), (0.5, (1, 0, 0, 0), (0, 1, 9, 0), "max")]:
    a = {"max": [MAXA] * MAXN, "zero": [0] * MAXN, "rand": [ri(0, MAXA) for _ in range(MAXN)]}[vals]
    k = int(first * MAXQ)
    ops = rand_ops(k, mix1) + rand_ops(MAXQ - k, mix2)
    if vals != "zero":
        ops[-300:] = [('B', ri(0, RANDENC - 1))] + rand_ops(299, (5, 1, 4, 0))
    add(a, ops)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

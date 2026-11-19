# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4201)
MAXQ, MAXV = 200000, 10**9
tests = []


def add(ops):
    q = len(ops)
    assert 1 <= q <= MAXQ
    bags = {"A": {}, "B": {}}
    for op, b, x in ops:
        assert op in "+-" and b in "AB" and -MAXV <= x <= MAXV
        if op == "+":
            bags[b][x] = bags[b].get(x, 0) + 1
        else:
            assert bags[b].get(x, 0) > 0
            bags[b][x] -= 1
    tests.append(f"{q}\n" + "".join(f"{op} {b} {x}\n" for op, b, x in ops))


def build(q, val, grow, erase_p=0.5, keep=1):
    ops, cards = [], {"A": [], "B": []}
    for i in range(q):
        b = random.choice("AB")
        if i >= grow * q and len(cards[b]) > keep and random.random() < erase_p:
            c = cards[b]
            j = random.randrange(len(c))
            c[j], c[-1] = c[-1], c[j]
            ops.append(("-", b, c.pop()))
        else:
            x = val(b)
            cards[b].append(x)
            ops.append(("+", b, x))
    return ops


def uni(lo, hi):
    return lambda b: random.randint(lo, hi)


add([("+", "A", 5), ("+", "B", -3), ("+", "A", -10), ("+", "B", 4), ("-", "A", -10), ("-", "B", -3)])
add([("+", "B", 7), ("+", "A", 2), ("+", "A", 6), ("-", "A", 6), ("-", "A", 2)])
add([("+", "A", MAXV)])
add([("+", "A", -MAXV), ("+", "B", -MAXV), ("+", "B", MAXV)])
add([("+", "A", 0), ("+", "B", -5), ("+", "B", -5), ("+", "A", -2), ("-", "A", 0)])

add([("+", "B", 3), ("+", "B", 3), ("+", "A", 4), ("-", "B", 3), ("-", "B", 3), ("+", "B", -1)])
add([("+", "A", -7), ("+", "A", -2), ("+", "B", 9), ("+", "B", 1), ("-", "A", -2), ("+", "A", -1)])
add(build(40, uni(-5, 5), 0.3, keep=0))
add(build(300, lambda b: random.randint(-MAXV, -1) if b == "A" else random.randint(1, MAXV), 0.2))
add(build(2000, uni(-3, 3), 0.1, keep=0))
add(build(2000, uni(-MAXV, MAXV), 0.3))
add(build(2000, lambda b: random.choice([-MAXV, MAXV, 0, 1, -1]), 0.2))

Q = MAXQ
add(build(Q, uni(-MAXV, MAXV), 0.5))
add(build(Q, lambda b: random.randint(-MAXV, -1) if b == "A" else random.randint(1, MAXV), 0.5))
add(build(Q, lambda b: random.randint(1, MAXV) if b == "A" else random.randint(-MAXV, -1), 0.5))
add(build(Q, uni(-3, 3), 0.5, erase_p=0.6))
add(build(Q, lambda b: random.choice([-MAXV, MAXV, -MAXV + 1, MAXV - 1]), 0.5))
add(build(Q, lambda b: random.choice([-MAXV, MAXV]), 0.6, erase_p=0.7))
add(build(Q, uni(-20, 20), 0.5, erase_p=0.55))

ops = build(Q // 2, lambda b: random.randint(-MAXV, -1) if b == "A" else random.randint(1, MAXV), 1.0)
cur = {"A": [x for o, b, x in ops if b == "A"], "B": [x for o, b, x in ops if b == "B"]}
for i in range(Q // 2):
    if i % 2 == 0 and cur["B"]:
        ops.append(("-", "B", cur["B"].pop()))
    else:
        x = random.randint(-MAXV, -1)
        cur["B"].insert(0, x)
        ops.append(("+", "B", x))
add(ops)

ops = build(Q // 2, uni(-MAXV, MAXV), 1.0)
rest = [(b, x) for o, b, x in ops]
random.shuffle(rest)
ops += [("-", b, x) for b, x in rest]
add(ops)

ops = build(Q // 2, uni(-MAXV // 2, MAXV // 2), 1.0)
for i in range(Q // 4):
    b = random.choice("AB")
    x = random.choice([-MAXV, MAXV])
    ops += [("+", b, x), ("-", b, x)]
add(ops)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

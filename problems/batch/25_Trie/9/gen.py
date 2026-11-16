# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(250009)
MAXQ, MAXV = 200_000, (1 << 20) - 1
tests = []


def add(ops):
    q = len(ops)
    assert 1 <= q <= MAXQ
    have = {}
    for op in ops:
        assert op[0] in "+-?" and 0 <= op[1] <= MAXV
        if op[0] == "+":
            have[op[1]] = have.get(op[1], 0) + 1
        elif op[0] == "-":
            assert have.get(op[1], 0) >= 1
            have[op[1]] -= 1
        else:
            assert len(op) == 3 and 1 <= op[2] <= MAXQ
    assert any(op[0] == "?" for op in ops)
    tests.append(f"{q}\n" + "".join(" ".join(map(str, op)) + "\n" for op in ops))


def churn(q, lo, hi, p_add, p_del, kmode="any"):
    ops, bag = [], []
    for _ in range(q):
        r = random.random()
        if r < p_add or not bag:
            x = random.randint(lo, hi) if not bag or random.random() < 0.8 else random.choice(bag)
            ops.append(("+", x))
            bag.append(x)
        elif r < p_add + p_del:
            i = random.randrange(len(bag))
            bag[i], bag[-1] = bag[-1], bag[i]
            ops.append(("-", bag.pop()))
        else:
            m = len(bag)
            if kmode == "big":
                k = random.randint(max(1, m - 5), m + 1)
            else:
                k = random.choice([1, m, m + 1, random.randint(1, m), random.randint(1, m)])
            ops.append(("?", random.randint(lo, hi), k))
    return ops


# samples
add([("+", 5), ("+", 1), ("+", 6), ("?", 4, 1), ("?", 4, 2), ("?", 4, 3), ("?", 4, 4)])
add([("+", 3), ("+", 3), ("+", 0), ("?", 3, 2), ("-", 3), ("?", 3, 2), ("?", 0, 1)])
add([("?", 7, 1), ("+", 7), ("?", 7, 1)])
add([("+", 12), ("+", 9), ("+", 2), ("+", 9), ("?", 8, 2), ("-", 12), ("?", 8, 3), ("?", 1, 1)])
add([("+", 0), ("+", 15), ("+", 8), ("+", 7), ("?", 15, 3), ("?", 8, 4), ("-", 7), ("?", 8, 4)])
# hidden: small
add([("?", 0, 1)])
add(churn(30, 0, 15, 0.5, 0.2))
add(churn(200, 0, 31, 0.4, 0.2))
add(churn(1000, 0, MAXV, 0.4, 0.2))
add(churn(3000, 0, 7, 0.4, 0.3))
add(churn(5000, 0, 1023, 0.5, 0.1, "big"))
# hidden: maximum size
Q = MAXQ
ops = [("+", random.randint(0, MAXV)) for _ in range(Q // 2)]
ops += [("?", random.randint(0, MAXV), random.randint(1, Q // 2)) for _ in range(Q // 2)]
add(ops)                                                              # all inserts first, then queries
ops = [("+", random.randint(0, MAXV)) for _ in range(Q // 2)]
ops += [("?", random.randint(0, MAXV), random.choice([1, Q // 2, Q // 2 - 1, Q // 4])) for _ in range(Q // 2)]
add(ops)
add(churn(Q, 0, MAXV, 0.5, 0.1))
add(churn(Q, 0, 255, 0.45, 0.2))                                       # many copies of each value
add(churn(Q, 0, MAXV, 0.35, 0.3, "big"))
ops = [("+", 777)] * (Q // 2) + [("?", random.randint(0, MAXV), random.randint(1, Q // 2 + 1)) for _ in range(Q // 2)]
add(ops)                                                              # one value only
ops = [("+", x) for x in random.sample(range(MAXV + 1), Q // 2)]
ops += [("?", 0, random.randint(1, Q // 2)) for _ in range(Q // 2)]   # x = 0: the k-th smallest value itself
add(ops)
ops = []
bag = []
for i in range(Q):
    if i % 3 == 2 and bag:
        x = bag.pop(random.randrange(len(bag)))
        ops.append(("-", x))
        ops.append(("?", x, random.randint(1, len(bag) + 1)))
    else:
        x = random.choice([0, MAXV, 1 << 19, (1 << 19) - 1]) ^ random.randint(0, 15)
        ops.append(("+", x))
        bag.append(x)
add(ops[:Q])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

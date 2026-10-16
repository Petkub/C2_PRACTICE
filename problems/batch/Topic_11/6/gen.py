# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(110006)
MAXRC, MAXQ, MAXX = 4000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(R, C, ops):
    q = len(ops)
    assert 1 <= R <= MAXRC and 1 <= C <= MAXRC and 1 <= q <= MAXQ
    for op in ops:
        if op[0] == 1:
            assert len(op) == 4 and 1 <= op[1] <= R and 1 <= op[2] <= C and 1 <= op[3] <= MAXX
        else:
            assert len(op) == 5 and op[0] == 2
            assert 1 <= op[1] <= R and 1 <= op[3] <= R and 1 <= op[2] <= C and 1 <= op[4] <= C
    assert any(op[0] == 2 for op in ops)
    tests.append(f"{R} {C} {q}\n" + "".join(f"1 {op[1]} {op[2]} {op[3]}\n" if op[0] == 1 else
                                            f"2 {op[1]} {op[2]} {op[3]} {op[4]}\n" for op in ops))


def corners(r1, c1, r2, c2):
    """the same rectangle, its corners given in a random one of the four ways"""
    return ((2, r1, c1, r2, c2), (2, r2, c2, r1, c1), (2, r1, c2, r2, c1), (2, r2, c1, r1, c2))[int(random.random() * 4)]


def rnd_ops(R, C, q, p_add, xmax, kind="any", where="any"):
    """p_add = chance of planting; kind of rectangles: any / big (almost the whole field) / small;
    where the planting happens: any / top (rows 1..9) / left (columns 1..9)"""
    ops = []
    for _ in range(q):
        if random.random() < p_add:
            r = ri(1, min(R, 9)) if where == "top" else ri(1, R)
            c = ri(1, min(C, 9)) if where == "left" else ri(1, C)
            ops.append((1, r, c, ri(1, xmax)))
            continue
        if kind == "big":
            r1, r2 = ri(1, min(R, 9)), ri(max(1, R - 9), R)
            c1, c2 = ri(1, min(C, 9)), ri(max(1, C - 9), C)
        elif kind == "small":
            r1, c1 = ri(1, R), ri(1, C)
            r2, c2 = min(R, r1 + ri(0, 3)), min(C, c1 + ri(0, 3))
        else:
            r1, r2 = sorted((ri(1, R), ri(1, R)))
            c1, c2 = sorted((ri(1, C), ri(1, C)))
        ops.append(corners(r1, c1, r2, c2))
    if all(op[0] == 1 for op in ops):
        ops[-1] = (2, 1, 1, R, C)
    return ops


# samples
add(3, 4, [(1, 1, 1, 5), (1, 2, 3, 2), (2, 1, 1, 3, 4), (1, 3, 4, 1), (2, 3, 4, 2, 2)])
add(2, 2, [(1, 1, 2, 10), (1, 2, 1, 20), (2, 2, 1, 1, 2), (2, 2, 2, 2, 2)])
add(1, 1, [(1, 1, 1, MAXX), (1, 1, 1, MAXX), (2, 1, 1, 1, 1)])
add(1, 6, [(1, 1, 2, 3), (1, 1, 5, 4), (2, 1, 6, 1, 3), (1, 1, 3, 1), (2, 1, 2, 1, 5)])
add(4, 3, [(1, 4, 1, 2), (1, 2, 2, 6), (1, 1, 3, 1), (2, 4, 3, 1, 1), (2, 2, 2, 4, 1)])
# hidden: small
add(1, 1, [(2, 1, 1, 1, 1), (1, 1, 1, 3), (2, 1, 1, 1, 1)])
for R, C, q, xmax in ((3, 3, 15, 5), (5, 8, 40, 10), (20, 10, 100, 1000), (60, 60, 500, MAXX), (100, 300, 2000, 100), (1, 2000, 2000, MAXX), (2000, 1, 2000, 9)):
    add(R, C, rnd_ops(R, C, q, 0.5, xmax))
add(200, 200, rnd_ops(200, 200, 3000, 0.6, MAXX, "big"))
add(300, 300, rnd_ops(300, 300, 5000, 0.5, 9, "small"))
# hidden: maximum size (the rectangles cover almost the whole field; planting near the top or left edge
# makes keeping prefix sums of every row or of every column slow as well)
R = C = MAXRC
Q = MAXQ
add(R, C, rnd_ops(R, C, Q, 0.5, 9, "big"))
add(R, C, rnd_ops(R, C, Q, 0.3, 9, "big"))
add(R, C, rnd_ops(R, C, Q, 0.1, 9, "big"))
add(R, C, rnd_ops(R, C, Q, 0.5, 9, "big", "top"))
add(R, C, rnd_ops(R, C, Q, 0.6, 9, "big", "left"))
add(R, C, rnd_ops(R, C, Q, 0.85, 9, "big", "top"))
add(R, C, rnd_ops(R, C, Q, 0.5, 9, "big", "left"))
add(R, C, [(1, ri(1, 9), ri(1, 9), ri(1, 9)) if k % 2 == 0 else corners(1, 1, R, C) for k in range(Q)])
add(R, C, rnd_ops(R, C, 120_000, 0.5, 999))
add(R, C, rnd_ops(R, C, 120_000, 0.5, 9, "small"))
add(R, C, [(1, ri(1, R), ri(1, C), MAXX) if k % 2 == 0 else corners(1, 1, R, C) for k in range(140_000)])  # totals near 7 * 10^13
add(1, MAXRC, rnd_ops(1, MAXRC, Q, 0.5, MAXX, "big"))
add(MAXRC, 2, rnd_ops(MAXRC, 2, 150_000, 0.5, MAXX))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

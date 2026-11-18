# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 100_000, 10 ** 6, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, ops):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    assert all(0 <= x <= MAXV for x in a)
    saves = 1
    for t, v, y, z in ops:
        assert t in (1, 2) and 0 <= v < saves and 0 <= y < ENC
        if t == 1:
            assert 0 <= z <= MAXV
            saves += 1
        else:
            assert 0 <= z < ENC
    assert any(t == 2 for t, _, _, _ in ops)
    tests.append(f"{len(a)} {len(ops)}\n" + " ".join(map(str, a)) + "\n"
                 + "".join(f"{t} {v} {y} {z}\n" for t, v, y, z in ops))


def crafted(a, real):
    saves, last, ops = [list(a)], 0, []
    for t, v, y, z in real:
        if t == 1:
            b = list(saves[v])
            b[y - 1] = z
            saves.append(b)
            ops.append((1, v, (y - 1) ^ last, z))
        else:
            assert 1 <= y <= z <= len(a)
            ops.append((2, v, (y - 1) ^ last, (z - 1) ^ last))
            last = sum(saves[v][y - 1:z])
    add(a, ops)


def rand_ops(n, q, p_set, p_latest, vmax=MAXV, recent=0, front=False, window=0):
    ops, saves = [], 1
    for j in range(q):
        if (j < p_set * q) if front else (random.random() < p_set):
            v = saves - 1 if random.random() < p_latest else ri(max(0, saves - window) if window else 0, saves - 1)
            ops.append((1, v, ri(0, RANDENC - 1), ri(0, vmax)))
            saves += 1
        else:
            v = ri(max(0, saves - recent), saves - 1) if recent else ri(0, saves - 1)
            ops.append((2, v, ri(0, RANDENC - 1), ri(0, RANDENC - 1)))
    if all(o[0] == 1 for o in ops):
        ops[-1] = (2, saves - 2, 0, 1)
    return ops


random.seed(300201)

crafted([3, 1, 4, 1, 5], [(2, 0, 2, 4), (1, 0, 3, 10), (2, 1, 1, 5), (1, 0, 1, 0), (2, 2, 1, 3), (2, 0, 1, 3)])
crafted([7, 7, 7], [(1, 0, 2, 0), (1, 1, 3, 2), (1, 1, 1, 9), (2, 2, 1, 3), (2, 3, 1, 3), (2, 1, 2, 2)])
crafted([1000000], [(2, 0, 1, 1), (1, 0, 1, 0), (2, 1, 1, 1), (2, 0, 1, 1)])
crafted([0, 5, 0, 5], [(1, 0, 4, 1), (1, 1, 2, 2), (2, 2, 1, 4), (2, 1, 2, 3)])
crafted([2, 4, 6, 8, 10, 12], [(2, 0, 1, 6), (1, 0, 6, 0), (2, 1, 3, 6), (2, 0, 6, 6)])

add([4], rand_ops(1, 10, 0.5, 0.5, 10))
add([ri(0, 5) for _ in range(3)], rand_ops(3, 40, 0.5, 0.3, 5))
add([ri(0, 9) for _ in range(10)], rand_ops(10, 300, 0.6, 0.5, 9))
add([ri(0, MAXV) for _ in range(50)], rand_ops(50, 1000, 0.5, 0.9))
add([ri(0, MAXV) for _ in range(300)], rand_ops(300, 3000, 0.7, 0.2, MAXV, 20))
add([ri(0, 100) for _ in range(2000)], rand_ops(2000, 5000, 0.5, 0.95))
add([MAXV] * 5000, rand_ops(5000, 10000, 0.5, 0.99, MAXV, 50))

for p_set, p_latest, recent, vals, front in [
        (0.5, 1.0, 10, "max", True), (0.5, 0.999, 100, "rand", True), (0.6, 0.999, 1000, "max", True),
        (0.4, 1.0, 10, "rand", True), (0.5, 1.0, 1, "small", True), (0.6, 0.999, 1000, "rand", False),
        (0.5, 1.0, 20000, "max", False), (0.3, 1.0, 1000, "rand", True), (0.6, 0.9995, 50, "max", True),
        (0.5, 1.0, 5, "max", True)]:
    if vals == "max":
        a = [MAXV - ri(0, 3) for _ in range(MAXN)]
    elif vals == "small":
        a = [ri(0, 9) for _ in range(MAXN)]
    else:
        a = [ri(0, MAXV) for _ in range(MAXN)]
    add(a, rand_ops(MAXN, MAXQ, p_set, p_latest, MAXV if vals != "small" else 9, recent, front, 3000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

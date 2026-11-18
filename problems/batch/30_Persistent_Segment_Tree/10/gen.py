# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, ENC = 100_000, 100_000, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    assert 1 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    plans = 1
    for o in ops:
        assert o[0] in (1, 2, 3) and len(o) == (3 if o[0] == 3 else 4)
        assert 0 <= o[1] < plans and all(0 <= x < ENC for x in o[2:])
        if o[0] == 1:
            plans += 1
    assert any(o[0] != 1 for o in ops)
    tests.append(f"{n} {len(ops)}\n" + "".join(" ".join(map(str, o)) + "\n" for o in ops))


def comp(n, edges, a):
    g = [[] for _ in range(n + 1)]
    for x, y in edges:
        g[x].append(y); g[y].append(x)
    seen, st = {a}, [a]
    while st:
        x = st.pop()
        for y in g[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    return seen


def crafted(n, real):
    plans, last, ops = [[]], 0, []
    for o in real:
        if o[0] == 1:
            plans.append(plans[o[1]] + [(o[2], o[3])])
            ops.append((1, o[1], (o[2] - 1) ^ last, (o[3] - 1) ^ last))
        elif o[0] == 2:
            ops.append((2, o[1], (o[2] - 1) ^ last, (o[3] - 1) ^ last))
            last = 1 if o[3] in comp(n, plans[o[1]], o[2]) else 0
        else:
            ops.append((3, o[1], (o[2] - 1) ^ last))
            last = len(comp(n, plans[o[1]], o[2]))
    add(n, ops)


def rand_ops(q, p_new, p_newest, recent=0, window=0, front=0.0, p3=0.5):
    ops, plans = [], 1
    e = lambda: ri(0, RANDENC - 1)
    for j in range(q):
        if j < front * q or random.random() < p_new:
            v = plans - 1 if random.random() < p_newest else ri(max(0, plans - window) if window else 0, plans - 1)
            ops.append((1, v, e(), e()))
            plans += 1
        else:
            v = ri(max(0, plans - recent), plans - 1) if recent else ri(0, plans - 1)
            ops.append((3, v, e()) if random.random() < p3 else (2, v, e(), e()))
    if all(o[0] == 1 for o in ops):
        ops[-1] = (3, 0, 0)
    return ops


random.seed(301001)

crafted(5, [(1, 0, 1, 2), (1, 1, 3, 4), (2, 2, 1, 4), (1, 2, 2, 3), (2, 3, 1, 4), (3, 1, 2), (2, 2, 3, 4)])
crafted(4, [(3, 0, 2), (1, 0, 1, 1), (1, 1, 2, 4), (3, 2, 4), (2, 1, 2, 4)])
crafted(1, [(3, 0, 1), (1, 0, 1, 1), (2, 1, 1, 1)])
crafted(6, [(1, 0, 1, 2), (1, 1, 5, 6), (1, 2, 2, 6), (3, 3, 1), (2, 1, 1, 6)])
crafted(3, [(2, 0, 1, 1), (2, 0, 1, 2), (1, 0, 1, 3), (3, 1, 3), (2, 1, 2, 3)])

add(1, rand_ops(10, 0.5, 0.5))
add(3, rand_ops(40, 0.5, 0.3))
add(10, rand_ops(300, 0.4, 0.4))
add(50, rand_ops(1000, 0.3, 0.7))
add(300, rand_ops(3000, 0.5, 0.5, 30))
add(3000, rand_ops(6000, 0.6, 0.9))
add(20000, rand_ops(20000, 0.5, 0.999, 1000, 100))

for n, p_new, p_newest, recent, window, front in [
        (MAXN, 0.1, 1.0, 2000, 0, 0.5), (MAXN, 0.2, 0.999, 5000, 2000, 0.4), (MAXN, 0.05, 0.99, 1000, 500, 0.5),
        (MAXN, 0.3, 1.0, 0, 0, 0.3), (1000, 0.1, 1.0, 3000, 0, 0.5), (MAXN, 0.1, 0.995, 20000, 3000, 0.5),
        (50000, 0.2, 1.0, 100, 0, 0.6), (MAXN, 0.0, 1.0, 10000, 0, 0.5), (MAXN, 0.1, 0.99, 3000, 1000, 0.45),
        (2, 0.1, 1.0, 1000, 0, 0.5)]:
    add(n, rand_ops(MAXQ, p_new, p_newest, recent, window, front))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

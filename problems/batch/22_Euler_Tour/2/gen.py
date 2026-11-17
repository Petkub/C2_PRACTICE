# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(220202)
MAXN, MAXQ, MAXV = 100_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def tree(n, kind):
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    random.shuffle(lab)
    lab = [1] + lab
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p, lab


def add(n, p, a, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(a) == n and len(p) == n + 1
    assert all(0 <= x <= MAXV for x in a)
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n
    for op in ops:
        assert 1 <= op[1] <= n
        if op[0] == 1:
            assert len(op) == 3 and 1 <= op[2] <= MAXV
        else:
            assert op[0] == 2 and len(op) == 2
    assert any(op[0] == 2 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, a)) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, p_save, vhi, top=None, p_top=1.0):
    res = []
    for _ in range(q):
        if random.random() < p_save:
            res.append((1, ri(1, n), ri(1, vhi)))
        elif top and random.random() < p_top:
            res.append((2, lab[int(random.random() * top)]))
        else:
            res.append((2, ri(1, n)))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1))
    return res


def case(n, kind, q, p_save, vhi, top=None, p_top=1.0, ahi=None):
    p, lab = tree(n, kind)
    a = [ri(0, vhi if ahi is None else ahi) for _ in range(n)]
    add(n, p, a, rops(n, q, lab, p_save, vhi, top, p_top))


add(6, [0, 0, 1, 1, 2, 2, 3], [3, 1, 4, 1, 5, 9], [(2, 2), (1, 4, 6), (2, 1), (2, 1)])
add(4, [0, 0, 1, 2, 3], [2, 7, 1, 8], [(2, 3), (1, 4, 5), (2, 2), (2, 1)])
add(2, [0, 0, 1], [0, 0], [(2, 1), (1, 2, 5), (2, 2), (2, 1)])
add(5, [0, 0, 3, 1, 3, 2], [1, 2, 3, 4, 5], [(1, 5, 10), (2, 2), (2, 3), (2, 1)])
add(5, [0, 0, 1, 1, 1, 1], [5, 0, 0, 7, 0], [(1, 3, 4), (2, 3), (2, 2), (2, 1)])

for n, kind, q in ((3, "path", 6), (10, "random", 20), (30, "deep", 50), (50, "star", 80), (80, "caterpillar", 120),
                   (200, "binary", 300)):
    case(n, kind, q, 0.6, 100, top=max(2, n // 10), p_top=0.4)
case(5000, "random", 8000, 0.6, MAXV, top=20, p_top=0.3)
case(5000, "broom", 8000, 0.5, 1000, top=100, p_top=0.5)
case(5000, "chains", 8000, 0.5, MAXV, top=300, p_top=0.5)
case(5000, "path", 8000, 0.7, MAXV, top=2500, p_top=0.5)

case(MAXN, "path", MAXQ, 0.3, MAXV, top=2000, p_top=0.95, ahi=99)
case(MAXN, "path", MAXQ, 0.3, MAXV, top=100, p_top=0.95, ahi=99)
case(MAXN, "deep", MAXQ, 0.3, MAXV, top=2000, p_top=0.95, ahi=99)
case(MAXN, "caterpillar", MAXQ, 0.3, MAXV, top=3000, p_top=0.95, ahi=99)
case(MAXN, "broom", MAXQ, 0.3, 1000, top=20_000, p_top=0.95)
case(MAXN, "chains", MAXQ, 0.3, MAXV, top=200, p_top=0.95, ahi=99)
case(MAXN, "star", MAXQ, 0.3, 1000, top=1, p_top=0.9)
case(MAXN, "binary", MAXQ, 0.3, 1000, top=3, p_top=0.95)
case(MAXN, "random", MAXQ, 0.3, 1000, top=1, p_top=0.9)
case(MAXN, "deep", MAXQ, 0.2, MAXV, top=50, p_top=0.97, ahi=99)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

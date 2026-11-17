# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(220005)
MAXN, MAXQ, MAXA, MAXX = 100_000, 100_000, 10**9, 10**6
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
        elif kind == "longchains":
            p = i - 1 if (i - 1) % max(2, n // 20) else ri(1, i - 1)
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
def add(n, a, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(a) == n and len(p) == n + 1
    assert all(0 <= x <= MAXA for x in a)
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
            assert len(op) == 3 and 1 <= op[2] <= MAXX
        else:
            assert op[0] == 2 and len(op) == 2
    assert any(op[0] == 2 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, a)) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def rops(n, q, lab, p1=0.5, xlo=1, xhi=MAXX, top=None, low=None):
    res = []
    for _ in range(q):
        if random.random() < p1:
            v = lab[n - 1 - int(random.random() * low)] if low else ri(1, n)
            res.append((1, v, ri(xlo, xhi)))
        else:
            v = lab[int(random.random() * top)] if top else ri(1, n)
            res.append((2, v))
    if not any(op[0] == 2 for op in res):
        res.append((2, 1))
    return res


def big(kind, q, p1, ahi, xhi, top, low, n=MAXN, xlo=1):
    p, lab = tree(n, kind)
    a = [ri(0, ahi) for _ in range(n)]
    add(n, a, p, rops(n, q, lab, p1, xlo, xhi, top, low))


add(5, [1, 2, 3, 4, 5], [0, 0, 1, 1, 2, 2], [(1, 4, 10), (2, 2), (1, 3, 1), (2, 1)])
add(4, [0, 0, 0, 0], [0, 0, 1, 2, 3], [(1, 4, 5), (2, 3), (1, 2, 1), (2, 1)])
add(2, [MAXA, MAXA], [0, 0, 1], [(1, 2, MAXX), (2, 1), (2, 2)])
add(6, [3, 0, 2, 0, 1, 5], [0, 0, 1, 1, 1, 1, 1], [(1, 1, 4), (1, 6, 2), (2, 1), (2, 6), (2, 2)])
add(6, [2, 7, 1, 8, 2, 8], [0, 0, 5, 1, 3, 1, 4], [(1, 2, 3), (2, 3), (1, 6, 1), (2, 5), (2, 1)])

for n, kind, q in ((3, "path", 6), (10, "random", 15), (30, "deep", 40), (50, "star", 60), (80, "caterpillar", 100),
                   (200, "binary", 300)):
    p, lab = tree(n, kind)
    add(n, [ri(0, 100) for _ in range(n)], p, rops(n, q, lab, 0.5, 1, 100))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains")):
    p, lab = tree(n, kind)
    add(n, [ri(0, MAXA) for _ in range(n)], p, rops(n, 8000, lab, 0.5, 1, MAXX, top=50, low=200))

big("path", 100_000, 0.5, 9999, MAXX, 2_000, 2_000)
big("path", 60_000, 0.7, MAXA, MAXX, 100, 100, n=90_000, xlo=MAXX)
big("deep", 100_000, 0.5, 9999, MAXX, 1_000, 1_000)
big("deep", 100_000, 0.8, 9999, 9999, 100, 20_000)
big("caterpillar", 100_000, 0.5, 9999, MAXX, 1_000, 5_000)
big("broom", 100_000, 0.5, 9999, MAXX, 500, 20_000)
big("longchains", 100_000, 0.6, 9999, MAXX, 200, 5_000)
big("path", 100_000, 0.4, 9999, MAXX, 1_000, 1_000)
big("star", 100_000, 0.1, 9999, 9999, 1, None, n=20_000)
big("path", 100_000, 0.3, 9999, MAXX, 50_000, 50_000)
big("caterpillar", 100_000, 0.6, MAXA, MAXX, 100, 2_000, xlo=MAXX // 2)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

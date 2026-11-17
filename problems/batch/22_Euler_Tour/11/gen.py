# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(220011)
MAXN, MAXQ, MAXX = 100_000, 100_000, 10**9
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


def add(n, p, ops):
    q = len(ops)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(p) == n + 1
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
            assert op[0] in (2, 3) and len(op) == 2
    assert any(op[0] == 3 for op in ops)
    t = (f"{n} {q}\n" + " ".join(map(str, p[2:])) + "\n"
         + "".join(("%d %d %d\n" if len(op) == 3 else "%d %d\n") % op for op in ops))
    assert len(t) <= 3_100_000
    tests.append(t)


def pick(n, lab, lo, hi):
    return lab[lo + int(random.random() * (hi - lo))]


def rops(n, q, lab, pf, pd, xhi=MAXX, ftop=None, dlow=None, qmid=None):
    res = []
    for _ in range(q):
        u = random.random()
        if u < pf:
            v = pick(n, lab, 0, ftop) if ftop else ri(1, n)
            res.append((1, v, ri(1, xhi)))
        elif u < pf + pd:
            v = pick(n, lab, n - dlow, n) if dlow else ri(1, n)
            res.append((2, v))
        else:
            v = pick(n, lab, qmid[0], qmid[1]) if qmid else ri(1, n)
            res.append((3, v))
    if not any(op[0] == 3 for op in res):
        res.append((3, 1))
    return res


def big(kind, q, pf, pd, ftop, dlow, qmid, xhi=MAXX, n=MAXN):
    p, lab = tree(n, kind)
    add(n, p, rops(n, q, lab, pf, pd, xhi, ftop, dlow, qmid))


add(6, [0, 0, 1, 1, 2, 2, 3], [(1, 2, 5), (2, 4), (3, 5), (3, 4), (1, 1, 7), (3, 2)])
add(4, [0, 0, 1, 2, 3], [(1, 1, 3), (2, 3), (3, 4), (3, 3), (1, 2, 9), (3, 4)])
add(2, [0, 0, 1], [(3, 2), (1, 2, 4), (2, 1), (3, 2)])
add(5, [0, 0, 1, 1, 1, 1], [(1, 1, 6), (2, 3), (3, 2), (3, 3), (3, 4)])
add(5, [0, 0, 3, 1, 3, 4], [(1, 3, MAXX), (2, 5), (3, 2), (3, 5), (1, 4, 1), (3, 5)])

add(6, [0, 0, 1, 1, 2, 2, 3], [(1, 2, 5), (2, 4), (3, 5), (3, 2), (1, 1, 7), (3, 4)])
add(4, [0, 0, 1, 2, 3], [(1, 1, 3), (2, 3), (3, 4), (3, 2), (1, 2, 9), (3, 1)])
add(5, [0, 0, 3, 1, 3, 4], [(1, 3, MAXX), (2, 5), (3, 2), (3, 4), (3, 3), (1, 4, 1), (3, 5), (3, 1)])

for n, kind, q in ((3, "path", 8), (8, "random", 15), (20, "star", 30), (40, "deep", 60), (60, "caterpillar", 90),
                   (100, "binary", 150), (300, "random", 500)):
    p, lab = tree(n, kind)
    add(n, p, rops(n, q, lab, 0.3, 0.3, 9))
for n, kind in ((4000, "path"), (6000, "broom"), (6000, "chains")):
    p, lab = tree(n, kind)
    add(n, p, rops(n, 6000, lab, 0.3, 0.3, MAXX, 200, 2000, (0, n // 2)))

N = MAXN
big("path", 100_000, 0.3, 0.3, 5_000, 30_000, (0, 50_000))
big("path", 100_000, 0.2, 0.5, 1_000, 1_000, (0, 99_000), 9)
big("deep", 100_000, 0.3, 0.3, 2_000, 20_000, (0, 60_000))
big("caterpillar", 100_000, 0.3, 0.3, 5_000, 50_000, (0, 50_000))
big("broom", 100_000, 0.35, 0.3, 30_000, 50_000, (0, N))
big("chains", 100_000, 0.3, 0.3, 300, 30_000, (0, 3_000))
big("random", 100_000, 0.3, 0.3, 100, None, (0, 1_000))
big("star", 100_000, 0.3, 0.3, 1, None, None, 9)
big("path", 100_000, 0.45, 0.1, 50_000, 50_000, (0, N))
big("deep", 100_000, 0.1, 0.45, 100, 1_000, (0, 1_000))
big("broom", 100_000, 0.2, 0.4, 2_000, 40_000, (0, 50_000))
big("caterpillar", 100_000, 0.25, 0.35, 500, 10_000, (0, 20_000), 9)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

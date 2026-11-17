# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(220007)
MAXN, MAXQ, MAXV = 100_000, 100_000, 10**9
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
    height = [0] * (n + 1)
    for i in range(n, 1, -1):
        if height[i] + 1 > height[par[i]]:
            height[par[i]] = height[i] + 1
    return p, lab, height[1:]


def add(n, w, p, qs):
    q = len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ and len(w) == n and len(p) == n + 1
    assert 0 <= min(w) and max(w) <= MAXV
    ch = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        ch[p[i]].append(i)
    order = [1]
    for u in order:
        order.extend(ch[u])
    assert len(order) == n
    vs, ks = zip(*qs)
    assert 1 <= min(vs) and max(vs) <= n and 0 <= min(ks) and max(ks) <= n
    t = (f"{n} {q}\n" + " ".join(map(str, w)) + "\n" + " ".join(map(str, p[2:])) + "\n"
         + "".join("%d %d\n" % e for e in qs))
    assert len(t) <= 3_100_000
    tests.append(t)


def rqs(n, q, lab, height, top=None, full=0.05, zero=0.03):
    res = []
    for _ in range(q):
        i = int(random.random() * (top or n))
        h = height[i]
        r = random.random()
        if r < zero:
            k = 0
        elif r < zero + full:
            k = ri(h, n)
        else:
            k = ri(h // 4, max(h // 4, (3 * h) // 4))
        res.append((lab[i], k))
    return res


def big(kind, q, vhi, top, n=MAXN, full=0.05):
    p, lab, height = tree(n, kind)
    add(n, [ri(0, vhi) for _ in range(n)], p, rqs(n, q, lab, height, top, full))


add(7, [3, 1, 4, 1, 5, 9, 2], [0, 0, 1, 1, 2, 2, 4, 3], [(1, 1), (2, 1), (2, 5), (1, 2)])
add(4, [10, 20, 30, 40], [0, 0, 1, 2, 3], [(1, 2), (3, 0), (2, 4)])
add(2, [MAXV, MAXV], [0, 0, 1], [(1, 1), (2, 0), (1, 0)])
add(5, [0, 1, 2, 3, 4], [0, 0, 1, 1, 1, 1], [(1, 0), (1, 1), (4, 3)])
add(6, [1, 2, 3, 4, 5, 6], [0, 0, 6, 1, 2, 3, 1], [(1, 1), (6, 1), (1, 2), (6, 3)])

for n, kind, q in ((3, "path", 6), (10, "random", 20), (30, "deep", 40), (40, "star", 60), (80, "caterpillar", 100),
                   (300, "binary", 300)):
    p, lab, height = tree(n, kind)
    add(n, [ri(0, 100) for _ in range(n)], p, rqs(n, q, lab, height, None, 0.1, 0.1))
for n, kind in ((5000, "path"), (8000, "broom"), (8000, "chains")):
    p, lab, height = tree(n, kind)
    add(n, [ri(0, MAXV) for _ in range(n)], p, rqs(n, 8000, lab, height, 200))

big("path", MAXQ, MAXV, 2_000)
big("path", 70_000, MAXV, 200, full=0.0)
big("deep", MAXQ, 9999, 2_000)
big("caterpillar", MAXQ, MAXV, 2_000)
big("broom", MAXQ, 9999, 1_000)
big("chains", MAXQ, MAXV, 300)
big("star", MAXQ, 9999, 1, full=0.3)
big("binary", MAXQ, 9999, 3, full=0.5)
big("random", MAXQ, MAXV, 5)
big("deep", MAXQ, MAXV, 50, full=0.0)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind, legs=4):
    par = [0, 0]
    half = max(1, n // 2)
    leg = max(1, (n - 1) // legs)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "spider":
            p = 1 if (i - 2) % leg == 0 or i - 1 > leg * legs else i - 1
        elif kind == "lopsided":
            p = 1 if i == 2 or i == 2 + (n - 1) * 9 // 10 else i - 1
        elif kind == "forkdeep":
            q = n // 4
            if i <= q:
                p = i - 1
            elif i == q + 1 or i == q + 2:
                p = q
            else:
                p = i - 2
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def depths(par):
    d = [0] * len(par)
    for i in range(2, len(par)):
        d[i] = d[par[i]] + 1
    return d


def relabel(par):
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(1, n + 1))
    shuffle(lab)
    j = lab.index(1)
    lab[0], lab[j] = lab[j], lab[0]
    P = [0] * (n + 1)
    for i in range(2, n + 1):
        P[lab[i - 1]] = lab[par[i] - 1]
    return P, lab


def check_tree(n, P):
    assert len(P) == n + 1
    kids = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        assert 1 <= P[i] <= n and P[i] != i
        kids[P[i]].append(i)
    seen, order = [False] * (n + 1), [1]
    seen[1] = True
    for v in order:
        for c in kids[v]:
            assert not seen[c]
            seen[c] = True
            order.append(c)
    assert len(order) == n


MAXN, MAXQ, MAXK = 100_000, 100_000, 200_000


def add(n, P, qs):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ and sum(len(g) for g in qs) <= MAXK
    check_tree(n, P)
    for g in qs:
        assert len(g) >= 1 and len(set(g)) == len(g) and 1 <= min(g) and max(g) <= n
    t = f"{n} {len(qs)}\n" + " ".join(str(P[i]) for i in range(2, n + 1)) + "\n" \
        + "".join(f"{len(g)} " + " ".join(map(str, g)) + "\n" for g in qs)
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    tests.append(t)


def pick(pool, k, used):
    if k > 500:
        out = [x for x in pool if x not in used]
        m = len(out)
        k = min(k, m)
        rnd = random.random
        for i in range(k):
            j = i + int(rnd() * (m - i))
            out[i], out[j] = out[j], out[i]
        out = out[:k]
        used.update(out)
        return out
    out = []
    rnd = random.random
    tries = 0
    while len(out) < k and tries < 20 * k + 100:
        tries += 1
        x = pool[int(rnd() * len(pool))]
        if x not in used:
            used.add(x)
            out.append(x)
    return out


def make(n, kind, sizes, mode="rand", legs=4, top=10, deep=0.01, ptop=0.5):
    par = shape(n, kind, legs)
    P, lab = relabel(par)
    d = depths(par)
    byd = sorted(range(1, n + 1), key=lambda i: d[i])
    bottom = byd[-max(2, int(n * deep)):]
    tops = byd[1:1 + max(1, top)] if n > 1 else byd
    allv = list(range(1, n + 1))
    rnd = random.random
    qs = []
    for k in sizes:
        used = set()
        if mode == "far":
            g = []
            if k >= 2 and rnd() < ptop:
                g = pick(tops, 1, used)
            g += pick(bottom, k - len(g), used)
            if len(g) < k:
                g += pick(allv, k - len(g), used)
        else:
            g = pick(allv, k, used)
        if len(g) > 1:
            j = int(rnd() * len(g))
            g[0], g[j] = g[j], g[0]
        qs.append([lab[x - 1] for x in g])
    add(n, P, qs)


random.seed(230302)

add(9, [0, 0, 5, 1, 2, 1, 4, 4, 3, 6], [[9, 7, 4], [7, 8], [6], [9, 2]])
add(5, [0, 0, 4, 5, 1, 2], [[3, 4], [5, 3, 2]])
add(2, [0, 0, 1], [[1, 2], [2]])
add(6, [0, 0, 1, 1, 1, 1, 1], [[2, 3, 4, 5, 6], [4], [6, 1], [5, 2]])
add(8, [0, 0, 7, 2, 2, 8, 4, 1, 1], [[5, 3], [4, 6, 3], [6, 8], [2, 7, 1], [3, 5, 4]])

add(2, [0, 0, 1], [[2, 1], [1], [2]])
make(10, "random", [ri(1, 4) for _ in range(30)])
make(60, "deep", [ri(1, 6) for _ in range(100)], "far", top=3, deep=0.2)
make(100, "caterpillar", [ri(2, 10) for _ in range(100)])
make(300, "binary", [ri(1, 20) for _ in range(200)])
make(3000, "star", [ri(1, 5) for _ in range(2000)])
make(4000, "random", [ri(1, 8) for _ in range(2000)])
make(5000, "spider", [ri(2, 4) for _ in range(3000)], "far", legs=6, deep=0.05)

make(MAXN, "path", [2] * MAXQ, "far", top=50)
make(MAXN, "spider", [2] * MAXQ, "far", legs=2)
make(MAXN, "spider", [ri(2, 3) for _ in range(70_000)], "far", legs=7, deep=0.02)
make(MAXN, "deep", [2] * MAXQ, "far", top=1000)
make(MAXN, "caterpillar", [ri(1, 3) for _ in range(95_000)], "far", deep=0.05)
make(MAXN, "broom", [2] * MAXQ, "far")
make(MAXN, "path", [60_000, 40_000, 60_000, 40_000], "far", top=5, deep=0.65, ptop=1)
make(MAXN, "broom", [48_000] * 4, "far", top=3, deep=0.5, ptop=1)
make(MAXN, "path", [30_000] * 6 + [100, 2, 1], "far", top=20, deep=0.3, ptop=1)
make(MAXN, "lopsided", [40_000] * 4 + [20_000] * 2, "far", top=2, deep=0.4, ptop=1)
make(MAXN, "path", [MAXN, MAXN], "rand")
make(MAXN, "forkdeep", [50_000] * 4, "far", top=20, deep=0.6, ptop=1)
make(MAXN, "deep", [1000] * 200, "far", deep=0.4)
make(MAXN, "spider", [10] * 20_000, "far", legs=4, deep=0.3)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

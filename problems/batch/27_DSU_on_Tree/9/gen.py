# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    h = max(1, 3 * n // 5)
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
        elif kind == "twopaths":
            p = 1 if i <= 3 else i - 2
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        elif kind == "longrandom":
            p = i - 1 if i <= h else ri(1, i - 1)
        elif kind == "longbinary":
            p = i - 1 if i <= h else h - 1 + (i - h + 1) // 2
        elif kind == "longstar":
            p = i - 1 if i <= h else 1
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def relabel(par):
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(n + 1))
    rest = lab[2:]
    shuffle(rest)
    lab[2:] = rest
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i]] = lab[par[i]]
    return lab, p


def check_parents(n, p):
    assert len(p) == n + 1
    state = [0] * (n + 1)
    state[1] = 1
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        path = []
        x = i
        while state[x] == 0:
            state[x] = 2
            path.append(x)
            x = p[x]
            assert state[x] != 2
        for y in path:
            state[y] = 1


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(270505)
MAXN = 200_000
MAXQ = 100_000


def add(n, p, c, qs):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    check_parents(n, p)
    assert len(c) == n + 1 and all(1 <= x <= n for x in c[1:])
    for v, k in qs:
        assert 1 <= v <= n and 1 <= k <= n
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, c[1:])) + "\n"
                 + "".join(f"{v} {k}\n" for v, k in qs))


def make(n, kind, ncol, q, top=1.0, kmax=None):
    par = shape(n, kind)
    lab, p = relabel(par)
    ncol = min(ncol, n)
    pool = [ri(1, min(n, 3 * ncol + 6)) for _ in range(ncol)]
    c = [0] + [pool[ri(0, ncol - 1)] for _ in range(n)]
    lim = max(1, int(top * n))
    typ = max(1, n // ncol)
    if kmax is None:
        kmax = min(n, 2 * typ)
    qs = []
    for _ in range(q):
        v = lab[ri(1, lim)]
        r = random.random()
        if r < 0.05:
            k = 1
        elif r < 0.1:
            k = ri(1, n)
        else:
            k = ri(1, kmax)
        qs.append((v, k))
    add(n, p, c, qs)


add(7, [0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 2, 1, 2, 2, 3, 1], [(1, 2), (1, 3), (2, 2), (3, 1), (3, 2), (1, 4)])
add(6, [0, 0, 1, 2, 3, 4, 5], [0, 5, 4, 5, 4, 4, 1], [(1, 2), (2, 3), (3, 2), (6, 1)])
add(2, [0, 0, 1], [0, 2, 2], [(1, 2), (1, 1), (2, 1), (2, 2)])
add(8, [0, 0, 1, 1, 1, 2, 2, 4, 4], [0, 3, 3, 1, 1, 3, 1, 1, 2], [(1, 1), (1, 3), (1, 4), (2, 2), (4, 2), (4, 3)])
add(5, [0, 0, 1, 1, 2, 2], [0, 4, 4, 4, 4, 4], [(1, 5), (2, 3), (5, 1), (3, 2)])

make(10, "random", 3, 30)
make(30, "caterpillar", 4, 60)
make(60, "binary", 5, 100)
make(200, "random", 2, 300)
make(300, "deep", 10, 300)
make(1000, "chains", 30, 1000)
make(2000, "broom", 3, 2000)
make(5000, "random", 50, 5000)

BQ = 60_000
make(MAXN, "path", 2, BQ, 0.3)
make(MAXN, "path", 1, BQ, 0.5, MAXN)
make(MAXN, "deep", 1, BQ, 0.3)
make(MAXN, "caterpillar", 2, BQ, 0.2)
make(MAXN, "broom", 1, BQ, 0.4)
make(MAXN, "longrandom", 2, BQ, 0.3)
make(MAXN, "longbinary", 1, BQ, 0.3)
make(MAXN, "longstar", 1, BQ, 0.3)
make(MAXN, "twopaths", 1, BQ, 0.1)
make(MAXN, "deep", 300, BQ, 0.2)
make(MAXN, "caterpillar", 1, BQ, 0.3)
make(MAXN, "path", 3, BQ, 0.2)
make(MAXN, "random", 3, BQ, 0.001)

write_all()

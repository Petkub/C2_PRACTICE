# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + random.getrandbits(40) % (hi - lo + 1)


def pct(p):
    return random.getrandbits(40) % 100 < p


def isqrt(x):
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, isqrt(n))
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
        elif kind == "deepchains":
            c = max(2, n // 50)
            p = i - 1 if (i - 1) % c else ri(max(1, i - 1 - c // 10), i - 1)
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
    for i in range(len(a) - 1, 0, -1):
        j = ri(0, i)
        a[i], a[j] = a[j], a[i]


class Tree:

    def __init__(self, n, kind):
        par = shape(n, kind)
        lab = list(range(1, n + 1))
        shuffle(lab)
        j = lab.index(1)
        lab[0], lab[j] = lab[j], lab[0]
        self.n = n
        self.p = [0] * (n + 1)
        for i in range(2, n + 1):
            self.p[lab[i - 1]] = lab[par[i] - 1]
        d = [0] * (n + 1)
        for i in range(2, n + 1):
            d[i] = d[par[i]] + 1
        self.dep = [0] * (n + 1)
        for i in range(1, n + 1):
            self.dep[lab[i - 1]] = d[i]
        order = sorted(range(1, n + 1), key=lambda i: d[i])
        k = max(1, n // 20)
        self.shallow = [lab[i - 1] for i in order[:k]]
        self.deep = [lab[i - 1] for i in order[-k:]]

    def node(self):
        return ri(1, self.n)

    def far_pair(self):
        u = self.deep[ri(0, len(self.deep) - 1)]
        v = self.shallow[ri(0, len(self.shallow) - 1)] if pct(50) else self.node()
        return (u, v) if pct(50) else (v, u)

    def pair(self, far):
        if pct(far):
            return self.far_pair()
        return self.node(), self.node()


def check_parents(n, p):
    assert len(p) == n + 1 and p[1] == 0
    state = [0] * (n + 1)
    state[1] = 2
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        path = []
        x = i
        while state[x] == 0:
            state[x] = 1
            path.append(x)
            x = p[x]
        assert state[x] == 2, "cycle"
        for y in path:
            state[y] = 2


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_145_728, len(t)
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(280404)
MAXN, MAXQ, MAXA = 100_000, 100_000, 10**9


def add(n, a, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(a) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(-MAXA <= x <= MAXA for x in a[1:])
    assert any(o[0] == "M" for o in ops)
    for o in ops:
        assert 1 <= o[1] <= n
        if o[0] == "R":
            assert len(o) == 4 and 1 <= o[2] <= n and -MAXA <= o[3] <= MAXA
        elif o[0] == "S":
            assert len(o) == 3 and -MAXA <= o[2] <= MAXA
        else:
            assert o[0] == "M" and len(o) == 3 and 1 <= o[2] <= n
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, a[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(" ".join(map(str, o)) + "\n" for o in ops))


def make(n, kind, q, amax, cmax, mix, far):
    t = Tree(n, kind)
    a = [0] + [ri(-amax, amax) for _ in range(n)]
    ops = []
    c0, c1 = mix[0], mix[0] + mix[1]
    tot = sum(mix)
    for _ in range(q):
        r = ri(0, tot - 1)
        if r < c0:
            u, v = t.pair(far)
            ops.append(("R", u, v, ri(-cmax, cmax)))
        elif r < c1:
            ops.append(("S", t.node(), ri(-amax, amax)))
        else:
            ops.append(("M",) + t.pair(far))
    ops[-1] = ("M",) + t.far_pair()
    add(n, a, t.p, ops, True)


add(7, [0, 3, -5, 2, 4, -1, -6, 0], [0, 0, 1, 1, 2, 2, 3, 3],
    [("M", 4, 6), ("R", 4, 6, 10), ("M", 5, 7), ("R", 2, 3, 0), ("M", 5, 7)])
add(4, [0, 1, 2, 3, 4], [0, 0, 1, 2, 3],
    [("R", 1, 4, 5), ("R", 2, 3, 1), ("M", 3, 4), ("S", 1, -9), ("M", 1, 3)])
add(2, [0, -1000000000, 1000000000], [0, 0, 1],
    [("R", 1, 2, 0), ("M", 2, 1), ("S", 1, 0), ("M", 1, 2)])
add(6, [0, 1, 1, -1, -1, 1, -1], [0, 0, 1, 2, 3, 1, 5],
    [("R", 4, 6, 2), ("M", 2, 3), ("M", 6, 4), ("R", 3, 3, -4), ("M", 4, 3)])
add(8, [0, 0, 5, -5, 2, -2, 7, -7, 1], [0, 0, 1, 1, 2, 2, 3, 3, 4],
    [("M", 8, 7), ("R", 5, 6, -3), ("M", 8, 6), ("R", 8, 1, 9), ("M", 4, 3)])

make(5, "random", 40, 5, 5, (1, 1, 1), 0)
make(8, "path", 60, 3, 3, (3, 1, 2), 30)
make(12, "binary", 80, 10, 10, (2, 1, 1), 30)
make(40, "caterpillar", 200, 100, 100, (2, 1, 2), 50)
make(300, "random", 500, MAXA, MAXA, (2, 1, 2), 50)
make(2_000, "chains", 3_000, 1000, 1000, (2, 1, 2), 50)
make(10_000, "deep", 10_000, MAXA, MAXA, (2, 1, 2), 80)
make(10_000, "broom", 10_000, 0, 5, (3, 0, 2), 80)

make(MAXN, "path", 80_000, MAXA, MAXA, (2, 1, 2), 90)
make(MAXN, "deep", MAXQ, 1000, 1000, (2, 1, 2), 90)
make(MAXN, "caterpillar", 80_000, MAXA, MAXA, (1, 1, 1), 90)
make(MAXN, "broom", MAXQ, 10, 10, (2, 1, 2), 90)
make(MAXN, "twopaths", 80_000, MAXA, MAXA, (2, 1, 2), 90)
make(MAXN, "longrandom", MAXQ, 100, 100, (3, 1, 2), 90)
make(MAXN, "longbinary", 80_000, MAXA, MAXA, (2, 1, 2), 90)
make(MAXN, "longstar", MAXQ, 1000, 99, (2, 1, 2), 90)
make(MAXN, "deepchains", 80_000, MAXA, MAXA, (2, 1, 2), 90)
make(MAXN, "deep", MAXQ, 0, 9, (3, 1, 1), 90)

write_all()

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
        return 1 + int(random.random() * self.n)

    def far_pair(self):
        rnd = random.random
        u = self.deep[int(rnd() * len(self.deep))]
        v = self.shallow[int(rnd() * len(self.shallow))] if rnd() < 0.5 else 1 + int(rnd() * self.n)
        return (u, v) if rnd() < 0.5 else (v, u)

    def pair(self, far):
        if random.random() < far:
            return self.far_pair()
        return 1 + int(random.random() * self.n), 1 + int(random.random() * self.n)


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
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(280505)
MAXN, MAXQ, MAXV = 100_000, 100_000, 10**9


def add(n, gc, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(gc) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(-MAXV <= g <= MAXV and 0 <= c <= MAXV for g, c in gc[1:])
    assert any(o[0] == 2 for o in ops)
    for o in ops:
        assert len(o) == 4 and 1 <= o[1] <= n
        if o[0] == 1:
            assert -MAXV <= o[2] <= MAXV and 0 <= o[3] <= MAXV
        else:
            assert o[0] == 2 and 1 <= o[2] <= n and 0 <= o[3] <= MAXV
    tests.append(f"{n} {len(ops)}\n" + "".join(f"{g} {c}\n" for g, c in gc[1:]) + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{o[0]} {o[1]} {o[2]} {o[3]}\n" for o in ops))


def village(gmax, cmax):
    return (ri(-gmax, gmax), ri(0, cmax) if random.random() < 0.7 else ri(cmax // 2, cmax))


def make(n, kind, q, gmax, cmax, upd, far):
    t = Tree(n, kind)
    gc = [None] + [village(gmax, cmax) for _ in range(n)]
    ops = []
    for _ in range(q):
        if random.random() < upd:
            g, c = village(gmax, cmax)
            ops.append((1, t.node(), g, c))
        else:
            u, v = t.pair(far)
            ops.append((2, u, v, ri(0, cmax)))
    u, v = t.far_pair()
    ops[-1] = (2, u, v, 0)
    add(n, gc, t.p, ops, True)


add(5, [None, (5, 10), (-3, 10), (8, 9), (-6, 20), (2, 3)], [0, 0, 1, 2, 3, 2],
    [(2, 5, 4, 1), (1, 3, -1, 5), (2, 1, 4, 7)])
add(3, [None, (4, 4), (-1, 100), (5, 7)], [0, 0, 1, 2], [(2, 1, 3, 0), (2, 1, 3, 9), (2, 1, 2, 2)])
add(2, [None, (-1000000000, 0), (1000000000, 1000000000)], [0, 0, 1],
    [(2, 1, 2, 1000000000), (1, 1, 7, 1000000000), (2, 1, 2, 3)])
add(4, [None, (0, 5), (3, 8), (-2, 9), (6, 6)], [0, 0, 1, 1, 2], [(2, 3, 4, 4), (1, 2, -8, 8), (2, 1, 4, 0)])
add(4, [None, (1, 5), (-2, 5), (3, 4), (-3, 3)], [0, 0, 1, 2, 1], [(2, 4, 3, 3), (1, 2, -1, 1), (2, 1, 3, 0)])

make(5, "random", 40, 5, 10, 0.3, 0.0)
make(12, "path", 80, 10, 20, 0.3, 0.5)
make(40, "caterpillar", 200, 20, 60, 0.3, 0.5)
make(300, "random", 500, MAXV, MAXV, 0.3, 0.5)
make(2_000, "chains", 3_000, 100, 1000, 0.3, 0.7)
make(10_000, "deep", 10_000, 10**6, 10**7, 0.3, 0.8)

make(MAXN, "path", MAXQ, 100, 1000, 0.3, 0.9)
make(MAXN, "deep", MAXQ, 50, 1000, 0.3, 0.9)
make(MAXN, "caterpillar", MAXQ, 100, 999, 0.3, 0.9)
make(MAXN, "broom", MAXQ, 10, 100, 0.3, 0.9)
make(MAXN, "twopaths", MAXQ, 100, 1000, 0.2, 0.9)
make(MAXN, "longrandom", MAXQ, 30, 500, 0.3, 0.9)
make(MAXN, "longbinary", MAXQ, 100, 1000, 0.3, 0.9)
make(MAXN, "longstar", MAXQ, 99, 999, 0.3, 0.9)
make(MAXN, "path", MAXQ, 5, 50, 0.1, 0.9)
make(MAXN, "deep", MAXQ, 300, 999, 0.4, 0.9)

write_all()

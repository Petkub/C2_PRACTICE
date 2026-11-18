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

random.seed(280202)
MAXN, MAXQ, MAXV = 100_000, 100_000, 10**9


def add(n, c, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(c) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(1 <= x <= MAXV for x in c[2:])
    assert any(o[0] == 2 for o in ops)
    for o in ops:
        assert 1 <= o[1] <= n and 1 <= o[2] <= n and o[1] != o[2]
        assert (o[0] == 1 and len(o) == 4 and 1 <= o[3] <= MAXV) or (o[0] == 2 and len(o) == 3)
    tests.append(f"{n} {len(ops)}\n" + "".join(f"{p[i]} {c[i]}\n" for i in range(2, n + 1))
                 + "".join(f"{o[0]} {o[1]} {o[2]} {o[3]}\n" if len(o) == 4 else f"{o[0]} {o[1]} {o[2]}\n" for o in ops))


def make(n, kind, q, wmode, xmax, upd, far):
    t = Tree(n, kind)
    md = max(t.dep) + 1
    c = [0] * (n + 1)
    for i in range(2, n + 1):
        if wmode == "rand":
            c[i] = ri(1, MAXV)
        elif wmode == "small":
            c[i] = ri(1, 20)
        else:
            c[i] = 1 + (MAXV // 2) * t.dep[i] // md + ri(0, 1000)
    ops = []
    for _ in range(q):
        u, v = t.pair(far)
        while u == v:
            u, v = t.pair(far)
        if random.random() < upd:
            ops.append((1, u, v, ri(1, xmax)))
        else:
            ops.append((2, u, v))
    if all(o[0] == 1 for o in ops):
        ops[-1] = (2, ops[-1][1], ops[-1][2])
    add(n, c, t.p, ops, True)


add(6, [0, 0, 5, 8, 3, 6, 4], [0, 0, 1, 1, 2, 2, 3],
    [(2, 4, 6), (1, 4, 6, 2), (2, 4, 6), (2, 5, 4)])
add(4, [0, 0, 7, 1, 9], [0, 0, 1, 2, 3], [(2, 2, 4), (1, 1, 3, 5), (2, 1, 4)])
add(2, [0, 0, 5], [0, 0, 1], [(2, 1, 2), (1, 2, 1, 1000000000), (2, 2, 1)])
add(7, [0, 0, 4, 9, 2, 7, 6, 5], [0, 0, 1, 2, 2, 1, 5, 5],
    [(2, 3, 7), (1, 3, 6, 3), (2, 4, 6), (2, 7, 3), (1, 7, 1, 1), (2, 6, 7)])
add(8, [0, 0, 3, 3, 3, 3, 3, 3, 3], [0, 0, 1, 2, 3, 1, 5, 6, 1],
    [(2, 4, 7), (1, 2, 8, 4), (2, 4, 7), (2, 3, 1)])

make(5, "random", 30, "small", 5, 0.4, 0.0)
make(10, "binary", 60, "down", 10, 0.3, 0.5)
make(40, "caterpillar", 200, "small", 20, 0.3, 0.5)
make(300, "random", 500, "rand", MAXV, 0.3, 0.3)
make(2_000, "chains", 3_000, "down", 1000, 0.4, 0.7)
make(10_000, "deep", 10_000, "rand", MAXV, 0.3, 0.8)

make(MAXN, "path", MAXQ, "rand", 1000, 0.3, 0.9)
make(MAXN, "path", MAXQ, "down", 1000, 0.3, 0.9)
make(MAXN, "deep", MAXQ, "down", MAXV, 0.3, 0.9)
make(MAXN, "caterpillar", MAXQ, "small", MAXV, 0.5, 0.9)
make(MAXN, "broom", MAXQ, "down", 10, 0.3, 0.9)
make(MAXN, "twopaths", MAXQ, "small", MAXV, 0.3, 0.9)
make(MAXN, "longrandom", MAXQ, "down", 100, 0.3, 0.9)
make(MAXN, "longbinary", MAXQ, "rand", 100, 0.3, 0.9)
make(MAXN, "longstar", MAXQ, "down", MAXV, 0.4, 0.9)
make(MAXN, "longrandom", MAXQ, "small", 5, 0.1, 0.9)

write_all()

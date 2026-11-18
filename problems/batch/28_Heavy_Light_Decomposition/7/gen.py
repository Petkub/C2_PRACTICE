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

random.seed(280909)
MAXN, MAXQ, MAXW, MAXX, MAXH = 100_000, 100_000, 10**9, 10_000, 3 * 10**9


def add(n, w, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(w) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(0 <= x <= MAXW for x in w[1:])
    assert any(o[0] == 2 for o in ops)
    for o in ops:
        assert len(o) == 4 and 1 <= o[1] <= n and 1 <= o[2] <= n
        assert 1 <= o[3] <= (MAXX if o[0] == 1 else MAXH)
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, w[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{o[0]} {o[1]} {o[2]} {o[3]}\n" for o in ops))


def make(n, kind, q, wmax, xmax, upd, far, rare, down=0.0):
    t = Tree(n, kind)
    w = [0] + [ri(0, wmax) for _ in range(n)]
    ops = []
    top = wmax
    for _ in range(q):
        if random.random() < down:
            u = t.shallow[int(random.random() * len(t.shallow))] if random.random() < 0.7 else t.node()
            v = t.deep[int(random.random() * len(t.deep))] if random.random() < 0.7 else t.node()
        else:
            u, v = t.pair(far)
        if random.random() < upd:
            x = ri(1, xmax)
            ops.append((1, u, v, x))
            top += x // 4
        else:
            h = max(1, min(MAXH, int(top * (rare + (1 - rare) * random.random() * 1.1))))
            ops.append((2, u, v, h))
    u, v = t.far_pair()
    ops[-1] = (2, u, v, max(1, top))
    add(n, w, t.p, ops, True)


add(7, [0, 3, 5, 2, 1, 8, 4, 6], [0, 0, 1, 1, 2, 2, 3, 3],
    [(2, 4, 7, 5), (2, 7, 4, 5), (1, 4, 6, 3), (2, 6, 5, 6), (2, 1, 4, 9)])
add(5, [0, 1, 1, 1, 1, 1], [0, 0, 1, 2, 3, 4], [(2, 1, 5, 2), (1, 2, 4, 1), (2, 5, 1, 2), (2, 1, 5, 2)])
add(2, [0, 1000000000, 0], [0, 0, 1], [(1, 1, 2, 10000), (2, 2, 1, 1000010000), (2, 2, 2, 3000000000)])
add(8, [0, 0, 9, 9, 0, 0, 0, 0, 0], [0, 0, 1, 1, 2, 2, 3, 3, 5],
    [(2, 8, 7, 9), (1, 7, 7, 9), (2, 8, 7, 9), (2, 7, 8, 9), (2, 4, 5, 1)])
add(6, [0, 2, 4, 6, 8, 6, 4], [0, 0, 1, 2, 3, 4, 5], [(2, 6, 1, 7), (2, 1, 6, 7), (1, 6, 3, 2), (2, 6, 1, 7)])

make(5, "random", 40, 10, 3, 0.3, 0.0, 0.5)
make(12, "binary", 80, 20, 5, 0.3, 0.5, 0.7, 0.5)
make(40, "caterpillar", 200, 100, 10, 0.3, 0.5, 0.9)
make(300, "random", 500, MAXW, MAXX, 0.3, 0.5, 0.8, 0.6)
make(2_000, "chains", 3_000, 1000, 10, 0.3, 0.7, 0.99)
make(10_000, "longbinary", 10_000, 10**6, 100, 0.3, 0.8, 0.8, 0.7)

make(MAXN, "path", 80_000, 10**6, 100, 0.3, 0.9, 0.9999)
make(MAXN, "deep", 80_000, 10**6, 1000, 0.3, 0.9, 0.9995)
make(MAXN, "caterpillar", 70_000, MAXW, MAXX, 0.3, 0.9, 0.8, 0.7)
make(MAXN, "broom", 80_000, 10**5, 10, 0.3, 0.9, 0.9999)
make(MAXN, "twopaths", 80_000, 10**6, 100, 0.3, 0.9, 0.95, 0.5)
make(MAXN, "longrandom", 80_000, 10**6, 100, 0.3, 0.9, 0.7, 0.7)
make(MAXN, "longbinary", 80_000, 10**6, 100, 0.3, 0.9, 0.8, 0.7)
make(MAXN, "longstar", 80_000, 10**6, 100, 0.3, 0.9, 0.9, 0.7)
make(MAXN, "path", 80_000, 10**5, 10, 0.5, 0.9, 1.0)
make(MAXN, "longbinary", 70_000, MAXW, MAXX, 0.2, 0.9, 0.6, 0.8)

write_all()

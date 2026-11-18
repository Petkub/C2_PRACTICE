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

random.seed(281010)
MAXN, MAXQ, MAXW = 100_000, 100_000, 10_000


def add(n, p, w, qs, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ and len(w) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(1 <= x <= MAXW for x in w[2:])
    for l, r, z in qs:
        assert 1 <= l <= r <= n and 1 <= z <= n
    tests.append(f"{n} {len(qs)}\n" + "".join(f"{p[i]} {w[i]}\n" for i in range(2, n + 1))
                 + "".join(f"{l} {r} {z}\n" for l, r, z in qs))


def make(n, kind, q, wmax, wide, deepz):
    t = Tree(n, kind)
    w = [0, 0] + [ri(1, wmax) if wmax > 1 else 1 for _ in range(n - 1)]
    qs = []
    for _ in range(q):
        if random.random() < wide:
            a = ri(1, n // 2)
            l, r = a, a + n // 2 - 1 + ri(0, n // 2 - a + 1 if n // 2 - a + 1 > 0 else 0)
            r = min(r, n)
        else:
            l, r = sorted((t.node(), t.node()))
        z = t.deep[int(random.random() * len(t.deep))] if random.random() < deepz else t.node()
        qs.append((l, r, z))
    add(n, t.p, w, qs, True)


add(6, [0, 0, 1, 1, 2, 2, 3], [0, 0, 2, 5, 1, 3, 4], [(1, 6, 1), (4, 5, 6), (2, 3, 4), (6, 6, 6)])
add(4, [0, 0, 1, 2, 3], [0, 0, 1, 1, 1], [(1, 4, 2), (3, 4, 1), (1, 1, 4)])
add(2, [0, 0, 1], [0, 0, 10000], [(1, 2, 1), (2, 2, 2), (1, 1, 2)])
add(7, [0, 0, 4, 1, 3, 4, 4, 2], [0, 0, 3, 7, 2, 6, 1, 9], [(2, 5, 7), (1, 7, 4), (3, 6, 3), (5, 7, 1)])
add(5, [0, 0, 1, 1, 1, 1], [0, 0, 10, 20, 30, 40], [(1, 5, 1), (2, 5, 2), (3, 3, 5)])

make(5, "random", 30, 5, 0.3, 0.3)
make(12, "binary", 60, 10, 0.3, 0.5)
make(40, "caterpillar", 150, 100, 0.5, 0.5)
make(300, "random", 400, MAXW, 0.5, 0.5)
make(2_000, "chains", 2_000, MAXW, 0.5, 0.5)
make(6_000, "deep", 6_000, 1, 0.5, 0.8)

make(MAXN, "path", MAXQ, MAXW, 0.8, 0.5)
make(MAXN, "deep", MAXQ, MAXW, 0.8, 0.5)
make(MAXN, "caterpillar", MAXQ, 1000, 0.8, 0.5)
make(MAXN, "broom", MAXQ, MAXW, 0.8, 0.5)
make(MAXN, "twopaths", MAXQ, 1, 0.8, 0.5)
make(MAXN, "longrandom", MAXQ, MAXW, 0.8, 0.5)
make(MAXN, "longbinary", MAXQ, MAXW, 0.9, 0.5)
make(MAXN, "binary", MAXQ, MAXW, 0.9, 0.5)
make(MAXN, "random", MAXQ, MAXW, 0.9, 0.5)
make(MAXN, "star", MAXQ, MAXW, 0.9, 0.5)

write_all()

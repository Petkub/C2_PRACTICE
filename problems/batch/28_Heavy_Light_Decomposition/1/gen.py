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

random.seed(280101)
MAXN, MAXQ, MAXH = 100_000, 100_000, 10**9


def add(n, h, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(h) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(1 <= x <= MAXH for x in h[1:])
    assert any(o[0] == 2 for o in ops)
    for o in ops:
        assert o[0] in (1, 2) and 1 <= o[1] <= n
        assert 1 <= o[2] <= (MAXH if o[0] == 1 else n)
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, h[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{a} {b} {c}\n" for a, b, c in ops))


def make(n, kind, q, hmax, upd, far):
    t = Tree(n, kind)
    h = [0] + [ri(1, hmax) for _ in range(n)]
    ops = []
    for _ in range(q):
        if random.random() < upd:
            ops.append((1, t.node(), ri(1, hmax)))
        else:
            u, v = t.pair(far)
            ops.append((2, u, v))
    if all(o[0] == 1 for o in ops):
        ops[-1] = (2, 1, n)
    add(n, h, t.p, ops, True)


add(7, [0, 5, 3, 8, 7, 2, 8, 4], [0, 0, 1, 1, 2, 2, 3, 6],
    [(2, 4, 7), (1, 3, 6), (2, 7, 4), (2, 5, 3)])
add(5, [0, 1, 6, 2, 6, 6], [0, 0, 1, 2, 3, 3], [(2, 4, 5), (2, 1, 4), (1, 2, 3), (2, 1, 4)])
add(3, [0, 1, 5, 5], [0, 0, 1, 1], [(2, 2, 3), (1, 3, 4), (2, 3, 2)])
add(6, [0, 2, 9, 4, 9, 1, 9], [0, 0, 1, 2, 1, 4, 5], [(2, 3, 6), (2, 6, 2), (1, 2, 1), (2, 3, 6), (1, 6, 10), (2, 2, 6)])
add(8, [0, 1, 4, 1, 4, 3, 2, 4, 3], [0, 0, 1, 1, 3, 3, 2, 6, 6],
    [(2, 4, 8), (2, 7, 5), (1, 5, 4), (2, 8, 5), (2, 7, 4)])

add(3, [0, 5, 5, 5], [0, 0, 1, 1], [(2, 2, 3), (2, 1, 1), (2, 2, 2), (1, 1, 6), (2, 2, 3), (2, 3, 1)])
make(6, "random", 40, 3, 0.3, 0.0)
make(12, "binary", 80, 4, 0.3, 0.0)
make(40, "caterpillar", 200, 5, 0.3, 0.5)
make(300, "random", 500, 10**9, 0.3, 0.3)
make(2_000, "chains", 3_000, 6, 0.4, 0.5)
make(10_000, "deep", 10_000, 50, 0.3, 0.8)

make(MAXN, "path", MAXQ, 10**9, 0.3, 0.9)
make(MAXN, "path", MAXQ, 3, 0.3, 0.9)
make(MAXN, "deep", MAXQ, 100, 0.2, 0.9)
make(MAXN, "caterpillar", MAXQ, 10**9, 0.3, 0.9)
make(MAXN, "broom", MAXQ, 10, 0.3, 0.9)
make(MAXN, "twopaths", MAXQ, 1000, 0.3, 0.9)
make(MAXN, "longrandom", MAXQ, 10**9, 0.3, 0.9)
make(MAXN, "longbinary", MAXQ, 5, 0.3, 0.9)
make(MAXN, "longstar", MAXQ, 2, 0.4, 0.9)
make(MAXN, "longrandom", MAXQ, 20, 0.1, 0.9)

write_all()

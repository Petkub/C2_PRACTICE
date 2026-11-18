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

    def up(self, v, k):
        while k > 0 and self.p[v]:
            v = self.p[v]
            k -= 1
        return v


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

random.seed(281111)
MAXN, MAXQ = 100_000, 100_000


def add(n, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    if not tree_ok:
        check_parents(n, p)
    assert any(o[0] == 2 for o in ops)
    for o in ops:
        assert o[0] in (1, 2) and 1 <= o[1] <= n and 1 <= o[2] <= n
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{o[0]} {o[1]} {o[2]}\n" for o in ops))


def make(n, kind, q, upd, hole, far, follow):
    t = Tree(n, kind)
    ops = []
    recent = [t.far_pair()]
    for _ in range(q):
        if pct(upd):
            if pct(hole):
                v = t.node()
                ops.append((1, v, v if pct(50) else t.up(v, 1)))
            else:
                a, b = t.pair(far)
                ops.append((1, a, b))
                recent.append((a, b))
                if len(recent) > 8:
                    recent.pop(0)
        elif pct(follow):
            a, b = recent[ri(0, len(recent) - 1)]
            k = ri(0, 3)
            if k == 1:
                a = t.up(a, ri(0, 30))
            elif k == 2:
                b = t.node()
            elif k == 3:
                b = t.far_pair()[0]
            ops.append((2, a, b) if pct(50) else (2, b, a))
        else:
            ops.append((2,) + t.pair(far))
    ops[-1] = (2,) + recent[-1]
    add(n, t.p, ops, True)


add(8, [0, 0, 1, 2, 3, 4, 2, 3, 6], [(1, 8, 5), (2, 5, 1), (1, 4, 4), (2, 2, 5)])
add(5, [0, 0, 1, 2, 3, 4], [(1, 1, 5), (2, 4, 1), (1, 3, 3), (2, 5, 1), (2, 3, 3)])
add(2, [0, 0, 1], [(2, 1, 2), (1, 2, 1), (2, 1, 2), (1, 1, 1), (2, 2, 1)])
add(8, [0, 0, 1, 2, 3, 4, 2, 3, 6], [(1, 6, 3), (1, 2, 5), (1, 6, 8), (2, 5, 8), (2, 4, 6)])
add(7, [0, 0, 1, 1, 2, 2, 3, 3], [(1, 1, 1), (1, 1, 4), (2, 4, 7), (1, 5, 5), (2, 6, 5), (2, 3, 3)])

make(5, "random", 40, 50, 30, 0, 50)
make(12, "binary", 80, 50, 30, 50, 60)
make(40, "caterpillar", 200, 50, 30, 50, 60)
make(300, "random", 500, 50, 30, 50, 60)
make(2_000, "star", 3_000, 50, 30, 50, 60)
make(2_000, "chains", 3_000, 50, 30, 50, 70)
make(10_000, "deep", 10_000, 40, 30, 80, 70)

make(MAXN, "path", MAXQ, 50, 30, 90, 70)
make(MAXN, "deep", MAXQ, 50, 30, 90, 70)
make(MAXN, "caterpillar", MAXQ, 50, 30, 90, 70)
make(MAXN, "broom", MAXQ, 50, 30, 90, 70)
make(MAXN, "twopaths", MAXQ, 40, 30, 90, 70)
make(MAXN, "longrandom", MAXQ, 50, 30, 90, 70)
make(MAXN, "longbinary", MAXQ, 50, 30, 90, 70)
make(MAXN, "longstar", MAXQ, 50, 20, 90, 70)
make(MAXN, "deepchains", MAXQ, 50, 30, 90, 70)
make(MAXN, "path", MAXQ, 60, 50, 70, 80)
make(MAXN, "deep", MAXQ, 30, 40, 90, 60)

write_all()

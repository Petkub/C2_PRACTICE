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

random.seed(280808)
MAXN, MAXQ, MAXT, MAXF = 100_000, 100_000, 100_000, 10_000


def add(n, team, fans, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(team) == n + 1 and len(fans) == n + 1
    if not tree_ok:
        check_parents(n, p)
    assert all(1 <= x <= MAXT for x in team[1:]) and all(1 <= x <= MAXF for x in fans[1:])
    assert any(o[0] == "Q" for o in ops)
    lines = []
    for o in ops:
        if o[0] == "T":
            assert len(o) == 3 and 1 <= o[1] <= n and 1 <= o[2] <= MAXT
        elif o[0] == "F":
            assert len(o) == 3 and 1 <= o[1] <= n and 1 <= o[2] <= MAXF
        elif o[0] == "M":
            assert len(o) == 3 and 1 <= o[1] <= MAXT and 1 <= o[2] <= MAXT and o[1] != o[2]
        else:
            assert o[0] == "Q" and len(o) == 4 and 1 <= o[1] <= n and 1 <= o[2] <= n and 1 <= o[3] <= MAXT
        lines.append(" ".join(map(str, o)))
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, team[1:])) + "\n" + " ".join(map(str, fans[1:])) + "\n"
                 + " ".join(map(str, p[2:])) + "\n" + "\n".join(lines) + "\n")


class Teams:

    def __init__(self, team):
        self.gp, self.gt, self.cur = [], [], {}
        self.grp = [0] + [self.group(t) for t in team[1:]]

    def group(self, t):
        if t not in self.cur:
            self.cur[t] = len(self.gp)
            self.gp.append(len(self.gp))
            self.gt.append(t)
        return self.cur[t]

    def find(self, g):
        gp = self.gp
        r = g
        while gp[r] != r:
            r = gp[r]
        while gp[g] != r:
            gp[g], g = r, gp[g]
        return r

    def of(self, v):
        return self.gt[self.find(self.grp[v])]

    def move(self, v, t):
        self.grp[v] = self.group(t)

    def merge(self, a, b):
        if a not in self.cur:
            return
        ga = self.cur.pop(a)
        if b in self.cur:
            self.gp[ga] = self.cur[b]
        else:
            self.cur[b] = ga
            self.gt[ga] = b


def make(n, kind, q, k, fmax, mix, far):
    t = Tree(n, kind)
    labels = sorted(set(ri(1, MAXT) for _ in range(k)))
    pick = lambda: labels[int(random.random() * len(labels))]
    team = [0] + [pick() for _ in range(n)]
    fans = [0] + [ri(1, fmax) for _ in range(n)]
    cur = Teams(team)
    ops = []
    c0, c1, c2, tot = mix[0], mix[0] + mix[1], mix[0] + mix[1] + mix[2], sum(mix)
    for _ in range(q):
        r = random.random() * tot
        if r < c0:
            v = t.node()
            b = pick()
            cur.move(v, b)
            ops.append(("T", v, b))
        elif r < c1:
            ops.append(("F", t.node(), ri(1, fmax)))
        elif r < c2:
            a = cur.of(t.node()) if random.random() < 0.85 else pick()
            if random.random() < 0.9 and len(labels) > 1:
                b = pick()
                while b == a:
                    b = pick()
            else:
                b = ri(1, MAXT)
                while b == a:
                    b = ri(1, MAXT)
                if len(labels) < 2 * k + 2:
                    labels.append(b)
            cur.merge(a, b)
            ops.append(("M", a, b))
        else:
            u, v = t.pair(far)
            c = cur.of(u if random.random() < 0.5 else v) if random.random() < 0.8 else pick()
            ops.append(("Q", u, v, c))
    u, v = t.far_pair()
    ops[-1] = ("Q", u, v, cur.of(u))
    add(n, team, fans, t.p, ops, True)


add(7, [0, 1, 2, 1, 1, 2, 2, 1], [0, 5, 3, 4, 2, 7, 1, 6], [0, 0, 1, 1, 2, 2, 3, 3],
    [("Q", 4, 7, 1), ("M", 2, 1), ("Q", 4, 6, 1)])
add(4, [0, 3, 3, 8, 3], [0, 2, 2, 2, 2], [0, 0, 1, 2, 3],
    [("M", 3, 8), ("Q", 2, 3, 8), ("Q", 1, 2, 3)])
add(2, [0, 100000, 100000], [0, 10000, 10000], [0, 0, 1],
    [("Q", 1, 2, 100000), ("M", 100000, 99999), ("Q", 2, 2, 99999)])
add(6, [0, 4, 4, 4, 5, 5, 4], [0, 1, 2, 3, 4, 5, 6], [0, 0, 1, 2, 3, 3, 1],
    [("Q", 5, 6, 4), ("F", 6, 1), ("Q", 6, 4, 4)])
add(5, [0, 9, 9, 9, 9, 9], [0, 7, 1, 7, 1, 7], [0, 0, 1, 1, 2, 2],
    [("T", 1, 2), ("M", 9, 2), ("Q", 4, 5, 2)])

make(5, "random", 40, 2, 5, (1, 1, 1, 2), 0.0)
make(12, "binary", 80, 3, 10, (2, 1, 1, 2), 0.3)
make(40, "caterpillar", 200, 4, 100, (2, 1, 1, 2), 0.5)
make(300, "random", 500, 20, MAXF, (1, 1, 1, 2), 0.5)
make(2_000, "chains", 3_000, 50, MAXF, (2, 1, 1, 2), 0.7)
make(10_000, "deep", 10_000, 5, 100, (2, 1, 1, 3), 0.8)

make(MAXN, "path", MAXQ, 2, 100, (2, 1, 1, 3), 0.9)
make(MAXN, "caterpillar", MAXQ, 100, 100, (2, 1, 1, 2), 0.9)
make(MAXN, "broom", MAXQ, 3, 10, (2, 1, 2, 3), 0.9)
make(MAXN, "twopaths", MAXQ, 1000, 1000, (2, 1, 1, 3), 0.9)
make(MAXN, "longrandom", 80_000, MAXT, MAXF, (2, 1, 1, 3), 0.9)
make(MAXN, "longbinary", MAXQ, 5, 100, (2, 1, 1, 3), 0.9)
make(MAXN, "longstar", MAXQ, 20, 1000, (2, 1, 1, 3), 0.9)
make(MAXN, "path", MAXQ, 2, 10, (1, 1, 3, 3), 0.9)
make(MAXN, "deep", MAXQ, 300, 100, (3, 1, 2, 3), 0.9)
make(MAXN, "chains", 90_000, 1, MAXF, (0, 1, 1, 3), 0.9)

write_all()

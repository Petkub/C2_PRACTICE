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

random.seed(280707)
MAXN, MAXQ = 100_000, 100_000


def add(n, p, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    if not tree_ok:
        check_parents(n, p)
    present, made = set(), 0
    lines = []
    for o in ops:
        if o[0] == "+":
            assert len(o) == 3 and 1 <= o[1] <= n and 1 <= o[2] <= n and o[1] != o[2]
            made += 1
            present.add(made)
            lines.append(f"+ {o[1]} {o[2]}")
        else:
            assert len(o) == 2 and o[1] in present
            present.remove(o[1])
            lines.append(f"- {o[1]}")
    tests.append(f"{n} {len(ops)}\n" + " ".join(map(str, p[2:])) + "\n" + "\n".join(lines) + "\n")


def make(n, kind, q, keep, far):
    t = Tree(n, kind)
    ops, present, made = [], [], 0
    for _ in range(q):
        if present and random.random() < len(present) / (2 * keep):
            j = int(random.random() * len(present))
            present[j], present[-1] = present[-1], present[j]
            ops.append(("-", present.pop()))
        else:
            u, v = t.pair(far)
            while u == v:
                u, v = t.pair(far)
            made += 1
            present.append(made)
            ops.append(("+", u, v))
    add(n, t.p, ops, True)


add(7, [0, 0, 1, 1, 2, 2, 3, 3], [("+", 4, 5), ("+", 6, 2), ("+", 4, 1), ("-", 3), ("+", 7, 1)])
add(5, [0, 0, 1, 2, 3, 4], [("+", 2, 4), ("+", 1, 3), ("+", 5, 3), ("-", 1)])
add(2, [0, 0, 1], [("+", 1, 2), ("+", 2, 1), ("-", 1)])
add(8, [0, 0, 1, 1, 1, 2, 2, 3, 4], [("+", 5, 7), ("+", 8, 6), ("+", 2, 3), ("+", 4, 1), ("-", 3), ("+", 6, 5)])
add(6, [0, 0, 1, 2, 2, 4, 4], [("+", 5, 6), ("+", 3, 5), ("+", 6, 3), ("-", 1), ("+", 1, 2)])

make(5, "random", 40, 2, 0.0)
make(12, "binary", 80, 3, 0.5)
make(40, "caterpillar", 200, 5, 0.5)
make(300, "random", 500, 10, 0.5)
make(2_000, "chains", 3_000, 30, 0.7)
make(5_000, "deep", 5_000, 20, 0.8)

make(MAXN, "path", MAXQ, 5, 0.9)
make(MAXN, "path", MAXQ, 50, 0.9)
make(MAXN, "deep", MAXQ, 20, 0.9)
make(MAXN, "caterpillar", MAXQ, 100, 0.9)
make(MAXN, "broom", MAXQ, 10, 0.9)
make(MAXN, "twopaths", MAXQ, 30, 0.9)
make(MAXN, "longrandom", MAXQ, 200, 0.9)
make(MAXN, "longbinary", MAXQ, 50, 0.9)
make(MAXN, "longstar", MAXQ, 1000, 0.9)
make(MAXN, "deep", MAXQ, 3, 0.9)

write_all()

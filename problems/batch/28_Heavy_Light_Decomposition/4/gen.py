# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random


tests = []


def rb(m):
    return (random.getrandbits(32) * m) >> 32


def ri(lo, hi):
    return lo + rb(hi - lo + 1)


def isqrt(n):
    r = 0
    while (r + 1) * (r + 1) <= n:
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
        elif kind == "combs":
            s = n // 3
            if i <= s:
                p = i - 1
            elif (i - s) % 2 == 1:
                p = 1 + (i - s - 1) // 2 % s
            else:
                p = i - 1
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = rb(i + 1)
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
        order = sorted(range(1, n + 1), key=lambda i: (d[i], i))
        k = max(1, n // 20)
        self.shallow = [lab[i - 1] for i in order[:k]]
        self.deep = [lab[i - 1] for i in order[-k:]]

    def node(self):
        return 1 + rb(self.n)

    def top(self):
        return self.shallow[rb(len(self.shallow))]

    def far_pair(self):
        u = self.deep[rb(len(self.deep))]
        v = self.top() if rb(2) else self.node()
        return (u, v) if rb(2) else (v, u)

    def pair(self, far100):
        if rb(100) < far100:
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
    assert 18 <= len(tests) <= 30
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open("tests/%02d.in" % i, "w") as f:
            f.write(t)


random.seed(280303)
MAXN, MAXQ, MAXA, MAXX = 100_000, 100_000, 10**9, 1000


def add(n, a, p, ops):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ and len(a) == n + 1
    check_parents(n, p)
    assert all(-MAXA <= x <= MAXA for x in a[1:])
    assert any(o[0] in (2, 4) for o in ops)
    lines = []
    for o in ops:
        if o[0] == 1:
            assert len(o) == 4 and 1 <= o[1] <= n and 1 <= o[2] <= n and -MAXX <= o[3] <= MAXX
        elif o[0] == 2:
            assert len(o) == 3 and 1 <= o[1] <= n and 1 <= o[2] <= n
        elif o[0] == 3:
            assert len(o) == 3 and 1 <= o[1] <= n and -MAXX <= o[2] <= MAXX
        else:
            assert o[0] == 4 and len(o) == 2 and 1 <= o[1] <= n
        lines.append(" ".join(map(str, o)))
    tests.append("%d %d\n" % (n, len(ops)) + " ".join(map(str, a[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "\n".join(lines) + "\n")


def make(n, kind, q, amax, xmax, mix, far100, top100=30):
    t = Tree(n, kind)
    a = [0] + [ri(-amax, amax) for _ in range(n)]
    ops = []
    cum = [sum(mix[:i + 1]) for i in range(4)]
    for _ in range(q):
        r = rb(cum[3])
        if r < cum[0]:
            u, v = t.pair(far100)
            ops.append((1, u, v, ri(-xmax, xmax)))
        elif r < cum[1]:
            u, v = t.pair(far100)
            ops.append((2, u, v))
        elif r < cum[2]:
            ops.append((3, t.top() if rb(100) < top100 else t.node(), ri(-xmax, xmax)))
        else:
            ops.append((4, t.top() if rb(100) < top100 else t.node()))
    ops[-1] = (4, 1)
    add(n, a, t.p, ops)


def overflow(n, q):
    p = [0, 0] + list(range(1, n))
    a = [0] + [MAXA] * n
    ops = []
    for i in range(q):
        if i % 4 == 0:
            ops.append((1, 1, n, MAXX))
        elif i % 4 == 1:
            ops.append((3, 1, MAXX))
        elif i % 4 == 2:
            ops.append((2, n, 1))
        else:
            ops.append((4, 1))
    add(n, a, p, ops)


add(7, [0, 3, -1, 4, 1, 5, -9, 2], [0, 0, 1, 1, 2, 2, 4, 3],
    [(2, 6, 7), (3, 2, 10), (2, 6, 3), (4, 4)])
add(4, [0, 0, 0, 0, 0], [0, 0, 1, 2, 3],
    [(3, 2, 5), (1, 1, 3, 1), (4, 1), (2, 4, 2), (3, 1, -1), (4, 3)])
add(2, [0, -1000000000, -1000000000], [0, 0, 1], [(3, 1, 1000), (2, 1, 2), (4, 2)])
add(8, [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 0, 1, 2, 2, 1, 3, 3, 5],
    [(3, 5, 3), (1, 7, 4, 5), (2, 6, 8), (4, 5)])
add(6, [0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 3, 2, 1],
    [(1, 4, 6, 7), (3, 3, 2), (4, 2)])

make(5, "random", 40, 10, 5, (1, 1, 1, 1), 0)
make(12, "binary", 80, 100, 10, (1, 1, 2, 1), 30)
make(40, "random", 200, MAXA, MAXX, (1, 1, 1, 1), 50)
make(60, "combs", 300, 1000, MAXX, (1, 1, 2, 2), 50)
make(300, "chains", 500, 1000, 1000, (2, 2, 1, 1), 50)
make(2_000, "random", 3_000, MAXA, MAXX, (1, 1, 1, 1), 50)
make(10_000, "deep", 10_000, 10, 10, (2, 2, 1, 1), 80)
overflow(1_000, 2_000)

make(MAXN, "path", MAXQ, 1000, MAXX, (2, 2, 1, 1), 90)
make(MAXN, "deep", MAXQ, 10**8, MAXX, (2, 2, 1, 1), 90)
make(MAXN, "caterpillar", MAXQ, 1000, MAXX, (1, 1, 1, 1), 90)
make(MAXN, "broom", MAXQ, 10, 10, (2, 2, 1, 1), 90)
make(MAXN, "twopaths", MAXQ, 1000, 1000, (1, 2, 1, 2), 90)
make(MAXN, "longrandom", MAXQ, 1000, MAXX, (2, 2, 1, 1), 90)
make(MAXN, "longbinary", MAXQ, 100, 100, (1, 1, 1, 1), 90)
make(MAXN, "combs", MAXQ, 1000, MAXX, (1, 1, 2, 2), 90, 60)
make(MAXN, "longrandom", MAXQ, 10, MAXX, (1, 3, 1, 1), 90)
make(MAXN, "deep", MAXQ, 100, 100, (1, 1, 2, 2), 90, 60)
overflow(MAXN, MAXQ)

write_all()

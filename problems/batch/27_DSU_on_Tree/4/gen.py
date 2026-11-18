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


def relabel(par):
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(n + 1))
    rest = lab[2:]
    shuffle(rest)
    lab[2:] = rest
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i]] = lab[par[i]]
    return lab, p


def check_parents(n, p):
    assert len(p) == n + 1
    state = [0] * (n + 1)
    state[1] = 1
    for i in range(2, n + 1):
        assert 1 <= p[i] <= n and p[i] != i
        path = []
        x = i
        while state[x] == 0:
            state[x] = 2
            path.append(x)
            x = p[x]
            assert state[x] != 2
        for y in path:
            state[y] = 1


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(270404)
MAXN = 100_000
MAXC = 10 ** 9
MAXB = 10 ** 15


def add(n, b, p, c):
    assert 2 <= n <= MAXN and 1 <= b <= MAXB
    check_parents(n, p)
    assert len(c) == n + 1 and all(1 <= x <= MAXC for x in c[1:])
    tests.append(f"{n} {b}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, c[1:])) + "\n")


def make(n, kind, wmode, crew):
    par = shape(n, kind)
    lab, p = relabel(par)
    c = [0] * (n + 1)
    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[par[i]] + 1
    for i in range(1, n + 1):
        v = lab[i]
        if wmode == "rand":
            c[v] = ri(1, MAXC)
        elif wmode == "small":
            c[v] = ri(1, 100)
        elif wmode == "eq":
            c[v] = MAXC
        else:
            c[v] = max(1, min(MAXC, MAXC - depth[i] * (MAXC // max(1, n)) + ri(0, MAXC // 1000)))
            if wmode == "upsmall" and random.random() < 0.5:
                c[v] = ri(1, 1000)
    avg = sum(c[1:]) // n
    b = MAXB if crew == 0 else max(1, min(MAXB, avg * crew + ri(0, avg)))
    add(n, b, p, c)


add(6, 10, [0, 0, 1, 1, 2, 2, 3], [0, 6, 2, 5, 4, 3, 4])
add(5, 7, [0, 0, 1, 2, 3, 4], [0, 1, 5, 4, 3, 2])
add(2, 1, [0, 0, 1], [0, 2, 2])
add(7, 12, [0, 0, 1, 1, 2, 2, 3, 3], [0, 7, 3, 8, 5, 4, 2, 6])
add(4, 1000000000000000, [0, 0, 1, 1, 1], [0, 1000000000, 1000000000, 1000000000, 1000000000])

make(10, "random", "small", 3)
make(30, "caterpillar", "rand", 5)
make(60, "binary", "updown", 8)
make(200, "random", "small", 20)
make(300, "deep", "upsmall", 30)
make(1000, "chains", "rand", 40)
make(2000, "broom", "eq", 100)
make(5000, "random", "rand", 0)

make(MAXN, "path", "rand", 300)
make(MAXN, "path", "updown", 2000)
make(MAXN, "deep", "small", 10_000)
make(MAXN, "caterpillar", "rand", 50)
make(MAXN, "broom", "upsmall", 500)
make(MAXN, "longrandom", "rand", 5000)
make(MAXN, "longbinary", "updown", 100)
make(MAXN, "longstar", "eq", 1000)
make(MAXN, "twopaths", "rand", 20_000)
make(MAXN, "deep", "rand", 0)
make(MAXN, "caterpillar", "upsmall", 3000)

write_all()

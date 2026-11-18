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

random.seed(270202)
MAXN = 100_000
MAXA = 10 ** 9


def add(n, p, a):
    assert 2 <= n <= MAXN
    check_parents(n, p)
    assert len(a) == n + 1 and all(0 <= x <= MAXA for x in a[1:])
    tests.append(f"{n}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, a[1:])) + "\n")


def make(n, kind, mode):
    par = shape(n, kind)
    lab, p = relabel(par)
    a = [0] * (n + 1)
    if mode == "rand":
        for v in range(1, n + 1):
            a[v] = ri(0, MAXA)
    elif mode == "dense":
        for v in range(1, n + 1):
            a[v] = ri(0, 3 * n)
    elif mode == "spaced":
        vals = [i * 9000 for i in range(n)]
        shuffle(vals)
        for v in range(1, n + 1):
            a[v] = vals[v - 1] + ri(0, 4000)
    else:
        for v in range(1, n + 1):
            a[v] = MAXA - ri(0, 50 * n)
    add(n, p, a)


add(7, [0, 0, 1, 1, 2, 2, 3, 3], [0, 50, 10, 30, 20, 13, 31, 45])
add(5, [0, 0, 1, 2, 2, 1], [0, 8, 1, 20, 5, 7])
add(2, [0, 0, 1], [0, 0, 1000000000])
add(6, [0, 0, 1, 2, 3, 4, 5], [0, 100, 40, 70, 60, 41, 99])
add(8, [0, 0, 1, 1, 1, 2, 3, 4, 4], [0, 5, 9, 16, 3, 9, 30, 27, 1])

make(10, "random", "dense")
make(30, "caterpillar", "rand")
make(60, "binary", "spaced")
make(200, "random", "dense")
make(300, "deep", "spaced")
make(1000, "chains", "rand")
make(2000, "broom", "spaced")
make(5000, "random", "rand")

make(MAXN, "path", "rand")
make(MAXN, "path", "spaced")
make(MAXN, "deep", "dense")
make(MAXN, "caterpillar", "spaced")
make(MAXN, "broom", "rand")
make(MAXN, "longrandom", "spaced")
make(MAXN, "longbinary", "max")
make(MAXN, "longstar", "spaced")
make(MAXN, "twopaths", "rand")
make(MAXN, "deep", "spaced")
make(MAXN, "caterpillar", "max")

write_all()

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

random.seed(270808)
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
    for i in range(1, n + 1):
        v = lab[i]
        if mode == "rand":
            a[v] = ri(0, MAXA)
        elif mode == "small":
            a[v] = ri(0, 5)
        elif mode == "ext":
            a[v] = MAXA if random.random() < 0.5 else 0
        elif mode == "up":
            a[v] = min(MAXA, i * (MAXA // n) + ri(0, 100))
        else:
            a[v] = max(0, MAXA - i * (MAXA // n) - ri(0, 100))
    add(n, p, a)


add(7, [0, 0, 1, 1, 2, 2, 3, 3], [0, 4, 1, 9, 3, 2, 10, 6])
add(5, [0, 0, 1, 2, 3, 4], [0, 5, 1, 8, 2, 7])
add(2, [0, 0, 1], [0, 0, 1000000000])
add(8, [0, 0, 1, 1, 2, 2, 2, 3, 3], [0, 7, 3, 3, 1, 9, 3, 6, 0])
add(6, [0, 0, 1, 1, 1, 1, 1], [0, 2, 2, 2, 5, 5, 5])

make(10, "random", "small")
make(30, "caterpillar", "rand")
make(60, "binary", "ext")
make(200, "random", "up")
make(300, "deep", "rand")
make(1000, "chains", "down")
make(2000, "broom", "ext")
make(5000, "random", "rand")

make(MAXN, "path", "rand")
make(MAXN, "path", "up")
make(MAXN, "deep", "ext")
make(MAXN, "caterpillar", "rand")
make(MAXN, "broom", "down")
make(MAXN, "longrandom", "rand")
make(MAXN, "longbinary", "ext")
make(MAXN, "longstar", "up")
make(MAXN, "twopaths", "rand")
make(MAXN, "deep", "small")
make(MAXN, "caterpillar", "ext")

write_all()

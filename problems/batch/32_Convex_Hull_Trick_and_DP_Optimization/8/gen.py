# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(320505)
MAXN, MAXL, MAXP = 100_000, 100, 10 ** 9
tests = []


def add(par, ln, P):
    n = len(par) - 1
    assert 2 <= n <= MAXN
    assert all(1 <= par[i] <= n and par[i] != i for i in range(2, n + 1))
    assert all(1 <= ln[i] <= MAXL and 1 <= P[i] <= MAXP for i in range(2, n + 1))
    depth = [None] * (n + 1)
    depth[1] = 0
    for i in range(2, n + 1):
        path, x = [], i
        while depth[x] is None:
            path.append(x)
            x = par[x]
            assert len(path) <= n
        for y in reversed(path):
            depth[y] = depth[par[y]] + 1
    tests.append(f"{n}\n" + " ".join(map(str, par[2:])) + "\n" + " ".join(map(str, ln[2:])) + "\n"
                 + " ".join(map(str, P[2:])) + "\n")


def shape(n, kind):
    rnd = random.random
    par = [0, 0]
    half, h = max(1, n // 2), max(1, 3 * n // 5)
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "caterpillar":
            p = i - 1 if i <= half else 1 + int(rnd() * half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "deep":
            p = max(1, i - 1 - int(rnd() * 3))
        elif kind == "twopaths":
            p = 1 if i <= 3 else i - 2
        elif kind == "longrandom":
            p = i - 1 if i <= h else 1 + int(rnd() * (i - 1))
        elif kind == "combs":
            p = i - 1 if (i % 50) else max(1, i - 1 - int(rnd() * 2000))
        elif kind == "random":
            p = 1 + int(rnd() * (i - 1))
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def make(n, kind, lk="rand", pk="rand"):
    rnd = random.random
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    for i in range(len(lab) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        lab[i], lab[j] = lab[j], lab[i]
    lab = [0, 1] + lab
    p2, l2, P2 = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for i in range(2, n + 1):
        v = lab[i]
        p2[v] = lab[par[i]]
        l2[v] = MAXL if lk == "max" else (1 + int(rnd() * 3) if lk == "short" else 1 + int(rnd() * MAXL))
        if pk == "rand":
            P2[v] = 1 + int(rnd() * MAXP)
        elif pk == "cheap":
            P2[v] = 1 + int(rnd() * 1000)
        else:
            P2[v] = 1 + int(rnd() * 10 ** 7)
    add(p2, l2, P2)


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_000_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)


def sample(par, ln, P):
    add([0, 0] + par, [0, 0] + ln, [0, 0] + P)


sample([1, 2, 3, 2], [3, 1, 2, 4], [5, 2, 1, 10])
sample([1, 2, 3], [1, 1, 1], [1, 1, 1])
sample([1], [100], [1000000000])
sample([1, 1, 2, 2, 3, 6], [2, 5, 1, 3, 2, 2], [4, 1, 9, 2, 8, 3])
sample([3, 1, 2, 4, 4, 5], [2, 2, 2, 2, 2, 2], [7, 1, 3, 9, 2, 6])

make(2, "path", "max", "rand")
make(9, "caterpillar", "rand", "cheap")
make(40, "deep", "rand", "mid")
make(200, "random", "short", "cheap")
make(1000, "broom", "rand", "mid")
make(5000, "combs", "short", "cheap")
make(20_000, "longrandom", "rand", "mid")
make(50_000, "caterpillar", "max", "rand")

for kind, lk, pk in [("path", "rand", "mid"), ("path", "short", "cheap"), ("caterpillar", "rand", "cheap"),
                     ("caterpillar", "short", "mid"), ("broom", "rand", "mid"), ("deep", "rand", "cheap"),
                     ("twopaths", "max", "rand"), ("longrandom", "short", "cheap"), ("broom", "short", "cheap"),
                     ("path", "max", "rand"), ("deep", "short", "mid")]:
    make(MAXN, kind, lk, pk)
write_all()

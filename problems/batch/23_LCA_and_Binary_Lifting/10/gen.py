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


def labels(par):
    n = len(par) - 1
    assert all(1 <= par[i] < i for i in range(2, n + 1))
    lab = list(range(1, n + 1))
    shuffle(lab)
    j = lab.index(1)
    lab[0], lab[j] = lab[j], lab[0]
    return lab


def random_ancestors(par, stay):
    n = len(par) - 1
    far = list(range(n + 1))
    rnd = random.random
    for i in range(2, n + 1):
        far[i] = far[par[i]] if par[i] != 1 and rnd() < stay else par[i]
    return far


def check_tree(n, edges):
    assert len(edges) == n - 1
    root = list(range(n + 1))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    for e in edges:
        u, v = e[0], e[1]
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b
        root[a] = b


def write_all():
    for t in tests:
        assert t.endswith("\n") and "  " not in t and " \n" not in t
        assert len(t) <= 3_400_000
    os.makedirs("tests", exist_ok=True)
    for i, t in enumerate(tests, 1):
        with open(f"tests/{i:02d}.in", "w") as f:
            f.write(t)

random.seed(230111)
MAXN, MAXQ, MAXK = 200_000, 100_000, 200_000


def add(n, p, qs, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(qs) <= MAXQ and len(p) == n + 1
    assert 1 <= min(p[2:]) and max(p[2:]) <= n and not any(map(int.__eq__, p[2:], range(2, n + 1)))
    if not tree_ok:
        for i in range(2, n + 1):
            x, steps = i, 0
            while x != 1:
                x = p[x]
                steps += 1
                assert steps <= n
    assert sum(len(s) for s in qs) <= MAXK
    for s in qs:
        assert 1 <= len(s) <= n and len(set(s)) == len(s) and 1 <= min(s) and max(s) <= n
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{len(s)} " + " ".join(map(str, s)) + "\n" for s in qs))


def sample(pop, k):
    a = list(pop)
    rnd = random.random
    n = len(a)
    for i in range(k):
        j = i + int(rnd() * (n - i))
        a[i], a[j] = a[j], a[i]
    return a[:k]


def make(n, kind, sizes, mode="rand"):
    par = shape(n, kind)
    lab = labels(par)
    p = [0] * (n + 1)
    for x, y in zip(lab[1:], [lab[q - 1] for q in par[2:]]):
        p[x] = y
    rnd = random.random
    far = random_ancestors(par, 0.95) if mode == "chain" else None
    qs = []
    for k in sizes:
        k = min(k, n)
        if mode == "rand" or k > n // 2:
            s = sample(range(1, n + 1), k) if k > 30 else list(dict.fromkeys(1 + int(rnd() * n) for _ in range(k)))
            s = [lab[x - 1] for x in s]
        elif mode == "sub":
            st = 1 + int(rnd() * (n - k))
            win = range(st, min(n, st + 3 * k) + 1)
            s = [lab[x - 1] for x in sample(win, min(k, len(win)))]
        else:
            x = 1 + int(rnd() * n)
            ch = []
            while len(ch) < k // 2 and x != 1:
                ch.append(x)
                x = far[x]
            s = list(dict.fromkeys(ch + [1 + int(rnd() * n) for _ in range(k - len(ch))]))
            s = [lab[y - 1] for y in s]
        qs.append(s)
    add(n, p, qs, True)


add(8, [0, 0, 1, 1, 2, 2, 3, 5, 5], [[4, 7, 8], [2, 7, 6], [6], [4, 5, 6, 3]])
add(4, [0, 0, 1, 2, 1], [[3, 2, 1], [3, 4]])
add(2, [0, 0, 1], [[2, 1], [1]])
add(7, [0, 0, 3, 1, 3, 4, 4, 1], [[5, 6, 7], [2, 6, 5], [5, 4, 2, 6, 1], [7, 3]])
add(9, [0, 0, 1, 1, 3, 3, 4, 4, 2, 8], [[5, 6, 7, 9], [4, 8], [9, 7, 5], [9, 8, 2, 3, 6]])

add(9, [0, 0, 1, 1, 3, 3, 4, 4, 2, 8], [[2, 3, 6, 8, 9], [6, 9, 2, 3, 8], [5, 7, 6, 9, 4], [3, 9, 2], [7, 5, 6],
                                       [1, 9, 4], [8, 3, 7, 2], [9, 2, 6, 8, 3, 7, 5, 4, 1]])
make(6, "random", [ri(1, 6) for _ in range(40)])
make(12, "binary", [ri(2, 8) for _ in range(60)], "sub")
make(30, "caterpillar", [ri(2, 12) for _ in range(80)], "chain")
make(60, "deep", [ri(2, 20) for _ in range(100)], "chain")
make(300, "random", [ri(2, 60) for _ in range(200)], "sub")
make(3000, "chains", [ri(2, 100) for _ in range(300)], "sub")
make(20_000, "binary", [3] * 6_000, "sub")
make(20_000, "path", [2] * 20_000, "rand")

make(MAXN, "longbinary", [100_000, 100_000], "rand")
make(MAXN, "path", [100_000, 100_000], "rand")
make(MAXN, "deep", [50_000] * 4, "chain")
make(MAXN, "longrandom", [40_000] * 5, "sub")
make(MAXN, "caterpillar", [20_000] * 10, "sub")
make(MAXN, "chains", [10_000] * 20, "sub")
make(MAXN, "longbinary", [1_000] * 200, "sub")
make(MAXN, "longrandom", [2_000] * 100, "chain")
make(MAXN, "twopaths", [5_000] * 40, "chain")
make(MAXN, "longstar", [100_000, 99_999, 1], "rand")

write_all()

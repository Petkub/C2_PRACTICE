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

random.seed(271212)
MAXN = 100_000
MAXA = 10 ** 9
MAXT = 10 ** 15


def add(n, t, p, a):
    assert 2 <= n <= MAXN and abs(t) <= MAXT
    check_parents(n, p)
    assert len(a) == n + 1 and all(0 <= x <= MAXA for x in a[1:])
    tests.append(f"{n} {t}\n" + " ".join(map(str, p[2:])) + "\n" + " ".join(map(str, a[1:])) + "\n")


def make(n, kind, mode, tmode="rand"):
    par = shape(n, kind)
    lab, p = relabel(par)
    a = [0] * (n + 1)
    tmpl = [ri(0, MAXA) for _ in range(3)]
    for v in range(1, n + 1):
        if mode == "big":
            a[v] = ri(0, 9999) * 100_000 + v - 1
        elif mode == "small":
            a[v] = ri(0, 2)
        else:
            a[v] = tmpl[ri(0, 2)] if random.random() < 0.75 else ri(0, MAXA)
    if mode == "bush":
        hasKid = [False] * (n + 1)
        for v in range(2, n + 1):
            hasKid[p[v]] = True
        first = {}
        for v in range(1, n + 1):
            a[v] = ri(0, 9999) * 100_000 + v - 1
        for v in range(2, n + 1):
            if not hasKid[v]:
                if p[v] in first:
                    a[v] = a[first[p[v]]]
                else:
                    first[p[v]] = v
    if tmode == "leaf":
        cost = [0] * (n + 1)
        cost[lab[1]] = a[lab[1]]
        for i in range(2, n + 1):
            cost[lab[i]] = cost[lab[par[i]]] + a[lab[i]]
        hasKid = [False] * (n + 1)
        for v in range(2, n + 1):
            hasKid[p[v]] = True
        leaves = [v for v in range(2, n + 1) if not hasKid[v]]
        t = cost[leaves[ri(0, len(leaves) - 1)]]
    elif tmode == "far":
        t = -ri(1, MAXT)
    else:
        t = ri(0, MAXT) if mode != "small" else ri(0, 2 * n)
    add(n, t, p, a)


def bushes(n, tmode):
    par = [0, 0]
    i = 2
    spine = [1]
    while i <= n:
        s = spine[-1]
        if i + 1 <= n:
            par.append(s)
            side = i
            i += 1
            for _ in range(ri(1, 3)):
                if i > n:
                    break
                par.append(side)
                i += 1
        if i <= n:
            par.append(s)
            spine.append(i)
            i += 1
    par = par[:n + 1]
    lab, p = relabel(par)
    a = [0] * (n + 1)
    for v in range(1, n + 1):
        a[v] = ri(0, 9999) * 100_000 + v - 1
    hasKid = [False] * (n + 1)
    for v in range(2, n + 1):
        hasKid[p[v]] = True
    first = {}
    for v in range(2, n + 1):
        if not hasKid[v]:
            if p[v] in first:
                a[v] = a[first[p[v]]]
            else:
                first[p[v]] = v
    t = -ri(1, MAXT) if tmode == "far" else ri(0, MAXT)
    add(n, t, p, a)


add(6, 10, [0, 0, 1, 1, 2, 2, 3], [0, 2, 3, 5, 5, 4, 3])
add(7, 7, [0, 0, 1, 1, 1, 2, 2, 2], [0, 1, 2, 4, 6, 4, 4, 1])
add(2, 1000000000, [0, 0, 1], [0, 0, 1000000000])
add(8, 9, [0, 0, 1, 2, 2, 1, 5, 5, 5], [0, 3, 1, 5, 5, 2, 4, 4, 1])
add(5, 6, [0, 0, 1, 2, 3, 4], [0, 1, 2, 3, 0, 0])

make(8, "random", "small", "leaf")
make(10, "binary", "small")
make(12, "caterpillar", "small", "leaf")
make(14, "random", "mix")
make(200, "random", "small", "leaf")
make(300, "binary", "mix", "rand")
make(1000, "caterpillar", "small")
make(3000, "random", "mix", "leaf")
make(20_000, "caterpillar", "mix", "leaf")
make(20_000, "broom", "mix")

make(MAXN, "caterpillar", "big")
make(MAXN, "caterpillar", "big", "leaf")
make(MAXN, "broom", "big", "far")
make(MAXN, "longrandom", "big")
make(MAXN, "broom", "big", "leaf")
make(MAXN, "caterpillar", "big", "far")
bushes(MAXN, "rand")
make(MAXN, "deep", "big", "leaf")
make(MAXN, "longrandom", "big", "leaf")
bushes(MAXN, "far")
bushes(MAXN - 7, "rand")

write_all()

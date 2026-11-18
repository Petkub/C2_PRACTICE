# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, ENC = 100_000, 70_000, 2 ** 30
RANDENC = 2 ** 17


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    par = [0, 0]
    half, h = max(1, n // 2), max(1, 3 * n // 5)
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
        elif kind == "twopaths":
            p = 1 if i <= 3 else i - 2
        elif kind == "longrandom":
            p = i - 1 if i <= h else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def relabel(par):
    n = len(par) - 1
    lab = list(range(1, n + 1))
    shuffle(lab)
    j = lab.index(1)
    lab[0], lab[j] = lab[j], lab[0]
    p = [0] * (n + 1)
    for i in range(2, n + 1):
        p[lab[i - 1]] = lab[par[i] - 1]
    return p


def path_tolls(c, p, dep, u, v):
    b = []
    while u != v:
        if dep[u] >= dep[v]:
            b.append(c[u]); u = p[u]
        else:
            b.append(c[v]); v = p[v]
    b.append(c[u])
    return b


def depths(p):
    n = len(p) - 1
    dep = [-1] * (n + 1)
    dep[1] = 0
    for i in range(2, n + 1):
        st, x = [], i
        while dep[x] < 0:
            st.append(x); x = p[x]
        while st:
            y = st.pop(); dep[y] = dep[p[y]] + 1
    return dep


def add(c, p, qs):
    n = len(c) - 1
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= n for x in c[1:])
    assert all(1 <= p[i] <= n and p[i] != i for i in range(2, n + 1))
    dep = depths(p)
    assert all(d >= 0 for d in dep[1:])
    assert all(0 <= x < ENC for t in qs for x in t)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, c[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{x} {y}\n" for x, y in qs))


def majority(c, p, dep, u, v):
    b = path_tolls(c, p, dep, u, v)
    for x in set(b):
        if 2 * b.count(x) > len(b):
            return x
    return -1


def crafted(c, p, real):
    c, p = [0] + c, [0, 0] + p
    dep, last, qs = depths(p), 0, []
    for u, v in real:
        qs.append(((u - 1) ^ last, (v - 1) ^ last))
        ans = majority(c, p, dep, u, v)
        last = 0 if ans == -1 else ans
    add(c, p, qs)


def rand_queries(q):
    return [(ri(0, RANDENC - 1), ri(0, RANDENC - 1)) for _ in range(q)]


def big(n, kind, share, q, regions=1):
    p = relabel(shape(n, kind))
    dom = [ri(1, n) for _ in range(regions)]
    c = [0] * (n + 1)
    dep = depths(p)
    md = max(dep) + 1
    for v in range(1, n + 1):
        r = dep[v] * regions // md
        c[v] = dom[r] if random.random() < share else ri(1, n)
    add(c, p, rand_queries(q))


random.seed(300801)

crafted([2, 2, 3, 2, 3, 3, 1], [1, 1, 2, 2, 3, 3], [(4, 5), (6, 7), (4, 6), (1, 7)])
crafted([5, 5, 1, 5, 2], [1, 2, 3, 4], [(1, 5), (3, 5), (2, 4)])
crafted([1], [], [(1, 1), (1, 1)])
crafted([4, 4, 4, 1, 2, 4], [1, 1, 2, 2, 3], [(4, 5), (5, 6), (1, 6), (4, 3)])
crafted([3, 1, 3, 3, 1, 1, 3, 1], [1, 2, 3, 4, 5, 6, 7], [(1, 7), (2, 6), (3, 7), (4, 8), (1, 3)])

for n, kind, share, q, reg in [(2, "path", 0.5, 20, 1), (8, "random", 0.6, 100, 1), (30, "binary", 0.5, 300, 2),
                               (100, "caterpillar", 0.55, 1000, 1), (1000, "deep", 0.6, 2000, 3),
                               (5000, "random", 0.7, 5000, 1), (20000, "path", 0.5, 20000, 1),
                               (50000, "binary", 0.8, 50000, 1), (50000, "star", 0.5, 50000, 1)]:
    big(n, kind, share, q, reg)

for kind, share, reg in [("path", 0.5, 1), ("path", 0.6, 3), ("twopaths", 0.55, 1), ("deep", 0.5, 2),
                         ("caterpillar", 0.6, 1), ("longrandom", 0.7, 2), ("longrandom", 0.5, 1),
                         ("caterpillar", 0.45, 1), ("path", 0.52, 2), ("deep", 0.65, 4)]:
    big(MAXN, kind, share, MAXQ, reg)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []
MAXN, MAXQ, MAXV, ENC = 100_000, 70_000, 10 ** 9, 2 ** 30
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
    assert all(1 <= x <= MAXV for x in c[1:])
    assert all(1 <= p[i] <= n and p[i] != i for i in range(2, n + 1))
    dep = depths(p)
    assert all(d >= 0 for d in dep[1:])
    assert all(0 <= x < ENC for t in qs for x in t)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, c[1:])) + "\n" + " ".join(map(str, p[2:])) + "\n"
                 + "".join(f"{x} {y}\n" for x, y in qs))


def crafted(c, p, real):
    c, p = [0] + c, [0, 0] + p
    dep, last, qs = depths(p), 0, []
    for u, v in real:
        qs.append(((u - 1) ^ last, (v - 1) ^ last))
        b = sorted(path_tolls(c, p, dep, u, v))
        last = b[(len(b) + 1) // 2 - 1]
    add(c, p, qs)


def rand_queries(q):
    return [(ri(0, RANDENC - 1), ri(0, RANDENC - 1)) for _ in range(q)]


def big(n, kind, vk, q):
    p = relabel(shape(n, kind))
    if vk == "rand":
        c = [0] + [ri(1, MAXV) for _ in range(n)]
    elif vk == "few":
        c = [0] + [ri(1, 3) for _ in range(n)]
    elif vk == "max":
        c = [0] + [MAXV - ri(0, 1) for _ in range(n)]
    else:
        c = [0] + [ri(1, 1000) for _ in range(n)]
    add(c, p, rand_queries(q))


random.seed(300301)

crafted([90, 50, 70, 3, 8, 1, 6], [1, 1, 2, 2, 3, 3], [(4, 5), (4, 6), (7, 1), (2, 7)])
crafted([50, 10, 20, 30, 40], [1, 2, 1, 4], [(3, 5), (2, 4), (1, 3)])
crafted([1000000000, 999999999], [1], [(1, 2), (2, 1)])
crafted([9, 2, 2, 9, 4, 4], [1, 1, 3, 3, 5], [(2, 6), (6, 4), (2, 5)])
crafted([70, 60, 10, 20, 30, 40, 50, 5], [1, 2, 3, 2, 5, 1, 7], [(4, 6), (4, 8), (6, 8), (3, 7)])

add([0, 5], [0, 0], rand_queries(3))
for n, kind, vk, q in [(3, "path", "few", 20), (8, "random", "small", 100), (30, "binary", "rand", 300),
                       (100, "caterpillar", "few", 1000), (1000, "deep", "small", 2000),
                       (5000, "random", "rand", 5000), (20000, "path", "rand", 20000), (50000, "binary", "rand", 50000),
                       (50000, "star", "small", 50000)]:
    big(n, kind, vk, q)

for kind, vk in [("path", "rand"), ("path", "few"), ("twopaths", "rand"), ("deep", "rand"), ("caterpillar", "rand"),
                 ("longrandom", "max"), ("longrandom", "few"), ("caterpillar", "small"), ("path", "small"),
                 ("deep", "small")]:
    big(MAXN, kind, vk, MAXQ)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_400_000
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

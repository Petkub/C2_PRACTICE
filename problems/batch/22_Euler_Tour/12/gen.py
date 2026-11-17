# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(220012)
MAXN = 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuf(a, m=None):
    rnd = random.random
    n = len(a)
    for i in range(min(n - 1, m if m is not None else n)):
        j = i + int(rnd() * (n - i))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    rnd = random.random
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    if kind == "path":
        par = list(range(-1, n))
    elif kind == "star":
        par = [0, 0] + [1] * (n - 1)
    elif kind == "random":
        par = [0, 0] + [1 + int(rnd() * (i - 1)) for i in range(2, n + 1)]
    elif kind == "deep":
        par = [0, 0] + [max(1, i - 3) + int(rnd() * (i - max(1, i - 3))) for i in range(2, n + 1)]
    elif kind == "binary":
        par = [0, 0] + [i // 2 for i in range(2, n + 1)]
    elif kind == "caterpillar":
        par = [0, 0] + [i - 1 if i <= half else 1 + int(rnd() * half) for i in range(2, n + 1)]
    elif kind == "broom":
        par = [0, 0] + [i - 1 if i <= half else half for i in range(2, n + 1)]
    elif kind == "longchains":
        L = max(2, n // 20)
        par = [0, 0] + [i - 1 if (i - 1) % L else 1 + int(rnd() * (i - 1)) for i in range(2, n + 1)]
    elif kind == "chains":
        par = [0, 0] + [i - 1 if (i - 1) % b else 1 + int(rnd() * (i - 1)) for i in range(2, n + 1)]
    else:
        raise ValueError(kind)
    par[0] = par[1] = 0
    assert len(par) == n + 1 and all(1 <= par[i] < i for i in range(2, n + 1))
    return par


def tree(n, kind):
    par = shape(n, kind)
    lab = list(range(2, n + 1))
    shuf(lab)
    lab = [1] + lab
    assert lab[0] == 1 and len(set(lab)) == n and min(lab) == 1 and max(lab) == n
    p = [0] * (n + 1)
    for v, pv in zip(lab[1:], [lab[x - 1] for x in par[2:]]):
        p[v] = pv
    return p, lab


def add(n, c, p, is_tree=False):
    assert 2 <= n <= MAXN and len(c) == n and len(p) == n + 1
    assert min(c) >= 1 and max(c) <= n
    pp = p[2:]
    assert min(pp) >= 1 and max(pp) <= n and all(map(int.__ne__, pp, range(2, n + 1)))
    if not is_tree:
        ch = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            ch[p[i]].append(i)
        order = [1]
        for u in order:
            order.extend(ch[u])
        assert len(order) == n
    t = f"{n}\n" + " ".join(map(str, c)) + "\n" + " ".join(map(str, pp)) + "\n"
    assert len(t) <= 3_100_000
    tests.append(t)


def colours(n, lab, p, kind, k=0):
    c = [0] * n
    rnd = random.random
    if kind == "few":
        c = [1 + int(rnd() * k) for _ in range(n)]
    elif kind == "any":
        c = [1 + int(rnd() * n) for _ in range(n)]
    elif kind == "distinct":
        c = list(range(1, n + 1))
        shuf(c)
    elif kind == "pairs":
        cols = [i // 2 + 1 for i in range(n)]
        shuf(cols)
        c = cols
    elif kind == "blocks":
        perm = list(range(1, n + 1))
        shuf(perm, n // k + 1)
        for i in range(n):
            c[lab[i] - 1] = perm[i // k]
    elif kind == "depth":
        depth = [0] * (n + 1)
        ch = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            ch[p[i]].append(i)
        order = [1]
        for u in order:
            for w in ch[u]:
                depth[w] = depth[u] + 1
                order.append(w)
        for v in range(1, n + 1):
            c[v - 1] = min(n, depth[v] // max(1, k) + 1)
    elif kind == "mix":
        perm = list(range(k + 1, n + 1))
        shuf(perm, n // 50 + 1)
        for i in range(n):
            c[lab[i] - 1] = ri(1, k) if random.random() < 0.5 else perm[(i // 50) % len(perm)]
    else:
        raise ValueError(kind)
    return c


def case(n, kind, ckind, k=0):
    p, lab = tree(n, kind)
    add(n, colours(n, lab, p, ckind, k), p, True)


add(6, [1, 1, 2, 3, 2, 2], [0, 0, 1, 1, 2, 2, 3])
add(5, [1, 2, 1, 2, 3], [0, 0, 1, 2, 3, 4])
add(2, [2, 2], [0, 0, 1])
add(5, [3, 1, 2, 2, 4], [0, 0, 1, 1, 1, 1])
add(8, [2, 2, 1, 2, 3, 1, 3, 4], [0, 0, 1, 1, 2, 2, 3, 6, 6])

add(6, [1, 2, 1, 3, 2, 3], [0, 0, 1, 1, 2, 2, 3])
add(8, [1, 2, 2, 1, 3, 3, 1, 2], [0, 0, 1, 1, 2, 2, 3, 6, 6])
case(3, "path", "few", 2)
case(10, "random", "few", 3)
case(30, "deep", "any")
case(50, "star", "few", 5)
case(80, "caterpillar", "pairs")
case(200, "binary", "blocks", 7)
case(500, "random", "mix", 10)
case(3000, "path", "blocks", 40)
case(4000, "chains", "few", 30)
case(5000, "broom", "pairs")
case(20_000, "star", "few", 2)

N = MAXN
case(N, "path", "few", 20)
case(N, "path", "blocks", 1000)
case(N, "path", "pairs")
case(N, "deep", "any")
case(N, "deep", "mix", 100)
case(N, "caterpillar", "blocks", 300)
case(N, "caterpillar", "distinct")
case(N, "broom", "few", 1000)
case(N, "longchains", "depth", 3)
case(N, "path", "distinct")
case(N, "deep", "pairs")
case(N, "longchains", "few", 50)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

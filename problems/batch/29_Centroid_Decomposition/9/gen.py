# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def shape(n, kind):
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    h = max(1, 3 * n // 5)
    legs = max(1, int(n ** 0.5) // 2)
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
        elif kind == "spider":
            p = 1 if i <= legs + 1 else i - legs
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        elif kind == "longrandom":
            p = i - 1 if i <= h else ri(1, i - 1)
        elif kind == "sqrtstar":
            p = i - 1 if i <= b else ri(1, b)
        else:
            raise ValueError(kind)
        assert 1 <= p < i
        par.append(p)
    return par


def tree_edges(n, kind):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    return [(lab[i], lab[par[i]]) if rnd() < 0.5 else (lab[par[i]], lab[i]) for i in range(2, n + 1)]


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

random.seed(290901)
MAXN = 200_000


def add(n, s, edges, tree_ok=False):
    assert 2 <= n <= MAXN and len(s) == n and set(s) <= set("()")
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    tests.append(f"{n}\n{s}\n" + "".join(["%d %d\n" % e for e in edges]))


def make(n, kind, mode, p=0.5, noise=0.0):
    par = shape(n, kind)
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    rnd = random.random
    ch = [""] * (n + 1)
    depth = [0] * (n + 1)
    for i in range(1, n + 1):
        if i > 1:
            depth[i] = depth[par[i]] + 1
        if mode == "random":
            o = rnd() < p
        else:
            o = depth[i] % 2 == 0
            if rnd() < noise:
                o = not o
        ch[lab[i]] = "(" if o else ")"
    edges = [(lab[i], lab[par[i]]) if rnd() < 0.5 else (lab[par[i]], lab[i]) for i in range(2, n + 1)]
    add(n, "".join(ch[1:]), edges, True)


def double_star(n):
    lab = list(range(n + 1))
    body = lab[1:]
    shuffle(body)
    lab[1:] = body
    ch = [""] * (n + 1)
    ch[lab[1]], ch[lab[2]] = "(", ")"
    e = [(1, 2)]
    for i in range(3, n + 1):
        c = 1 + (i & 1)
        e.append((c, i))
        o = (c == 1) == (random.random() < 0.9)
        ch[lab[i]] = "(" if o else ")"
    edges = [(lab[a], lab[b]) for a, b in e]
    shuffle(edges)
    add(n, "".join(ch[1:]), edges, True)


add(6, "((()))", [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6)])
add(4, "()()", [(1, 2), (2, 3), (3, 4)])
add(2, "((", [(1, 2)])
add(7, "(()(())", [(1, 2), (1, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
add(8, ")(()()()", [(1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (4, 7), (7, 8)])

add(2, ")(", [(1, 2)])
add(2, "()", [(2, 1)])
make(10, "random", "random")
make(40, "path", "random", 0.5)
make(200, "binary", "parity")
make(1000, "caterpillar", "random", 0.55)
make(3000, "random", "parity", noise=0.05)
make(3000, "path", "parity")

make(MAXN, "path", "parity")
make(MAXN, "path", "random", 0.6)
make(MAXN, "deep", "parity")
make(MAXN, "twopaths", "parity", noise=0.001)
make(MAXN, "spider", "parity")
make(MAXN, "caterpillar", "parity", noise=0.01)
make(MAXN, "broom", "parity")
make(MAXN, "longrandom", "random", 0.58)
make(MAXN, "random", "parity")
make(MAXN, "binary", "parity", noise=0.02)
make(MAXN, "sqrtstar", "parity")
make(MAXN, "deep", "random", 0.56)
double_star(MAXN)

write_all()

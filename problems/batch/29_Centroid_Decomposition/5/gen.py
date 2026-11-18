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

random.seed(290301)
MAXN, MAXQ, MAXW = 100_000, 100_000, 100_000


def add(n, opened, edges, ops, tree_ok=False):
    assert 2 <= n <= MAXN and 1 <= len(ops) <= MAXQ
    assert len(opened) == n and set(opened) <= set("01")
    assert all(1 <= e[2] <= MAXW for e in edges)
    if tree_ok:
        assert len(edges) == n - 1
    else:
        check_tree(n, edges)
    assert all(t in (1, 2) and 1 <= v <= n for t, v in ops) and any(t == 2 for t, v in ops)
    tests.append(f"{n} {len(ops)}\n{opened}\n" + "".join(["%d %d %d\n" % e for e in edges])
                 + "".join(["%d %d\n" % o for o in ops]))


def make(n, kind, wlo, whi, q, start_open, keep, pq=0.5):
    edges = tree_edges(n, kind)
    edges = [(a, b, ri(wlo, whi)) for a, b in edges]
    is_open = [0] * (n + 1)
    opened = []
    for v in range(1, start_open + 1):
        x = ri(1, n)
        if not is_open[x]:
            is_open[x] = 1
            opened.append(x)
    s = "".join("1" if is_open[v] else "0" for v in range(1, n + 1))
    pos = {x: i for i, x in enumerate(opened)}
    ops = []
    rnd = random.random
    for _ in range(q):
        if rnd() < pq or not ops:
            ops.append((2, ri(1, n)))
            continue
        if opened and (len(opened) > keep or rnd() < 0.5):
            i = int(rnd() * len(opened))
            x = opened[i]
            last = opened.pop()
            if last != x:
                opened[i] = last
                pos[last] = i
            del pos[x]
            is_open[x] = 0
        else:
            x = ri(1, n)
            if is_open[x]:
                i = pos.pop(x)
                last = opened.pop()
                if last != x:
                    opened[i] = last
                    pos[last] = i
                is_open[x] = 0
            else:
                is_open[x] = 1
                pos[x] = len(opened)
                opened.append(x)
        ops.append((1, x))
    add(n, s, edges, ops, True)


add(4, "0000", [(1, 2, 5), (1, 3, 5), (1, 4, 5)], [(2, 3), (1, 2), (2, 3), (2, 2)])
add(6, "100000", [(1, 2, 3), (2, 3, 4), (3, 4, 2), (4, 5, 6), (3, 6, 1)],
    [(2, 5), (1, 4), (2, 5), (1, 1), (2, 6)])
add(5, "01010", [(1, 2, 10), (2, 3, 10), (3, 4, 10), (4, 5, 10)], [(2, 3), (1, 1), (2, 5)])
add(4, "0001", [(1, 2, 1), (1, 3, 2), (1, 4, 6)], [(2, 2), (1, 3), (2, 2), (1, 2), (2, 1)])
add(3, "000", [(1, 2, 100_000), (2, 3, 100_000)], [(2, 1), (1, 3), (2, 1)])

make(2, "path", 1, 10, 10, 0, 1)
make(10, "random", 1, 10, 30, 2, 2)
make(50, "caterpillar", 1, 100, 200, 3, 3, 0.4)
make(300, "binary", 1, 1000, 500, 5, 4)
make(2000, "deep", 1, MAXW, 2000, 10, 5)
make(8000, "path", MAXW - 10, MAXW, 8000, 2, 2)
make(10_000, "random", 1, 100, 10_000, 50, 20)

make(MAXN, "path", MAXW - 100, MAXW, MAXQ, 3, 2)
make(MAXN, "path", 1, MAXW, MAXQ, 10, 4)
make(MAXN, "deep", 1, MAXW, MAXQ, 5, 3)
make(MAXN, "twopaths", MAXW // 2, MAXW, MAXQ, 2, 2)
make(MAXN, "spider", 1, MAXW, MAXQ, 20, 8)
make(MAXN, "caterpillar", 1, MAXW, MAXQ, 30, 10)
make(MAXN, "broom", 1, MAXW, MAXQ, 5, 3, 0.6)
make(MAXN, "longrandom", 1, MAXW, MAXQ, 10, 5)
make(MAXN, "random", 1, MAXW, MAXQ, 0, 1, 0.7)
make(MAXN, "star", 1, MAXW, MAXQ, 100, 30)
make(MAXN, "sqrtstar", 1, MAXW, MAXQ, 3, 3)
make(MAXN, "binary", 1, MAXW, MAXQ, 1, 1, 0.8)
make(MAXN, "chains", 1, MAXW, MAXQ, 1000, 1000)
make(MAXN, "path", 1, 1, MAXQ, 0, 1, 0.3)

write_all()

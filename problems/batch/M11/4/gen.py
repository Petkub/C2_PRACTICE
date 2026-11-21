# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(511055)
MAXN = 200000
MAXQ = 100000
tests = []


def ri(a, b):

    return a + int(random.random() * (b - a + 1))


def add(n, p, ks):

    assert 2 <= n <= MAXN
    assert len(p) == n - 1
    q = len(ks)
    assert 1 <= q <= MAXQ

    root = list(range(n + 1))
    for u, v in zip(range(2, n + 1), p):
        assert 1 <= v <= n and u != v
        while root[u] != u:
            root[u] = root[root[u]]
            u = root[u]
        while root[v] != v:
            root[v] = root[root[v]]
            v = root[v]
        assert u != v
        root[u] = v
    for k in ks:
        assert 0 <= k <= n
    tests.append("%d %d\n" % (n, q) + " ".join(map(str, p)) + "\n" + " ".join(map(str, ks)) + "\n")


def relabel(par):


    n = len(par) - 1
    rnd = random.random
    r = 1 + int(rnd() * n)
    prev, x = 0, r
    while x != 0:
        par[x], prev, x = prev, x, par[x]
    perm = [0] + sorted(range(1, n + 1), key=lambda _: rnd())
    j = perm.index(1)
    perm[j], perm[r] = perm[r], perm[j]
    up = [0] * (n + 1)
    for i in range(1, n + 1):
        if i != r:
            up[perm[i]] = perm[par[i]]
    return n, up[2:]


def random_tree(n, window=None):
    rnd = random.random
    par = [0, 0]
    for i in range(2, n + 1):
        lo = 1 if window is None else max(1, i - window)
        par.append(lo + int(rnd() * (i - lo)))
    return par


def path(n):
    return [0, 0] + list(range(1, n))


def star(n):
    return [0, 0] + [1] * (n - 1)


def legs(par, at, sizes, shape):

    for s in sizes:
        first = len(par)
        par.append(at)
        for j in range(1, s):
            if shape == "path":
                par.append(len(par) - 1)
            elif shape == "star":
                par.append(first)
            else:
                par.append(ri(first, len(par) - 1))
    return par


def spider(sizes, shape="path"):
    return legs([0, 0], 1, sizes, shape)


def caterpillar(n, spine):
    par = [0, 0] + list(range(1, spine))
    while len(par) <= n:
        par.append(ri(1, spine))
    return par


def shape_b(n, arm, branches):

    par = [0, 0]
    rest = n - 1 - arm
    sizes = [rest // branches] * branches
    for i in range(rest % branches):
        sizes[i] += 1
    legs(par, 1, sizes, "random")
    legs(par, 1, [arm], "path")
    assert len(par) == n + 1
    return par


def queries(q, n, top):

    ks = []
    for _ in range(q):
        r = random.random()
        if r < 0.15:
            ks.append(0)
        elif r < 0.55:
            ks.append(ri(1, min(n, 12)))
        elif r < 0.9:
            ks.append(ri(0, min(n, top)))
        else:
            ks.append(ri(0, n))
    return ks


def big(par, top, q=MAXQ):
    n, p = relabel(par)
    add(n, p, queries(q, n, top))


add(8, [1, 2, 3, 3, 5, 5, 5], [0, 1, 2])
add(7, [1, 4, 1, 4, 5, 3], [2, 0, 1, 5])
add(2, [1], [0, 2])
add(6, [4, 4, 1, 4, 4], [1, 3, 0, 4])
add(6, [5, 1, 6, 1, 3], [0, 1])

add(3, [3, 1], [0, 1, 3])
n, e = relabel(spider([2, 2, 1, 4], "path"))
add(n, e, [0, 1, 2, 3, 4])
n, e = relabel(shape_b(16, 11, 2))
add(n, e, list(range(0, 6)))
n, e = relabel(shape_b(40, 27, 3))
add(n, e, queries(30, n, 8))
n, e = relabel(random_tree(60))
add(n, e, queries(40, n, 10))
n, e = relabel(caterpillar(120, 15))
add(n, e, queries(80, n, 15))
n, e = relabel(spider([3] * 30 + [40], "random"))
add(n, e, queries(100, n, 35))

big(random_tree(3000), 20, 3000)
big(shape_b(5000, 3500, 4), 45, 5000)

big(random_tree(MAXN), 15)
big(random_tree(MAXN, 3), 5)
big(path(MAXN), 3)
big(star(MAXN), MAXN)
big(caterpillar(MAXN, 400), 600)
big(spider([700] * 285 + [MAXN - 1 - 700 * 285], "random"), 300)
big(shape_b(MAXN, 98000, 60), 70)
big(shape_b(MAXN, 101000, 9), 12)
big(shape_b(MAXN, 140000, 3), 6)
big(shape_b(MAXN, 125000, 8), 12)
big(spider([1] * 1000 + [2] * 1000 + [99999, 97000], "path"), 2100)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open("tests/%02d.in" % i, "w") as f:
        f.write(t)

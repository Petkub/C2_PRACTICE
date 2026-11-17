# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2402)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXN, MAXM = 200_000, 200_000
tests = []


def shuffled(a):
    """a random permutation of the list a (faster than random.shuffle for long lists)"""
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    assert 1 <= n <= MAXN and 0 <= len(edges) <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
    tests.append(f"{n} {len(edges)}\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, edges):
    """random computer numbers, random cable order and random ends"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    l0 = [0] + lab
    e = [(l0[a], l0[b]) if rnd() < 0.5 else (l0[b], l0[a]) for a, b in edges]
    e = shuffled(e)
    return e


def path(n):
    return [(i, i + 1) for i in range(1, n)]


def tree(n, kind):
    e = []
    for i in range(2, n + 1):
        if kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        else:
            p = 1
        e.append((p, i))
    return e


def cactus(n, lo, hi):
    """cycles of random length lo..hi glued in a chain by single cables (the cables between cycles are critical)"""
    e, start, prev = [], 1, None
    while start <= n:
        s = min(ri(lo, hi), n - start + 1)
        if s >= 3:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        elif s == 2:
            e += [(start, start + 1), (start + 1, start)]          # two parallel cables
        if prev is not None:
            e.append((ri(prev[0], prev[1]), ri(start, start + s - 1)))
        prev = (start, start + s - 1)
        start += s
    return e


def extra(n, e, k):
    e = list(e)
    while k > 0:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
            k -= 1
    return e


# samples
add(6, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (4, 6)])
add(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
add(1, [])
add(5, [(1, 2), (3, 4), (4, 5), (5, 3)])
add(7, [(1, 2), (2, 3), (3, 4), (4, 2), (5, 6), (6, 7), (7, 5)])
# hidden: small
add(2, [(1, 2), (1, 2)])
add(3, [(1, 2), (2, 1), (2, 3)])
add(7, [(1, 2), (2, 3), (3, 4), (4, 2), (5, 6), (6, 7), (6, 5)])
add(2, [])
for n, m in ((6, 6), (8, 9), (10, 10), (12, 14)):
    add(n, extra(n, [], m))
add(9, relabel(9, cactus(9, 2, 3)))
add(2000, relabel(2000, extra(2000, tree(2000, "random"), 500)))
add(1500, relabel(1500, cactus(1500, 1, 6)))
# hidden: maximum size
N = MAXN
add(N, relabel(N, path(N)))                                                   # every cable critical, deep DFS
h, c = 50_001, 100_000
add(h + c - 1, relabel(h + c - 1, path(h) + path(h) + path(c) + [(h + c - 1, h - 1)]))
#                                       a path of doubled cables, then a long cycle: none critical
t = 133_334
add(t, relabel(t, path(t) + [(i, i + 1) for i in range(1, t, 2)]))                 # every other cable doubled
add(N, relabel(N, path(N) + [(N, 1)]))                                       # one long cycle
add(157_000, relabel(157_000, cactus(157_000, 1, 5)))
add(133_332, relabel(133_332, cactus(133_332, 2, 2)))                         # pairs of parallel cables in a chain
add(N - 50, relabel(N - 50, extra(N - 50, tree(N - 50, "deep"), 50)))
add(N // 2, relabel(N // 2, extra(N // 2, tree(N // 2, "random"), N // 2)))
add(N, relabel(N, extra(N, [], MAXM)))                                       # random, many separate groups
add(N, relabel(N, tree(N, "star")))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

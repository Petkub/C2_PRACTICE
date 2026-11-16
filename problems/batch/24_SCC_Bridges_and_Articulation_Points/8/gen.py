# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2408)
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


def connected(n, edges):
    """union-find with path halving, written inline (fast enough for 2 * 10^5 edges)"""
    root = list(range(n + 1))
    comps = n
    for u, v in edges:
        while root[u] != u:
            root[u] = root[root[u]]
            u = root[u]
        while root[v] != v:
            root[v] = root[root[v]]
            v = root[v]
        if u != v:
            root[u] = v
            comps -= 1
    return comps == 1


def add(n, edges):
    assert 1 <= n <= MAXN and n - 1 <= len(edges) <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
    assert connected(n, edges)
    tests.append(f"{n} {len(edges)}\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, edges):
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    l0 = [0] + lab
    e = [(l0[a], l0[b]) if rnd() < 0.5 else (l0[b], l0[a]) for a, b in edges]
    e = shuffled(e)
    return e


def tree(n, kind):
    e = []
    half = n // 2
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "broom":
            p = i - 1 if i <= half else half
        else:
            p = 1
        e.append((p, i))
    return e


def cactus(n, lo, hi):
    """cycles of length lo..hi; each new cycle starts at a random vertex of the previous one"""
    e, start, prev = [], 2, (1, 1)
    while start <= n:
        s = min(ri(lo, hi), n - start + 1)
        hub = ri(prev[0], prev[1])
        cyc = [hub] + list(range(start, start + s))
        if len(cyc) == 2:
            e.append((cyc[0], cyc[1]))
        else:
            e += [(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
        prev = (start, start + s - 1)
        start += s
    return e


def extra(n, e, k, near=0):
    e = list(e)
    while k > 0:
        u = ri(1, n)
        v = ri(1, n) if near == 0 else ri(max(1, u - near), min(n, u + near))
        if u != v:
            e.append((u, v))
            k -= 1
    return e


# samples
add(6, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (4, 6)])
add(4, [(1, 2), (2, 3), (3, 4)])
add(1, [])
add(5, [(1, 2), (1, 3), (1, 4), (1, 5)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
add(5, [(1, 2), (2, 1), (2, 3), (3, 4), (4, 5), (5, 3)])
# hidden: small
add(2, [(1, 2)])
add(3, [(1, 2), (2, 3), (2, 3)])
for n, k in ((6, 2), (8, 3), (10, 2), (12, 5)):
    add(n, relabel(n, extra(n, tree(n, "random"), k)))
add(9, relabel(9, cactus(9, 1, 3)))
add(2000, relabel(2000, extra(2000, tree(2000, "random"), 300)))
add(1500, relabel(1500, cactus(1500, 1, 5)))
# hidden: maximum size
N = MAXN
add(N, relabel(N, tree(N, "path")))                                     # deep DFS, about 10^10 pairs
add(N, relabel(N, tree(N, "star")))                                     # the centre: N-1 choose 2
add(N, relabel(N, tree(N, "path") + [(N, 1)]))                          # one long cycle: all 0
add(150_000, relabel(150_000, cactus(150_000, 1, 6)))
add(150_000, relabel(150_000, cactus(150_000, 3, 3)))
add(N, relabel(N, tree(N, "binary")))
add(N, relabel(N, tree(N, "broom")))
add(N - 2000, relabel(N - 2000, extra(N - 2000, tree(N - 2000, "deep"), 2000, 50)))
add(N // 2, relabel(N // 2, extra(N // 2, tree(N // 2, "random"), N // 2)))
add(N // 2, relabel(N // 2, extra(N // 2, tree(N // 2, "path"), N // 2, 3)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

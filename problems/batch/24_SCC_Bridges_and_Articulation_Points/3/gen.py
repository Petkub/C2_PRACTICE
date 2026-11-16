# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2403)
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


def relabel(n, edges, fix=()):
    """random junction numbers (the shape's vertices in fix keep their numbers), random road order and ends"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    for x in fix:
        j = lab.index(x)
        lab[x - 1], lab[j] = lab[j], lab[x - 1]
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
        elif kind == "binary":
            p = i // 2
        else:
            p = 1
        e.append((p, i))
    return e


def cactus(n, lo, hi):
    """cycles of length lo..hi; each new cycle starts at a vertex of the previous one (that vertex is a key junction)"""
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
add(7, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 4), (6, 7)])
add(6, [(1, 2), (1, 3), (1, 4), (5, 6)])
add(1, [])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
add(4, [(1, 2), (2, 3), (3, 2), (3, 4)])
add(8, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3), (6, 7), (7, 8), (8, 6)])
# hidden: small
add(2, [(1, 2)])
add(3, [(2, 1), (2, 3)])
add(3, [(1, 2), (1, 3)])
for n, m in ((6, 6), (8, 8), (10, 11), (12, 13)):
    add(n, extra(n, [], m))
add(2000, relabel(2000, extra(2000, tree(2000, "random"), 300)))
add(1500, relabel(1500, cactus(1500, 1, 5)))
# hidden: maximum size
N = MAXN
add(N, relabel(N, path(N), fix=(1,)))                                  # junction 1 at an end: not key
add(N, relabel(N, path(N)))                                            # junction 1 somewhere inside
add(N, relabel(N, path(N) + [(N, 1)]))                                 # one long cycle: none
add(150_000, relabel(150_000, cactus(150_000, 2, 6)))
add(N, relabel(N, tree(N, "star"), fix=(1,)))                          # the centre is junction 1 (root rule)
add(N, relabel(N, tree(N, "star"), fix=(2,)))                          # junction 1 is a leaf
add(N, relabel(N, tree(N, "binary"), fix=(1,)))
add(N - 1000, relabel(N - 1000, extra(N - 1000, tree(N - 1000, "deep"), 1000)))
add(N // 2, relabel(N // 2, extra(N // 2, tree(N // 2, "random"), N // 2)))
add(N, relabel(N, extra(N, [], MAXM)))                                 # random, many separate groups

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

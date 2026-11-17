# Test generator of this problem (the judge runs it to rebuild the big tests).
import gc, os, random

random.seed(2410)
gc.disable()
rnd = random.random
MAXN, MAXM = 200_000, 200_000
tests = []


def shuffled(a):
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def connected(n, edges):
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
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "binary":
            p = i // 2
        else:
            p = 1
        e.append((p, i))
    return e


def blow_up(tree_edges, k, lo, hi, fixed=None):
    e, rng, start = [], [], 1
    for j in range(1, k + 1):
        s = ri(lo, hi)
        if fixed and j in fixed:
            s = fixed[j]
        rng.append((start, start + s - 1))
        if s >= 3:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        elif s == 2:
            e += [(start, start + 1), (start + 1, start)]
        start += s
    for a, b in tree_edges:
        e.append((ri(*rng[a - 1]), ri(*rng[b - 1])))
    return start - 1, e


def extra(n, e, k, near=0):
    e = list(e)
    while k > 0:
        u = ri(1, n)
        v = ri(1, n) if near == 0 else ri(max(1, u - near), min(n, u + near))
        if u != v:
            e.append((u, v))
            k -= 1
    return e


add(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)])
add(4, [(1, 2), (1, 3), (1, 4)])
add(3, [(1, 2), (2, 3), (3, 1)])
add(2, [(1, 2)])
add(2, [(1, 2), (2, 1)])
add(7, [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7)])

add(1, [])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5)])
add(5, [(1, 2), (1, 3), (1, 4), (1, 5)])
add(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
add(5, [(1, 2), (2, 1), (2, 3), (3, 4), (4, 3), (4, 5)])
add(4, [(1, 2), (2, 3), (3, 4), (4, 2)])

n, e = blow_up(tree(300, "random"), 300, 1, 4)
add(n, relabel(n, e))
add(1500, relabel(1500, extra(1500, tree(1500, "random"), 600)))

N = MAXN
add(N, relabel(N, tree(N, "path")))
add(N, relabel(N, tree(N, "star")))
add(N, relabel(N, tree(N, "path") + [(N, 1)]))
h, c = 50_001, 100_000
add(h + c - 1, relabel(h + c - 1, tree(h, "path") + tree(h, "path") + [(i, i + 1) for i in range(h, h + c - 1)]
                       + [(h + c - 1, h - 1)]))
n, e = blow_up(tree(57_000, "random"), 57_000, 2, 3)
add(n, relabel(n, e))
n, e = blow_up(tree(50_000, "star"), 50_000, 3, 3)
add(n, relabel(n, e))
add(N, relabel(N, tree(N, "caterpillar")))
n, e = blow_up(tree(73_500, "binary"), 73_500, 1, 3)
add(n, relabel(n, e))
add(197_000, relabel(197_000, extra(197_000, tree(197_000, "deep"), 3000, 20)))
add(N // 2, relabel(N // 2, extra(N // 2, tree(N // 2, "random"), N // 2)))
n, e = blow_up(tree(74_000, "path"), 74_000, 1, 3, {1: 3, 74_000: 3})
add(n, relabel(n, e))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

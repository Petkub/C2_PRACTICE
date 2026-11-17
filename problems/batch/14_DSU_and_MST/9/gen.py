# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(140909)
MAXN, MAXK, MAXM = 100_000, 10, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, k, links, mix=True):
    links = list(links)
    if mix:
        shuffle(links)
    m = len(links)
    assert 2 <= n <= MAXN and 1 <= k <= MAXK and 1 <= m <= MAXM
    for u, v, p in links:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= p <= k
    tests.append(f"{n} {k} {m}\n" + "".join(f"{u} {v} {p}\n" for u, v, p in links))


def tree_links(group, p, shape="random"):
    g = list(group)
    shuffle(g)
    res = []
    for i in range(1, len(g)):
        j = i - 1 if shape == "path" else (0 if shape == "star" else ri(0, i - 1))
        a, b = g[i], g[j]
        res.append((a, b, p) if random.random() < 0.5 else (b, a, p))
    return res


def planted(n, k, fine, coarse, m, cover=None, shape="random", common=0.0):
    who = list(range(1, n + 1))
    shuffle(who)
    cover = n if cover is None else cover
    who = who[:cover]
    cut = sorted(set(ri(1, cover - 1) for _ in range(fine - 1)))
    groups = [who[a:b] for a, b in zip([0] + cut, cut + [cover])]
    links, bigs = [], []
    shared = [tree_links(g, 0, shape) for g in groups]
    for p in range(1, k + 1):
        c = coarse[p - 1]
        big = {}
        for gi in range(len(groups)):
            big.setdefault(ri(1, c), []).append(gi)
        for key in sorted(big):
            gis = big[key]
            for gi in gis:
                if gi < common * len(groups):
                    links += [(a, b, p) for a, b, _ in shared[gi]]
                else:
                    links += tree_links(groups[gi], p, shape)
            for t in range(1, len(gis)):
                a = groups[gis[t]][ri(0, len(groups[gis[t]]) - 1)]
                prev = groups[gis[ri(0, t - 1)]]
                links.append((a, prev[ri(0, len(prev) - 1)], p))
            members = [x for gi in gis for x in groups[gi]]
            if len(members) > 1:
                bigs.append((p, members))
    m = max(m, len(links))
    assert bigs
    while len(links) < m:
        p, members = bigs[ri(0, len(bigs) - 1)]
        a, b = members[ri(0, len(members) - 1)], members[ri(0, len(members) - 1)]
        if a != b:
            links.append((a, b, p))
    return n, k, links


def random_apps(n, k, m):
    links = []
    while len(links) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            links.append((a, b, ri(1, k)))
    return n, k, links


add(5, 2, [(1, 2, 1), (2, 3, 1), (4, 5, 1), (1, 2, 2), (2, 3, 2), (3, 4, 2)], mix=False)
add(4, 3, [(1, 2, 1), (2, 1, 2), (3, 4, 3), (1, 2, 1)], mix=False)
add(6, 1, [(1, 2, 1), (3, 4, 1), (4, 5, 1), (5, 3, 1), (2, 6, 1)], mix=False)
add(4, 2, [(1, 2, 1), (2, 1, 2), (1, 2, 2), (3, 4, 1), (4, 3, 2), (2, 3, 1)], mix=False)
add(7, 3, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (5, 6, 1), (1, 2, 2), (2, 3, 2), (3, 4, 2), (6, 7, 2), (1, 2, 3),
           (2, 3, 3), (3, 4, 3), (5, 7, 3), (4, 5, 3)], mix=False)

add(2, 1, [(2, 1, 1)])
add(2, 2, [(1, 2, 1), (1, 2, 1)])
add(5, 2, [(1, 2, 1), (2, 3, 1), (1, 3, 2), (3, 2, 2), (4, 5, 2)])
add(*planted(8, 2, 3, [2, 2], 9))
add(*planted(12, 3, 4, [2, 3, 2], 20, cover=10))
add(*random_apps(10, 10, 60))
add(*planted(2000, 3, 60, [10, 12, 8], 7000))
add(*planted(1500, 1, 30, [6], 2000))
add(*planted(1800, 4, 40, [5, 5, 5, 5], 8000, common=0.5))

N, M = MAXN, MAXM
add(*planted(N, 2, 50, [1, 2], M))
add(*planted(N, 1, 1, [1], M, shape="path"))
add(*planted(N, 2, 1, [1, 1], M, shape="star"))
add(*planted(N, 10, 400, [3] * 10, M, cover=18_000))
add(*planted(N, 5, 2000, [20, 30, 25, 40, 15], M, cover=35_000))
add(*planted(N, 3, 300, [1, 1, 1], M, cover=66_000, common=0.3))
add(*planted(N, 2, 20, [1, 2], M, shape="path"))
add(*random_apps(N, 2, M))
add(*planted(N, 10, 30, [2] * 10, M, cover=19_000, shape="star"))
add(*planted(N, 4, 5000, [100, 120, 90, 110], M, cover=45_000, common=0.8))
add(*planted(N, 7, 150, [4, 5, 3, 6, 4, 5, 3], M, cover=25_000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(140303)
MAXN, MAXM, MAXW = 100_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, roads):
    m = len(roads)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAXW for u, v, w in roads)
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in roads))


def labels(n):
    """a random numbering of towns 1..n that keeps town 1 first"""
    p = list(range(2, n + 1))
    random.shuffle(p)
    return [1] + p


def tree(p, shape, wlo, whi):
    """roads joining the towns of p into a tree; p[0] is the first town of the tree"""
    res = []
    for i in range(1, len(p)):
        if shape == "path":
            j = i - 1
        elif shape == "star":
            j = 0
        elif shape == "deep":
            j = max(0, i - ri(1, 3))
        elif shape == "cater":
            j = i - 1 if i % 2 else max(0, i - 2)
        else:
            j = ri(0, i - 1)
        u, v = p[i], p[j]
        if random.random() < 0.5:
            u, v = v, u
        res.append((u, v, ri(wlo, whi)))
    return res


def extra(n, k, wlo, whi):
    res = []
    while len(res) < k:
        u, v = ri(1, n), ri(1, n)
        if u != v:
            res.append((u, v, ri(wlo, whi)))
    return res


def mixed(roads):
    random.shuffle(roads)
    return roads


# samples
add(5, [(1, 2, 4), (1, 3, 2), (3, 4, 5), (2, 5, 1), (4, 5, 3)])
add(6, [(1, 3, 5), (1, 2, 5), (2, 4, 7), (3, 4, 9), (5, 6, 1)])
add(1, [])
add(4, [(1, 2, 3), (1, 2, 1), (2, 3, 2), (1, 3, 2), (3, 4, 10), (2, 4, 10)])
add(5, [(2, 3, 1), (1, 4, 7), (4, 5, 2)])

# hidden: small
add(2, [])
add(2, [(2, 1, 1000000000), (1, 2, 1000000000)])
for n, m, whi in ((5, 7, 5), (6, 9, 3), (7, 10, 10), (8, 14, 2), (8, 12, 100)):
    p = labels(n)
    add(n, mixed(tree(p, "rand", 1, whi) + extra(n, m - n + 1, 1, whi)))
add(10, extra(10, 8, 1, 4))                                         # probably not connected
p = labels(300)
add(300, mixed(tree(p[:200], "rand", 1, 50) + tree(p[200:], "rand", 1, 50) + extra(300, 0, 1, 1)))
p = labels(2000)
add(2000, mixed(tree(p, "deep", 1, MAXW) + extra(2000, 3000, 1, MAXW)))
p = labels(3000)
add(3000, mixed(tree(p, "rand", 1, 3) + extra(3000, 6000, 1, 3)))

# hidden: maximum size (town 1 reaches almost every town)
N = MAXN
p = labels(N)
add(N, mixed(tree(p, "rand", 1, MAXW) + extra(N, 25_000, 1, MAXW)))
p = labels(N)
add(N, mixed(tree(p, "rand", 1, 5) + extra(N, MAXM - N + 1, 1, 5)))          # many ties
p = labels(N)
add(N, mixed(tree(p, "rand", 7, 7) + extra(N, MAXM - N + 1, 7, 7)))          # every road costs the same
p = labels(N)
add(N, mixed(tree(p, "path", 1, MAXW) + extra(N, 20_000, 1, MAXW)))
p = labels(N)
add(N, mixed(tree(p, "star", 1, MAXW) + extra(N, 25_000, 1, MAXW)))
p = labels(N)
add(N, mixed(tree(p, "deep", 1, 1000) + extra(N, 60_000, 1, 1000)))
p = labels(N)
add(N, mixed(tree(p, "cater", 1, 100) + extra(N, MAXM - N + 1, 1, 100)))
p = labels(N)
tail = p[95_000:]                                                  # 5 000 towns town 1 never reaches
add(N, mixed(tree(p[:95_000], "rand", 1, MAXW) + tree(tail, "rand", 1, MAXW) + extra(95_000, 20_000, 1, MAXW)))
p = labels(N)
road = [(p[i], p[i + 1], 1000 - (i % 1000)) for i in range(N - 1)]  # the cheap road always leads far away
add(N, mixed(road + [(1, p[ri(1, N - 1)], ri(1, 1000)) for _ in range(20_000)]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_300_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

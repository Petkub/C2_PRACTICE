# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100117)
MAXN, MAXK, MAXA = 100_000, 1000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(K, a, par):
    """a[1..n] values, par[2..n] bosses (index 0 and 1 unused)"""
    n = len(a) - 1
    assert 2 <= n <= MAXN and 1 <= K <= min(n, MAXK)
    assert all(-MAXA <= x <= MAXA for x in a[1:])
    assert len(par) == n + 1 and all(1 <= par[i] <= n and par[i] != i for i in range(2, n + 1))
    depth_known = [False] * (n + 1)              # every chain of bosses reaches person 1
    depth_known[1] = True
    for i in range(2, n + 1):
        path = []
        x = i
        while not depth_known[x]:
            path.append(x)
            x = par[x]
            assert len(path) <= n
        for y in path:
            depth_known[y] = True
    tests.append(f"{n} {K}\n" + " ".join(map(str, a[1:])) + "\n" + " ".join(map(str, par[2:])) + "\n")


def shape(n, kind, k=0):
    """par[i] < i in creation order; node 1 is the root"""
    par = [0, 0]
    for i in range(2, n + 1):
        if kind == "random":
            p = ri(1, i - 1)
        elif kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "deep":
            p = ri(max(1, i - 4), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "broom":
            p = i - 1 if i <= n // 2 else n // 2
        elif kind == "blocks":                   # the root has many children, each heads a block of k people
            j = (i - 2) % k
            p = 1 if j == 0 else i - ri(1, min(j, 3))
        elif kind == "cater":                    # a spine with legs of length 1
            p = i - 1 if i <= n // 3 else ri(1, n // 3)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def build(n, K, kind, val, k=0):
    """val(i, depth) gives the value of the i-th created person; labels 2..n are shuffled"""
    par = shape(n, kind, k)
    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[par[i]] + 1
    lab = [0, 1] + random.sample(range(2, n + 1), n - 1)
    a = [0] * (n + 1)
    p = [0] * (n + 1)
    for i in range(1, n + 1):
        a[lab[i]] = val(i, depth[i])
        if i >= 2:
            p[lab[i]] = lab[par[i]]
    add(K, a, p)


def uni(lo, hi):
    return lambda i, d: ri(lo, hi)


def bait(i, d):
    """negative people that guard very good ones further down"""
    return -ri(MAXA // 2, MAXA) if d % 3 == 1 else ri(0, MAXA)


# samples
add(4, [0, 5, -2, 3, 10, 1, -4], [0, 0, 1, 1, 2, 2, 3])
add(3, [0, -1, 4, -6, 7], [0, 0, 1, 2, 3])
add(1, [0, -1000000000, 1000000000], [0, 0, 1])
add(5, [0, 2, 2, 2, 2, 2], [0, 0, 3, 1, 1, 4])
add(6, [0, 0, -5, 8, -1, 9, 6, -3], [0, 0, 1, 1, 3, 2, 4, 2])
# hidden: small
add(2, [0, 3, -7], [0, 0, 1])
build(8, 8, "random", uni(-10, 10))
build(12, 12, "deep", bait)
build(30, 20, "random", uni(-100, 100))
build(200, 60, "cater", uni(-MAXA, MAXA))
build(1000, 300, "random", bait)
build(3000, 1000, "blocks", uni(-MAXA, MAXA), 50)
build(5000, 700, "deep", uni(-1000, 2000))
build(8000, 1000, "star", uni(-MAXA, MAXA))
# hidden: maximum size
N, K = MAXN, MAXK
build(N, K, "path", uni(-MAXA, MAXA))                       # deep chain
build(N, K, "path", uni(MAXA, MAXA))                        # the largest answers
build(N, K, "star", uni(-MAXA, MAXA))
build(N, K, "random", uni(-MAXA, MAXA))
build(N, K, "random", bait)
build(N, K, "blocks", uni(-MAXA, MAXA), 1000)               # worst case for the merging work
build(N, K, "blocks", bait, 600)
build(N, K, "blocks", uni(-MAXA, -1), 1500)                 # every value negative
build(N, K, "deep", bait)
build(N, K, "binary", uni(-MAXA, MAXA))
build(N, K, "broom", uni(-MAXA, MAXA))
build(N, K, "cater", bait)
build(N, 1, "random", uni(-MAXA, MAXA))
build(N, K, "blocks", uni(-MAXA, MAXA), 2)                  # many tiny branches below the root

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

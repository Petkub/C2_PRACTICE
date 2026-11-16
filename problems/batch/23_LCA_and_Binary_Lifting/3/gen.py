import os, random

tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    """Fisher-Yates with random.random (faster than random.shuffle, same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


random.seed(230103)
MAXN, MAXQ, MAXK = 100_000, 50_000, 10**18


def add(a, c, qs):
    n = len(a)
    assert 1 <= n <= MAXN and len(c) == n and 1 <= len(qs) <= MAXQ
    assert all(1 <= x <= n for x in a) and all(0 <= x <= 4 for x in c)
    assert all(1 <= s <= n and 1 <= k <= MAXK for s, k in qs)
    tests.append(f"{n} {len(qs)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, c)) + "\n"
                 + "".join(f"{s} {k}\n" for s, k in qs))


def graph(n, kind):
    """arrows in a hidden numbering 1..n (node 1 is a far tail start where it matters), then relabelled;
    returns (a, lab) with lab[i - 1] = label of hidden node i"""
    nxt = [0] * (n + 1)
    if kind == "rho":                         # tail 1 -> 2 -> ... -> h, then a cycle h+1 .. n
        h = n // 2
        for i in range(1, n):
            nxt[i] = i + 1
        nxt[n] = h + 1
    elif kind == "cycle":
        for i in range(1, n + 1):
            nxt[i] = i % n + 1
    elif kind == "tailloop":                  # a long tail into a self-loop
        for i in range(1, n):
            nxt[i] = i + 1
        nxt[n] = n
    elif kind == "random":
        for i in range(1, n + 1):
            nxt[i] = ri(1, n)
    elif kind == "smallcycles":               # cycles of length 1..20, trees hanging on them
        i = 1
        core = []
        while i <= n // 3:
            ln = min(ri(1, 20), n // 3 - i + 1)
            for j in range(ln):
                nxt[i + j] = i + (j + 1) % ln
            core.append(i)
            i += ln
        for v in range(i, n + 1):
            nxt[v] = ri(1, v - 1)
    elif kind == "twocycles":                 # tails of n/4 into two cycles of n/4
        q = n // 4
        for i in range(1, n + 1):
            nxt[i] = i + 1
        nxt[2 * q] = q + 1                    # tail 1..q, cycle q+1..2q
        nxt[3 * q] = 1                        # tail 2q+1..3q joins at 1 (longer tail)
        nxt[n] = 3 * q + 1                    # cycle 3q+1..n
    else:
        raise ValueError(kind)
    lab = list(range(1, n + 1))
    shuffle(lab)
    a = [0] * n
    for i in range(1, n + 1):
        a[lab[i - 1] - 1] = lab[nxt[i] - 1]
    return a, lab


def make(n, kind, q, cmode="rand", kmode="mix", start="any"):
    a, lab = graph(n, kind)
    rnd = random.random
    if cmode == "max":
        c = [4] * n
    elif cmode == "rand":
        c = [int(rnd() * 5) for _ in range(n)]
    else:
        c = [0 if rnd() < 0.8 else int(rnd() * 5) for _ in range(n)]
    qs = []
    for _ in range(q):
        s = lab[int(rnd() * min(n, 50))] if start == "tail" else 1 + int(rnd() * n)
        r = rnd()
        if kmode == "max" or (kmode == "mix" and r < 0.3):
            k = MAXK - int(rnd() * 1000)
        elif r < 0.5:
            k = 1 + int(rnd() * 3 * n)
        elif r < 0.6:
            k = 1 + int(rnd() * 20)
        else:
            k = 1 + int(rnd() * MAXK)
        qs.append((s, k))
    add(a, c, qs)


# samples
add([2, 3, 1, 2, 5], [1, 2, 3, 4, 4], [(4, 5), (5, 10**18), (1, 3), (2, 7)])
add([2, 3, 2], [4, 0, 1], [(1, 1), (1, 4), (3, 999_999_999_999)])
add([1], [3], [(1, 1), (1, 10**18)])
add([3, 3, 4, 2, 4, 1], [0, 4, 1, 2, 0, 3], [(6, 2), (5, 10), (1, 123_456_789_012)])
add([4, 1, 2, 5, 3, 7, 6], [1, 0, 2, 4, 3, 1, 1], [(1, 5), (7, 4), (2, 1000), (6, 3), (3, 10**17)])
# hidden: small and medium
add([1, 1], [0, 0], [(2, 1), (2, 10**18), (1, 5)])
make(5, "random", 30)
make(10, "rho", 40, start="tail")
make(30, "smallcycles", 60)
make(50, "twocycles", 80, start="tail")
make(2000, "rho", 2000, start="tail")
make(3000, "random", 3000, "sparse")
# hidden: maximum size
make(MAXN, "rho", MAXQ, start="tail")
make(MAXN, "rho", MAXQ, "max", "max", start="tail")
make(MAXN, "cycle", MAXQ)
make(MAXN, "tailloop", MAXQ, "max", start="tail")
make(MAXN, "twocycles", MAXQ, start="tail")
make(MAXN, "random", MAXQ)
make(MAXN, "smallcycles", MAXQ, "sparse")
make(MAXN, "cycle", MAXQ, "max", "max")
make(MAXN, "rho", MAXQ, "sparse")

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_400_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

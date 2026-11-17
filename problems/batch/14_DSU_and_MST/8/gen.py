# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(140808)
MAXN, MAXM, MAXT, MAXC = 100_000, 100_000, 10**6, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = int(random.random() * (i + 1))
        a[i], a[j] = a[j], a[i]


def add(n, edges, mix=True):
    edges = list(edges)
    if mix:
        shuffle(edges)
    m = len(edges)
    assert 2 <= n <= MAXN and 1 <= m <= MAXM
    for u, v, t, c in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= t <= MAXT and 1 <= c <= MAXC
    tests.append(f"{n} {m}\n" + "".join(f"{u} {v} {t} {c}\n" for u, v, t, c in edges))


def flip(u, v, t, c):
    return (u, v, t, c) if random.random() < 0.5 else (v, u, t, c)


def cost(t, tmax, cmax, corr):
    """corr: a faster link costs more (with some noise), so the earliest links are the expensive ones"""
    if not corr:
        return ri(1, cmax)
    base = cmax - (cmax - 1) * t // tmax
    return max(1, min(cmax, base - ri(0, cmax // 10)))


def build(n, m, tmax=MAXT, cmax=MAXC, late=1, corr=False, shape="random", tlate=None, cfix=None):
    """a connected graph: a spanning tree of the first n - late vertices plus random extra links among them;
    each of the last `late` vertices gets a few links, all slow (time >= tlate), so the finishing time is high
    and almost every distinct time is below it"""
    p = list(range(1, n + 1))
    shuffle(p)
    core, outs = p[:n - late], p[n - late:]
    if tlate is None:
        tlate = tmax - tmax // 20
    edges = []

    def mk(a, b, lo, hi):
        t = ri(lo, hi)
        c = cfix if cfix is not None else cost(t, tmax, cmax, corr)
        return flip(a, b, t, c)

    for i in range(1, len(core)):
        if shape == "path":
            j = i - 1
        elif shape == "star":
            j = 0
        else:
            j = ri(0, i - 1)
        edges.append(mk(core[i], core[j], 1, tmax))
    per = 3
    for x in outs:
        for _ in range(per):
            edges.append(mk(x, core[ri(0, len(core) - 1)], tlate, tmax))
    while len(edges) < m:
        a, b = core[ri(0, len(core) - 1)], core[ri(0, len(core) - 1)]
        if a != b:
            edges.append(mk(a, b, 1, tmax))
    return n, edges[:m] if len(edges) > m else edges


def split(n, m, tmax=MAXT, cmax=MAXC):
    """two halves with no link between them: -1"""
    h = n // 2
    a = build(h, m // 2, tmax, cmax, late=0)[1]
    b = build(n - h, m - m // 2, tmax, cmax, late=0)[1]
    return n, a + [(u + h, v + h, t, c) for u, v, t, c in b]


# samples
add(4, [(1, 2, 2, 4), (2, 3, 5, 3), (1, 3, 5, 6), (3, 4, 1, 2), (1, 4, 7, 1)], mix=False)
add(4, [(1, 2, 3, 5), (2, 1, 1, 9), (3, 4, 2, 2)], mix=False)
add(5, [(1, 2, 4, 3), (2, 3, 4, 1), (3, 4, 4, 4), (4, 5, 4, 2), (5, 1, 4, 5), (2, 4, 4, 2)], mix=False)
add(2, [(1, 2, 5, 1), (2, 1, 3, 100), (1, 2, 3, 50)], mix=False)
add(6, [(1, 2, 3, 7), (2, 3, 6, 2), (3, 4, 2, 1), (4, 5, 6, 4), (5, 6, 1, 3), (6, 1, 8, 1), (2, 5, 6, 6),
        (1, 4, 9, 2)], mix=False)
# hidden: small (checked against brute.cpp)
add(2, [(2, 1, 1000000, 1000000000)])
add(3, [(1, 2, 2, 10), (2, 3, 2, 10), (1, 3, 1, 30)])                    # the fast link is the expensive one
add(*build(6, 10, 5, 10))
add(*build(7, 14, 4, 20, corr=True))
add(*build(8, 16, 6, 6, late=2))
add(*split(8, 12, 5, 9))
add(*build(300, 1000, 50, 100, corr=True))
add(*build(2000, 6000, late=3, corr=True))
add(*build(1500, 5000, 1, 1000))                                        # every link takes the same time
# hidden: maximum size
N, M = MAXN, MAXM
add(*build(N, M))
add(*build(N // 2, M, corr=True))
add(*build(N, M, cfix=MAXC))                                            # every link costs 10^9
add(*build(N // 2, M, corr=True, shape="path"))
add(*split(N // 2, M))                                                  # never connected: -1
add(*build(N, M, tlate=MAXT, corr=True))                                # finishing time is exactly 10^6
add(*build(N // 2, M, shape="star", corr=True, late=2))
add(*build(N // 2, M, cmax=10))                                         # many equal costs
add(*build(N, M, corr=True, late=5))
add(*build(N // 2, M, corr=True, cfix=None, tlate=MAXT - 10))
add(*build(N, M, shape="path", cfix=MAXC - 1))
add(*build(N // 2, M, corr=True, late=1, tlate=MAXT // 2))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

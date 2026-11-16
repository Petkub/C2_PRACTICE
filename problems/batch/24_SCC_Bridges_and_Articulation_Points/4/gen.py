# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import gc, os, random

random.seed(2404)
gc.disable()                    # millions of small tuples: no cyclic GC needed, much faster
rnd = random.random
MAXN, MAXM, MAXC = 200_000, 200_000, 10**9
tests = []


def shuffled(a):
    """a random permutation of the list a (faster than random.shuffle for long lists)"""
    rnd = random.random
    keys = [rnd() for _ in a]
    return [a[i] for i in sorted(range(len(a)), key=keys.__getitem__)]


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, c, edges):
    assert 1 <= n <= MAXN and 0 <= len(edges) <= MAXM and len(c) == n
    assert all(1 <= x <= MAXC for x in c)
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {len(edges)}\n" + " ".join(map(str, c)) + "\n" + "".join(["%d %d\n" % p for p in edges]))


def relabel(n, c, edges):
    """random member numbers (costs move with the members) and a random rule order"""
    lab = list(range(1, n + 1))
    lab = shuffled(lab)
    c2 = [0] * n
    for i in range(n):
        c2[lab[i] - 1] = c[i]
    l0 = [0] + lab
    e = [(l0[a], l0[b]) for a, b in edges]
    e = shuffled(e)
    return n, c2, e


def blocks(n, m, size_fn, back=0.0):
    """consecutive blocks, each a cycle; rules go forward between blocks (a DAG of blocks, the last block is a sink);
    with probability back a random rule stays inside its block"""
    e, bl, start = [], [], 1
    while start <= n:
        s = min(size_fn(), n - start + 1)
        bl.append((start, start + s - 1))
        if s >= 2:
            e += [(i, i + 1) for i in range(start, start + s - 1)] + [(start + s - 1, start)]
        start += s
    where = [0] * (n + 1)
    for j, (a, b) in enumerate(bl):
        for x in range(a, b + 1):
            where[x] = j
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v and where[u] < where[v]:
            e.append((u, v))
        elif u != v and where[u] == where[v] and random.random() < back:
            e.append((u, v))
    return e[:m], bl


def rand_edges(n, m):
    e = []
    while len(e) < m:
        u = 1 + int(rnd() * n)
        v = 1 + int(rnd() * n)
        if u != v:
            e.append((u, v))
    return e


def rc(n, lo=1, hi=MAXC):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(5, [4, 3, 5, 2, 6], [(1, 2), (2, 1), (2, 3), (4, 5)])
add(4, [3, 3, 1, 5], [(1, 2), (2, 1), (3, 4), (4, 3)])
add(1, [7], [])
add(3, [2, 2, 2], [])
add(3, [MAXC] * 3, [(1, 2), (2, 3), (3, 1)])
add(6, [5, 1, 1, 1, 4, 9], [(2, 3), (3, 4), (4, 2), (4, 5), (1, 6), (6, 1)])
# hidden: small
add(2, [5, 5], [(1, 2)])
add(2, [5, 5], [(1, 2), (2, 1)])
for n, m in ((6, 6), (8, 10), (10, 9), (12, 16), (14, 12)):
    add(n, rc(n, 1, 6), rand_edges(n, m))
e, bl = blocks(2000, 4000, lambda: ri(1, 4))
add(*relabel(2000, rc(2000, 1, 50), e))
add(3000, rc(3000, 1, 3), rand_edges(3000, 2500))
# hidden: maximum size
N = MAXN
add(*relabel(N, rc(N), [(i, i + 1) for i in range(1, N)]))        # one long chain: only the last member is a sink
add(*relabel(N, [MAXC] * N, [(i, i + 1) for i in range(1, N)] + [(N, 1)]))      # everyone in one group: 2 * 10^14
e, bl = blocks(N, MAXM, lambda: ri(1, 3))
c = rc(N, 1, 1000)
add(*relabel(N, c, e))
n = 120_000                                              # 120 000 cycle rules, 80 000 rules between / inside blocks
e, bl = blocks(n, MAXM, lambda: ri(50, 500), back=0.3)
c = [1] * n                                              # the cheapest group is the first block, which is not a sink
for x in range(bl[-1][0], bl[-1][1] + 1):
    c[x - 1] = MAXC
add(*relabel(n, c, e))
add(N, [1] * N, [])                                     # nobody needs anybody: N ways
add(N, rc(N, 1, 2), rand_edges(N, N // 2))              # many sinks, many ties
add(N, rc(N, 1, 10), rand_edges(N, MAXM))
# many equal sink pairs hanging below a long chain of cheap members
h, p = 99_000, 50_000
e = [(i, i + 1) for i in range(1, h)]
c = [1] * h
for j in range(p):
    a, b = h + 2 * j + 1, h + 2 * j + 2
    e += [(a, b), (b, a)]
    c += [MAXC // 2, MAXC // 2]
    if j < 1000:
        e.append((ri(h - 1000, h), a))                  # only near the end: every closure walks the chain
e.append((h, h + 1))
add(*relabel(h + 2 * p, c, e))
# a chain in number order whose only sink is the last member, the most expensive one: every closure is long
add(N, [1 + i % 1000 for i in range(N - 1)] + [MAXC], [(i, i + 1) for i in range(1, N)])
e, bl = blocks(150_000, MAXM, lambda: 20_000)           # 8 big groups in a DAG, only the last one is a sink
add(*relabel(150_000, rc(150_000, MAXC - 10, MAXC), e))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

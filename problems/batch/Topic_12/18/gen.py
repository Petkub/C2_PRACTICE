# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(100118)
MAXN, MAXQ, MAXA = 100_000, 100_000, 10**6
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, par, qs):
    """a[1..n] ranks, par[2..n] bosses (index 0 and 1 unused), qs = [(v, x)]"""
    n, q = len(a) - 1, len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and len(par) == n + 1
    assert all(1 <= x <= MAXA for x in a[1:])
    assert all(1 <= par[i] <= n and par[i] != i for i in range(2, n + 1))
    assert all(1 <= v <= n and 1 <= x <= MAXA for v, x in qs)
    done = [False] * (n + 1)                     # every chain of bosses reaches person 1
    done[1] = True
    for i in range(2, n + 1):
        path, x = [], i
        while not done[x]:
            path.append(x)
            x = par[x]
            assert len(path) <= n
        for y in path:
            done[y] = True
    lines = [f"{n} {q}", " ".join(map(str, a[1:]))]
    if n > 1:
        lines.append(" ".join(map(str, par[2:])))
    tests.append("\n".join(lines) + "\n" + "".join(f"{v} {x}\n" for v, x in qs))


def shape(n, kind):
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
        elif kind == "broom":                    # a long handle, then many leaves at its end
            p = i - 1 if i <= n // 2 else n // 2
        elif kind == "cater":
            p = i - 1 if i <= n // 2 else ri(1, n // 2)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def build(n, kind, val, q, qgen):
    """val(i, depth, n) ranks the i-th created person; qgen(info) gives one query on created indices"""
    par = shape(n, kind)
    depth = [0] * (n + 1)
    for i in range(2, n + 1):
        depth[i] = depth[par[i]] + 1
    rank = [0] + [val(i, depth[i], n) for i in range(1, n + 1)]
    lab = [0, 1] + random.sample(range(2, n + 1), n - 1)
    a, p = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        a[lab[i]] = rank[i]
        if i >= 2:
            p[lab[i]] = lab[par[i]]
    md = max(depth)
    deep = [i for i in range(1, n + 1) if 3 * depth[i] >= md]
    pp = par + [0]
    pp[0] = 0
    a2 = [pp[pp[i]] for i in range(n + 1)]
    a4 = [a2[a2[i]] or 1 for i in range(n + 1)]   # the 4th boss above (person 1 if fewer)
    info = (n, par, rank, deep, a4)
    qs = []
    for _ in range(q):
        v, x = qgen(info)
        qs.append((lab[v], x))
    add(a, p, qs)


def up_rank(i, d, n):                            # ranks grow towards the top, with ties
    return max(1, min(MAXA, MAXA - d * MAXA // (n + 1) - ri(0, 3)))


def rnd_rank(i, d, n):
    return ri(1, MAXA)


def small_rank(i, d, n):                         # many equal ranks
    return ri(1, 5)


def comb_rank(i, d, n):                          # ranks fall going down the handle, the leaves beat them all
    return MAXA if d >= n // 2 else MAXA - 1 - d


def cater_comb(lo):
    """the spine's ranks fall going down, the legs beat (almost) the whole spine above them"""
    def f(i, d, n):
        return MAXA - 1 - d if i <= n // 2 else MAXA - ri(0, lo)
    return f


def q_any(info):
    n = info[0]
    v = ri(1, n)
    return v, ri(1, MAXA)


def q_chain(info):
    """x near the ranks above v, so the answer is often far up the chain"""
    n, par, rank, deep, a4 = info
    v = deep[int(random.random() * len(deep))]
    u = v
    for _ in range(int(random.random() * 4)):
        u = a4[u]
    r = random.random()
    if r < 0.1:
        return v, MAXA                           # often nobody reaches the top rank
    if r < 0.2:
        return v, max(1, rank[v] - ri(0, 2))     # v decides itself
    w = 1 if r < 0.35 else (par[u] or 1 if r < 0.55 else u)
    return v, max(1, min(MAXA, rank[w] + ri(-1, 1)))


def q_mix(info):
    return q_any(info) if random.random() < 0.3 else q_chain(info)


# samples
add([0, 9, 4, 7, 2, 4, 1, 8], [0, 0, 1, 2, 2, 4, 5, 3], [(6, 3), (6, 5), (6, 10), (7, 9), (3, 7)])
add([0, 5, 5, 3, 6], [0, 0, 1, 2, 3], [(4, 6), (3, 5), (3, 6), (2, 5)])
add([0, 1], [0, 0], [(1, 1), (1, 2)])
add([0, 10, 3, 6, 6, 1, 2], [0, 0, 1, 1, 3, 4, 4], [(5, 2), (6, 7), (5, 11)])
add([0, 1000000, 1], [0, 0, 1], [(2, 1000000)])
# hidden: small
build(2, "path", rnd_rank, 6, q_any)
build(10, "random", small_rank, 50, q_mix)
build(30, "path", up_rank, 100, q_mix)
build(200, "deep", small_rank, 300, q_mix)
build(1000, "cater", up_rank, 1000, q_mix)
build(2000, "broom", comb_rank, 2000, q_mix)
build(3000, "random", rnd_rank, 3000, q_mix)
build(5000, "deep", up_rank, 5000, q_chain)
# hidden: maximum size
N, Q = MAXN, MAXQ
build(N, "path", up_rank, Q, q_chain)            # one long chain of holders
build(N, "path", small_rank, Q, q_mix)
build(N, "broom", comb_rank, Q, q_mix)           # finding the next holder by hopping is slow here
build(N, "deep", up_rank, Q, q_chain)
build(N, "cater", up_rank, Q, q_chain)
build(N, "random", rnd_rank, Q, q_mix)
build(N, "cater", cater_comb(2), Q, q_mix)        # hopping to the next holder walks the spine again
build(N, "cater", cater_comb(30), Q, q_chain)
build(N, "deep", lambda i, d, n: MAXA - d // 7, Q, q_chain)   # long runs of equal ranks
build(N, "broom", lambda i, d, n: comb_rank(i, d, n) if d < n // 2 else ri(1, MAXA), Q, q_mix)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

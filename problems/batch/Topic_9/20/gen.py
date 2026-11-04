# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(92020)
MAXN = 200_000
MAXQ = 200_000
tests = []


def add(f, qs):
    """f[1..n] given as a list of length n (f[0] is lock 1)"""
    n, q = len(f), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(1 <= x <= n for x in f)
    assert all(1 <= a <= n and 1 <= b <= n for a, b in qs)
    lines = [f"{n} {q}", " ".join(map(str, f))] + [f"{a} {b}" for a, b in qs]
    tests.append("\n".join(lines) + "\n")


def relabel(f, qs):
    """random names for the locks (f and queries use 1-based labels)"""
    n = len(f)
    p = list(range(1, n + 1))
    random.shuffle(p)
    g = [0] * n
    for v in range(1, n + 1):
        g[p[v - 1] - 1] = p[f[v - 1] - 1]
    return g, [(p[a - 1], p[b - 1]) for a, b in qs]


def rand_q(n, q, same=0.02):
    rnd = random.random
    out = []
    for _ in range(q):
        a = int(rnd() * n) + 1
        b = a if rnd() < same else int(rnd() * n) + 1
        out.append((a, b))
    return out


def tree_loop(n, parent_of):
    """lock 1 drains into itself, lock v > 1 drains into parent_of(v) < v"""
    f = [1] + [parent_of(v) for v in range(2, n + 1)]
    return f


def depths(f):
    """steps until reaching lock 1 for a tree_loop (parents have smaller numbers)"""
    d = [0] * (len(f) + 1)
    for v in range(2, len(f) + 1):
        d[v] = d[f[v - 1]] + 1
    return d


def deep_pairs(f, q, top):
    """pairs among the `top` deepest locks (they meet late or only near the root)"""
    d = depths(f)
    order = sorted(range(1, len(f) + 1), key=lambda v: -d[v])[:top]
    return [(random.choice(order), random.choice(order)) for _ in range(q)]


def rho(n, tails, cyc):
    """one cycle of length cyc (locks 1..cyc), the other locks form `tails` chains entering it"""
    f = [0] * n
    for v in range(1, cyc + 1):
        f[v - 1] = v % cyc + 1
    rest = list(range(cyc + 1, n + 1))
    chains = [rest[i::tails] for i in range(tails)]
    for ch in chains:
        if not ch:
            continue
        f[ch[0] - 1] = random.randint(1, cyc)
        for x, y in zip(ch[1:], ch):
            f[x - 1] = y
    return f


def comps(n, k):
    """k components: each a cycle with random trees hanging from it"""
    f = [0] * n
    cuts = sorted(random.sample(range(1, n), k - 1)) if k > 1 else []
    for lo, hi in zip([0] + cuts, cuts + [n]):
        size = hi - lo
        cyc = random.randint(1, max(1, min(size, 50)))
        for i in range(cyc):
            f[lo + i] = lo + (i + 1) % cyc + 1
        for i in range(cyc, size):
            f[lo + i] = lo + random.randint(max(0, i - 3), i - 1) + 1   # long thin trees
    return f


# samples
add([2, 3, 4, 5, 3, 4], [(1, 4), (6, 3), (2, 2), (3, 4)])
add([2, 3, 3, 3, 4], [(1, 5), (1, 3), (2, 4)])
add([1], [(1, 1)])
add([2, 3, 4, 1], [(1, 3), (2, 2), (4, 1)])
add([3, 3, 5, 3, 2, 8, 6, 7], [(1, 2), (4, 1), (6, 7), (8, 5), (3, 4)])
# hidden: small (the brute force checks them)
add([2, 1], [(1, 2), (2, 1), (1, 1)])
add([1, 1], [(1, 2), (2, 1), (2, 2)])
n = 10
add([random.randint(1, n) for _ in range(n)], [(a, b) for a in range(1, n + 1) for b in range(1, n + 1)])
n = 200
add([random.randint(1, n) for _ in range(n)], rand_q(n, 2000))
add(*relabel(comps(300, 4), rand_q(300, 3000)))
add(*relabel(rho(1000, 3, 7), rand_q(1000, 3000)))
f = tree_loop(1000, lambda v: v - 1)                   # a path into a lock that drains into itself
add(*relabel(f, rand_q(1000, 3000)))
f = tree_loop(5000, lambda v: max(1, v - random.randint(1, 3)))
add(*relabel(f, deep_pairs(f, 10000, 300)))
add(*relabel(rho(8000, 2, 4000), rand_q(8000, 10000)))
add(*relabel(comps(10000, 30), rand_q(10000, 10000)))
# hidden: large
N = MAXN
Q = 100_000
f = tree_loop(N, lambda v: v - 1)                      # one long path: meeting up to minute N - 1
qs = [(N, 1), (1, N), (N, N - 1), (N, 2)] + [(random.randint(N // 2, N), random.randint(1, N)) for _ in range(Q - 4)]
add(*relabel(f, qs))
f = tree_loop(N, lambda v: 1 if v == 3 * N // 4 + 1 else v - 1)
add(*relabel(f, deep_pairs(f, Q, 2000)))              # two long branches
f = tree_loop(N, lambda v: v - 1 if v % 5 else max(1, v - 2))   # deep with short side steps
add(*relabel(f, deep_pairs(f, Q, 3000)))
f = tree_loop(N, lambda v: max(1, v - random.choice([1, 1, 1, 2])))
add(*relabel(f, deep_pairs(f, Q, 5000)))
f = tree_loop(N, lambda v: max(1, v - random.choice([1, 1, 1, 2, 50])))
add(*relabel(f, deep_pairs(f, Q, 20000)))
f = tree_loop(N, lambda v: random.randint(max(1, v - 10), v - 1))
add(*relabel(f, rand_q(N, Q)))
add(*relabel(rho(N, 2, N // 2), rand_q(N, Q)))         # two long tails into a long cycle: many -1
add(*relabel(rho(N, 1, 6), rand_q(N, Q)))               # a long tail into a short cycle
add(*relabel(rho(N, 1000, 1000), rand_q(N, Q)))
add(*relabel(comps(N, 20), rand_q(N, Q)))
add(*relabel([v % N + 1 for v in range(1, N + 1)], rand_q(N, Q, 0.3)))   # one big cycle
add([random.randint(1, N) for _ in range(N)], rand_q(N, Q))              # random drains
f = rho(N, 1, 3)                                        # a long tail with short side chains
for v in range(170_004, N + 1):
    f[v - 1] = random.randint(4, v - 1)
add(*relabel(f, [(random.randint(150_000, N), random.randint(100_000, N)) for _ in range(Q)]))
f = tree_loop(N, lambda v: v - 1 if v <= 180_000 else random.randint(1, v - 1))
add(*relabel(f, deep_pairs(f, Q, 40_000)))
f = tree_loop(50_000, lambda v: 1)                     # a star: everything meets by minute 1
add(*relabel(f, rand_q(50_000, MAXQ)))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(150081)
MAXN, MAXW = 100_000, (1 << 30) - 1
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shape(n, kind):
    """par[i] (< i) for the cities 2..n of a tree of the given shape, before relabelling"""
    par = [0, 0]
    half = max(1, n // 2)
    b = max(2, int(n ** 0.5))
    for i in range(2, n + 1):
        if kind == "path":
            p = i - 1
        elif kind == "star":
            p = 1
        elif kind == "random":
            p = ri(1, i - 1)
        elif kind == "deep":
            p = ri(max(1, i - 3), i - 1)
        elif kind == "binary":
            p = i // 2
        elif kind == "caterpillar":
            p = i - 1 if i <= half else ri(1, half)
        elif kind == "broom":
            p = i - 1 if i <= half else half
        elif kind == "chains":
            p = i - 1 if (i - 1) % b else ri(1, i - 1)
        else:
            raise ValueError(kind)
        par.append(p)
    return par


def add(n, k, edges):
    assert 2 <= n <= MAXN and 0 <= k <= MAXW and len(edges) == n - 1
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 0 <= w <= MAXW
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * (n + 1)              # connected (n - 1 edges, so a tree)
    seen[1] = True
    st = [1]
    while st:
        u = st.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                st.append(v)
    assert all(seen[1:])
    tests.append(f"{n} {k}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def tree(n, kind, code):
    """edges of a tree of the given shape with random labels, edge order and ends; code() gives each code"""
    par = shape(n, kind)
    lab = list(range(1, n + 1))
    random.shuffle(lab)
    lab = [0] + lab
    edges = []
    for i in range(2, n + 1):
        u, v = lab[i], lab[par[i]]
        if random.random() < 0.5:
            u, v = v, u
        edges.append((u, v, code()))
    random.shuffle(edges)
    return edges


def pair_code(n, edges):
    """the code of the route between two random cities (so that the answer is at least 1)"""
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    px = [-1] * (n + 1)
    px[1] = 0
    st = [1]
    while st:
        u = st.pop()
        for v, w in adj[u]:
            if px[v] < 0:
                px[v] = px[u] ^ w
                st.append(v)
    a = ri(1, n)
    b = ri(1, n - 1)
    b += b >= a
    return px[a] ^ px[b]


def case(n, kind, mode, k=None):
    if mode == "big":                       # any 30-bit code: few pairs, K taken from a real pair
        code = lambda: ri(0, MAXW)
    elif mode == "small":                   # codes 0..3: a huge number of pairs
        code = lambda: ri(0, 3)
    elif mode == "zero":
        code = lambda: 0
    elif mode == "bits":                    # one bit out of the lowest 6
        code = lambda: 1 << ri(0, 5)
    elif mode == "mid":                     # codes 0..255
        code = lambda: ri(0, 255)
    else:
        raise ValueError(mode)
    edges = tree(n, kind, code)
    if k is None:
        k = pair_code(n, edges)
    add(n, k, edges)


def planted(n, kind, k, vals):
    """codes chosen so that the route code from city 1 to every city is one of vals (picked at random):
    a huge number of pairs"""
    t = [0] + [vals[int(random.random() * len(vals))] for _ in range(n)]
    t[1] = 0
    edges = [(u, v, t[u] ^ t[v]) for u, v, _ in tree(n, kind, lambda: 0)]
    add(n, k, edges)


# samples
add(5, 3, [(1, 2, 1), (1, 3, 2), (2, 4, 3), (2, 5, 2)])
add(4, 0, [(1, 2, 5), (3, 1, 5), (1, 4, 5)])
add(2, 7, [(2, 1, 7)])
add(4, 6, [(1, 2, 1), (2, 3, 2), (3, 4, 4)])
add(7, 4, [(3, 1, 6), (1, 5, 2), (3, 2, 4), (6, 3, 0), (5, 7, 6), (4, 5, 2)])
# hidden: small and medium (the brute force checks these)
case(3, "path", "small", 0)
case(10, "random", "bits")
case(20, "star", "small", 3)
case(40, "binary", "mid")
case(60, "caterpillar", "zero", 0)
case(100, "deep", "big")
case(300, "chains", "small", 1)
case(2000, "random", "mid", 0)
case(5000, "path", "bits")
# hidden: maximum size
N = MAXN
case(N, "path", "big")
planted(N, "path", 6, [0, 6])                   # about N^2 / 4 pairs
case(N, "star", "zero", 0)                      # every pair: N (N - 1) / 2
planted(N, "random", 0, [0, 9])
case(N, "random", "big")
planted(N, "binary", 3, [1, 2])
planted(N, "caterpillar", 5, [0, 5, 0, 5, 7])
case(N, "broom", "mid")
planted(N, "deep", 0, [MAXW, 0])
case(N, "chains", "bits", 0)
case(N, "random", "zero", 5)                    # no pair at all
planted(N, "chains", 1 << 29, [0, 1 << 29])
case(N, "deep", "small", 3)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

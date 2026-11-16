# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(2112)
MAXN = 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    """Fisher-Yates driven by random.random() only (fast, and the same on every Python 3 version)"""
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def check(n, roads):
    """n roads, no loop, no repeated pair, connected (so exactly one cycle)"""
    assert len(roads) == n
    pairs = set()
    adj = [[] for _ in range(n + 1)]
    for u, v in roads:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        key = (min(u, v), max(u, v))
        assert key not in pairs
        pairs.add(key)
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * (n + 1)
    seen[1] = True
    st = [1]
    while st:
        x = st.pop()
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True
                st.append(y)
    assert all(seen[1:])


def add(n, roads, from_build=False):
    """from_build: the cycle 1..L (L >= 3) plus par[i] < i for the other nodes already guarantees the rules"""
    assert 3 <= n <= MAXN and len(roads) == n
    if not from_build:
        check(n, roads)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in roads))


def build(n, L, kind):
    """a cycle 1..L, then nodes L+1..n hang from earlier nodes; random labels and order"""
    assert 3 <= L <= n
    par = [0] * (n + 1)
    for i in range(L + 1, n + 1):
        if kind == "random":
            par[i] = ri(1, i - 1)
        elif kind == "tail":                 # one long path from cycle node 1
            par[i] = 1 if i == L + 1 else i - 1
        elif kind == "legs":                 # every cycle node gets a path, round robin
            par[i] = i - L
        elif kind == "star":                 # all extra nodes on cycle node 1
            par[i] = 1
        elif kind == "deep":
            par[i] = ri(max(1, i - 3), i - 1)
        elif kind == "half":                 # long tails on two opposite cycle nodes
            par[i] = (1 if i == L + 1 else (L // 2 + 1 if i == L + 2 else i - 2))
        else:
            raise ValueError(kind)
        assert 1 <= par[i] < i
    lab = list(range(1, n + 1))
    shuffle(lab)
    roads = [(i, i % L + 1) for i in range(1, L + 1)] + [(i, par[i]) for i in range(L + 1, n + 1)]
    roads = [(lab[u - 1], lab[v - 1]) if random.random() < 0.5 else (lab[v - 1], lab[u - 1]) for u, v in roads]
    shuffle(roads)
    add(n, roads, n > 1000)


# samples
add(6, [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 6)])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
add(3, [(1, 2), (3, 2), (1, 3)])
add(7, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (2, 6), (7, 1)])
add(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (2, 7), (7, 8)])
# hidden: small and medium
build(4, 4, "random")
build(10, 4, "random")
build(30, 6, "legs")
build(60, 3, "star")
build(300, 300, "random")
build(301, 150, "half")
build(2000, 40, "deep")
build(5000, 2500, "legs")
build(8000, 3, "tail")
# hidden: maximum size
N = MAXN
build(N, N, "random")                 # one big cycle (even length)
build(N - 1, N - 1, "random")         # odd length
build(N, 3, "tail")                   # the largest sums
build(N, N // 2, "half")
build(N, 85_000, "legs")
build(N, 1000, "random")
build(N, 316, "legs")
build(N, 3, "star")
build(N, 20_000, "deep")
build(N, 99_999, "random")
build(N, 4, "random")
build(N, 70_001, "random")
for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t and len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(2112)
MAXN = 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def shuffle(a):
    rnd = random.random
    for i in range(len(a) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        a[i], a[j] = a[j], a[i]


def check(n, roads):
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
    assert 3 <= n <= MAXN and len(roads) == n
    if not from_build:
        check(n, roads)
    tests.append(f"{n}\n" + "".join(f"{u} {v}\n" for u, v in roads))


def build(n, L, kind):
    assert 3 <= L <= n
    par = [0] * (n + 1)
    for i in range(L + 1, n + 1):
        if kind == "random":
            par[i] = ri(1, i - 1)
        elif kind == "tail":
            par[i] = 1 if i == L + 1 else i - 1
        elif kind == "legs":
            par[i] = i - L
        elif kind == "star":
            par[i] = 1
        elif kind == "deep":
            par[i] = ri(max(1, i - 3), i - 1)
        elif kind == "half":
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


add(6, [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 6)])
add(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
add(3, [(1, 2), (3, 2), (1, 3)])
add(7, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (2, 6), (7, 1)])
add(8, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (2, 7), (7, 8)])

build(4, 4, "random")
build(10, 4, "random")
build(30, 6, "legs")
build(60, 3, "star")
build(300, 300, "random")
build(301, 150, "half")
build(2000, 40, "deep")
build(5000, 2500, "legs")
build(8000, 3, "tail")

N = MAXN
build(N, N, "random")
build(N - 1, N - 1, "random")
build(N, 3, "tail")
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

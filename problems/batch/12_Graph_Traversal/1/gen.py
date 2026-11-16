# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(7001)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, edges):
    m = len(edges)
    assert 1 <= n <= MAXN and 0 <= m <= MAXM
    assert all(1 <= a <= n and 1 <= b <= n and a != b for a, b in edges)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in edges))


def relabel(n, edges):
    """random person numbers and random order of pairs and of the two ends"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    res = [(p[a - 1], p[b - 1]) if random.random() < 0.5 else (p[b - 1], p[a - 1]) for a, b in edges]
    random.shuffle(res)
    return res


def path(start, k):
    return [(start + i, start + i + 1) for i in range(k - 1)]


def rnd_edges(n, m):
    res = []
    while len(res) < m:
        a, b = ri(1, n), ri(1, n)
        if a != b:
            res.append((a, b))
    return res


# samples
add(6, [(1, 2), (4, 2), (3, 6)])
add(5, [(2, 5), (4, 3), (3, 4)])
add(1, [])
add(4, [])
add(7, [(5, 7), (7, 3), (1, 2), (6, 4)])
add(5, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 3), (2, 1)])
# hidden: small
add(2, [(2, 1)])
add(2, [(1, 2), (2, 1), (1, 2)])
add(3, [(2, 3)])                                     # the largest group does not contain 1
add(8, [(8, 7), (6, 5), (4, 3)])                     # three groups of size 2, answer 3
add(10, relabel(10, path(1, 4) + path(5, 4)))        # two groups of size 4 with random numbers
add(12, rnd_edges(12, 6))
add(30, rnd_edges(30, 20))
add(50, relabel(50, path(1, 50)))
add(200, rnd_edges(200, 120))
add(2000, rnd_edges(2000, 1500))
add(5000, relabel(5000, path(1, 2500) + path(2501, 2500)))
# hidden: large
N = MAXN
add(N, relabel(N, path(1, N)))                       # one long path, random numbers: labels spread slowly
add(N, [(i + 1, i) for i in range(N - 1, 0, -1)])    # path N - (N-1) - ... - 1, listed from the far end
add(N, relabel(N, path(1, N // 2) + path(N // 2 + 1, N // 2)))   # two equal halves
add(N, [(1, i) for i in range(2, N + 1)])            # a star
add(N, [])                                           # nobody has a friend
add(N, rnd_edges(N, MAXM))
add(N, rnd_edges(N, N // 2))                         # many small groups
add(N, relabel(N, [(1, 2)] * MAXM))                  # one pair repeated
edges = []
for s in range(1, N + 1, 50_000):                    # 4 paths of 50 000; the first is cut, 3 tie
    edges += path(s, 50_000)
edges.pop(0)
add(N, relabel(N, edges))
rest = [(150_000 + a, 150_000 + b) for a, b in rnd_edges(50_000, 49_999)]
add(N, relabel(N, path(1, 150_000) + rest))          # a long path and a random part
comb = path(1, N // 2) + [(i, N // 2 + i) for i in range(1, N // 2 + 1)]
add(N, relabel(N, comb))                             # a path with one extra friend at every person
edges = [(a + 100_000, b + 100_000) for a, b in relabel(100_000, path(1, 100_000))]
for s in range(1, 100_001, 1000):                    # many groups of 1000 among 1..100 000
    edges += path(s, 1000)
random.shuffle(edges)
add(N, edges)                                        # the unique largest group is 100 001..200 000

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

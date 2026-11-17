# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(90101)
MAXN = 10 ** 6
MAXK = 200000
tests = []


def add(n, pots):
    pots = list(pots)
    assert 1 <= n <= MAXN
    assert 0 <= len(pots) <= min(2 * n, MAXK)
    assert len(set(pots)) == len(pots)
    assert all(r in (1, 2) and 1 <= c <= n for r, c in pots)
    tests.append(f"{n} {len(pots)}\n" + "".join(f"{r} {c}\n" for r, c in pots))


def rnd(n, k):
    s = set()
    while len(s) < k:
        s.add((random.randint(1, 2), random.randint(1, n)))
    s = sorted(s)
    random.shuffle(s)
    return s


# samples
add(2, [])
add(3, [(1, 2)])
add(1, [(1, 1), (2, 1)])
add(6, [(2, 2), (1, 5)])
add(10, [])
add(8, [(1, 4), (2, 7), (2, 4)])
# hidden: small (every tiling can be listed)
add(1, [])
add(1, [(2, 1)])
add(4, [(1, 1), (2, 4)])
add(7, [(1, c) for c in range(1, 8)])                  # one whole row of pots
add(9, rnd(9, 4))
add(12, rnd(12, 3))
add(5, [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (2, 3), (1, 4), (2, 4), (1, 5), (2, 5)])   # no free cell
# hidden: medium
add(40, [])
add(1000, rnd(1000, 30))
add(5000, [(1 + c % 2, c) for c in range(3, 5000, 7)])
# hidden: large
N = MAXN
add(N, [])
add(N, rnd(N, MAXK))
add(N, rnd(N, 1000))
add(N, [(1 + (c // 5) % 2, c) for c in range(5, 5 * MAXK + 1, 5)])      # a pot every 5 columns, rows alternate
add(N, [(1, c) for c in range(1, MAXK + 1)])                           # a long half-blocked stretch
add(N, [(r, c) for c in range(N // 2 - 50000, N // 2 + 50000) for r in (1, 2)])   # a wall of full columns
add(N, [(2, 1), (1, N)] + [(1 + c % 2, c) for c in range(1000, N, 997)])
add(N, [(r, c) for c in range(3, N, 11) for r in (1, 2)][:MAXK])         # full columns, gaps of 10
add(N - 1, rnd(N - 1, 50))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(10515)
MAXN = 20000
MAXCELLS = 1_500_000
MAXA = 10**9
DIG = "0123456789"
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add_rows(n, m, rows):
    """rows: n strings, each holding m numbers separated by single spaces"""
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and n + m >= 3 and n * m <= MAXCELLS
    assert len(rows) == n
    for r in rows:
        tok = r.split(" ")
        assert len(tok) == m
        assert all(t.isdigit() and (t == "0" or t[0] != "0") and int(t) <= MAXA for t in tok)
    tests.append(f"{n} {m}\n" + "".join(r + "\n" for r in rows))


def add(g):
    add_rows(len(g), len(g[0]), [" ".join(map(str, r)) for r in g])


def rnd(n, m, lo, hi):
    return [[ri(lo, hi) for _ in range(m)] for _ in range(n)]


def const(n, m, v):
    return [[v] * m for _ in range(n)]


def digits(n, m, alphabet=DIG):
    """big grid of one-digit costs drawn from alphabet (fast)"""
    add_rows(n, m, [" ".join(random.choices(alphabet, k=m)) for _ in range(n)])


def const_big(n, m, v):
    row = " ".join([str(v)] * m)
    add_rows(n, m, [row] * n)


# samples
add([[1, 3, 1, 2], [4, 5, 1, 1], [2, 2, 6, 1]])
add([[1, 1, 2], [2, 1, 1]])
add([[5, 0, 7, 2]])
add(const(3, 4, 0))
add(const(4, 2, 9))
add([[0, 2, 3], [1, 9, 0], [1, 1, 4], [5, 0, 0]])
# hidden: small (checked against trying every route)
add([[7], [3]])
add(rnd(5, 5, 0, 1))
add(rnd(6, 7, 0, 9))
add(rnd(8, 8, 0, 2))
add(rnd(7, 9, MAXA - 3, MAXA))
add(const(9, 9, 1))
add([[ri(0, 1) * 5 for _ in range(10)] for _ in range(4)])
add(rnd(10, 10, 0, 1))
# hidden: medium
add(rnd(60, 300, 0, 9))
add(rnd(300, 2, 0, 3))
# hidden: large
digits(150, 10000, "01")
const_big(500, 3000, 0)                     # every route is optimal
const_big(1000, 1000, 7)                    # as many X as possible; which order?
digits(500, 3000, "0001")
add(rnd(MAXN, 1, 0, 9))                     # a single column
add(rnd(1, MAXN, 0, 9))                     # a single row
digits(75, MAXN, "01")                      # very long routes
const_big(MAXN, 75, 0)
digits(100, 15000, "0001")
digits(MAXN, 75, "0123")
add(rnd(520, 520, MAXA - 10**6, MAXA))      # the cost does not fit in 32 bits
g = [random.choices(range(1, 10), k=1000) for _ in range(1000)]   # a cheap zero staircase
for i in range(1000):
    g[i][i] = 0
    if i + 1 < 1000:
        g[i][i + 1] = 0
        g[i + 1][i] = 0
add(g)
add_rows(1000, 1500, [" ".join("01"[(i + j) % 2] for j in range(1500)) for i in range(1000)])   # chessboard
digits(200, 7500, "0000000123")             # mostly zeros

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

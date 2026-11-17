# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10014)
MAXN, MAXRC, MAXV = 100000, 100000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(cells):
    n = len(cells)
    assert 1 <= n <= MAXN
    assert len(set((r, c) for r, c, v in cells)) == n
    assert all(1 <= r <= MAXRC and 1 <= c <= MAXRC and 1 <= v <= MAXV for r, c, v in cells)
    tests.append(f"{n}\n" + "".join(f"{r} {c} {v}\n" for r, c, v in cells))


def scatter(n, rows, cols, vmax):
    """n distinct cells inside rows x cols, random values in 1..vmax"""
    assert n <= rows * cols
    if n * 2 > rows * cols:
        pos = random.sample(range(rows * cols), n)
    else:
        seen = set()
        pos = []
        while len(pos) < n:
            p = ri(0, rows * cols - 1)
            if p not in seen:
                seen.add(p); pos.append(p)
    return [(p // cols + 1, p % cols + 1, ri(1, vmax)) for p in pos]


def dense(k, f):
    return [(i + 1, j + 1, f(i, j)) for i in range(k) for j in range(k)]


# samples
add([(1, 1, 1), (1, 3, 2), (2, 3, 3), (2, 1, 5)])
add([(1, 1, 4), (1, 2, 4), (2, 1, 4), (2, 2, 4)])
add([(1, 1, 1), (1, 2, 2), (2, 1, 2), (2, 2, 3)])
add([(5, 5, 7)])
add([(3, 1, 9), (3, 4, 2), (1, 4, 5), (1, 2, 6), (4, 2, 8), (4, 1, 1), (2, 2, 3)])
# hidden: small (brute.cpp checks these)
add(scatter(10, 4, 4, 5))
add(scatter(30, 6, 6, 10))
add(dense(8, lambda i, j: i + j + 1))
add(scatter(200, 20, 20, 50))
add(scatter(2000, 100, 100, 1000))
add(dense(40, lambda i, j: (i * 7 + j * 3) % 11 + 1))
# hidden: medium (short rows and columns)
add(scatter(30000, MAXRC, MAXRC, MAXV))                      # spread out
add(dense(100, lambda i, j: i + j + 1))                      # number of longest paths is a big binomial
add(dense(100, lambda i, j: 1))                              # all equal: every cell alone
add(dense(100, lambda i, j: ri(1, 3)))
# hidden: maximum size (long rows or columns)
N = MAXN
add(scatter(N, 2, MAXRC, MAXV))                              # two long rows
add(scatter(N, 5, MAXRC, 1000))                              # five rows, many equal values
add([(1 + (k % 2), k // 2 + 1, 1 + k // 2) for k in range(N)])   # two rows, equal values in every column
add([(1 + (k % 2), k // 2 + 1, k // 2 + 1 + k % 2) for k in range(N)])   # big number of longest paths
add([(1, k + 1, 7) for k in range(N)])                       # all equal: every cell alone
add(scatter(N, 3, 40000, 3))
add(scatter(N, 3, MAXRC, 20))                                # three rows, many equal values
add([(1, k + 1, k + 1) for k in range(N)])                   # one row, increasing
add([(k % 3 + 1, k // 3 + 1, MAXV - k) for k in range(N)])
add([(k + 1, 1, ri(1, 50)) for k in range(N)])                # one long column, many equal values
add([(1, k + 1, ri(1, 100)) for k in range(N)])               # one long row, many equal values
add(scatter(N, 2, N // 2, 200))                               # two full rows, many equal values
add([(1, k + 1, ri(1, 3000)) for k in range(N // 2)]
    + [(k + 2, 1, ri(1, 3000)) for k in range(N // 2)])       # one long row and one long column

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

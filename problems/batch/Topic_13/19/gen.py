# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11019)
MAXN, MAXQ, MAXW, MAXC = 100_000, 100_000, 10**9, 1000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(w, cost, ops):
    n, q = len(cost), len(ops)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ and 0 <= w <= MAXW
    ok = lambda c: c == -1 or 1 <= c <= MAXC
    assert all(len(row) == 3 and all(ok(c) for c in row) for row in cost)
    lines = []
    for op in ops:
        if op[0] == "U":
            assert 1 <= op[1] <= n and 1 <= op[2] <= 3 and ok(op[3])
        else:
            assert 1 <= op[1] <= op[2] <= n
        lines.append(" ".join(map(str, op)))
    assert any(op[0] == "Q" for op in ops)
    t = f"{n} {q} {w}\n" + "".join(f"{a} {b} {c}\n" for a, b, c in cost) + "\n".join(lines) + "\n"
    assert len(t) <= 3_000_000
    tests.append(t)


def cell(pclosed, cmax=MAXC):
    return -1 if random.random() < pclosed else ri(1, cmax)


def table(n, pclosed, cmax=MAXC):
    return [[cell(pclosed, cmax) for _ in range(3)] for _ in range(n)]


def rnd_range(n):
    l = ri(1, n)
    return l, ri(l, n)


def wide_range(n, slack):
    return ri(1, min(n, slack)), ri(max(1, n - slack), n)


def ops_of(n, q, pu, rng, pclosed, cmax=MAXC):
    ops = []
    for _ in range(q):
        if random.random() < pu:
            ops.append(("U", ri(1, n), ri(1, 3), cell(pclosed, cmax)))
        else:
            ops.append(("Q",) + rng())
    return ops


def snake_table(n, pclosed, cmax=MAXC, pturn=0.3):
    """a hidden path of open lanes (moving at most one lane per section); other cells closed with pclosed"""
    cost, path, lane = [], [], ri(0, 2)
    for i in range(n):
        if random.random() < pturn:
            lane = max(0, min(2, lane + random.choice((-1, 1))))
        row = [cell(pclosed, cmax) for _ in range(3)]
        row[lane] = ri(1, cmax)
        cost.append(row)
        path.append(lane)
    return cost, path


def snake_ops(n, q, path, pu, rng, pclosed, pbreak, cmax=MAXC):
    """updates keep the hidden path open, except with probability pbreak"""
    ops = []
    for _ in range(q):
        if random.random() < pu:
            i, j = ri(1, n), ri(1, 3)
            if j - 1 == path[i - 1]:
                ops.append(("U", i, j, -1 if random.random() < pbreak else ri(1, cmax)))
            else:
                ops.append(("U", i, j, cell(pclosed, cmax)))
        else:
            ops.append(("Q",) + rng())
    return ops


# samples
add(5, [[3, 9, 9], [8, 2, 9], [7, 7, 1], [1, 6, 5]], [("Q", 1, 4), ("Q", 2, 3), ("U", 3, 2, 1), ("Q", 1, 4)])
add(2, [[1, -1, -1], [-1, -1, 1], [4, 4, 4]], [("Q", 1, 2), ("Q", 2, 3), ("U", 2, 2, 3), ("Q", 1, 3), ("Q", 2, 2)])
add(MAXW, [[1, 1000, 1000], [-1, 1, 1000], [-1, -1, 1]], [("Q", 1, 3)])
add(0, [[-1, -1, -1]], [("Q", 1, 1), ("U", 1, 3, 7), ("Q", 1, 1)])
add(0, [[1, 9, -1], [-1, 9, 1]], [("Q", 1, 2)])
add(10, [[5, 1, 5], [1, 5, 5], [5, 5, 1], [5, 1, 5], [1, 5, 1]],
    [("Q", 1, 5), ("U", 4, 2, -1), ("Q", 1, 5), ("Q", 3, 4), ("U", 2, 1, 50), ("Q", 1, 2)])
# hidden: small
add(3, [[2, 5, -1]], [("Q", 1, 1), ("U", 1, 1, -1), ("Q", 1, 1), ("U", 1, 2, -1), ("Q", 1, 1)])
add(1, table(8, 0.4, 10), ops_of(8, 30, 0.3, lambda: rnd_range(8), 0.4, 10))
add(0, table(30, 0.3, 5), ops_of(30, 100, 0.3, lambda: rnd_range(30), 0.3, 5))
add(MAXW, table(100, 0.25), ops_of(100, 300, 0.4, lambda: rnd_range(100), 0.25))
add(37, table(2000, 0.2), ops_of(2000, 2000, 0.3, lambda: rnd_range(2000), 0.2))
add(500, table(2000, 0.45), ops_of(2000, 2000, 0.5, lambda: rnd_range(2000), 0.45))
# hidden: maximum size
N, Q = MAXN, MAXQ
add(300, table(N, 0.0), ops_of(N, Q, 0.3, lambda: wide_range(N, 99), 0.0))
c, p = snake_table(N, 0.2)
add(MAXW, c, snake_ops(N, Q, p, 0.3, lambda: wide_range(N, 99), 0.2, 0.0005))        # costly lane changes
c, p = snake_table(N, 0.5)
add(150, c, snake_ops(N, Q, p, 0.4, lambda: wide_range(N, 9999), 0.5, 0.0002))       # many closures
c, p = snake_table(N, 1.0, MAXC, 0.2)                                               # exactly one open lane
add(MAXW, c, snake_ops(N, Q, p, 0.2, lambda: wide_range(N, 999), 1.0, 0.00005))
alt = [[ri(1, 9), MAXC, -1] if i % 2 else [-1, MAXC, ri(1, 9)] for i in range(N)]    # lane 1 and 3 never meet
add(0, alt, ops_of(N, Q, 0.1, lambda: wide_range(N, 99), 0.0, 9))
c, p = snake_table(N, 0.3)
add(0, c, snake_ops(N, Q, p, 0.3, lambda: wide_range(N, 99), 0.3, 0.0003))
add(MAXW, [[MAXC] * 3 for _ in range(N)], ops_of(N, Q, 0.2, lambda: wide_range(N, 9), 0.0))
c, p = snake_table(N, 0.15)
add(70, c, snake_ops(N, Q, p, 0.5, lambda: rnd_range(N), 0.15, 0.001))
add(10**6, table(N, 0.2), ops_of(N, Q, 0.3, lambda: (lambda i: (i, i))(ri(1, N)), 0.3))  # single sections
c, p = snake_table(N, 0.3, 50)
add(999, c, snake_ops(N, Q, p, 0.1, lambda: (1, N), 0.3, 0.0, 50))                   # always the whole road
c, p = snake_table(N, 0.1)
add(25, c, snake_ops(N, Q, p, 0.4, lambda: wide_range(N, 30000), 0.7, 0.003))         # closing and reopening
c, p = snake_table(N, 0.33, MAXC, 0.05)
add(MAXW, c, snake_ops(N, Q, p, 0.3, lambda: wide_range(N, 99), 0.33, 0.0))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

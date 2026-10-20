# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1102)
MAXRC, MAXQ, MAXA, MAXK = 500, 100_000, 100_000, 1000
tests = []

def add(g, qs):
    R, C, q = len(g), len(g[0]), len(qs)
    assert 1 <= R <= MAXRC and 1 <= C <= MAXRC and 1 <= q <= MAXQ
    assert all(len(row) == C and all(0 <= v <= MAXA for v in row) for row in g)
    assert all(1 <= r <= R and 1 <= c <= C and 0 <= k <= MAXK for r, c, k in qs)
    lines = [f"{R} {C} {q}"] + [" ".join(map(str, row)) for row in g] + [f"{r} {c} {k}" for r, c, k in qs]
    tests.append("\n".join(lines) + "\n")

def grid(R, C, lo, hi):
    return [[random.randint(lo, hi) for _ in range(C)] for _ in range(R)]

def queries(R, C, q, kmode):
    qs = []
    for _ in range(q):
        r, c = random.randint(1, R), random.randint(1, C)
        if kmode == "big":
            k = random.randint(max(R, C) // 2, MAXK)
        elif kmode == "mid":
            k = random.randint(max(R, C) // 4, max(R, C))
        else:
            k = random.randint(0, min(MAXK, max(R, C) + 2))
        qs.append((r, c, k))
    return qs

# samples
add([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [(2, 2, 1), (1, 4, 1), (3, 1, 0)])
add([[5, 0], [2, 7]], [(1, 1, 5), (2, 1, 0)])
add([[100000]], [(1, 1, 0), (1, 1, 1000)])
add([[3, 1, 4, 1, 5, 9, 2]], [(1, 4, 2), (1, 1, 3), (1, 7, 1)])
add([[0, 1, 0], [1, 2, 1], [0, 1, 0], [4, 4, 4]], [(2, 2, 1), (4, 3, 1), (3, 2, 2)])
# hidden: small
add([[0]], [(1, 1, 0)])
add(grid(6, 1, 0, 9), queries(6, 1, 20, "any"))
add(grid(7, 9, 0, 20), queries(7, 9, 60, "any"))
add(grid(30, 25, 0, 1000), queries(30, 25, 300, "any"))
add(grid(80, 100, 0, MAXA), queries(80, 100, 1000, "any"))
add([[MAXA] * 120 for _ in range(120)], queries(120, 120, 3000, "mid"))
add(grid(100, 1, 0, MAXA), queries(100, 1, 5000, "any"))
add([[0] * 50 for _ in range(50)], queries(50, 50, 500, "any"))
# hidden: maximum size
add(grid(MAXRC, MAXRC, 0, MAXA), queries(MAXRC, MAXRC, MAXQ, "big"))
add([[MAXA] * MAXRC for _ in range(MAXRC)], queries(MAXRC, MAXRC, MAXQ, "big"))
add(grid(MAXRC, MAXRC, MAXA - 10, MAXA), queries(MAXRC, MAXRC, MAXQ, "mid"))
add(grid(MAXRC, MAXRC, 0, MAXA), queries(MAXRC, MAXRC, MAXQ, "any"))
add(grid(MAXRC, MAXRC, 0, 9), [(MAXRC // 2, MAXRC // 2, MAXK)] * MAXQ)
add(grid(MAXRC, 300, 0, MAXA), queries(MAXRC, 300, MAXQ, "big"))
add(grid(1, MAXRC, 0, MAXA), queries(1, MAXRC, MAXQ, "mid"))
add(grid(MAXRC, MAXRC, 0, MAXA), [(random.choice([1, MAXRC]), random.choice([1, MAXRC]), random.randint(MAXRC - 2, MAXRC)) for _ in range(MAXQ)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

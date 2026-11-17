# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30101)
MAXN, MAXQ, MAXA = 100_000, 50_000, 10_000
tests = []


def add(a, b, qs):
    n, m, q = len(a), len(b), len(qs)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 1 <= q <= MAXQ
    assert all(-MAXA <= x <= MAXA for x in a + b)
    assert all(1 <= r1 <= r2 <= n and 1 <= c1 <= c2 <= m for r1, c1, r2, c2 in qs)
    lines = [f"{n} {m} {q}", " ".join(map(str, a)), " ".join(map(str, b))]
    lines += [f"{r1} {c1} {r2} {c2}" for r1, c1, r2, c2 in qs]
    tests.append("\n".join(lines) + "\n")


def rng(n, mode):
    if mode == "long":
        lo = random.randint(1, max(1, n // 20))
        hi = random.randint(n - n // 20, n)
        return lo, max(lo, hi)
    if mode == "point":
        x = random.randint(1, n)
        return x, x
    x, y = random.randint(1, n), random.randint(1, n)
    return min(x, y), max(x, y)


def queries(n, m, q, mode):
    out = []
    for _ in range(q):
        md = mode if mode != "mix" else random.choice(["long"] * 6 + ["any", "point"])
        r1, r2 = rng(n, md)
        c1, c2 = rng(m, md)
        out.append((r1, c1, r2, c2))
    return out


def vals(k, lo=-MAXA, hi=MAXA):
    return [random.randint(lo, hi) for _ in range(k)]


add([1, 2, 3], [1, -1, 2, 0], [(1, 1, 2, 3), (2, 3, 3, 4), (1, 1, 3, 4)])
add([-2, 5], [3, 4, -1], [(2, 2, 2, 3), (1, 1, 2, 1), (1, 2, 1, 2)])
add([7], [-6], [(1, 1, 1, 1)])
add([MAXA] * 4, [-MAXA] * 5, [(1, 1, 4, 5), (2, 3, 3, 3)])
add([3, -3, 1, 0, 2], [2, 2, -5], [(1, 1, 2, 3), (3, 1, 5, 3), (4, 2, 4, 3), (1, 3, 5, 3)])

add([0, 0], [5, -5], [(1, 1, 2, 2), (1, 2, 1, 2)])
add(vals(10, -9, 9), vals(12, -9, 9), queries(10, 12, 40, "any"))
add(vals(50), vals(40), queries(50, 40, 200, "mix"))
add(vals(300), vals(1), queries(300, 1, 300, "any"))
add(vals(1), vals(300), queries(1, 300, 300, "any"))
add([MAXA] * 400, [MAXA] * 400, queries(400, 400, 500, "long"))
add(vals(2000, -MAXA, -MAXA + 50), vals(1500, MAXA - 50, MAXA), queries(2000, 1500, 2000, "mix"))

add(vals(MAXN), vals(MAXN), queries(MAXN, MAXN, MAXQ, "long"))
add([MAXA] * MAXN, [MAXA] * MAXN, queries(MAXN, MAXN, MAXQ, "long"))
add([-MAXA] * MAXN, [MAXA] * MAXN, queries(MAXN, MAXN, MAXQ, "long"))
add(vals(MAXN, 0, MAXA), vals(MAXN, -MAXA, 0), queries(MAXN, MAXN, MAXQ, "mix"))
add(vals(MAXN), vals(MAXN), [(1, 1, MAXN, MAXN)] * MAXQ)
add(vals(MAXN, MAXA - 100, MAXA), vals(MAXN, -MAXA, -MAXA + 100), queries(MAXN, MAXN, MAXQ, "long"))
add([random.choice([-MAXA, MAXA]) for _ in range(MAXN)], vals(MAXN, 9000, MAXA), queries(MAXN, MAXN, MAXQ, "long"))
add(vals(MAXN, -3, 3), vals(MAXN, -3, 3), queries(MAXN, MAXN, MAXQ, "long"))
add(vals(MAXN, MAXA - 10, MAXA), vals(MAXN, MAXA - 10, MAXA), queries(MAXN, MAXN, MAXQ, "mix"))
add([MAXA if i % 2 else -MAXA for i in range(MAXN)], [MAXA] * MAXN, queries(MAXN, MAXN, MAXQ, "long"))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

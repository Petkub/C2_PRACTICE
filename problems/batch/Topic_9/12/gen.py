# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(131201)
MAXN = 30
MAXQ = 100000
tests = []


def add(n, qs):
    assert 1 <= n <= MAXN and 1 <= len(qs) <= MAXQ
    side = 1 << n
    for q in qs:
        if q[0] == 1:
            assert len(q) == 2 and 0 <= q[1] < side * side
        else:
            assert q[0] == 2 and len(q) == 3 and 0 <= q[1] < side and 0 <= q[2] < side
    tests.append(f"{n} {len(qs)}\n" + "".join(" ".join(map(str, q)) + "\n" for q in qs))


def rq(n, p1=0.5):
    side = 1 << n
    if random.random() < p1:
        return (1, random.randrange(side * side))
    return (2, random.randrange(side), random.randrange(side))


def edge_q(n):
    """steps next to the borders of the quadrants of every level, cells on borders and diagonals"""
    side = 1 << n
    k = random.randint(0, n - 1)
    r = random.random()
    if r < 0.4:
        d = random.randint(0, 3) * 4**k + random.choice((-1, 0, 1)) + random.randrange(side * side // 4**(k + 1) or 1) * 4**(k + 1)
        return (1, min(max(d, 0), side * side - 1))
    s = 1 << k
    x = random.randrange(side) // (2 * s) * (2 * s) + random.choice((s - 1, s, 0, 2 * s - 1))
    if r < 0.7:
        y = random.choice((x, side - 1 - x, 0, side - 1, random.randrange(side)))
    else:
        y = random.randrange(side) // (2 * s) * (2 * s) + random.choice((s - 1, s))
    return (2, min(x, side - 1), min(y, side - 1))


# samples
add(2, [(1, 6), (1, 13), (2, 3, 3), (2, 0, 2)])
add(1, [(1, 3), (2, 0, 1), (2, 1, 1)])
add(3, [(1, 21), (2, 4, 3), (2, 7, 0)])
add(30, [(1, 5), (2, 0, 2**30 - 1), (2, 2**30 - 1, 0)])
add(5, [(1, 500), (2, 31, 16), (1, 1023)])
# hidden: small (the brute force walks the whole curve)
add(1, [(1, d) for d in range(4)] + [(2, x, y) for x in range(2) for y in range(2)])
add(3, [(1, d) for d in range(64)] + [(2, x, y) for x in range(8) for y in range(8)])
add(4, [(1, d) for d in range(256)][::-1] + [(2, x, y) for y in range(16) for x in range(16)])
add(7, [rq(7) for _ in range(3000)])
add(9, [edge_q(9) for _ in range(5000)])
add(11, [rq(11) for _ in range(20000)])
# hidden: large
add(30, [rq(30) for _ in range(MAXQ)])
add(30, [rq(30, 1.0) for _ in range(MAXQ)])
add(30, [rq(30, 0.0) for _ in range(MAXQ)])
add(30, [edge_q(30) for _ in range(MAXQ)])
add(29, [rq(29) for _ in range(MAXQ)])
add(25, [edge_q(25) for _ in range(MAXQ)])
add(20, [rq(20) for _ in range(MAXQ)])
add(16, [rq(16) for _ in range(MAXQ)])
add(14, [rq(14) for _ in range(MAXQ)])
add(30, [(1, 4**30 - 1 - i) for i in range(MAXQ // 2)] + [(2, 2**30 - 1 - i, i) for i in range(MAXQ // 2)])
add(28, [(2, x, x) for x in random.sample(range(2**28), MAXQ)])
add(30, [(1, random.randrange(4**15)) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47003)
MAXN, MAXV, MAXX = 200_000, 10_000, 5 * 10**18
tests = []


def add(x, a, b):
    n, m = len(a), len(b)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 1 <= x <= MAXX
    assert all(1 <= v <= MAXV for v in a + b)
    tests.append(f"{n} {m} {x}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n")


def vals(n, kind):
    if kind == "uni":
        return [random.randint(1, MAXV) for _ in range(n)]
    if kind == "small":
        return [random.randint(1, 20) for _ in range(n)]
    if kind == "skew":
        return [MAXV - random.randint(0, 50) if random.random() < 0.05 else random.randint(1, 30) for _ in range(n)]
    if kind == "log":
        return [max(1, int(MAXV ** random.random())) for _ in range(n)]
    return [MAXV] * n


add(10000, [40, 25, 70, 72, 30], [50, 35, 48, 12])
add(1000000, [10, 20, 30], [40, 50, 60])
add(1, [5, 7], [3, 4])
add(170, [90, 80, 3, 2], [1, 1, 2])
add(100000, [12, 300, 7, 45, 9, 120], [33, 3, 250, 18, 60, 2])

add(22, [10, 10], [1])
add(4, [1], [1])
add(5, [1], [1])

for n, m, ka, kb, x in [(6, 7, "small", "small", 2633), (8, 5, "skew", "small", 1848), (9, 9, "log", "log", 13777344)]:
    a, b = vals(n, ka), vals(m, kb)
    random.randint(1, 9)
    add(x, a, b)
add(84063595, vals(300, "skew"), vals(200, "small"))
add(11036641400144, vals(2000, "uni"), vals(1500, "log"))
add(2000000004, vals(50_000, "max"), vals(1, "small"))

for ka, kb, x in [("uni", "uni", 500060851886181075), ("uni", "uni", 989051480060808522),
                  ("skew", "small", 141628538626816), ("small", "skew", 195707279218770),
                  ("log", "uni", 65437516455971818), ("log", "log", 37572577664300268),
                  ("skew", "skew", 10492414412966806), ("uni", "small", 1991672496963932)]:
    add(x, vals(MAXN, ka), vals(MAXN, kb))
add(4000000004000000001, vals(MAXN, "max"), vals(MAXN, "max"))
add(1001744440209669625, vals(MAXN, "uni"), vals(MAXN, "uni"))
add(MAXX, vals(MAXN, "skew"), vals(MAXN, "uni"))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

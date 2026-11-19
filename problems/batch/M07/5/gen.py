# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(47005)
MAXN, MAXM = 10**9, 200_000
tests = []


def add(n, people):
    m = len(people)
    assert 1 <= m <= n <= MAXN and m <= MAXM
    assert all(d in "LR" and isinstance(c, int) and 1 <= c <= n for d, c in people)
    assert len({c for _, c in people}) == m
    tests.append(f"{n} {m}\n" + "".join(f"{d} {c}\n" for d, c in people))


def shuffled_add(n, people):
    random.shuffle(people)
    add(n, people)


def rnd(n, m):
    seats = random.sample(range(1, n + 1), m)
    return [(random.choice("LR"), c) for c in seats]


def runs(n, m, run_lo, run_hi, fill, first=None, unequal=False):
    sizes, d, total = [], first or random.choice("LR"), 0
    while total < m:
        k = random.randint(run_lo, run_hi)
        if unequal and d == "L":
            k = max(1, k // 3) if random.random() < 0.5 else k * 2
        k = min(k, m - total)
        sizes.append((d, k))
        total += k
        d = "L" if d == "R" else "R"
    inner = [1 + (random.random() < 0.3) for _ in range(m)]
    free = int((n - sum(inner)) * fill)
    w = [random.randint(1, 10**6) for _ in range(len(sizes))]
    total_w = sum(w)
    gaps = [free * x // total_w for x in w]
    people, pos, k = [], 0, 0
    for (d, cnt), g in zip(sizes, gaps):
        pos += g
        for _ in range(cnt):
            pos += inner[k]
            k += 1
            people.append((d, pos))
    assert people[-1][1] <= n
    return people


add(10, [("L", 3), ("R", 4), ("L", 7), ("R", 9)])
add(5, [("L", 1), ("R", 3), ("L", 4), ("R", 5)])
add(10**9, [("R", 1)])
add(15, [("L", 9), ("R", 4), ("L", 12), ("R", 2)])
add(9, [("L", 5), ("R", 6), ("R", 1), ("L", 3)])

add(1, [("L", 1)])
add(12, [("R", 3), ("L", 10)])
add(12, [("R", 1), ("R", 2), ("R", 3), ("L", 10)])
add(13, [("R", 4), ("L", 9), ("L", 10), ("L", 12)])
add(14, [("L", 2), ("R", 5), ("R", 6), ("L", 11), ("R", 12), ("L", 14)])
for n, m in [(10, 4), (12, 6), (14, 5), (14, 9)]:
    shuffled_add(n, rnd(n, m))

shuffled_add(300, runs(300, 60, 1, 6, 0.8, unequal=True))
shuffled_add(5000, runs(5000, 400, 1, 20, 0.8, unequal=True))

shuffled_add(MAXN, runs(MAXN, MAXM, 20, 200, 0.9, unequal=True))
shuffled_add(MAXN, runs(MAXN, MAXM, 5, 60, 0.9, unequal=True))
shuffled_add(MAXN, runs(MAXN, MAXM, 50000, 50000, 0.9, first="R", unequal=True))
shuffled_add(MAXN, runs(MAXN, MAXM, 1000, 30000, 0.95, first="L"))
shuffled_add(MAXN, runs(MAXN, MAXM, 100, 100, 0.9, first="R"))
shuffled_add(MAXN, [("R", c) for c in random.sample(range(1, 3 * 10**8), MAXM // 2)] +
             [("L", c) for c in random.sample(range(7 * 10**8, MAXN + 1), MAXM // 2)])
shuffled_add(MAXN, [("R", c) for c in range(1, MAXM // 4 + 1)] +
             [("L", MAXN - k) for k in range(3 * MAXM // 4)])
shuffled_add(MAXN, [("R", 1)] + [("L", c) for c in random.sample(range(MAXN // 2, MAXN + 1), MAXM - 1)])
shuffled_add(MAXN, runs(MAXN, MAXM, 2, 40, 0.5, unequal=True))
shuffled_add(MAXN, runs(MAXN, MAXM, 200, 3000, 0.97, first="R", unequal=True))
shuffled_add(MAXN, [("R", c) for c in range(1, MAXM // 2 + 1)] + [("L", MAXN - k) for k in range(MAXM // 2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

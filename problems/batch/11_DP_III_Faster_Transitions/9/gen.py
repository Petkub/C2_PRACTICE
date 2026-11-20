# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(110009)
MAXN = 200000
MAXC = 5
MAXA = 10 ** 9
tests = []


def add(k, c, col, a):
    n = len(col)
    assert 1 <= n <= MAXN and 1 <= k <= n and 1 <= c <= MAXC
    assert len(a) == n and all(1 <= x <= c for x in col) and all(0 <= x <= MAXA for x in a)
    tests.append(f"{n} {k} {c}\n" + " ".join(map(str, col)) + "\n" + " ".join(map(str, a)) + "\n")


def runs(n, c, mean_run):
    col = []
    while len(col) < n:
        e = random.randint(1, c)
        if col and e == col[-1]:
            continue
        col += [e] * random.randint(1, 2 * mean_run - 1)
    return col[:n]


def gems(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def falling(n):
    return [max(0, MAXA - i * (MAXA // n) - random.randint(0, MAXA // n * 3)) for i in range(n)]


add(2, 3, [3, 1, 1, 2, 2, 3, 2, 3], [9, 5, 5, 9, 9, 7, 8, 6])
add(1, 2, [1, 2, 2, 1], [4, 6, 6, 4])
add(1, 1, [1], [7])
add(3, 3, [2, 2, 2, 1, 2, 1, 2], [3, 8, 4, 8, 9, 6, 3])
add(2, 2, [2, 2, 1, 2, 2, 1], [2, 2, 5, 2, 2, 5])

add(1, 1, [1, 1], [1, 1])
for n, k, c, mr in [(2, 1, 2, 1), (6, 2, 2, 2), (9, 3, 3, 2), (12, 4, 2, 3), (15, 5, 4, 3), (18, 6, 3, 4), (18, 17, 5, 2)]:
    add(k, c, runs(n, c, mr), gems(n, 0, 30))

add(60, 3, runs(3000, 3, 20), falling(3000))
add(200, 5, runs(5000, 5, 60), gems(5000, 0, MAXA))

add(60000, 3, runs(MAXN, 3, 9000), falling(MAXN))
add(100000, 2, runs(MAXN, 2, 15000), falling(MAXN))
add(50000, 5, runs(MAXN, 5, 4000), gems(MAXN, 0, MAXA))
add(80000, 4, runs(MAXN, 4, 30000), falling(MAXN))
add(MAXN - 1, 5, runs(MAXN, 5, 2), gems(MAXN, 0, MAXA))
add(30000, 2, runs(MAXN, 2, 20000), gems(MAXN, 0, 1000))
add(70000, 5, [random.randint(1, 5) for _ in range(MAXN)], falling(MAXN))
add(40000, 3, runs(MAXN, 3, 25000), [MAXA] * MAXN)
col = runs(MAXN, 3, 5000)
for i in range(60000, 60000 + 2 * 40000 + 5):
    col[i] = 1
col[59999] = 2
col[60000 + 80005] = 3
add(40000, 3, col, gems(MAXN, 0, 999))
add(90000, 2, runs(MAXN, 2, 40000), falling(MAXN))
add(25000, 4, runs(MAXN, 4, 3000), falling(MAXN))
add(120000, 3, runs(MAXN, 3, 50000), gems(MAXN, 0, MAXA))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

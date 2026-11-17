# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(30610)
MAXNM, MAXA = 700, 9999
tests = []

def add(a, K):
    n, m = len(a), len(a[0])
    assert 1 <= n <= MAXNM and 1 <= m <= MAXNM and 1 <= K <= min(n, m)
    assert all(len(row) == m and all(0 <= x <= MAXA for x in row) for row in a)
    tests.append(f"{n} {m} {K}\n" + "\n".join(" ".join(map(str, row)) for row in a) + "\n")

def additive(n, m, lo=0, hi=MAXA):
    half = (hi - lo) // 2
    R = [random.randint(0, half) for _ in range(n)]
    C = [random.randint(0, half) for _ in range(m)]
    return [[lo + R[i] + C[j] for j in range(m)] for i in range(n)]

def spoil(a, cells):
    for i, j in cells:
        v = a[i][j]
        while a[i][j] == v:
            a[i][j] = min(MAXA, max(0, v + random.choice([-1, 1]) * random.randint(1, 5)))
    return a

def spots(n, m, k, r0=0, r1=None, c0=0, c1=None):
    r1 = n if r1 is None else r1
    c1 = m if c1 is None else c1
    return [(random.randrange(r0, r1), random.randrange(c0, c1)) for _ in range(k)]


add([[6, 7, 3, 6], [3, 2, 0, 3], [6, 7, 3, 6]], 2)
add([[3, 5, 1, 3], [5, 7, 3, 5], [3, 8, 4, 6]], 3)
add([[1, 2, 3], [4, 5, 6]], 1)
add([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 8]], 4)
add([[0, 2, 2, 5, 2], [2, 0, 0, 3, 0], [4, 2, 2, 5, 2], [4, 2, 2, 5, 2]], 2)

add([[7]], 1)
add([[1, 2], [3, 5]], 2)
add(additive(6, 6, 0, 20), 6)
add(spoil(additive(8, 9, 0, 30), spots(8, 9, 2)), 3)
add([[random.randint(0, 2) for _ in range(10)] for _ in range(7)], 2)
add(spoil(additive(12, 10, 0, 50), spots(12, 10, 3)), 5)
add(spoil(additive(9, 9, 0, 40), spots(9, 9, 1)), 6)
add(spoil(additive(40, 60), spots(40, 60, 6)), 12)
add(spoil(additive(150, 120), spots(150, 120, 15)), 40)
add(spoil(additive(1, 300), [(0, 5)]), 1)

n = m = MAXNM
add(spoil(additive(n, m), spots(n, m, 40, 0, 120, 0, 120)), 300)
add(spoil(additive(n, m), spots(n, m, 30, 500, 700, 0, 700)), 250)
add(spoil(additive(n, m), spots(n, m, 25, 300, 400, 300, 400)), 200)
add(additive(n, m), 350)
add(spoil(additive(n, m), [(random.randrange(n), 699 - random.randrange(3)) for _ in range(20)]), 400)
add(spoil(additive(n, m), spots(n, m, 60, 0, 700, 200, 230)), 230)
add(spoil(additive(n, m), [(i, i) for i in range(0, 700, 37)]), 180)
add(spoil(additive(n, 690), spots(n, 690, 3)), 333)
add(spoil(additive(690, m), spots(690, m, 50, 600, 690, 600, 700)), 450)
add(spoil(additive(n, m), spots(n, m, 5)), 280)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

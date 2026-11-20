# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(460004)
MAXN = 50000
MAXK = 100
MAXG = 10 ** 6
tests = []


def add(k, g):
    n = len(g)
    assert 1 <= n <= MAXN and 0 <= k <= MAXK
    assert all(len(row) == 3 and all(0 <= x <= MAXG for x in row) for row in g)
    tests.append(f"{n} {k}\n" + "".join(f"{x} {y} {z}\n" for x, y, z in g))


def rnd(n, lo=0, hi=MAXG):
    return [[random.randint(lo, hi) for _ in range(3)] for _ in range(n)]


def blocks(n, lo, hi, base, noise):
    g = []
    while len(g) < n:
        c = random.randrange(3)
        for _ in range(random.randint(lo, hi)):
            row = [random.randint(0, noise) for _ in range(3)]
            row[c] = base + random.randint(0, noise)
            g.append(row)
    return g[:n]


add(1, [[8, 4, 1], [9, 5, 1], [5, 8, 4], [2, 9, 7], [6, 8, 9]])
add(2, [[9, 1, 8], [2, 5, 0], [1, 8, 4], [2, 9, 8], [6, 2, 3], [5, 2, 3], [2, 2, 0]])
add(1, [[4, 8, 1], [1, 0, 0], [4, 5, 7], [7, 2, 1], [8, 5, 1], [8, 2, 2]])
add(0, [[5, 1, 1], [5, 9, 1], [5, 1, 1]])
add(3, [[4, 7, 2]])

add(0, [[0, 0, 0]])
add(1, [[3, 0, 0], [0, 0, 9]])
add(2, rnd(10, 0, 9))
add(3, rnd(12, 0, 20))
add(1, [[5, 0, 0], [0, 6, 0], [0, 0, 7], [5, 0, 0], [0, 6, 0], [0, 0, 7], [5, 0, 0], [0, 6, 0], [0, 0, 7]])
add(4, blocks(12, 2, 4, 50, 10))

add(20, rnd(2000, 0, 1000))
add(50, blocks(3000, 5, 60, MAXG // 2, MAXG // 4))
add(7, [[MAXG if t % 3 == c else 0 for c in range(3)] for t in range(2500)])
add(0, [[random.randint(MAXG // 2, MAXG) if c == t * 3 // 3000 else random.randint(0, MAXG * 2 // 3)
         for c in range(3)] for t in range(3000)])

add(MAXK, rnd(MAXN))
add(MAXK, [[MAXG] * 3 for _ in range(MAXN)])
add(MAXK, blocks(MAXN, 100, 300, MAXG // 2, MAXG // 3))
add(MAXK, blocks(MAXN, 1, 40, MAXG - 1000, 1000))
add(2, [[random.randint(MAXG // 2, MAXG) if c == t * 3 // MAXN else random.randint(0, MAXG * 2 // 3)
         for c in range(3)] for t in range(MAXN)])
add(1, [[random.randint(MAXG // 2, MAXG) if c == (t * 4 // MAXN) % 3 else random.randint(0, MAXG // 2)
         for c in range(3)] for t in range(MAXN)])
add(MAXK, [[MAXG if t % 3 == c else 0 for c in range(3)] for t in range(MAXN)])
add(MAXK, [[random.randint(0, MAXG) if (t // 150) % 2 == 0 else 0, random.randint(0, MAXG) if (t // 150) % 2 else 0,
            MAXG * 2 // 5] for t in range(MAXN)])
add(MAXK, rnd(MAXN, 0, 10))
add(MAXK, [[random.randint(0, 5) * (MAXG // 5) if random.random() < 0.05 else 0 for c in range(3)]
           for t in range(MAXN)])
add(37, rnd(MAXN, MAXG // 2, MAXG))
add(MAXK, [[MAXG - random.randint(0, 3) for _ in range(3)] for t in range(MAXN)])
add(80, blocks(MAXN, 20, 600, MAXG // 4, MAXG // 4))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90016)
MAXCELLS = 500000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(g):
    r, c = len(g), len(g[0])
    assert r >= 1 and c >= 1 and r * c <= MAXCELLS
    assert all(len(row) == c and -1000 <= min(row) and max(row) <= 1000 for row in g)
    tests.append(f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))


def rnd(r, c, lo=-1000, hi=1000):
    flat = random.choices(range(lo, hi + 1), k=r * c)
    return [flat[i * c:(i + 1) * c] for i in range(r)]


def zigzag(r, c):
    g = []
    for i in range(r):
        k = max(1, c // 10)
        left = random.choices(range(300, 1001), k=k)
        mid = random.choices(range(-150, 51), k=max(0, c - 2 * k))
        right = random.choices(range(300, 1001), k=c - k - len(mid))
        g.append(left + mid + right)
    return g


def bands(r, c):
    g = rnd(r, c, -1000, 300)
    for row in g:
        a = ri(0, c - 1); b = ri(a, min(c - 1, a + c // 3))
        row[a:b + 1] = random.choices(range(0, 1001), k=b - a + 1)
    return g


add([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
add([[-5, 9, -1, 9], [9, -1, 9, -5], [-9, -9, -9, -9]])
add([[3, -4, 2, -1, 5]])
add([[2], [-3], [4], [-1]])
add([[0, -1, 7, -2, 3], [6, 2, -5, 4, -6], [-1, -9, 8, 1, 2]])

add([[-2, 6, -1], [4, -8, 3], [5, 1, -7], [-3, 2, 2]])
add([[7]])
add([[-1000]])
add(rnd(2, 2))
add(rnd(6, 7))
add(rnd(8, 8, -10, 10))
add(zigzag(9, 12))
add(rnd(1, 40))
add(rnd(40, 1))
add(bands(60, 60))
add(rnd(1, 30000))
add(rnd(30000, 1))

add(rnd(5, 100000))
add(zigzag(4, 125000))
add(bands(2, 250000))
add(rnd(2, 250000))
add(zigzag(10, 50000))
add(bands(20, 25000))
add([[-1000] * 100000 for _ in range(5)])
add([[1000] * 50000 for _ in range(10)])
add(rnd(40, 12500))
add(zigzag(25, 20000))
add(zigzag(3, 166666))
add(bands(50, 10000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

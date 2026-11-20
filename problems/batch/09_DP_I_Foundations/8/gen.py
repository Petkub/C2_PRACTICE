# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(90008)
MAXN = 2000
MAXV = 10 ** 9
tests = []


def add(x, rows):
    n = len(rows)
    assert 1 <= n <= MAXN and 0 <= x <= n
    for r in rows:
        assert len(r) == 3 and max(r) >= 0
        assert all(v == -1 or 0 <= v <= MAXV for v in r)
    tests.append(f"{n} {x}\n" + "".join(f"{r[0]} {r[1]} {r[2]}\n" for r in rows))


def day(lo_f, hi_f, lo_v, hi_v, lo_p, hi_p, miss=0.0):
    while True:
        r = [random.randint(lo_f, hi_f), random.randint(lo_v, hi_v), random.randint(lo_p, hi_p)]
        r = [-1 if random.random() < miss else v for v in r]
        if max(r) >= 0:
            return r


def small(n, miss):
    return [day(0, 20, 0, 20, 0, 20, miss) for _ in range(n)]


def fried_heavy(n, miss=0.0):
    return [day(6 * 10 ** 8, MAXV, 0, 3 * 10 ** 8, 3 * 10 ** 8, 7 * 10 ** 8, miss) for _ in range(n)]


def close(n, miss=0.0):
    out = []
    for _ in range(n):
        base = random.randint(4 * 10 ** 8, 6 * 10 ** 8)
        out.append(day(base, base + 400, base - 300, base + 100, base - 200, base + 300, miss))
    return out


def no_soup(n):
    return [[random.randint(5 * 10 ** 8, MAXV), random.randint(0, 5 * 10 ** 8), -1] for _ in range(n)]


add(3, [[5, 9, 9], [9, 6, 2], [6, 12, 10], [11, 1, 5], [6, 9, 12], [11, 5, 8]])
add(2, [[5, -1, 1], [4, 3, -1], [6, -1, 2], [7, -1, -1]])
add(0, [[9, 1, 2], [9, 1, 3], [9, 1, 1], [9, 1, 2], [9, 1, 5], [9, 1, 1], [9, 1, 2]])
add(1, [[5, 7, 9]])
add(3, [[9, 2, 9], [9, 6, 9], [9, 4, 9]])
add(3, [[3, 12, 1], [2, 10, 9], [7, 1, 4], [12, 10, 6], [5, -1, 11], [7, -1, 1], [11, 1, 8]])

add(2, [[10, 4, 3], [10, 5, 2], [10, 3, 6], [10, 6, 1], [10, 2, 5], [10, 5, 4]])
for n, miss in [(1, 0.3), (8, 0.0), (12, 0.25), (14, 0.15)]:
    add(random.randint(0, n), small(n, miss))
add(3, [[7, -1, -1], [8, -1, -1], [6, 2, -1]])
add(0, [[3, -1, -1], [3, -1, -1], [3, -1, -1], [3, 1, 1]])

add(70, close(150, 0.1))
add(55, no_soup(200))

add(700, fried_heavy(MAXN))
add(1000, fried_heavy(MAXN, 0.05))
add(1300, close(MAXN))
add(500, close(MAXN, 0.15))
add(900, no_soup(MAXN))
add(1000, [[MAXV, MAXV, MAXV] for _ in range(MAXN)])
add(MAXN, [[MAXV, MAXV, MAXV] for _ in range(MAXN)])
add(0, fried_heavy(MAXN))
add(400, [day(0, MAXV, 0, MAXV, 0, MAXV, 0.1) for _ in range(MAXN)])
rows = fried_heavy(MAXN)
veg_days = set(random.sample(range(MAXN), 599))
for i, r in enumerate(rows):
    if i not in veg_days:
        r[1] = -1
add(600, rows)
rows = fried_heavy(MAXN)
for i in (1234, 1235, 1236):
    rows[i] = [rows[i][0], -1, -1]
add(300, rows)
add(1200, no_soup(MAXN))
add(800, fried_heavy(MAXN, 0.02))
add(1500, close(MAXN, 0.05))
add(1000, [day(0, MAXV, 0, MAXV // 2, 0, MAXV, 0.03) for _ in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

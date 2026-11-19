# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4102)
MAXN, MAXV = 200000, 10**9
tests = []


def add(k, g, e):
    n = len(g)
    assert 1 <= n <= MAXN and len(e) == n and 0 <= k <= n
    assert all(0 <= x <= MAXV for x in g + e)
    tests.append(f"{n} {k}\n" + " ".join(map(str, g)) + "\n" + " ".join(map(str, e)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def waves(n, period, hi):
    g, e = [], []
    for i in range(n):
        if (i // period) % 2 == 0:
            g.append(random.randint(hi // 2, hi))
            e.append(random.randint(0, hi // 3))
        else:
            g.append(random.randint(0, hi // 3))
            e.append(random.randint(hi // 2, hi))
    return g, e


def sell_out(n, hi, big_days):
    g = rnd(n, 0, hi)
    e = [x + random.randint(0, 3) for x in g]
    for _ in range(big_days):
        i = random.randrange(n)
        g[i] = MAXV
        e[i] = random.randint(0, MAXV)
    return g, e


add(1, [6, 0, 2, 0], [2, 3, 1, 4])
add(0, [4, 7, 1, 5, 2], [3, 9, 0, 5, 8])
add(1, [10], [3])
add(2, [1000000000, 0, 0, 0], [0, 400000000, 500000000, 900000000])
add(6, [3, 0, 8, 1, 0, 5, 2], [1, 4, 2, 6, 3, 0, 7])

add(1, [5, 4, 1], [3, 3, 3])
add(2, [5, 0, 5, 0, 0], [2, 2, 2, 2, 2])
add(0, [MAXV] * 6, [MAXV] * 6)
add(3, rnd(15, 0, 10), rnd(15, 0, 10))
add(5, *waves(40, 4, 100))
add(2, *waves(60, 3, MAXV))
add(10, rnd(150, 0, 1000), rnd(150, 0, 1000))
add(30, *sell_out(300, 50, 3))

N = MAXN
add(N, [0] * (N - 3) + [MAXV] * 3, [1] * (N - 3) + [MAXV] * 3)
add(150000, *sell_out(N, 99999, 40))
add(120000, *sell_out(N, 9, 5))
add(100000, *waves(N, 50000, 99999))
add(130000, *waves(N, 70000, 99999))
add(110000, *waves(N, 1000, 99999))
g, e = sell_out(N, 99999, 0)
for i in range(0, N, 20000):
    g[i] = MAXV
add(140000, g, e)
add(150000, *waves(N, 25, 99999))
add(160000, [0] * (N // 2) + rnd(N // 2, 0, 99) , rnd(N // 2, 0, 99) + [100] * (N // 2))
add(N // 2 + 7, *sell_out(N, 999, 20))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

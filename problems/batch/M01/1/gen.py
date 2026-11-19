# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4103)
MAXN, MAXT, MAXV, MAXX = 100000, 100000, 10**9, 10**18
tests = []


def add(x, a, dl):
    n, t = len(a), len(dl)
    assert 1 <= n <= MAXN and 1 <= t <= MAXT and 1 <= x <= MAXX
    assert all(1 <= y <= MAXV for y in a)
    assert all(1 <= v <= n and 1 <= d <= MAXV for v, d in dl)
    tests.append(f"{n} {t} {x}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{v} {d}\n" for v, d in dl))


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def front_heavy(n, t, lo, hi):
    dl = []
    for j in range(t):
        top = max(1, n - (n * j) // t)
        dl.append((random.randint(1, top), random.randint(lo, hi)))
    return dl


def split(n, t, y):
    a = rnd(n, 1, MAXV)
    dl = []
    for j in range(t):
        if random.random() < 0.5:
            dl.append((random.randint(1, y - 1), random.randint(1, 10)))
        else:
            dl.append((random.randint(y, n), random.randint(MAXV // 2, MAXV)))
    return a, dl


add(12, [2, 1, 3, 1, 2], [(5, 2), (2, 8), (4, 5), (3, 1)])
add(6, [1, 5, 2, 2], [(3, 4), (1, 2)])
add(100, [5, 5, 5], [(1, 10), (3, 20)])
add(7, [7], [(1, 1000000000)])
add(20, [3, 4, 1, 5, 2, 4], [(3, 9), (6, 5), (5, 1), (4, 3), (2, 2)])

add(10, [3, 2, 1, 8], [(1, 1), (1, 1), (2, 1), (3, 1), (3, 1), (4, 1), (4, 1)])
add(1, [1], [(1, 1)])
add(MAXX, [MAXV] * 5, [(i % 5 + 1, MAXV) for i in range(5)])
add(5 * MAXV, [MAXV] * 5, [(5, MAXV), (1, MAXV), (2, MAXV)])
a = rnd(8, 1, 9); dl = [(random.randint(1, 8), random.randint(1, 9)) for _ in range(10)]
add(random.randint(35, 48), a, dl)
a = rnd(30, 1, 100); dl = front_heavy(30, 40, 1, 100)
add(random.randint(2646, 2734), a, dl)
a = rnd(200, 1, MAXV); dl = [(random.randint(1, 200), random.randint(1, MAXV)) for _ in range(300)]
add(random.randint(188182806030, 190164529812), a, dl)
a = rnd(1000, 1, 1000); dl = front_heavy(1000, 2000, 1, 1000)
add(random.randint(836846, 839554), a, dl)
add(9023142765, *split(50, 80, 20))

N, T = MAXN, MAXT
add(29928238263945, *split(N, T, 60000))
a = rnd(N, 1, MAXV); dl = front_heavy(N, T, 1, MAXV)
add(random.randint(67325421458520, 67326199004168), a, dl)
a = [MAXV] * N; dl = [(N, MAXV)] * T
add(MAXX, a, dl)
a = [MAXV] * N; dl = [(N, MAXV)] * T
add(N * MAXV + 12345 * MAXV, a, dl)
a = rnd(N, 1, MAXV); dl = sorted((random.randint(1, N), random.randint(1, MAXV)) for _ in range(T))
add(random.randint(80176897582016, 80177209293269), a, dl)
a = rnd(N, 1, MAXV); dl = [(1, random.randint(1, MAXV)) for _ in range(T)]
add(random.randint(94776608669387, 94777516476941), a, dl)
a = rnd(N, MAXV // 2, MAXV); dl = [(random.randint(1, N), random.randint(1, MAXV)) for _ in range(T)]
add(52513051427583, a, dl)
a = rnd(N, 1, 1000); dl = front_heavy(N, T, MAXV // 2, MAXV)
add(random.randint(63466035136499, 63466035137442), a, dl)
add(42450076543962, *split(N, T, 85000))
a = rnd(N, 1, MAXV); dl = [(random.randint(1, N), random.randint(1, MAXV)) for _ in range(T)]
add(100002573693384, a, dl)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

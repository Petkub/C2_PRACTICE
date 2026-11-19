# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4805)
MAXN, MAXX, MAXR, MAXD = 100000, 10**9, 10**9, 10**15
tests = []


def add(d, x, r):
    n = len(x)
    assert 1 <= n <= MAXN and len(r) == n
    assert all(0 <= v <= MAXX for v in x) and len(set(x)) == n
    assert all(1 <= v <= MAXR for v in r)
    assert 1 <= d <= MAXD
    tests.append(f"{n} {d}\n" + " ".join(map(str, x)) + "\n" + " ".join(map(str, r)) + "\n")


def dist_x(n, hi):
    return random.sample(range(0, hi + 1), n)


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


add(16, [14, 18, 26, 6, 16], [4, 5, 8, 1, 2])
add(18, [16, 5, 29, 23, 2], [3, 4, 8, 9, 2])
add(10, [0, 5, 9], [3, 10, 4])
add(20, [1, 2, 3], [5, 6, 7])
add(12, [29, 6, 23, 0], [2, 5, 7, 8])
add(6, [0, 1, 2], [2, 2, 2])

add(1, [7], [1])
add(2 * MAXR, [0, MAXX], [MAXR, MAXR])
for n, hi, d in [(8, 40, 64), (10, 100, 81), (12, 1000, 2561132807), (14, 60, 97), (16, MAXX, 3146711678)]:
    x, r = dist_x(n, hi), rnd(n, 1, 20 if hi < 1000 else MAXR)
    add(d, x, r)
x = list(range(0, 40, 3))
r = [1 if i % 2 == 0 else 9 for i in range(len(x))]
add(63, x, r)

x, r = dist_x(1500, 10**6), rnd(1500, 1, 1000)
add(254142, x, r)
x, r = dist_x(2000, MAXX), rnd(2000, 1, MAXR)
add(212991394622, x, r)

N = MAXN
x, r = dist_x(N, MAXX), rnd(N, 1, MAXR)
add(17139725196533, x, r)
x = [i * 10 for i in range(N)]
random.shuffle(x)
r = rnd(N, 1, MAXR)
add(21174413539118, x, r)
x, r = dist_x(N, MAXX), [MAXR] * N
add(33339000000000, x, r)
x = list(range(N))
r = [1 if i % 2 == 0 else MAXR for i in range(N)]
add(50000000000000, x, r)
x, r = dist_x(N, 3 * N), rnd(N, 1, MAXR)
add(50144115893480, x, r)
x, r = dist_x(N, MAXX), rnd(N, 1, MAXR)
add(999999986, x, r)
x, r = dist_x(N, 2 * N), rnd(N, 1, 10)
add(321560, x, r)
x = []
for c in range(1000):
    base = c * 10**6
    x += random.sample(range(base, base + 5000), N // 1000)
r = rnd(N, 1, MAXR)
add(5793663021216, x, r)
x = dist_x(N, MAXX)
r = [random.choice([1, 2, MAXR]) for _ in range(N)]
add(22149000026506, x, r)
x = dist_x(N, 10**7)
r = [MAXR - random.randint(0, 10) for _ in range(N)]
add(40226999851804, x, r)
x, r = dist_x(N, MAXX), rnd(N, 1, MAXR)
add(31439831542377, x, r)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

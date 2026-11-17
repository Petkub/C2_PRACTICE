# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(60111)
MAXN, MAXT = 150_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(shifts):
    n = len(shifts)
    assert 1 <= n <= MAXN
    assert all(1 <= l <= r <= MAXT for (l, r) in shifts)
    tests.append(f"{n}\n" + "".join(f"{l} {r}\n" for (l, r) in shifts))


def rnd(n, t=MAXT, maxlen=MAXT):
    s = []
    for _ in range(n):
        l = ri(1, t)
        s.append((l, min(t, l + ri(0, maxlen - 1))))
    return s


def islands(n, t=MAXT):
    s, k = [], max(1, n // 50)
    width = t // k
    for b in range(k):
        lo, hi = b * width + 1, (b + 1) * width
        s.append((lo, hi))
        inner = sorted(random.sample(range(lo + 1, hi), 2 * 49))
        for j in range(0, len(inner), 2):
            if len(s) < n:
                s.append((inner[j], inner[j + 1] - ri(0, 1) * (inner[j + 1] > inner[j])))
    while len(s) < n:
        s.append(rnd(1, t, 1000)[0])
    random.shuffle(s)
    return s


def chain(n, t=MAXT):
    s, x, step = [], 1, t // (n + 1)
    for _ in range(n):
        d = ri(step // 2, step)
        s.append((x, x + d))
        x += d + ri(0, 1)
    random.shuffle(s)
    return s


def dolls(n, t=MAXT):
    s, lo, hi = [], 1, t
    for _ in range(n):
        s.append((lo, hi))
        lo += ri(0, 2 * (t // (2 * n + 2)))
        hi -= ri(0, 2 * (t // (2 * n + 2)))
        if lo > hi:
            lo = hi
    random.shuffle(s)
    return s


add([(1, 6), (4, 9), (9, 15)])
add([(3, 3), (1, 2), (6, 10), (10, 10)])
add([(1, 1000000000)])
add([(5, 7), (7, 9), (9, 11)])
add([(1, 1000000000), (2, 1000000000)])
add([(28, 40), (10, 20), (45, 50), (15, 30), (41, 45)])

add([(1, 10), (3, 4), (7, 7)])
add([(5, 5), (5, 5), (5, 5)])
add(rnd(8, 30, 10))
add(rnd(12, 40, 15))
add(islands(150, 10**4))
add(rnd(800, 10**5, 2000))
add(dolls(1000))
add(rnd(5000, MAXT, 10**6))

N = MAXN
add(rnd(N))
add(rnd(N, MAXT, 5000))
add(rnd(N, MAXT, 20000))
add(islands(N))
add(islands(N, 10**7))
add(chain(N))
add(dolls(N))
add([(ri(1, 1000), MAXT - ri(0, 1000)) for _ in range(N - 1)] + [(1, MAXT)])
s = [(1, MAXT)] + [(2 * i + 1, 2 * i + 1) for i in range(1, N)]
random.shuffle(s)
add(s)
s = []
for i in range(N // 2):
    a = 1 + i * 5000
    s += [(a, a + 2500), (a + 2500, a + 4999)]
random.shuffle(s)
add(s)
add([(l, l + ri(0, 3)) for l in sorted(random.sample(range(1, MAXT), N))])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(19009)
MAXN, MAXW, MAXC = 200_000, 100_000, 100_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(c, b, w):
    n, m = len(b), len(w)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN and 0 <= c <= MAXC
    assert all(1 <= x <= m for x in b) and all(1 <= x <= MAXW for x in w)
    tests.append(f"{n} {m} {c}\n" + " ".join(map(str, b)) + "\n" + " ".join(map(str, w)) + "\n")


def rand_w(m, lo=1, hi=MAXW):
    return [ri(lo, hi) for _ in range(m)]


def uniform(n, m):
    return [ri(1, m) for _ in range(n)]


def local(n, m, width):
    b, cur = [], ri(1, m)
    for _ in range(n):
        cur = min(m, max(1, cur + ri(-width, width)))
        b.append(cur)
    return b


def phases(n, m, k):
    b = []
    for p in range(k):
        size = ri(3, 40)
        group = [ri(1, m) for _ in range(size)]
        length = n // k if p < k - 1 else n - len(b)
        b += [random.choice(group) for _ in range(length)]
    return b


def periodic(n, m, period):
    return [(i % period) + 1 if random.random() < 0.9 else ri(1, m) for i in range(n)]


add(3, [1, 2, 1, 3, 3, 2, 4], [5, 4, 6, 2])
add(10, [1, 2, 1], [3, 7])
add(0, [1], [MAXW])
add(4, [2, 1, 2, 3, 1, 1, 4, 2], [6, 5, 9, 3])
add(0, [3, 3, 1, 3, 1], [8, 1, 4])

for n, m, c in ((1, 1, 5), (2, 2, 1), (6, 3, 4), (12, 5, 7), (40, 15, 30), (300, 120, 300), (2000, 900, 5000),
                (3000, 300, 300)):
    add(c, uniform(n, m), rand_w(m, 1, 2 * c + 10))
add(MAXC, uniform(1000, 1000), rand_w(1000))
add(0, local(2000, 500, 5), rand_w(500))
add(50, phases(3000, 3000, 30), rand_w(3000, 1, 400))
add(7, periodic(2500, 2500, 40), rand_w(2500, 1, 20))

N = MAXN
add(50_000, uniform(N, N), rand_w(N))
add(5_000, uniform(N, 100_000), rand_w(100_000))
add(2_000, local(N, N, 30), rand_w(N, 1, 5_000))
add(500, phases(N, N, 200), rand_w(N, 1, 2_000))
add(1_000, periodic(N, N, 1000), rand_w(N, 1, 10_000))
add(0, uniform(N, N), [MAXW] * N)
add(MAXC, uniform(N, N), rand_w(N, 1, 90_000))
add(99_000, uniform(N, N), rand_w(N, 90_000, MAXW))
add(5_000, local(N, 20_000, 200), rand_w(20_000, 1, 40_000))
add(100, phases(N, N, 5_000), rand_w(N, 1, 300))
add(20_000, [i % N + 1 for i in range(N)], rand_w(N, 1, 40_000))
add(40_000, local(N, 50_000, 3_000), rand_w(50_000, 1, 80_000))
add(1_000, local(N, N, 20_000), rand_w(N, 50_000, MAXW))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
    assert len(t) <= 3_000_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

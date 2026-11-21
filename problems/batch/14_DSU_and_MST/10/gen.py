# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(140010)
MAXN = MAXM = 200000
tests = []


def add(m, cs):
    n = len(cs)
    assert 1 <= n <= MAXN and 2 <= m <= MAXM
    assert all(1 <= a <= m and 1 <= b <= m and a != b for a, b in cs)
    tests.append(f"{n} {m}\n" + "".join(f"{a} {b}\n" for a, b in cs))


def pair(lo, hi):
    a = random.randint(lo, hi)
    b = random.randint(lo, hi - 1)
    return (a, b + (b >= a))


def rnd(n, m):
    return [pair(1, m) for _ in range(n)]


def clusters(n, m, size):
    blocks = m // size
    return [pair(k * size + 1, (k + 1) * size) for k in sorted(random.randrange(blocks) for _ in range(n))]


def relabel(m, cs):
    p = list(range(1, m + 1))
    random.shuffle(p)
    return [(p[a - 1], p[b - 1]) for a, b in cs]


add(4, [(1, 2), (2, 3), (1, 3), (1, 2), (3, 4)])
add(6, [(1, 2), (3, 4), (5, 6), (2, 3), (4, 5), (6, 1), (1, 4)])
add(2, [(1, 2)])
add(2, [(1, 2), (2, 1), (1, 2)])
add(200000, [(200000, 1), (1, 200000), (199999, 200000), (1, 199999)])
add(3, [(2, 1), (1, 2), (2, 3), (3, 1), (1, 3)])

for n, m in ((5, 3), (8, 6), (10, 4), (20, 25), (40, 30), (200, 150)):
    add(m, rnd(n, m))
add(10, clusters(30, 10, 3))
cs = [(i, i + 1) for i in range(1, 50)] + [(50, 1)] + rnd(20, 50)
add(50, cs)

add(MAXM, rnd(MAXN, MAXM))
add(MAXM, rnd(MAXN, MAXM // 2 * 2))
add(1000, rnd(MAXN, 1000))
add(MAXM, clusters(MAXN, MAXM, 5))
add(MAXM, relabel(MAXM, clusters(MAXN, MAXM, 40)))
cs = [(i, i + 1) for i in range(1, MAXM)]
random.shuffle(cs)
add(MAXM, relabel(MAXM, cs[:150000] + rnd(50000, MAXM)))
cs = [(i, i + 1) for i in range(1, 100001)]
cs += [pair(100002 + 3 * k, 100004 + 3 * k) for k in range(30000)]
cs += rnd(MAXN - len(cs), MAXM)
random.shuffle(cs)
add(MAXM, cs)
add(2, [(1, 2) if random.random() < 0.5 else (2, 1) for _ in range(MAXN)])
cs = []
for k in range(MAXN // 4):
    base = 4 * (k % (MAXM // 4))
    cs.append(pair(base + 1, base + 4))
add(MAXM, relabel(MAXM, cs + clusters(MAXN - len(cs), MAXM, 4)))
add(MAXM, [pair(1, 50000) if i % 2 else pair(150001, 200000) for i in range(MAXN)])
add(MAXM, sorted(rnd(MAXN, MAXM), key=lambda x: -x[0]))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

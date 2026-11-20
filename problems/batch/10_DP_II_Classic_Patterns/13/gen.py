# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(100013)
MAXN = 50000
MAXM = 100000
MAXL = 50
MAXW = 10 ** 9
tests = []


def add(n, p, l, edges, shuffle=True):
    assert 2 <= n <= MAXN and 1 <= len(edges) <= MAXM and 1 <= p <= MAXW and 1 <= l <= MAXL
    assert all(1 <= u < v <= n and 1 <= w <= MAXW for u, v, w in edges)
    edges = list(edges)
    if shuffle:
        random.shuffle(edges)
    tests.append(f"{n} {len(edges)} {p} {l}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))


def rnd_dag(n, m, reach, wlo, whi):
    e = [(u, u + 1, random.randint(wlo, whi)) for u in range(1, n)]
    while len(e) < m:
        u = random.randint(1, n - 1)
        e.append((u, random.randint(u + 1, min(n, u + reach)), random.randint(wlo, whi)))
    return e


def stages(l, count, p, extra=0):
    e, a, n = [], 1, 1
    for _ in range(count):
        cheap = random.randint(p // (l + 2) + 1, p // (l + 1))
        heavy = random.randint(((l + 1) * cheap) // l + 1, ((l + 1) * cheap) // l + 1 + p // 50)
        hw = [a] + [n + i for i in range(1, l)]
        n += l - 1
        side = [a] + [n + i for i in range(1, l + 1)]
        n += l
        b = n + 1
        n = b
        hw.append(b)
        side.append(b)
        e += [(hw[i], hw[i + 1], heavy) for i in range(l)]
        e += [(side[i], side[i + 1], cheap + random.randint(0, 3)) for i in range(l + 1)]
        a = b
    for _ in range(extra):
        u = random.randint(1, n - 1)
        e.append((u, random.randint(u + 1, min(n, u + 2 * l)), random.randint(MAXW // 2, MAXW)))
    return n, e


add(5, 6, 2, [(1, 2, 6), (2, 5, 6), (1, 3, 2), (3, 4, 3), (4, 5, 8)], False)
add(4, 100, 1, [(1, 2, 7), (3, 4, 2)], False)
add(3, 10, 3, [(1, 2, 8), (2, 3, 9), (1, 3, 20)], False)
add(6, 9, 2, [(1, 2, 6), (2, 3, 6), (3, 4, 6), (4, 5, 6), (5, 6, 6), (1, 6, 25)], False)
add(2, 1, 1, [(1, 2, 1000000000)], False)

for n, m, p, l in [(2, 1, 3, 1), (4, 5, 7, 2), (6, 9, 15, 2), (7, 12, 10, 3), (8, 14, 25, 1), (9, 16, 12, 4)]:
    add(n, p, l, rnd_dag(n, m, 3, 1, 20))
n, e = stages(3, 2, 60)
add(n, 60, 3, e)

add(2000, 3000, 6, rnd_dag(2000, 5000, 30, 1, 1000))
n, e = stages(8, 100, 10 ** 7, 300)
add(n, 10 ** 7, 8, e)

n, e = stages(50, 495, 10 ** 9 - 7, 0)
add(n, 10 ** 9 - 7, 50, e)
n, e = stages(20, 1240, 5 * 10 ** 8, 40000)
add(n, 5 * 10 ** 8, 20, e)
n, e = stages(5, 4900, 10 ** 8, 30000)
add(n, 10 ** 8, 5, e)
add(MAXN, 3 * 10 ** 9 // 10, 50, rnd_dag(MAXN, MAXM, 60, 1, MAXW))
add(MAXN, 10 ** 9, 10, rnd_dag(MAXN, MAXM, 8, 1, MAXW))
add(MAXN, 5 * 10 ** 8, 1, rnd_dag(MAXN, MAXM, 4, 1, MAXW))
add(MAXN, 1, 50, rnd_dag(MAXN, MAXM, 100, 1, MAXW))
add(MAXN, MAXW, 50, rnd_dag(MAXN, MAXM, 3, 1, 1000))
add(MAXN, MAXW, 50, [(u, u + 1, MAXW) for u in range(1, MAXN)] + [(u, u + 2, MAXW) for u in range(1, MAXN - 1)])
add(MAXN, 7 * 10 ** 8, 37, rnd_dag(MAXN, MAXM, 40, 10 ** 7, MAXW))
e = [(u, v, w) for u, v, w in rnd_dag(MAXN, MAXM, 20, 1, MAXW) if not (u <= 25000 < v)]
add(MAXN, 10 ** 6, 50, e)
n, e = stages(30, 830, 9 * 10 ** 8, 20000)
add(n, 9 * 10 ** 8, 30, e)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

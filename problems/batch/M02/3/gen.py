# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(4803)
MAXN, MAXM, MAXV = 100000, 100000, 10**9
tests = []


def add(m, d, x, items):
    n, k = len(items), len(x)
    assert 1 <= k <= n <= MAXN and 1 <= m <= MAXM
    assert 1 <= d <= MAXV and all(1 <= v <= MAXV for v in x)
    assert all(1 <= v <= MAXV and 1 <= t <= k for v, t in items)
    tests.append(f"{n} {m} {k} {d}\n" + " ".join(map(str, x)) + "\n"
                 + "".join(f"{v} {t}\n" for v, t in items))


def xs_for(caps, d):
    out = []
    for c in caps:
        if c == 0:
            assert d < MAXV
            out.append(random.randint(d + 1, MAXV))
        else:
            lo, hi = d // (c + 1) + 1, d // c
            out.append(random.randint(lo, hi))
    for c, v in zip(caps, out):
        assert d // v == c
    return out


def rnd_items(n, k, lo, hi):
    items = [(random.randint(lo, hi), random.randint(1, k)) for _ in range(n)]
    return items


add(2, 8, [12, 4, 2], [(7, 1), (1, 2), (3, 2), (9, 3), (5, 2), (3, 2)])
add(2, 9, [5, 2, 12], [(8, 2), (8, 2), (5, 1), (2, 1), (5, 3), (5, 2)])
add(3, 5, [6, 7], [(4, 1), (9, 2)])
add(5, 10, [3, 5], [(1, 1), (2, 1), (3, 2), (4, 2)])
add(1, MAXV, [1], [(MAXV, 1)] * 3)

add(1, 1, [1], [(1, 1)])
add(1, 1, [2], [(MAXV, 1)])
add(3, 10, [5], [(9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1)])
add(2, 10, [10, 3], [(100, 1), (40, 2), (40, 2), (40, 2), (90, 1)])
for n, k, m, d in [(10, 3, 3, 20), (15, 4, 4, 30), (20, 5, 6, 50), (25, 3, 8, 12), (30, 6, 10, 100)]:
    caps = [random.randint(0, 4) for _ in range(k)]
    caps[0] = max(caps[0], 1)
    add(m, d, xs_for(caps, d), rnd_items(n, k, 1, 50))

caps = [random.randint(0, 6) for _ in range(40)]
add(300, 10**6, xs_for(caps, 10**6), rnd_items(2000, 40, 1, MAXV))
caps = [random.choice([1, 1, 2, 5]) for _ in range(200)]
add(250, 999, xs_for(caps, 999), rnd_items(3000, 200, 1, 1000))

N = MAXN
K = N // 2
items = [(random.randint(1, MAXV), t) for t in range(1, K + 1) for _ in range(2)]
random.shuffle(items)
add(MAXM, MAXV, [MAXV] * K, items)
K = N
caps = [random.randint(0, 3) for _ in range(K)]
add(N // 2, MAXV - 1, xs_for(caps, MAXV - 1), [(random.randint(1, MAXV), t) for t in range(1, K + 1)])
K = N // 2
caps = [random.randint(1, 10) for _ in range(K)]
add(MAXM, MAXV, xs_for(caps, MAXV), [(MAXV, t) for t in range(1, K + 1)] + rnd_items(N - K, K, MAXV, MAXV))
K = (2 * N) // 3
caps = [random.randint(0, 5) for _ in range(K)]
add(N // 2, 10**8, xs_for(caps, 10**8), [(t % 1000 + 1, t) for t in range(1, K + 1)] + rnd_items(N - K, K, 1, MAXV))

K = (3 * N) // 5
caps = [1] * (K // 2) + [3] * (K // 2)
items = [(MAXV - random.randint(0, 1000), t) for t in range(1, K // 2 + 1)]
for t in range(K // 2 + 1, K + 1):
    items += [(6 * 10**8 + random.randint(0, 1000), t)] * 2
items += [(1, random.randint(1, K)) for _ in range(N - len(items))]
random.shuffle(items)
add(N // 2, MAXV, xs_for(caps, MAXV), items)

K = (2 * N) // 3
Z = K // 5
caps = [0] * Z + [random.randint(1, 4) for _ in range(K - Z)]
items = [(MAXV, t) for t in range(1, Z + 1)] + [(random.randint(1, 10**8), t) for t in range(Z + 1, K + 1)]
items += [(random.randint(1, 10**8), random.randint(Z + 1, K)) for _ in range(N - len(items))]
add(N // 2, MAXV - 1, xs_for(caps, MAXV - 1), items)
K = (4 * N) // 5
caps = [random.choice([1, 1, 1, 2, 7]) for _ in range(K)]
items = [(random.randint(1, MAXV), t) for t in range(1, K + 1)] + rnd_items(N - K, K, 1, MAXV)
add(MAXM, 5 * 10**8, xs_for(caps, 5 * 10**8), items)
K = N // 2
caps = [1 if t % 2 else 2 for t in range(K)]
items = [(random.randint(MAXV - 100, MAXV), t) for t in range(1, K + 1) for _ in range(2)]
random.shuffle(items)
add((3 * N) // 4, 2, xs_for(caps, 2), items)
K = (3 * N) // 5
caps = [random.randint(0, 2) for _ in range(K)]
add(N // 2, 7, xs_for(caps, 7), [(random.randint(1, MAXV), t) for t in range(1, K + 1)] + rnd_items(N - K, K, 1, MAXV))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

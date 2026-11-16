# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(180011)
MAXN, MAXQ = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a) + 1, len(qs)
    assert 2 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(i < a[i - 1] <= n for i in range(1, n))
    assert all(1 <= s < t <= n for s, t in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{s} {t}\n" for s, t in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def reach(n, lo, hi):
    """a_i = i + (random step in [lo, hi]), capped at n"""
    return [min(n, i + ri(lo, hi)) for i in range(1, n)]


def far_qs(n, q):
    res = []
    for _ in range(q):
        s = ri(1, max(1, n // 20))
        res.append((s, ri(max(s + 1, n - n // 20), n)))
    return res


def rnd_qs(n, q):
    res = []
    for _ in range(q):
        s = ri(1, n - 1)
        res.append((s, ri(s + 1, n)))
    return res


def decoys(n, step):
    """every station reaches far, but the farthest station is a dead end: the far jump is wrong"""
    a = []
    for i in range(1, n):
        if i % step == 0:
            a.append(min(n, i + 1))                     # dead end at the far station
        else:
            a.append(min(n, (i // step + 1) * step + step - 1 if i % step == step - 1 else (i // step + 1) * step))
    return a


# samples
add([3, 5, 4, 6, 7, 7], [(1, 7), (1, 5), (2, 4), (3, 7)])
add([2, 3, 4], [(1, 4), (2, 3)])
add([2], [(1, 2)])
add([4, 3, 6, 8, 6, 8, 8], [(1, 8), (1, 4), (2, 6), (3, 5), (5, 8), (7, 8)])
add([10, 3, 4, 5, 6, 7, 8, 9, 10], [(1, 10), (2, 10), (2, 9), (5, 6), (3, 10)])
# hidden: small
n = 12
add(reach(n, 1, 3), [(s, t) for s in range(1, n) for t in range(s + 1, n + 1)])
add(reach(300, 1, 10), rnd_qs(300, 300))
add(reach(1000, 1, 40), rnd_qs(1000, 500) + far_qs(1000, 100))
add(decoys(800, 7), rnd_qs(800, 400))
a = reach(2000, 1, 2)
for _ in range(20):
    i = ri(1, 1999)
    a[i - 1] = ri(i + 1, 2000)                          # a few express stations
add(a, rnd_qs(2000, 500) + far_qs(2000, 100))
# hidden: maximum size
N = MAXN
add(reach(N, 1, 1), far_qs(N, 120_000))                 # one station per ticket: answers ~ N
add(reach(N, 1, 3), far_qs(N, 120_000))
add(reach(N, 1, 60), far_qs(N, 100_000) + rnd_qs(N, 20_000))
add(reach(N, 500, 3000), rnd_qs(N, 120_000))
add(decoys(N, 13), far_qs(N, 120_000))
a = reach(N, 1, 2)
for _ in range(30):
    i = ri(1, N - 1)
    a[i - 1] = min(N, i + ri(100, 2000))                  # a few short express trains
add(a, far_qs(N, 120_000))
a = [N] * (N - 1)                                        # every station goes to the end
add(a, rnd_qs(N, 120_000))
a = [min(N, i + (i & -i)) for i in range(1, N)]           # reach i + lowbit(i)
add(a, far_qs(N, 60_000) + rnd_qs(N, 60_000))
a = reach(N, 1, 2)
add(a, [(1, N)] * 1000 + [(ri(1, 10), ri(N - 10, N)) for _ in range(110_000)])
add(decoys(N, 3), far_qs(N, 120_000))
add(reach(N, 1, 8), far_qs(N, 120_000))
add(reach(N, 2, 5), far_qs(N, 90_000) + rnd_qs(N, 30_000))
a = reach(N, 1, 1)
for i in range(1, N, 2):
    a[i - 1] = min(N, i + 3)                                 # odd stations reach 3, even ones only 1
add(a, far_qs(N, 120_000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

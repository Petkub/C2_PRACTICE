# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(180012)
MAXN, MAXQ, MAXV = 200_000, 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(a, qs):
    n, q = len(a), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXQ
    assert all(0 <= v <= MAXV for v in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    t = f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs)
    assert len(t) <= 3_100_000
    tests.append(t)


def shuffled_ap(n, start, d, w):
    a = [start + d * i for i in range(n)]
    for b in range(0, n, w):
        part = a[b:b + w]
        random.shuffle(part)
        a[b:b + w] = part
    return a


def aligned_qs(n, w, q, long_frac=0.8):
    nb = (n + w - 1) // w
    res = []
    for _ in range(q):
        if random.random() < long_frac:
            b1, b2 = ri(0, max(0, nb // 10)), ri(max(0, nb - 1 - nb // 10), nb - 1)
        else:
            b1 = ri(0, nb - 1)
            b2 = ri(b1, nb - 1)
        l, r = b1 * w + 1, min(n, (b2 + 1) * w)
        x = random.random()
        if x < 0.15 and r > l:
            r -= 1
        elif x < 0.3 and r < n:
            r += 1
        res.append((l, r))
    return res


def dup_inside(a, w, frac):
    for b in range(0, len(a) - w + 1, w):
        if random.random() >= frac:
            continue
        part = a[b:b + w]
        lo, hi = min(part), max(part)
        i, j = random.sample([x for x in range(w) if lo < part[x] < hi], 2)
        a[b + i] = a[b + j]
    return a


def window_qs(n, w, q):
    nb = n // w
    return [(b * w + 1, b * w + w) for b in (ri(0, nb - 1) for _ in range(q))]


def rnd_qs(n, q):
    res = []
    for _ in range(q):
        l = ri(1, n)
        res.append((l, ri(l, n)))
    return res


add([5, 1, 9, 3, 7, 7, 4, 10], [(1, 5), (4, 6), (5, 6), (6, 8), (2, 4), (3, 3)])
add([0, 1, 1, 3], [(1, 4), (1, 2), (2, 3)])
add([MAXV], [(1, 1)])
add([0, MAXV, MAXV // 2], [(1, 3), (1, 2), (2, 3)])
add([4, 4, 4, 2, 6, 8, 0], [(1, 3), (1, 5), (3, 7), (4, 7), (2, 5)])

a = [ri(0, 6) for _ in range(10)]
add(a, [(l, r) for l in range(1, 11) for r in range(l, 11)])
add(shuffled_ap(300, 5, 3, 4), aligned_qs(300, 4, 500, 0.3) + rnd_qs(300, 100))
add(shuffled_ap(1000, 0, 1, 10), aligned_qs(1000, 10, 1000, 0.3))
a = shuffled_ap(1200, 7, 6, 12)
for _ in range(15):
    i = ri(0, 1199)
    a[i] = a[i] + 3
add(a, aligned_qs(1200, 12, 1500, 0.3))
a = shuffled_ap(1500, 100, 2, 6)
for _ in range(15):
    i = ri(1, 1499)
    a[i] = a[i - 1]
add(a, aligned_qs(1500, 6, 1500, 0.3))
add([ri(0, 3) * 5 for _ in range(2000)], rnd_qs(2000, 2000))

N = MAXN
add(shuffled_ap(N, 0, 1, 1), aligned_qs(N, 1, 120_000, 0.5) + rnd_qs(N, 10_000))
add(shuffled_ap(N, 3, 4, 100), aligned_qs(N, 100, 120_000))
add(shuffled_ap(N, 0, 1, N), [(1, N)] * 1000 + aligned_qs(N, N, 1000) + rnd_qs(N, 100_000))
add(shuffled_ap(N, 10, 4999, 2000), aligned_qs(N, 2000, 80_000))
a = shuffled_ap(N, 1, 2, 50)
for _ in range(40):
    i = ri(1, N - 1)
    a[i] = a[i - 1]
add(a, aligned_qs(N, 50, 120_000))
a = shuffled_ap(N, 0, 6, 64)
for _ in range(40):
    i = ri(0, N - 1)
    a[i] += 3 if a[i] + 3 <= MAXV else -3
add(a, aligned_qs(N, 64, 120_000))
a = shuffled_ap(N, 5, 3, 500)
a[N // 2] = a[N // 2 - 1]
add(a, aligned_qs(N, 500, 120_000))
add([777] * N, rnd_qs(N, 150_000))
add([ri(0, 99_999) for _ in range(N)], rnd_qs(N, 70_000) + [(i, i + ri(1, 2)) for i in range(1, 50_001)])
a = shuffled_ap(N, 0, 2, 200)
for i in range(0, N, 200):
    j = i + ri(0, 199)
    a[j] = a[j] + 1 if a[j] < 2 * N else a[j] - 1
add(a, aligned_qs(N, 200, 120_000))

add(dup_inside(shuffled_ap(300, 3, 7, 6), 6, 0.5), window_qs(300, 6, 300) + aligned_qs(300, 6, 300, 0.3))
add(dup_inside(shuffled_ap(N, 0, 1, 16), 16, 0.5), window_qs(N, 16, 60_000) + aligned_qs(N, 16, 60_000, 0.5))
add(dup_inside(shuffled_ap(N, 11, 4999, 500), 500, 0.3), window_qs(N, 500, 25_000) + aligned_qs(N, 500, 25_000, 0.5))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

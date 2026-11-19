# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(43003)
MAXN, MAXM = 200_000, 200_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(m, k, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM and 1 <= k <= m
    assert all(1 <= x <= m for x in a)
    tests.append(f"{n} {m} {k}\n" + " ".join(map(str, a)) + "\n")


def grow(n, m, k, left, right, chunk, dup, tail_out):
    lo, hi = max(1, k - left), min(m, k + right)
    order = [k]
    l, r = k - 1, k + 1
    while l >= lo or r <= hi:
        part = []
        for _ in range(chunk):
            if l >= lo:
                part.append(l)
                l -= 1
            if r <= hi:
                part.append(r)
                r += 1
        random.shuffle(part)
        order += part
    a = []
    for x in order:
        if len(a) >= n:
            break
        a.append(x)
        if random.random() < dup:
            a.append(ri(max(1, x - chunk), min(m, x + chunk)))

    if len(a) > 3 and random.random() < 0.7:
        j = a.index(k)
        p = ri(1, min(50, len(a) - 1))
        a[j], a[p] = a[p], a[j]
    while len(a) < n:
        a.append(ri(1, m) if random.random() < tail_out else ri(lo, hi))
    return a[:n]


add(7, 3, [4, 3, 6, 3, 2, 1])
add(5, 1, [2, 3, 2])
add(6, 2, [5, 2, 1, 2, 5, 5, 2, 4, 5])
add(8, 7, [6, 7, 2, 2, 6, 8, 2, 5])
add(1, 1, [1, 1, 1])


add(5, 3, [3])
add(4, 2, [1, 3, 4, 2, 2])
add(6, 1, [3, 3, 2, 4, 1, 6, 5])
for n, m in [(10, 5), (30, 10), (60, 40), (200, 50), (300, 300)]:
    add(m, ri(1, m), [ri(1, m) for _ in range(n)])
for n, m, ch in [(250, 120, 3), (300, 200, 6)]:
    k = ri(1, m)
    add(m, k, grow(n, m, k, m, m, ch, 0.3, 0.2))


add(MAXM, 1, [ri(1, MAXM) for _ in range(MAXN)])
add(1000, 500, [ri(1, 1000) for _ in range(MAXN)])


N, M = MAXN, MAXM
for k, left, right, ch, dup, out in [(M // 2, M, M, 1, 0.0, 0.0), (M // 2, M // 4, M // 4, 5, 0.3, 0.2),
                                     (1, 0, M, 20, 0.2, 0.3), (M, M, 0, 3, 0.5, 0.1),
                                     (ri(1, M), M // 3, M // 6, 50, 0.1, 0.5), (M // 3, M, M, 1000, 0.05, 0.0),
                                     (2 * M // 3, M // 5, M // 5, 2, 0.4, 0.4)]:
    add(M, k, grow(N, M, k, left, right, ch, dup, out))
a = grow(N // 2, M, M // 2, M // 4, M // 4, 10, 0.2, 0.0)
a += [ri(1, M) for _ in range(N - len(a) - 2)] + [1, M]
add(M, M // 2, a)
h = N // 2
a = [M // 2 + i for i in range(1, h)] + [M // 2] + [ri(M // 2 - 5, M // 2 + 5) for _ in range(N - h)]
add(M, M // 2, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

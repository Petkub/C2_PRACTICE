# Test generator of this problem (the judge runs it to rebuild the big tests).
import os, random

random.seed(11020)
MAXN, MAXK = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(K, L, c):
    n = len(c)
    assert 1 <= n <= MAXN and 2 <= K <= MAXK and 1 <= L <= n
    assert all(0 <= x <= K for x in c)
    tests.append(f"{n} {K} {L}\n" + " ".join(map(str, c)) + "\n")


def planted(n, p, palette):
    return [random.choice(palette) if random.random() < p else 0 for _ in range(n)]


def few(n, k, palette):
    c = [0] * n
    for i in random.sample(range(n), k):
        c[i] = random.choice(palette)
    return c


def blocks(n, L, palette, gap):
    c, i = [0] * n, 0
    while i < n:
        ln, col = ri(1, L), random.choice(palette)
        for j in range(i, min(n, i + ln)):
            c[j] = col
        i += ln + ri(0, gap)
    return c


def reveal(n, K, L, p, ncol):
    c, prev = [], 0
    while len(c) < n:
        col = random.choice([x for x in range(1, ncol + 1) if x != prev])
        c += [col] * ri(1, L)
        prev = col
    return [x if random.random() < p else 0 for x in c[:n]]


add(3, 2, [1, 0, 0, 1])
add(2, 1, [1, 0, 2])
add(2, 2, [0, 0, 0, 0, 0])
add(1000000000, 1, [0, 0, 0])
add(5, 2, [3, 3, 3, 0])
add(4, 3, [0, 2, 0, 0, 2, 2, 0, 1])

add(2, 1, [0])
add(7, 1, [7])
add(3, 5, [0] * 5)
add(2, 3, planted(12, 0.3, [1, 2]))
add(4, 2, reveal(14, 4, 2, 0.5, 4))
add(10**9, 3, planted(15, 0.2, [5, 10**9]))
add(3, 2, [1, 1, 0, 2, 2, 0, 3, 3, 0, 1, 1])

add(10**9, 40, planted(2000, 0.05, [1, 2, 3]))
add(3, 700, blocks(2000, 700, [1, 2, 3], 300))
add(5, 1, reveal(20_000, 5, 1, 0.3, 5))
add(4, 3, reveal(20_000, 4, 3, 0.6, 4))

N = MAXN
add(10**9, N, [0] * N)
add(2, 100_000, [0] * N)
add(10**9, 150_000, few(N, 4, [7, 8, 9]))
add(3, 80_000, blocks(N, 80_000, [1, 2, 3], 60_000))
add(2, 60_000, reveal(N, 2, 60_000, 0.00003, 2))
add(999_999_937, 180_000, few(N, 6, list(range(1, 50))))
add(5, 50_000, reveal(N, 5, 50_000, 0.0001, 5))
add(4, 100_000, reveal(N, 4, 100_000, 0.0001, 4))
add(10**9, 70_000, blocks(N, 70_000, [1, 2], 40_000))
add(2, N, few(N, 5, [1, 2]))
add(10**9, 100_000, [1] * 100_000 + [0] * (N - 100_000))
add(10**9, 99_999, [1] * 100_000 + [0] * (N - 100_000))
add(3, 60_000, [(i // 50_000) % 3 + 1 if i % 40_000 == 0 else 0 for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20220)
MAXN, MAXA = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(k, a):
    n = len(a)
    assert 1 <= k <= n <= MAXN
    assert all(1 <= x <= MAXA for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


def gadget(p, hlo, hhi, llo, lhi):
    """H^p L^(2p-1) H^p: only the whole block has a high middle among stretches of length >= 2p"""
    return rnd(p, hlo, hhi) + rnd(2 * p - 1, llo, lhi) + rnd(p, hlo, hhi)


def gadget_test(n, p, layers):
    """background of middle values with a few gadgets inside; k = 2p"""
    a = rnd(n, 2, 4 * 10**8)
    for j in range(layers):
        g = gadget(p, 9 * 10**8 + j * 10**7, 9 * 10**8 + j * 10**7 + 10**6, 1, 1000)
        s = ri(0, n - len(g))
        a[s:s + len(g)] = g
    return a


# samples
add(2, [1, 3, 2, 5, 4])
add(4, [9, 9, 1, 1, 1, 9, 9])
add(4, [4, 1, 3, 2])
add(1, [5, 8, 2])
add(1, [MAXA])
add(3, [6, 2, 7, 7, 1, 3, 8, 2])
# hidden: small
add(2, [1, 1])
add(2, [1, 2])
add(3, [5, 1, 5])
add(6, [10, 10, 10, 1, 1, 1, 1, 1, 10, 10, 10])
for n in (8, 20, 60, 300):
    add(ri(1, n), rnd(n, 1, 5))
add(150, rnd(1000, 1, MAXA))
add(10, gadget(5, 50, 60, 1, 10) + gadget(7, 40, 45, 1, 10))
add(200, gadget_test(3000, 100, 3))
add(3000, rnd(3000, 1, 3))
add(1, [7] * 2000)
# hidden: large
N = MAXN
add(60_000, gadget_test(N, 30_000, 1))                 # the best middle needs a long stretch
add(20_000, gadget_test(N, 10_000, 3))
add(2000, gadget_test(N, 1000, 5))
add(50_000, gadget(25_000, MAXA - 100, MAXA, 1, 10**8) + rnd(N - 99_999, 1, 10**8))
a = []
while len(a) < N - 1000:                                # many gadgets with small p
    a += gadget(ri(3, 50), ri(5 * 10**8, MAXA), MAXA, 1, ri(1, 5 * 10**8))
add(ri(10, 40), a[:N])
add(ri(N // 3, N // 2), rnd(N, 1, MAXA))
add(N, rnd(N, 1, MAXA))                                # the whole array
add(1, rnd(N, 1, MAXA))                                # the largest score
a = []
while len(a) < N:                                      # blocks (1 2)^1000 1: a stretch of length 2000..4000 has at
    a += [1, 2] * 1000 + [1]                           # most as many 2s as 1s, and some have exactly as many
add(ri(2000, 4000), a[:N])                             # only two values: the tie rule decides (answer 1)
add(ri(100, 300), rnd(N, 1, MAXA))
add(N // 2, [1 + i % 2 for i in range(N)])             # 1 2 1 2 ...: only odd stretches that start with 2 have middle 2
add(N // 2 + 1, [MAXA - (i % 2) for i in range(N)])
add(ri(100, 1000), sorted(rnd(N, 1, MAXA)))
add(ri(50_000, 100_000), [ri(1, 10**6) if (i // 7) % 2 else ri(10**6, MAXA) for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20219)
MAXN, MAXM, MAXH = 200_000, 10**9, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(m, w, h):
    n = len(h)
    assert 1 <= w <= n <= MAXN
    assert 1 <= m <= MAXM
    assert all(1 <= x <= MAXH for x in h)
    tests.append(f"{n} {m} {w}\n" + " ".join(map(str, h)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(3, 2, [2, 1, 3, 2, 1, 4])
add(5, 3, [1, 2, 3])
add(4, 1, [5, 1, 1, 5])
add(MAXM, 1, [MAXH])
add(4, 3, [3, 1, 4, 1, 5, 9, 2])
add(2, 2, [4, 4, 1, 4, 4])
# hidden: small (brute force tries every plan)
add(1, 1, [1, 1])
add(3, 2, [1, 5, 1])
for n, m in ((5, 4), (6, 4), (8, 3)):
    add(m, ri(1, n), rnd(n, 1, 6))
# hidden: medium
add(300, 7, rnd(50, 1, 100))
add(2000, 30, rnd(300, 1, 1000))
add(3000, 500, [1000 - i for i in range(1000)])
add(4000, 50, rnd(2000, MAXH - 1000, MAXH))
# hidden: large; most of them fall from left to right so that a short seedling appears at almost every position
N = MAXN


def walk_down(n, step):
    h, cur = [], MAXH
    for _ in range(n):
        h.append(cur)
        cur -= ri(0, step)
    return h


add(MAXM, N // 2, [MAXH - 3000 * i for i in range(N)])
add(MAXM, N // 3, [MAXH - 2 * i - ri(0, 1) for i in range(N)])
add(MAXM, ri(N // 4, N // 2), sorted(rnd(N, 1, MAXH), reverse=True))
add(MAXM, 20_000, [N - i for i in range(N)])
add(MAXM, 70_000, [1 + abs(N // 2 - i) * 9000 for i in range(N)])        # tall in the middle
add(MAXM - ri(0, 10**6), N // 2 + 1, [MAXH - i * 4000 if i < N // 2 else 1 + (i - N // 2) * 4000
                                       for i in range(N)])               # a valley
add(MAXM, 30_000, [(50_000 - i % 50_000) * 20 for i in range(N)])        # falling sawtooth
add(MAXM, 50_000, walk_down(N, 5000))
add(ri(10**8, MAXM), N // 2, [N - i + 1 for i in range(N)])
add(MAXM, 40_000, [(N - i) // 10 * 7 + 1 for i in range(N)])             # falling stairs
add(MAXM, N - 10, [5 * (N - i) + ri(0, 4) for i in range(N)])
add(MAXM, ri(N // 4, N // 2), [(N - i) * 50 + ri(0, 10**4) for i in range(N)])
add(MAXM, ri(15_000, 25_000), [(N - i) * 5 + ri(0, 100) for i in range(N)])
add(ri(10**8, MAXM), 60_000, sorted(rnd(N, 1, 10**6), reverse=True))
add(MAXM, N, [MAXH] * N)                                                 # answer 2 * 10^9
add(MAXM, 1, rnd(N, 1, MAXH))
add(MAXM, N // 2, [1 + 4000 * i for i in range(N)])                      # only the left end is short
add(1, ri(1, N), rnd(N, 1, MAXH))
add(500_000, 1000, rnd(N, 1, 10))
add(MAXM, ri(N // 4, N // 2), [(N - i) * 3000 + ri(0, 10**6) for i in range(N)])   # falling with noise

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(11015)
MAXN, MAXK, MAXV = 200_000, 300, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(K, a):
    n = len(a)
    assert 1 <= n <= MAXN and 1 <= K <= min(n, MAXK) and all(abs(x) <= MAXV for x in a)
    tests.append(f"{n} {K}\n" + " ".join(map(str, a)) + "\n")


def rnd(n, lo, hi):
    return [ri(lo, hi) for _ in range(n)]


# samples
add(2, [3, -1, 4, -9, 2, 6, -5, 1])
add(2, [-5, -2, -8, -1])
add(1, [2, -3, 5, -1, 4])
add(3, [1, 2, 3])
add(2, [5, -10, 5, -10, 5])
add(3, [-1, 7, -2, 7, -100, 3, -3, 4, -6])
# hidden: small (the brute tries everything)
add(1, [-MAXV])
add(1, [MAXV, -1, MAXV])
add(3, rnd(10, -10, 10))
add(4, rnd(12, -100, 100))
add(2, rnd(12, -5, 1))
add(5, rnd(11, -MAXV, MAXV))
# hidden: medium
add(20, rnd(2000, -1000, 1000))
add(10, rnd(1500, -MAXV, MAXV // 2))
# hidden: maximum size
N, K = MAXN, MAXK
add(K, rnd(N, -MAXV, MAXV))
add(K, rnd(N, -MAXV, MAXV // 20))                      # mostly negative
add(K, rnd(N, -MAXV, -1))                              # all negative: the K largest days
add(K, [MAXV] * N)                                     # 2 * 10^14
add(K, [MAXV if i % 2 == 0 else -MAXV for i in range(N)])
add(1, rnd(N, -MAXV, MAXV))                            # one stretch
add(K, rnd(N, -10**6, 10**6))
add(K - 1, [(MAXV if i % 1000 < 3 else -ri(1, 10**6)) for i in range(N)])
add(K, [ri(-MAXV, MAXV) if i % 7 else -MAXV for i in range(N)])
add(150, rnd(N, -10**4, 10**4))
add(K, [ri(1, 1000) if (i // 500) % 2 else -ri(1, 1000) for i in range(N)])   # 200 good blocks, K = 300

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

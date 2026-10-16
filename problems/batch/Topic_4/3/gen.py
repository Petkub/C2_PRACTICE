# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40403)
MAXN, MAXT = 200_000, 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(a, shuffle=False):
    a = list(a)
    if shuffle:
        random.shuffle(a)
    n = len(a)
    assert 1 <= n <= MAXN
    assert all(1 <= l <= r <= MAXT for l, r in a)
    tests.append(f"{n}\n" + "".join(f"{l} {r}\n" for l, r in a))


def rnd(n, T, maxlen):
    out = []
    for _ in range(n):
        l = ri(1, T)
        out.append((l, min(T, l + ri(0, maxlen))))
    return out


# samples
add([(1, 3), (2, 5), (6, 8), (5, 6)])
add([(1, 5), (5, 9), (9, 9), (10, 12)])
add([(7, 7)])
add([(1, 2), (3, 4), (5, 6), (10, 20)])
add([(3, 7)] * 5)
add([(1, 100), (2, 3), (50, 60), (61, 61), (60, 70)])
# hidden: small
add([(MAXT, MAXT), (1, MAXT)])
add([(1, 1), (2, 2), (1, 2), (2, 3), (3, 3)])
add(rnd(10, 20, 4))
add(rnd(60, 100, 10))
add(rnd(300, 1000, 50))
add(rnd(2000, 10**6, 300))
add(rnd(5000, MAXT, MAXT))
add([(i, i) for i in range(1, 3001)], True)          # nobody meets
add([(i, i + 1) for i in range(1, 3001)], True)      # only neighbours meet, at one minute
# hidden: large (N = 2*10^5; many pairs for the "list every meeting pair" way)
N = MAXN
add(rnd(N, 10**7, 100))                               # few pairs
add(rnd(N, 10**7, 2 * 10**6))
add(rnd(N, 10**6, 10**6))                             # about half of all pairs
add([(1, 10**6)] * N)                                 # every pair: N(N-1)/2
add([(i, 10**6) for i in range(1, N + 1)], True)      # everyone stays until the end
add([(i, i) for i in range(1, N + 1)])                # nobody meets, sorted
add([(N + 1 - i, N + 1 - i) for i in range(1, N + 1)])  # nobody meets, reverse sorted
add([(5 * i, 5 * i + 5) for i in range(1, N + 1)], True)  # only neighbours, touching
add([(ri(1, 1000), ri(999_000, 10**6)) for _ in range(N)])  # everyone shares the middle
add([(i, 2 * N + 1 - i) for i in range(1, N + 1)], True)  # nested
x = [(ri(1, 10**6), 0) for _ in range(N)]
add([(l, l + ri(0, 3)) for l, _ in x])                # short stays, touching often
add([(ri(1, 50), ri(50, 100)) for _ in range(N)])     # many equal times
add(rnd(140_000, MAXT, 10**8))                        # large times

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

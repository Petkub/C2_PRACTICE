# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(20206)
MAXN = 200_000
MAXM = 10**9
MAXT = 10**9
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(m, t):
    n = len(t)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= x <= MAXT for x in t)
    tests.append(f"{n} {m}\n" + " ".join(map(str, t)) + "\n")


# samples
add(7, [3, 2, 5])
add(MAXM, [MAXT])
add(5, [2, 2])
add(1, [5, 3, 9])
add(20, [4, 7, 6, 10])
add(MAXM, [1, 1, 1, MAXT])
# hidden: small (M small enough for an item-by-item check)
add(1, [1])
add(1, [MAXT])
add(10**6, [MAXT])
add(10**6, [ri(1, 100) for _ in range(10)])
add(500_000, [ri(1, MAXT) for _ in range(1000)])
add(300_000, [7] * 3000)
add(10**6, [1] * 999 + [MAXT])
add(777_777, [ri(1, 1000) * 1000 for _ in range(5000)])
# hidden: maximum size, M up to 10^9
N = MAXN
add(MAXM, [MAXT] * N)
add(MAXM, [ri(1, MAXT) for _ in range(N)])
add(MAXM, [1] * (N - 1) + [MAXT])               # a huge upper bound makes the sum overflow
add(MAXM, [1] * N)
add(MAXM, [ri(1, 10) for _ in range(N)])
add(MAXM, [MAXT] * (N - 1) + [1])
add(MAXM - 1, [ri(MAXT // 2, MAXT) for _ in range(N)])
add(ri(MAXM // 2, MAXM), [ri(1, MAXT) for _ in range(N)])
add(MAXM, [ri(1, 1000) for _ in range(N // 2)] + [ri(10**8, MAXT) for _ in range(N // 2)])
add(N, [MAXT - i for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests), "max", max(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

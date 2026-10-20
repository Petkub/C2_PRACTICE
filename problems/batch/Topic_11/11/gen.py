# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(91101)
MAXN, MAXM = 400_000, 400_000
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ps):
    m = len(ps)
    assert 1 <= n <= MAXN and 1 <= m <= MAXM
    assert all(1 <= p <= n for p in ps)
    tests.append(f"{n} {m}\n" + " ".join(map(str, ps)) + "\n")


def block_then_middle(n, m, filled):
    """first a long run of taken spots (cheap), then every car wants the middle of that run"""
    start = ri(1, n)
    ps = [(start - 1 + i) % n + 1 for i in range(filled)]
    mid = (start - 1 + filled // 2) % n + 1
    return ps + [mid] * (m - filled)


# samples
add(6, [3, 3, 3, 4, 1, 6, 2])
add(5, [5, 5, 5, 1])
add(1, [1, 1])
add(8, [4, 5, 3, 4, 4, 8, 2])
add(10, [10, 1, 10, 9, 2, 1, 10, 5, 6])
# hidden: small
add(1, [1])
add(2, [2, 2, 1, 2])
add(7, [ri(1, 7) for _ in range(10)])
add(30, [ri(1, 30) for _ in range(40)])
add(100, [50] * 100)
add(500, [1] * 600)
add(1000, block_then_middle(1000, 1200, 700))
add(3000, [ri(1, 3000) for _ in range(3000)])
add(5000, [ri(1, 10) for _ in range(5000)])
# hidden: maximum size
N, M = MAXN, MAXM
add(N, [N // 2] * M)                                         # one run grows to both sides
add(N, [1] * M)                                              # ... across the end of the ring
add(N, block_then_middle(N, M, N * 3 // 4))
add(N, block_then_middle(N, M, N // 2))
add(N // 2, block_then_middle(N // 2, M, N // 2 - 20000))     # the lot fills up, then many cars get 0
add(N, [ri(1, N) for _ in range(M)])
add(N, [ri(1, 100) for _ in range(M)])
add(N // 4, [ri(N // 8 - 50, N // 8 + 50) for _ in range(M)])  # the lot fills up, M = 4N
add(N, [ri(1, N) if i % 2 else N // 3 for i in range(M)])
ps = [i for i in range(1, N + 1, 2)]                         # every other spot first
random.shuffle(ps)
add(N, ps + [ri(1, N) for _ in range(M - len(ps))])
add(N, [N - (i % 7) for i in range(M)])
add(3, [ri(1, 3) for _ in range(M)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

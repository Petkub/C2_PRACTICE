# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10113)
MAXN = 200_000
MAXM = 200_000
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (faster than randint, still deterministic)"""
    return lo + int(random.random() * (hi - lo + 1))


def add(n, ops):
    assert 1 <= n <= MAXN and 1 <= len(ops) <= MAXM
    assert all(1 <= l <= r <= n for (l, r) in ops)
    tests.append(f"{n} {len(ops)}\n" + "".join(f"{l} {r}\n" for (l, r) in ops))


def rnd_ops(n, m, maxlen=None):
    out = []
    for _ in range(m):
        if maxlen is None:
            a, b = ri(1, n), ri(1, n)
            out.append((min(a, b), max(a, b)))
        else:
            ln = ri(1, min(maxlen, n))
            l = ri(1, n - ln + 1)
            out.append((l, l + ln - 1))
    return out


# samples
add(6, [(2, 4), (3, 6)])
add(5, [(1, 5), (5, 5), (1, 1)])
add(1, [(1, 1)])
add(4, [(1, 3), (1, 3), (2, 4)])
add(7, [(3, 3), (1, 7), (6, 7)])
# hidden (small)
add(3, [(3, 3)])
add(10, [(1, 10)] * 3)
add(50, rnd_ops(50, 40))
add(500, rnd_ops(500, 300, 20))
add(2000, rnd_ops(2000, 2000))
add(5000, [(1, 5000)] * 1000 + rnd_ops(5000, 1000))
add(3000, [(i, 3000) for i in range(1, 3001)])
# large
N, M = MAXN, MAXM
add(N, [(1, N)] * M)                                  # every column as high as possible
add(N, rnd_ops(N, M))
add(N, rnd_ops(N, M, 10))
add(N, [(ri(1, N),) * 2 for _ in range(M)])           # single columns only
add(N, [(1, ri(N // 2, N)) for _ in range(M)])
add(N, [(ri(1, N // 2), N) for _ in range(M)])
add(N, [(i % N + 1, N) for i in range(M)])
add(N, rnd_ops(N, M // 2) + [(1, N)] * (M // 2))
add(N, rnd_ops(N, M, 20000))
add(N - 1, [(1, N - 1)] * 1000 + rnd_ops(N - 1, M - 1000))
add(N, [(ri(1, 10), ri(N - 10, N)) for _ in range(M)])
add(N, [(1, N)])
add(N, [(ri(1, 100), ri(N - 100, N)) for _ in range(M // 2)])
add(N, [(1, ri(3 * N // 4, N)) for _ in range(M // 2)])
add(N, rnd_ops(N, M // 2, N // 2))
add(N, [(ri(1, N // 4), ri(3 * N // 4, N)) for _ in range(M // 2)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

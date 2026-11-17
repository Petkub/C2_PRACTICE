# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(160010)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN and all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


def blocks(n, lens):
    """a low seedling, then decreasing runs: many nights inside each run"""
    h = [1]
    while len(h) < n:
        k = min(random.choice(lens), n - len(h))
        top = ri(k + 1, MAXH)
        h.extend(top - j for j in range(k))
    return h


# samples
add([3, 6, 2, 7, 5, 4])
add([4, 4, 5, 5])
add([8])
add([5, 4, 3, 2, 1])
add([1, 5, 4, 3, 2])
# hidden: small
add([2, 1])
add([ri(1, 3) for _ in range(12)])
add([ri(1, 6) for _ in range(300)])
add([ri(1, MAXH) for _ in range(2000)])
add([1] + [3000 - i for i in range(2999)])
add(blocks(5000, [3, 10, 50]))
add([ri(1, 2) for _ in range(20000)])
add([ri(1, MAXH) for _ in range(20000)])
add([ri(1, 3) for _ in range(20000)])
add([i + 1 for i in range(20000)])                            # every seedling but the first on night 1
add([MAXH] * 20000)
# hidden: maximum size (long falls: many nights with many seedlings left)
N = MAXN
add([1] + [N + 1 - i for i in range(N - 1)])                  # N - 1 nights
add([1] + [MAXH - i // 2 for i in range(N - 1)])              # decreasing in pairs of equal heights
add(blocks(N, [N // 4, N // 2]))
add(blocks(N, [1000, 5000, 20000]))
add(blocks(N, [2000, 30000, 60000]))
h = [1]                                                        # nested: rising steps, each followed by a fall
while len(h) < N:
    base = len(h) * 30
    k = min(ri(20000, 60000), N - len(h))
    h.extend(base + k - j for j in range(k))
add(h)
add([1] + [MAXH - (i // 3) * 7 for i in range(N - 1)])                  # falling in equal triples
add([1] + [MAXH - ri(0, i // 10 + 1) - i * 4000 for i in range(N - 1)])   # long slow fall with noise
add([ri(1, MAXH) for _ in range(40000)] + [1] + [MAXH - i for i in range(N - 40001)])  # random, then a fall
add([ri(2, 4) for _ in range(40000)] + [1] + [MAXH - i // 2 for i in range(N - 40001)])
add([1] + [MAXH - i for i in range(149_999)] + [ri(1, MAXH) for _ in range(50000)])  # a fall, then random

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

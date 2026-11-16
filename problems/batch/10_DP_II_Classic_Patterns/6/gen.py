# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(10006)
MAXN, MAXH = 200000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    assert 1 <= len(h) <= MAXN and 1 <= min(h) and max(h) <= MAXH
    tests.append(f"{len(h)}\n" + " ".join(map(str, h)) + "\n")


def rnd(n, lo=1, hi=MAXH):
    return [ri(lo, hi) for _ in range(n)]


def noisy_up(n, step, noise):
    """an increasing trend with noise: long answers, many near misses"""
    return [max(1, min(MAXH, 1 + i * step + ri(-noise, noise))) for i in range(n)]


def blocks_equal(n, k):
    """k blocks; inside a block every height is the same"""
    out = []
    for b in range(k):
        out += [ri(1, MAXH)] * (n // k)
    return out + [1] * (n - len(out))


# samples
add([150, 160, 155, 170, 165, 180])
add([5, 5, 5, 6, 6])
add([170, 168, 165, 160])
add([1, 2, 3, 4, 5, 6, 7])
add([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
# hidden: small
add([1])
add([7, 7])
add(rnd(12, 1, 5))
add(rnd(40, 1, 20))
add(rnd(300, 1, 300))
add(noisy_up(2000, 10, 40))
# hidden: maximum size
N = MAXN
add(rnd(N))
add(rnd(N, 1, 100))                       # many equal heights
add(list(range(1, N + 1)))                # already increasing
add(list(range(N, 0, -1)))                # strictly decreasing
add([MAXH] * N)                            # everybody the same height
add(noisy_up(N, 5000, 30000))
add(noisy_up(N, 1, 3))                    # long runs of equal heights in an increasing trend
add([i // 2 + 1 for i in range(N)])        # 1 1 2 2 3 3 ...
add(blocks_equal(N, 500))
add([ri(1, 1000) * 1000 + (i % 1000) for i in range(N)])
add(sorted(rnd(N, 1, 50000)))             # non-decreasing with repeats
add([(i * 7919) % 100003 + 1 for i in range(N)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

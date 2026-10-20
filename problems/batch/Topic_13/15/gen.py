# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(11015)
MAXN, MAXH = 200_000, 10**9
tests = []


def ri(lo, hi):
    return lo + int(random.random() * (hi - lo + 1))


def add(h):
    n = len(h)
    assert 1 <= n <= MAXN
    assert all(1 <= x <= MAXH for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")


def pairs(n, base=1, gap=2):
    """2 1 4 3 6 5 ...: 2^(n/2) longest climbs"""
    h = []
    for i in range(n // 2):
        h += [base + gap * i + 1, base + gap * i]
    return h[:n]


def blocks(n, k):
    """k blocks, inside a block heights go down, every block is higher than the previous one:
    the longest climbs take one checkpoint from each block"""
    h, size = [], n // k
    for b in range(k):
        s = size + (n - size * k if b == k - 1 else 0)
        top = (b + 1) * (MAXH // k)
        h += sorted((ri(top - MAXH // k + 1, top) for _ in range(s)), reverse=True)
    return h


def noisy_up(n, step, noise):
    return [min(MAXH, max(1, i * step + ri(-noise, noise) + noise + 1)) for i in range(n)]


# samples
add([1, 3, 2, 4, 3])
add([7, 7, 7])
add([9, 8, 6, 5])
add([2, 1, 4, 3, 6, 5])
add([3, 1, 4, 1, 5, 2, 6, 5, 3, 5])
# hidden: small
add([MAXH])
add([1, 2, 2, 3, 3, 3])
add([ri(1, 5) for _ in range(12)])
add([ri(1, 30) for _ in range(40)])
add(pairs(80))                                       # 2^40 climbs: needs the modulus
add(blocks(2000, 40))
add([ri(1, 50) for _ in range(3000)])
add([ri(1, MAXH) for _ in range(3000)])
# hidden: maximum size
N = MAXN
add([ri(1, MAXH) for _ in range(N)])
add([ri(1, 10) for _ in range(N)])                  # many equal heights
add(list(range(1, N + 1)))                           # one climb through everything
add([MAXH - i for i in range(N)])                    # every checkpoint alone
add([MAXH] * N)
add(pairs(N, 1, 2))
add(blocks(N, 2))
add(blocks(N, 300))
add(noisy_up(N, 4000, 100_000))
add(noisy_up(N, 5, 1000))
h = []
for i in range(N):                                   # three interleaved increasing runs
    h.append(1 + (i % 3) * 7 + (i // 3) * 20)
add(h)
add([ri(1, 2 * N) for _ in range(N)])
add(blocks(N, 20000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

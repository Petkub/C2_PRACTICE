# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(40401)
MAXN, MAXL = 150_000, 10**18
tests = []


def ri(lo, hi):
    """uniform integer in [lo, hi] (deterministic, faster than randint)"""
    return lo + int(random.random() * (hi - lo + 1))


def rbig(lo, hi):
    return random.randint(lo, hi)        # exact for huge ranges


def add(L, p):
    n = len(p)
    assert 1 <= n <= MAXN and 1 <= L <= MAXL
    assert all(0 <= s <= L - 1 and 1 <= k <= L for s, k in p)
    tests.append(f"{n} {L}\n" + "".join(f"{s} {k}\n" for s, k in p))


# samples
add(10, [(2, 3), (8, 4), (3, 4)])
add(5, [(3, 5), (0, 1)])
add(10**18, [(5 * 10**17, 6 * 10**17), (1, 1)])
add(1, [(0, 1)])
add(20, [(0, 3), (5, 2), (5, 4), (15, 3)])
add(12, [(10, 5), (2, 3), (11, 2)])
# hidden: small
add(7, [(6, 2)])                                   # wraps onto post 0
add(1, [(0, 1)] * 5)
add(30, [(ri(0, 29), ri(1, 4)) for _ in range(6)])
add(50, [(ri(0, 49), ri(1, 50)) for _ in range(8)])
add(100, [(ri(0, 99), ri(1, 10)) for _ in range(40)])
add(1000, [(ri(0, 999), ri(1, 30)) for _ in range(300)])
add(10**18, [(rbig(0, MAXL - 1), rbig(1, 10**17)) for _ in range(500)])
add(10**18, [(MAXL - 1, MAXL)] + [(rbig(0, MAXL - 1), rbig(1, 10**6)) for _ in range(200)])  # whole ring
add(10**9, [(i * 2, 1) for i in range(2000)])     # touching nothing: gaps of one post
add(10**9, [(i * 3, 3) for i in range(2000)])     # touching pieces that must join
# hidden: large (L too big to mark posts one by one, and many long pieces for the O(N^2) way)
N = MAXN
B = 4 * 10**9
add(B, [(ri(0, B - 1), ri(1, 40_000)) for _ in range(N)])
add(B, [(ri(0, B - 1), ri(1, 80_000)) for _ in range(N)])          # nearly everything painted
add(B, [(ri(0, B - 1), ri(B // 2, B)) for _ in range(140_000)])    # everything, mostly by wrapping pieces
add(B, [(i * 26_000, 1 + (i % 7) * 4000) for i in range(N)])        # sorted, many separate pieces
add(B, [(ri(0, 10**6), ri(B - 10**6, B - 1)) for _ in range(140_000)])  # long pieces nested in each other
add(B, [(B - 1 - i * 26_000, 13_000 + (i % 5)) for i in range(N)])  # reverse order
add(B, [(i * 20_000, B // 2) for i in range(140_000)])              # each covers half of the ring, chained
add(B, [(ri(B - 5000, B - 1), ri(4000, 9000)) for _ in range(N)])  # all near the end, every one may wrap
add(B, [(1_234_567_890, 2_765_432_110)] * 130_000)                        # identical, ends exactly at post L-1
add(B, [(ri(0, B - 1), 1) for _ in range(N)])                      # single posts, some repeated
p = [(0, B // 2)] + [(ri(0, B // 2 - 1), ri(1, 1000)) for _ in range(N - 1)]  # nested inside one big piece
add(B, p)
M = 70_000
add(MAXL, [(rbig(0, MAXL - 1), rbig(1, 3 * 10**13)) for _ in range(M)])
add(MAXL, [(rbig(MAXL - 10**17, MAXL - 1), rbig(10**17, MAXL)) for _ in range(M)])
add(MAXL - 1, [(rbig(0, MAXL - 2), rbig(1, 10**12)) for _ in range(M - 1)] + [(MAXL - 2, MAXL - 1)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

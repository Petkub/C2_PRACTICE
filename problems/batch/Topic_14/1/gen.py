# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(14001)
MAXN = 300_000
MAXK = 10 ** 9
MAXA = 10 ** 18
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(k, a):
    assert 1 <= len(a) <= MAXN and 1 <= k <= MAXK
    assert all(-MAXA <= x <= MAXA for x in a)
    tests.append(f"{len(a)} {k}\n" + " ".join(map(str, a)) + "\n")


def with_rem(r, k, lim=MAXA):
    # a random value in [-lim, lim] with a % k == r
    lo = -(lim // k)
    hi = (lim - r) // k
    return ri(lo, hi) * k + r


# samples
add(10, [3, 7, 5, -3, 15])
add(2, [4, -6, 0, 10])
add(7, [1, 2, 3])
add(1, [-1_000_000_000_000_000_000, 5, 1_000_000_000_000_000_000])
add(6, [-9, 3, 9, -3, 21, 6])
# hidden: small (brute force checks them)
add(1_000_000_000, [7])
add(1, [ri(-MAXA, MAXA) for _ in range(500)])
add(5, [ri(-20, 20) for _ in range(800)])
add(1_000_000_000, [with_rem(random.choice([0, 500_000_000, 1, 999_999_999]), 10 ** 9) for _ in range(1000)])
add(ri(2, 50), [ri(-MAXA, MAXA) for _ in range(2000)])
add(4, [random.choice([2, -2, 6, -6, 0, 4]) for _ in range(1500)])
add(999_999_937, [ri(-MAXA, MAXA) for _ in range(1500)])
# hidden: large. Values near 10^18 take ~20 characters, so those tests have N = 100 000;
# the tests at N = 300 000 use shorter values to keep every input near 3 MB.
L = 10 ** 8
add(7, [42] * MAXN)                                                     # every pair, answer ~4.5*10^10
add(1_000_000_000, [MAXA] * 50_000 + [-MAXA] * 50_000)                  # all remainders 0
add(3, [ri(-MAXA, -MAXA + 10 ** 6) for _ in range(100_000)])
add(2, [ri(-L, L) for _ in range(MAXN)])
add(1_000_000_000, [with_rem(500_000_000, 10 ** 9, 2 * 10 ** 9) for _ in range(250_000)])  # 2r = K
add(99_999_998, [with_rem(random.choice([1, 99_999_997, 49_999_999]), 99_999_998, L) for _ in range(MAXN)])
add(ri(10 ** 7, 10 ** 8), [ri(-L, L) for _ in range(MAXN)])
add(1000, [ri(-10 ** 5, 10 ** 5) for _ in range(MAXN)])
add(10 ** 9, [ri(-10 ** 6, 10 ** 6) for _ in range(MAXN)])              # only a_i + a_j = 0 counts
add(500_000, [random.choice([1, -1]) * ri(0, 10 ** 6) for _ in range(MAXN)])
k = 12_345_678
add(k, [with_rem(r, k, L) for r in [ri(0, 50) if i % 2 else (k - ri(0, 50)) % k for i in range(MAXN)]])
add(1, [ri(-10 ** 6, 10 ** 6) for _ in range(MAXN)])
add(65_536, [-ri(1, L) for _ in range(MAXN)])                            # all negative
add(10, [ri(-99, 99) for _ in range(MAXN)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)

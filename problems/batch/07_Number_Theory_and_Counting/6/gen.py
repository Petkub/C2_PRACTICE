# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(140601)
MAXQ = 10_000
MAXX = 10 ** 18
tests = []


def ri(lo, hi):
    return random.randint(lo, hi)


def add(xs):
    assert 1 <= len(xs) <= MAXQ
    for x in xs:
        assert 1 <= x <= MAXX
    tests.append(f"{len(xs)}\n" + "".join(f"{x}\n" for x in xs))


def half(k):            # (3^k - 1) / 2: largest x that weights 3^0..3^(k-1) can balance
    return (3 ** k - 1) // 2


# samples
add([4, 7])
add([1, 2, 13])
add([1_000_000, 5])
add([8, 26, 27, 100])
add([half(8), half(8) + 1, 123_456])
# hidden: small (the brute force tries every placement)
add(list(range(1, 1001)))
add([ri(1, 3000) for _ in range(2000)])
add([3 ** k for k in range(8)] + [half(k) for k in range(1, 9)] + [half(k) + 1 for k in range(1, 8)]
    + [2 * 3 ** k for k in range(8)] + [3 ** k - 1 for k in range(1, 8)])
add([ri(1, 9000) for _ in range(300)])
# hidden: large
add([ri(1, MAXX) for _ in range(MAXQ)])
add([ri(MAXX // 2, MAXX) for _ in range(MAXQ)])
add([MAXX - i for i in range(MAXQ)])
add([3 ** k for k in range(38)] + [half(k) for k in range(1, 39)] + [half(k) + 1 for k in range(1, 38)]
    + [3 ** k - 1 for k in range(1, 38)] + [3 ** k + 1 for k in range(38)] + [2 * 3 ** k for k in range(37)])
add([half(38) + ri(1, MAXX - half(38)) for _ in range(MAXQ)])                  # needs weight 3^38
add([half(ri(30, 38)) for _ in range(MAXQ)])                                     # all weights on the right
ks = [ri(2, 38) for _ in range(MAXQ)]
add([half(k) - 2 * 3 ** ri(0, k - 2) for k in ks])                              # exactly one weight on the left
add([(3 ** ri(20, 37)) * ri(1, 2) - ri(0, 1) for _ in range(MAXQ)])
add([ri(1, 10 ** 9) for _ in range(MAXQ)])
add([sum(3 ** i for i in random.sample(range(38), ri(1, 38))) * 2 % MAXX + 1 for _ in range(MAXQ)])
add([ri(1, 3 ** ri(1, 37)) for _ in range(MAXQ)])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
